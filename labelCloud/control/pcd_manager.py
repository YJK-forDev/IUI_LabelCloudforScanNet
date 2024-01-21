"""
Module to manage the point clouds (loading, navigation, floor alignment).
Sets the point cloud and original point cloud path. Initiate the writing to the virtual object buffer.
"""
import logging
from pathlib import Path
from shutil import copyfile
from typing import TYPE_CHECKING, List, Optional, Set, Tuple

import pkg_resources

import numpy as np
import open3d as o3d

from ..definitions.types import Point3D
from ..io.pointclouds import BasePointCloudHandler, Open3DHandler
from ..model import BBox, Perspective
from ..model import PointCloud
from ..utils.logger import blue, green, print_column

from .config_manager import config
from .label_manager import LabelManager

if TYPE_CHECKING:
    from ..view.gui import GUI
    
from ..__main__ import args
from ..definitions.types import Point3D, Rotations3D, Translation3D


class PointCloudManger(object):
    
    PCD_EXTENSIONS = BasePointCloudHandler.get_supported_extensions()
    ORIGINALS_FOLDER = "original_pointclouds"
    TRANSLATION_FACTOR = config.getfloat("POINTCLOUD", "STD_TRANSLATION")
    ZOOM_FACTOR = config.getfloat("POINTCLOUD", "STD_ZOOM")
    #SEGMENTATION = LabelConfig().type == LabelingMode.SEMANTIC_SEGMENTATION    

    def __init__(self) -> None:
        #logging.info("pcd_manager.py PointCloudManager init...")
        # Point cloud management
        self.pcd_folder = config.getpath("FILE", "pointcloud_folder")
        #print_column(["self.pcd_folder:", self.pcd_folder]) #pointclouds
        self.pcds: List[Path] = []
        self.current_id = -1

        self.view: GUI
        self.label_manager = LabelManager()

        # Point cloud control
        self.pointcloud: Optional[PointCloud] = None
        self.collected_object_classes: Set[str] = set()
        self.saved_perspective: Optional[Perspective] = None
        
        
        #self.zoom_distance= 0
        
        #fix perspective
        """
        self.saved_perspective1: Rotations3D = (0, 0, 90)
        self.saved_perspective2: Rotations3D = (-30, 0, 45)
        self.saved_perspective3: Rotations3D = (-45, 0, 0)
       
    
        self.saved_perspective1: Rotations3D = (
            float(args.perspective[0]), 
            float(args.perspective[1]), 
            float(args.perspective[2]))
        self.saved_perspective2: Rotations3D = (
            float(args.perspective[3]), 
            float(args.perspective[4]), 
            float(args.perspective[5]))
        self.saved_perspective3: Rotations3D = (
            float(args.perspective[6]), 
            float(args.perspective[7]), 
            float(args.perspective[8]))
       """ 
        
    @property
    def pcd_path(self) -> Path:
        return self.pcds[self.current_id]

    @property
    def pcd_name(self) -> Optional[str]:
        if self.current_id >= 0:
            return self.pcd_path.name
        return None

    def read_pointcloud_folder(self) -> None:
        """Checks point cloud folder and sets self.pcds to all valid point cloud file names."""
        if self.pcd_folder.is_dir():
            self.pcds = []
            for file in sorted(self.pcd_folder.iterdir()):
                if file.suffix in PointCloudManger.PCD_EXTENSIONS:
                    self.pcds.append(file)
        else:
            logging.warning(
                f"Point cloud path {self.pcd_folder} is not a valid directory."
            )

        if self.pcds:
            self.view.status_manager.set_message(
                f"Found {len(self.pcds)} point clouds in the point cloud folder."
            )
            self.update_pcd_infos()
        else:
            self.view.show_no_pointcloud_dialog(
                self.pcd_folder, PointCloudManger.PCD_EXTENSIONS
            )
            self.view.status_manager.set_message(
                "Please set the point cloud folder to a location that contains point cloud files."
            )
            self.pointcloud = PointCloud.from_file(
                Path(
                    pkg_resources.resource_filename(
                        "labelCloud.resources", "labelCloud_icon.pcd"
                    )
                )
            )
            self.update_pcd_infos(pointcloud_label=" – (select folder!)")

        self.view.init_progress(min_value=0, max_value=len(self.pcds) - 1)
        self.current_id = -1
        
    def read_pointcloud_folder2(self) -> None:
        """Checks point cloud folder and sets self.pcds to all valid point cloud file names."""
        
        pcd_folder2 =  self.pcd_folder.joinpath(args.id)
        pcd_folder2 =  pcd_folder2.joinpath(args.condition)
        
        if pcd_folder2.is_dir():
            self.pcds = []
            for file in sorted(pcd_folder2.iterdir()):
                if file.suffix in PointCloudManger.PCD_EXTENSIONS:
                    self.pcds.append(file)
        else:
            logging.warning(
                f"Point cloud path {pcd_folder2} is not a valid directory."
            )

        if self.pcds:
            self.view.status_manager.set_message(
                f"Found {len(self.pcds)} point clouds in the point cloud folder."
            )
            self.update_pcd_infos()
        else:
            self.view.show_no_pointcloud_dialog(
                pcd_folder2, PointCloudManger.PCD_EXTENSIONS
            )
            self.view.status_manager.set_message(
                "Please set the point cloud folder to a location that contains point cloud files."
            )
            self.pointcloud = PointCloud.from_file(
                Path(
                    pkg_resources.resource_filename(
                        "labelCloud.resources", "labelCloud_icon.pcd"
                    )
                )
            )
            self.update_pcd_infos(pointcloud_label=" – (select folder!)")

        self.view.init_progress(min_value=0, max_value=len(self.pcds) - 1)
        self.current_id = -1

    # GETTER
    def pcds_left(self) -> bool:
        return self.current_id + 1 < len(self.pcds)

        
    """
    ################################
    def get_transparency_pcd(self, pcd_index: int) -> None:
        logging.info("Loading transparency point cloud...")
        self.pointcloud = PointCloud(path, points)
    ################################
    
    ################################
    def get_overlay_pcd(self, pcd_index: int) -> None:
        self.pointcloud = PointCloud(path, points)
        
    ################################
    """
    
    def get_custom_pcd(self, pcd_index: int) -> None:
        #logging.info("Loading custom point cloud...")
        if pcd_index < len(self.pcds):
            self.current_id = pcd_index
            self.save_current_perspective()
            self.pointcloud = PointCloud.from_file(
                self.pcd_path,
                self.saved_perspective,
                write_buffer=self.pointcloud is not None,
            )
            self.update_pcd_infos()
            #self.zoom_into2()
        else:
            logging.warning("This point cloud does not exists!")
    
    def get_reload_pcd(self, logdata: dict) -> None:
        #logging.info("Loading custom point cloud...")

        """
        self.pointcloud = PointCloud.from_file(
            self.pcd_path,
            self.saved_perspective,
            write_buffer=self.pointcloud is not None,
        )
        self.update_pcd_infos()
        """
        self.zoom_into2(logdata)

            

    def class_pcd(self, logdata: dict, classi: int) -> None:
        #logging.info("Loading next point cloud...")
        
        flag = False
        
        if args.condition == 'C0' or args.condition == 'C1' or args.condition == 'C2':
            pcdn = 'class' + str(classi)
        if args.condition == 'D0' or args.condition == 'D1' or args.condition == 'D2':
            pcdn = 'class' + str(classi)
            
        for i in range(len(self.pcds)):
            #logging.info(f"self.pcd !!! {i}") #pointclouds\P1\T13\1C_scene0013_00.ply
            if pcdn in self.pcds[i].stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
                self.current_id = i
                flag = True
                #logging.info(f"!!! {i}") #pointclouds\P1\T13\1C_scene0013_00.ply
        
        if flag == True:
            #self.current_id = classi
            self.save_current_perspective()
            self.pointcloud = PointCloud.from_file(
                self.pcd_path,
                self.saved_perspective,
                write_buffer=self.pointcloud is not None,
            )
            self.update_pcd_infos()
            self.zoom_into2(logdata)

            
    def get_next_pcd(self, logdata: dict) -> None:
        #logging.info("Loading next point cloud...")
        
        if self.pcds_left():
            self.current_id += 1
            self.save_current_perspective()
            self.pointcloud = PointCloud.from_file(
                self.pcd_path,
                self.saved_perspective,
                write_buffer=self.pointcloud is not None,
            )
            self.update_pcd_infos()
            self.zoom_into2(logdata)
        else:
            logging.warning("No point clouds left!")
            
    def get_prev_pcd(self, logdata: dict) -> None:
        #logging.info("Loading previous point cloud...")
        if self.current_id > 0:
            self.current_id -= 1
            self.save_current_perspective()
            self.pointcloud = PointCloud.from_file(
                self.pcd_path,
                self.saved_perspective
            )
            self.update_pcd_infos()
            self.zoom_into2(logdata)
        else:
            raise Exception("No point cloud left for loading!")
            
    ################################################################
    def get_next_pcd2(self, logdata: dict) -> None:
        #logging.info("Loading next point cloud...")
        if self.pcds_left():
            self.current_id += 1
            self.save_current_perspective()
            self.pointcloud = PointCloud.from_file(
                self.pcd_path,
                self.saved_perspective,
                write_buffer=self.pointcloud is not None,
            )
            #self.pointcloud.set_trans_z(self.pointcloud.trans_z + self.zoom_distance)
            self.update_pcd_infos()
            #self.zoom_into2(logdata)
            
        #else:
        #    logging.warning("No point clouds left!")
            
    def get_prev_pcd2(self, logdata: dict) -> None:
        #logging.info("Loading previous point cloud...")
        if self.current_id > 0:
            self.current_id -= 1
            self.save_current_perspective()
            self.pointcloud = PointCloud.from_file(
                self.pcd_path,
                self.saved_perspective
            )
            #self.pointcloud.set_trans_z(self.pointcloud.trans_z + self.zoom_distance)
            self.update_pcd_infos()
            #self.zoom_into2(logdata)
        else:
            raise Exception("No point cloud left for loading!")
    ################################################################
    
    def get_labels_from_file(self) -> List[BBox]:
        bboxes = self.label_manager.import_labels(self.pcd_path)
        #logging.info(green("Loaded %s bboxes!" % len(bboxes)))
        
        return bboxes

    # SETTER
    def set_view(self, view: "GUI") -> None:
        self.view = view
        self.view.gl_widget.set_pointcloud_controller(self)

    def save_labels_into_file(self, bboxes: List[BBox]) -> None:
        if self.pcds:
            self.label_manager.export_labels(self.pcd_path, bboxes)
            self.collected_object_classes.update(
                {bbox.get_classname() for bbox in bboxes}
            )
            self.view.update_label_completer(self.collected_object_classes)
            self.view.update_default_object_class_menu(self.collected_object_classes)
        else:
            logging.warning("No point clouds to save labels for!")
    ##############################################################        
    def save_labels_into_file2(self, logging: dict) -> None:
        if self.pcds:
            self.label_manager.export_labels2(self.pcd_path, logging)
        else:
            logging.warning("No point clouds to save labels for!")
            
    def get_filepath(self) -> dict:
        #logging.info("get_filepath")
        #logging.info(f"get_filepath.. self.pcds..{self.pcds}")
        #logging.info(f"get_filepath.. self.pcds..{self.current_id}") #-1
        #logging.info(f"get_filepath.. self.pcds..{self.pcd_path}")
        
        labels = self.label_manager.get_filepath2(self.pcd_path)
        return labels
        #logging.info(f"get_filepath.. self.pcd_path..{self.pcd_path}")
        """
        if self.pcds:
            return self.label_manager.get_filepath2(self.pcd_path)
        else:
            logging.warning("No point clouds to save labels for!")
            """
    def get_filepath_real(self) -> Path:
        #logging.info("get_filepath")
        #logging.info(f"get_filepath.. self.pcds..{self.pcds}")
        #logging.info(f"get_filepath.. self.pcds..{self.current_id}") #-1
        #logging.info(f"get_filepath.. self.pcds..{self.pcd_path}")
        
        #logging.info("get_filepath_real")
        labels = self.label_manager.get_filepath_real2(self.pcd_path)
        return labels

    def get_pers(self) -> dict:
        labels = self.label_manager.get_pers2(self.pcd_path)
        return labels
    ##############################################################
    
    def save_current_perspective(self) -> None:
        #if config.getboolean("USER_INTERFACE", "KEEP_PERSPECTIVE") and self.pointcloud:
        if self.pointcloud:
            self.saved_perspective = Perspective.from_point_cloud(self.pointcloud)
            #logging.info(f"!!Saved current perspective ({self.saved_perspective}).")

    # MANIPULATOR
    def rotate_around_x(self, dangle) -> None:
        assert self.pointcloud is not None
        self.pointcloud.set_rot_x(self.pointcloud.rot_x - dangle)

    def rotate_around_y(self, dangle) -> None:
        assert self.pointcloud is not None
        self.pointcloud.set_rot_y(self.pointcloud.rot_y - dangle)

    def rotate_around_z(self, dangle) -> None:
        assert self.pointcloud is not None
        self.pointcloud.set_rot_z(self.pointcloud.rot_z - dangle)

    def translate_along_x(self, distance) -> None:
        assert self.pointcloud is not None
        self.pointcloud.set_trans_x(
            self.pointcloud.trans_x - distance * PointCloudManger.TRANSLATION_FACTOR
        )

    def translate_along_y(self, distance) -> None:
        assert self.pointcloud is not None
        self.pointcloud.set_trans_y(
            self.pointcloud.trans_y + distance * PointCloudManger.TRANSLATION_FACTOR
        )

    def translate_along_z(self, distance) -> None:
        assert self.pointcloud is not None
        self.pointcloud.set_trans_z(
            self.pointcloud.trans_z - distance * PointCloudManger.TRANSLATION_FACTOR
        )
        

    def zoom_into(self, distance) -> None:
        assert self.pointcloud is not None
        self.zoom_distance = distance * PointCloudManger.ZOOM_FACTOR
        self.pointcloud.set_trans_z(self.pointcloud.trans_z + self.zoom_distance)
        
        #logging.info(f"!!self.pointcloud.set_trans_z = ({self.pointcloud.set_trans_z(self.pointcloud.trans_z + self.zoom_distance)})")

    #####################################################
    def zoom_into2(self, logdata: dict) -> None:
        assert self.pointcloud is not None
        

        if logdata:
            if len(logdata["logging"]) > 0:
                logging_last = logdata["logging"][len(logdata["logging"])-1]
                #logging.info(f"logging_last ({logging_last})") #logging_last ({'index': 6, 'id': 'TEST', 'condition': 'TEST_4000', 'pcd': 'A_scene0059_01.ply', 'time': '2023-03-11 11:10:57.425932', 'active': 'zoom_into', 'input': 'mouse_scroll_event', 'input_detail': 'mouse_scroll', 'mouse_position_x': '', 'mouse_position_y': ''})
                #logging.info(f"logging_last ({type(logging_last)})")  #logging_last (<class 'dict'>)
                
                if "rot_x" in logging_last:
                    
                    self.pointcloud.set_rot_x(logging_last["rot_x"])
                    self.pointcloud.set_rot_y(logging_last["rot_y"])
                    self.pointcloud.set_rot_z(logging_last["rot_z"])
                    
                    #self.pointcloud.draw_pointcloud
                    self.pointcloud.set_trans_x(logging_last["trans_x"])
                    self.pointcloud.set_trans_y(logging_last["trans_y"])
                    self.pointcloud.set_trans_z(logging_last["trans_z"])

    #####################################################
    
    def reset_translation(self) -> None:
        assert self.pointcloud is not None
        self.pointcloud.reset_perspective()

    def reset_rotation(self) -> None:
        assert self.pointcloud is not None
        self.pointcloud.rot_x, self.pointcloud.rot_y, self.pointcloud.rot_z = (0, 0, 0)
    
    """
    def reset_rotation1(self) -> None:
        assert self.pointcloud is not None
        self.pointcloud.rot_x, self.pointcloud.rot_y, self.pointcloud.rot_z = self.saved_perspective1
    def reset_rotation2(self) -> None:
        assert self.pointcloud is not None
        self.pointcloud.rot_x, self.pointcloud.rot_y, self.pointcloud.rot_z = self.saved_perspective2
    def reset_rotation3(self) -> None:
        assert self.pointcloud is not None
        self.pointcloud.rot_x, self.pointcloud.rot_y, self.pointcloud.rot_z = self.saved_perspective3
    """
    
    def reset_transformations(self) -> None:
        self.reset_translation()
        self.reset_rotation()

    def rotate_pointcloud(
        self, axis: List[float], angle: float, rotation_point: Point3D
    ) -> None:
        assert self.pointcloud is not None and self.pcd_name is not None
        # Save current, original point cloud in ORIGINALS_FOLDER
        originals_path = self.pcd_folder.joinpath(PointCloudManger.ORIGINALS_FOLDER)
        originals_path.mkdir(parents=True, exist_ok=True)
        copyfile(
            str(self.pcd_path),
            str(originals_path.joinpath(self.pcd_name)),
        )
        #logging.info("Copyied the original point cloud to %s.", blue(originals_path))

        # Rotate and translate point cloud
        rotation_matrix = o3d.geometry.get_rotation_matrix_from_axis_angle(
            np.multiply(axis, angle)
        )
        o3d_pointcloud = Open3DHandler().to_open3d_point_cloud(self.pointcloud)
        o3d_pointcloud.rotate(rotation_matrix, center=tuple(rotation_point))
        o3d_pointcloud.translate([0, 0, -rotation_point[2]])
        #logging.info("Rotating point cloud...")
        #print_column(["Angle:", str(np.round(angle, 3))])
        #print_column(["Axis:", str(np.round(axis, 3))])
        #print_column(["Point:", str(np.round(rotation_point, 3))], last=True)

        # Check if pointcloud is upside-down
        if abs(self.pointcloud.pcd_mins[2]) > self.pointcloud.pcd_maxs[2]:
            logging.warning("Point cloud is upside down, rotating ...")
            o3d_pointcloud.rotate(
                o3d.geometry.get_rotation_matrix_from_xyz([np.pi, 0, 0]),
                center=(0, 0, 0),
            )

        self.pointcloud = PointCloud(
            self.pcd_path, *Open3DHandler().to_point_cloud(o3d_pointcloud)
        )
        self.pointcloud.to_file()

    # HELPER

    def get_perspective(self) -> Tuple[float, float, float]:
        assert self.pointcloud is not None
        x_rotation = self.pointcloud.rot_x
        z_rotation = self.pointcloud.rot_z

        cosz = round(np.cos(np.deg2rad(z_rotation)), 1)
        sinz = -round(np.sin(np.deg2rad(z_rotation)), 1)

        # detect bottom-up state
        bottom_up = 1
        if 30 < x_rotation < 210:
            bottom_up = -1
        return cosz, sinz, bottom_up

    # UPDATE GUI

    def update_pcd_infos(self, pointcloud_label: str = None) -> None:
        self.view.set_pcd_label(pointcloud_label or self.pcd_name or "")
        self.view.update_progress(self.current_id)

        if self.current_id <= 0:
            self.view.button_prev_pcd.setEnabled(False)
            if self.pcds:
                self.view.button_next_pcd.setEnabled(True)
        else:
            self.view.button_next_pcd.setEnabled(True)
            self.view.button_prev_pcd.setEnabled(True)
