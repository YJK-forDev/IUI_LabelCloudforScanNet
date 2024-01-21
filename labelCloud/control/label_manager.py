import logging
from pathlib import Path
from typing import List

from ..io.labels import BaseLabelFormat, CentroidFormat, KittiFormat, VerticesFormat
from ..model import BBox
from .config_manager import config
from ..__main__ import args

def get_label_strategy(export_format: str, label_folder: Path) -> "BaseLabelFormat":
    #logging.info(f"export_format ({export_format}).") #(centroid_abs).
    export_format = "vertices"
    
    if export_format == "vertices":
        return VerticesFormat(label_folder, LabelManager.EXPORT_PRECISION)
    elif export_format == "centroid_rel":
        return CentroidFormat(
            label_folder, LabelManager.EXPORT_PRECISION, relative_rotation=True
        )
    elif export_format == "kitti":
        return KittiFormat(
            label_folder, LabelManager.EXPORT_PRECISION, relative_rotation=True
        )
    elif export_format == "kitti_untransformed":
        return KittiFormat(
            label_folder,
            LabelManager.EXPORT_PRECISION,
            relative_rotation=True,
            transformed=False,
        )
    elif export_format != "centroid_abs":
        logging.warning(
            f"Unknown export strategy '{export_format}'. Proceeding with default (centroid_abs)!"
        )
        
    return CentroidFormat(
        label_folder, LabelManager.EXPORT_PRECISION, relative_rotation=False
    )


class LabelManager(object):
    LABEL_FORMATS = [
        "vertices",
        "centroid_rel",
        "centroid_abs",
        "kitti",
    ]
    STD_LABEL_FORMAT = config.get("LABEL", "label_format")
    EXPORT_PRECISION = config.getint("LABEL", "export_precision")
    ID = args.id
    condition = args.condition


    def __init__(
        self, strategy: str = STD_LABEL_FORMAT, path_to_label_folder: Path = None
    ) -> None:
        self.label_folder = path_to_label_folder or config.getpath(
            "FILE", "label_folder"
        )
        self.label_folder = self.label_folder.joinpath(self.ID)
        self.label_folder = self.label_folder.joinpath(self.condition)
        
        if not self.label_folder.is_dir():
            self.label_folder.mkdir(parents=True)
        #logging.info(f"LabelManager : label_folder ({self.label_folder}).") #LabelManager : label_folder (labels).

        self.label_strategy = get_label_strategy(strategy, self.label_folder)
        
        
        self.logging_file = self.label_folder.joinpath('my.log') #
        #if not self.logging_file.is_dir():
            #logging.handlers.RotatingFileHandler(filename=self.logging_file)
            #console.log('MAKE IT!')
        #logging.info(f"LabelManager : logging_file ({self.logging_file}).")  #(labels\TEST_02\my.log).
        #logging.basicConfig(filename=self.logging_file, level=logging.DEBUG)
        #self.label_strategy2 = get_label_strategy(strategy, self.label_folder)

    def import_labels(self, pcd_path: Path) -> List[BBox]:
        try:
            #logging.info(f"import_labels pcd_path : ({pcd_path}).") #(pointclouds\scene0002_00_cabinet.ply)
            return self.label_strategy.import_labels(pcd_path)
        except KeyError as key_error:
            logging.warning("Found a key error with %s in the dictionary." % key_error)
            logging.warning(
                "Could not import labels, please check the consistency of the label format."
            )
            return []
        except AttributeError as attribute_error:
            logging.warning(
                "Attribute Error: %s. Expected a dictionary." % attribute_error
            )
            logging.warning(
                "Could not import labels, please check the consistency of the label format."
            )
            return []

    def export_labels(self, pcd_path: Path, bboxes: List[BBox]) -> None:
        """
        pcd_path2 = pcd_path / 'test' 
        logging.info(f"pcd_path2 ({pcd_path2}).")
        if not pcd_path2.exists():
            pcd_path2.mkdir(parents=True)
        """
        #logging.info(f"export_labels : pcd_path ({pcd_path}).") #(pointclouds\scene0002_00_vh_clean_2.ply).
        
        self.label_strategy.export_labels(bboxes, pcd_path)
    
    ##############################################################
    def export_labels2(self, pcd_path: Path, logtext: dict) -> None:
        """
        pcd_path2 = pcd_path / 'test' 
        logging.info(f"pcd_path2 ({pcd_path2}).")
        if not pcd_path2.exists():
            pcd_path2.mkdir(parents=True)
        """
        #logging.info(f"export_labels : pcd_path ({pcd_path}).") #(pointclouds\scene0002_00_vh_clean_2.ply).
        
        #logging.debug('TEST 01-29 12:00')
        #test_txt = 'TEST for logging...'
        self.label_strategy.export_labels2(logtext, pcd_path)
        #self.label_strategy2.export_labels2(logtext, pcd_path)

    def get_filepath2(self, pcd_path: Path) -> dict:
        """
        pcd_path2 = pcd_path / 'test' 
        logging.info(f"pcd_path2 ({pcd_path2}).")
        if not pcd_path2.exists():
            pcd_path2.mkdir(parents=True)
        """
        #logging.info(f"get_filepath2")
        return self.label_strategy.get_filepath3(pcd_path)
    
    def get_filepath_real2(self, pcd_path: Path) -> Path:

        #logging.info(f"get_filepath_real2")
        return self.label_strategy.get_filepath_real3(pcd_path)
    
    def get_pers2(self, pcd_path: Path) -> dict:
        """
        pcd_path2 = pcd_path / 'test' 
        logging.info(f"pcd_path2 ({pcd_path2}).")
        if not pcd_path2.exists():
            pcd_path2.mkdir(parents=True)
        """
        #logging.info(f"get_filepath2")
        return self.label_strategy.get_filepath3(pcd_path)
    ##############################################################