import ctypes
import logging
from pathlib import Path
from typing import Optional, Tuple
from typing import TYPE_CHECKING, Set

import pkg_resources

import numpy as np
import numpy.typing as npt
import OpenGL.GL as GL

from . import Perspective
from ..control.config_manager import config
from ..definitions.types import Point3D, Rotations3D, Translation3D
from ..io.pointclouds import BasePointCloudHandler
from ..utils.logger import end_section, green, print_column, red, start_section, yellow

from ..__main__ import args
from ..control.label_manager import LabelManager

#if TYPE_CHECKING:
from ..control.bbox_controller import BoundingBoxController
#import argparse

# Get size of float (4 bytes) for VBOs
SIZE_OF_FLOAT = ctypes.sizeof(ctypes.c_float)


# Creates an array buffer in a VBO
def create_buffer(attributes) -> GL.glGenBuffers:
    bufferdata = (ctypes.c_float * len(attributes))(*attributes)  # float buffer
    buffersize = len(attributes) * SIZE_OF_FLOAT  # buffer size in bytes

    vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, buffersize, bufferdata, GL.GL_STATIC_DRAW)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vbo


def calculate_init_translation(
    center: Tuple[float, float, float], mins: npt.NDArray, maxs: npt.NDArray
) -> Point3D:
    """Calculates the initial translation (x, y, z) of the point cloud. Considers ...

    - the point cloud center
    - the point cloud extents
    - the far plane setting (caps zoom)
    """
    zoom = min(  # type: ignore
        np.linalg.norm(maxs - mins),
        config.getfloat("USER_INTERFACE", "far_plane") * 0.9,
    )
    #return tuple(-np.add(center, [0, 0, zoom]))  # type: ignore
    #trans = tuple(-np.add(center, [0, 0, zoom]))
    #logging.info(trans) # (-0.026106731630759522, 0.3697311514628229, -4.224846528939395)
    return tuple(-np.add(center, [0, 0, zoom]))  # type: ignore


def colorize_points(points: npt.NDArray, z_min: float, z_max: float) -> npt.NDArray:
    palette = np.loadtxt(
        pkg_resources.resource_filename("labelCloud.resources", "rocket-palette.txt")
    )
    palette_len = len(palette) - 1

    colors = np.zeros(points.shape)
    for ind, height in enumerate(points[:, 2]):
        colors[ind] = palette[round((height - z_min) / (z_max - z_min) * palette_len)]
    return colors


class PointCloud(object):
    def __init__(
        self,
        path: Path,
        points: npt.NDArray[np.float32],
        colors: Optional[npt.NDArray[np.float32]] = None,
        init_translation: Optional[Tuple[float, float, float]] = None,
        init_rotation: Optional[Tuple[float, float, float]] = None,
        write_buffer: bool = True
    ) -> None:
        #logging.info("point_cloud.py PointCloud init...")
        start_section(f"Loading {path.name}")
        #print_column(["path:", path])
        #print_column(["points:", points])
        self.path: Path = path
        
        
        self.points: npt.NDArray = points # [[ 0.03533109  2.4780002   0.162     ]...]
        #######################################################################
        self.points2: npt.NDArray = points 
        #######################################################################
        self.label_manager = LabelManager()
        
        
        self.colors: Optional[npt.NDArray] = (
            colors if type(colors) == np.ndarray and len(colors) > 0 else None
        )
        #######################################################################
        self.colors2 = self.colors
        #######################################################################

        
        self.vbo = None
        self.center: Point3D = tuple(np.sum(points[:, i]) / len(points) for i in range(3))  # type: ignore
        self.pcd_mins: npt.NDArray[np.float32] = np.amin(points, axis=0)
        self.pcd_maxs: npt.NDArray[np.float32] = np.amax(points, axis=0)
        self.init_translation: Point3D = calculate_init_translation(
            self.center, self.pcd_mins, self.pcd_maxs
        )
        #######################################################################
        self.vbo2 = None
        self.center2: Point3D = tuple(np.sum(points[:, i]) / len(points) for i in range(3))  # type: ignore
        self.pcd_mins2: npt.NDArray[np.float32] = np.amin(points, axis=0)
        self.pcd_maxs2: npt.NDArray[np.float32] = np.amax(points, axis=0)        
        self.init_translation2: Point3D = calculate_init_translation(
            self.center, self.pcd_mins, self.pcd_maxs
        )
        #######################################################################
        
        #self.init_rotation: Rotations3D = (0, 0, 0)
        self.init_rotation: Rotations3D = init_rotation or tuple([0, 0, 0])  # type: ignore
        
        
        
        if 'scene0003_00' in self.path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            self.init_rotation: Rotations3D = (float(307.2000000000028), float(0), float(229.6000000000065))
            self.init_translation: Rotations3D = (float(-1.6277662659797736), float(-1.7807321539305445), float(-7.801795228213171))
        elif 'scene0011_00' in self.path.stem:
            #logging.info("scene0011_00??")
            #self.init_rotation: Rotations3D = init_rotation or tuple([0, 0, 0])
            #self.init_rotation: Rotations3D = (float(293.00000000000034), float(0), float(258.5999999999992))
            #self.init_translation: Rotations3D = (float(-3.584390495328566), float(-1.0423442474816014), float(229.6000000000065))
            self.init_rotation: Rotations3D = (float(303.0000000000032), float(0), float(231.20000000000138))
            self.init_translation: Rotations3D = (float(-3.8844081209962416), float(-0.8002430615353502), float(-9.485779675951255))
        elif 'scene0047_00' in self.path.stem: 
            #self.init_rotation: Rotations3D = (float(297.20000000000044), float(0), float(246.4000000000009))
            #self.init_translation: Rotations3D = (float(-1.6097798406801427), float(-2.5096627535107907), float(-8.463258668367077))
            self.init_rotation: Rotations3D = (float(310.99999999999966), float(0), float(311.5999999999975))
            self.init_translation: Rotations3D = (float(-3.307779840680122), float(-2.281662753510798), float(-9.96325866836708))
        
        elif 'scene0059_01' in self.path.stem:    
            #self.init_rotation: Rotations3D = (float(297.00000000000307), float(0), float(302.60000000000116))
            #self.init_translation: Rotations3D = (float(-3.610943730341161), float(-2.5549915063714783), float(-8.57422913283588))
            self.init_rotation: Rotations3D = (float(298.6000000000029), float(0), float(249.80000000000317))
            self.init_translation: Rotations3D = (float(-1.4629437303412067), float(-2.248991506371489), float(-11.274229132835886))
       
        elif 'scene0021_00' in self.path.stem: 
            self.init_rotation: Rotations3D = (float(293.99999999999994), float(0), float(255.8000000000005))
            self.init_translation: Rotations3D = (float(-3.9159086715321583), float(-4.248493166037783), float(-9.188616474128734))
        elif 'scene0013_00' in self.path.stem:    
            self.init_rotation: Rotations3D = init_rotation or tuple([0, 0, 0])
        else:
            #ogging.info("scene0011_00??")
            self.init_rotation: Rotations3D = init_rotation or tuple([0, 0, 0])
        
            
        """
        self.init_rotation: Rotations3D = (
            float(args.perspective[0]), 
            float(args.perspective[1]), 
            float(args.perspective[2]))
        """
        
        # Point cloud transformations
        self.trans_x, self.trans_y, self.trans_z = self.init_translation
        self.rot_x, self.rot_y, self.rot_z = self.init_rotation
        
        #print_column(["self.colorless:", self.colorless]) # False
        if self.colorless and config.getboolean("POINTCLOUD", "COLORLESS_COLORIZE"):
            self.colors = colorize_points(
                self.points, self.pcd_mins[2], self.pcd_maxs[2]
            )
            #######################################################################
            self.colors2 = colorize_points(
                self.points2, self.pcd_mins[2], self.pcd_maxs[2]
            )
            #######################################################################
            #logging.info("Generated colors for colorless point cloud based on height.")

        if write_buffer:
            self.write_vbo()
            ########################
            self.write_vbo2()
            ########################
            
        #logging.info(green(f"Successfully loaded point cloud from {path}!"))
        self.print_details()
        end_section()
           
    @classmethod
    def from_file(
        cls,
        path: Path,
        perspective: Optional[Perspective] = None,
        write_buffer: bool = True,
    ) -> "PointCloud":
        init_translation, init_rotation = (None, None)
        
        if perspective:
            init_translation = perspective.translation
            init_rotation = perspective.rotation

        points, colors = BasePointCloudHandler.get_handler(
            path.suffix
        ).read_point_cloud(path=path)
        return cls(path, points, colors, init_translation, init_rotation, write_buffer)

    def to_file(self, path: Optional[Path] = None) -> None:
        if not path:
            path = self.path
        BasePointCloudHandler.get_handler(path.suffix).write_point_cloud(
            path=path, pointcloud=self
        )

    #####################################################
    def pointsInBBoxes(self, points2, mins, maxs) -> None:
    
        #logging.info(f"* get pointsInBBoxes.. mins :({mins}).") #BBOX MIN points.. ([array([ 3.42841979,  5.87185131, -0.05789034]), array([ 5.0971608 ,
        #logging.info(f"* get pointsInBBoxes.. maxs :({maxs}).")
        
        #logging.info(f"* get pointsInBBoxes.. points :({type(points2)}).") #points :(<class 'numpy.ndarray'>).
        #logging.info(f"* get pointsInBBoxes.. min points :({len(points2)}).") #:(5855863).
        # get pointsInBBoxes.. points :(<class 'OpenGL.constant.IntConstant'>).
        

        # get coordinates
        len_points = len(points2)
        len_bboxes = len(mins)
        #logging.info(f"* get pointsInBBoxes.. min len :({len(mins)}).") #min len :(10).
        
        points_in_boxes = []
        
        for i in range(len_points):
            x = points2[i][0]
            y = points2[i][1]
            z = points2[i][2]
            #logging.info(f"* get pointsInBBoxes.. x :({x}).") #x :(2.5220000743865967) # 계속 미친듯이 돌고있음
            is_coordinate = False
            
            for j in range(len_bboxes): 
              if mins[j][0]<=x and x<=maxs[j][0] :
                  #logging.info("* X points in the BBOX.") 
                  if mins[j][1]<=y and y<=maxs[j][1] : 
                      #logging.info("* Y points in the BBOX.") 
                      if mins[j][2]<=z and maxs[j][2]<=z :
                          #logging.info("* Z points in the BBOX.") 
                          is_coordinate = True
            if is_coordinate == True :
                points_in_boxes.append([x,y,z])
                
        #logging.info(f"* get pointsInBBoxes.. points_in_boxes :({len(points_in_boxes), len(points2)}).") #((115836, 5855863))
        #logging.info(f"* get pointsInBBoxes.. points_in_boxes :({points_in_boxes}).") # (5.502635, 4.162, 0.6700001), 
        #logging.info(f"* get pointsInBBoxes.. points_in_boxes :({points2}).") #:([[2.522      0.47800002 0.15648337]
        
        return points2
    #####################################################
    @property
    def colorless(self):
        return self.colors is None

    # GETTERS AND SETTERS
    def get_no_of_points(self) -> int:
        return len(self.points)
        
    def get_no_of_colors(self) -> int:
        return len(self.colors) if self.colors else 0
    
    #######################################################################
    def get_no_of_points2(self) -> int:
        return len(self.points2)
    
    def get_no_of_colors2(self) -> int:
        return len(self.colors2) if self.colors2 else 0
    #######################################################################

    def get_rotations(self) -> Rotations3D:
        return self.rot_x, self.rot_y, self.rot_z

    def get_translation(self) -> Translation3D:
        return self.trans_x, self.trans_y, self.trans_z

    def get_mins_maxs(self) -> Tuple[npt.NDArray, npt.NDArray]:
        return self.pcd_mins, self.pcd_maxs

    def get_min_max_height(self) -> Tuple[float, float]:
        return self.pcd_mins[2], self.pcd_maxs[2]
    
    #######################################################################
    def get_mins_maxs2(self) -> Tuple[npt.NDArray, npt.NDArray]:
        return self.pcd_mins2, self.pcd_maxs2

    def get_min_max_height2(self) -> Tuple[float, float]:
        return self.pcd_mins2[2], self.pcd_maxs2[2]
    #######################################################################
    
    def set_rot_x(self, angle) -> None:
        self.rot_x = angle % 360

    def set_rot_y(self, angle) -> None:
        self.rot_y = angle % 360

    def set_rot_z(self, angle) -> None:
        self.rot_z = angle % 360

    def set_rotations(self, x: float, y: float, z: float) -> None:
        self.rot_x = x % 360
        self.rot_y = y % 360
        self.rot_z = z % 360

    def set_trans_x(self, val) -> None:
        self.trans_x = val

    def set_trans_y(self, val) -> None:
        self.trans_y = val

    def set_trans_z(self, val) -> None:
        self.trans_z = val

    def set_translations(self, x: float, y: float, z: float) -> None:
        self.trans_x = x
        self.trans_y = y
        self.trans_z = z

    # MANIPULATORS

       
    def transform_data(self) -> npt.NDArray:
        if self.colorless:
            attributes = self.points
        else:
            # Merge coordinates and colors in alternating order
            attributes = np.concatenate((self.points, self.colors), axis=1)  # type: ignore

        return attributes.flatten()  # flatten to single list

    def write_vbo(self) -> None:
        self.vbo = create_buffer(self.transform_data())
        
    #######################################################################    
    def transform_data2(self) -> npt.NDArray:
        if self.colorless:
            attributes = self.points2
        else:
            # Merge coordinates and colors in alternating order
            attributes = np.concatenate((self.points2, self.colors2), axis=1)  # type: ignore

        return attributes.flatten()  # flatten to single list

    def write_vbo2(self) -> None:
        self.vbo2 = create_buffer(self.transform_data2())
    #######################################################################
    
    def draw_pointcloud(self) -> None:
        GL.glTranslate(
            self.trans_x, self.trans_y, self.trans_z
        )  # third, pcd translation

        pcd_center = np.add(
            self.pcd_mins, (np.subtract(self.pcd_maxs, self.pcd_mins) / 2)
        )
        GL.glTranslate(*pcd_center)  # move point cloud back

        GL.glRotate(self.rot_x, 1.0, 0.0, 0.0)
        GL.glRotate(self.rot_y, 0.0, 1.0, 0.0)  # second, pcd rotation
        GL.glRotate(self.rot_z, 0.0, 0.0, 1.0)

        GL.glTranslate(*(pcd_center * -1))  # move point cloud to center for rotation

        #GL.glPointSize(config.getfloat("POINTCLOUD", "POINT_SIZE"))
        #GL.glPointSize(20.0)
        
        #logging.info(f"{self.rot_x} {self.rot_y} {self.rot_z} {self.trans_x} {self.trans_y} {self.trans_z} ")
        if self.trans_z < -6.0:
            GL.glPointSize(4.0)
        elif self.trans_z < -0.0:
            GL.glPointSize(10.0)
        else:
            GL.glPointSize(20.0)
            
        #GL.glPointSize(4.0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

        if self.colorless:
            stride = 3 * SIZE_OF_FLOAT  # (12 bytes) : [x, y, z] * sizeof(float)
            GL.glPointSize(1)
            GL.glColor3d(
                *config.getlist("POINTCLOUD", "COLORLESS_COLOR")
            )  # IDEA: Color by (height) position
        else:
            stride = (
                6 * SIZE_OF_FLOAT
            )  # (24 bytes) : [x, y, z, r, g, b] * sizeof(float)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glVertexPointer(3, GL.GL_FLOAT, stride, None)

        if not self.colorless:
            GL.glEnableClientState(GL.GL_COLOR_ARRAY)
            offset = (
                3 * SIZE_OF_FLOAT
            )  # (12 bytes) : the rgb color starts after the 3 coordinates x, y, z
            GL.glColorPointer(3, GL.GL_FLOAT, stride, ctypes.c_void_p(offset))
        GL.glDrawArrays(GL.GL_POINTS, 0, self.get_no_of_points())  # Draw the points

        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        if not self.colorless:
            GL.glDisableClientState(GL.GL_COLOR_ARRAY)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    #######################################################################
    def draw_pointcloud2(self, bbox_min, bbox_max) -> None:
        
        #logging.info(f"** draw_pointcloud2 bbox_min(): ({bbox_min}).") # GOOD
        #logging.info(f"** draw_pointcloud2 bbox_max(): ({bbox_max}).") # GOOD #: ([array([4.17841979, 6.42185131, 0.09210966]), array([5.8471608 , 
        
        self.points2 = self.pointsInBBoxes(self.points, bbox_min, bbox_max)
        
        GL.glTranslate(
            self.trans_x, self.trans_y, self.trans_z
        )  # third, pcd translation

        pcd_center = np.add(
            self.pcd_mins2, (np.subtract(self.pcd_maxs2, self.pcd_mins2) / 2)
        )
        GL.glTranslate(*pcd_center)  # move point cloud back

        GL.glRotate(self.rot_x, 1.0, 0.0, 0.0)
        GL.glRotate(self.rot_y, 0.0, 1.0, 0.0)  # second, pcd rotation
        GL.glRotate(self.rot_z, 0.0, 0.0, 1.0)

        GL.glTranslate(*(pcd_center * -1))  # move point cloud to center for rotation

        GL.glPointSize(config.getfloat("POINTCLOUD", "POINT_SIZE"))
        #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        #######################################################################  
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo2)
        #######################################################################  
        if self.colorless:
            stride = 3 * SIZE_OF_FLOAT  # (12 bytes) : [x, y, z] * sizeof(float)
            GL.glPointSize(1)
            GL.glColor3d(
                *config.getlist("POINTCLOUD", "COLORLESS_COLOR")
            )  # IDEA: Color by (height) position
        else:
            stride = (
                6 * SIZE_OF_FLOAT
            )  # (24 bytes) : [x, y, z, r, g, b] * sizeof(float)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glVertexPointer(3, GL.GL_FLOAT, stride, None)

        if not self.colorless:
            GL.glEnableClientState(GL.GL_COLOR_ARRAY)
            offset = (
                3 * SIZE_OF_FLOAT
            )  # (12 bytes) : the rgb color starts after the 3 coordinates x, y, z
            GL.glColorPointer(3, GL.GL_FLOAT, stride, ctypes.c_void_p(offset))
        
        #######################################################################  
        #GL.glDrawArrays(GL.GL_POINTS, 0, self.get_no_of_points2())  # Draw the points
        GL.glDrawArrays(GL.GL_POINTS, 0, self.get_no_of_points2())  # Draw the points
        #######################################################################  
        
        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        if not self.colorless:
            GL.glDisableClientState(GL.GL_COLOR_ARRAY)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    #######################################################################
    
    
    def reset_perspective(self) -> None:
        self.trans_x, self.trans_y, self.trans_z = self.init_rotation
        self.rot_x, self.rot_y, self.rot_z = self.init_rotation

    def print_details(self) -> None:
        
        """
        print_column(
            [
                "Number of Points:",
                green(len(self.points))
                if len(self.points) > 0
                else red(len(self.points)),
            ]
        )
        print_column(
            [
                "Number of Colors:",
                yellow("None")
                if self.colorless
                else green(len(self.colors))  # type: ignore
                if len(self.colors) == len(self.points)  # type: ignore
                else red(len(self.colors)),  # type: ignore
            ]
        )
        print_column(["Point Cloud Center:", str(np.round(self.center, 2))])
        print_column(["Point Cloud Minimums:", str(np.round(self.pcd_mins, 2))])
        print_column(["Point Cloud Maximums:", str(np.round(self.pcd_maxs, 2))])
        print_column(
            ["Initial Translation:", str(np.round(self.init_translation, 2))], last=True
        )
        """
        True
