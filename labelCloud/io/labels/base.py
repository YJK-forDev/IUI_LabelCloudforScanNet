import json
from abc import ABC, abstractmethod
import logging
from pathlib import Path
from typing import List, Optional, Union

import numpy as np

from ...model import BBox
from ...__main__ import args

class BaseLabelFormat(ABC):
    FILE_ENDING = ".json"
    ID = args.id

    def __init__(
        self, label_folder: Path, export_precision: int, relative_rotation: bool = False
    ) -> None:
        self.label_folder = label_folder
        #logging.info("Set export strategy to %s." % self.__class__.__name__)
        self.export_precision = export_precision
        self.relative_rotation = relative_rotation
        self.file_ending = ".json"
        if relative_rotation:
            True
            #logging.info("Saving rotations relatively to positve x-axis in radians (-pi..+pi).")
        elif self.__class__.__name__ == "VerticesFormat":
            True
            #logging.info("Saving rotations implicitly in the vertices coordinates.")
        else:
            True
            #logging.info("Saving rotations absolutely to positve x-axis in degrees (0..360°).")

    def update_label_folder(self, new_label_folder: Path) -> None:
        self.label_folder = new_label_folder
        #logging.info(f"Updated label folder to {new_label_folder}.")

    def round_dec(self, x, decimal_places: Optional[int] = None) -> List[float]:
        if not decimal_places:
            decimal_places = self.export_precision
        return np.round(x, decimal_places).tolist()

    def save_label_to_file(self, pcd_path: Path, data: Union[dict, str]) -> Path:
        label_path = self.label_folder.joinpath(pcd_path.stem + self.FILE_ENDING)
        #label_path = self.label_folder.joinpath(self.ID, pcd_path.stem + self.FILE_ENDING)
        #label_folder = self.label_folder.joinpath(self.ID)
        #logging.info(f"save_label_to_file : label_path {label_path}.") #labels\scene0002_00_vh_clean_2.json.
        #logging.info(f"save_label_to_file : pcd_path.stem {pcd_path.stem}.") #scene0002_00_vh_clean_2
        #logging.info(f"save_label_to_file : label_folder {label_folder}.") #scene0002_00_vh_clean_2
        
       # if not label_folder.exists():
        #    label_folder.mkdir(parents=True)
            
        if label_path.is_file():
            True
            #logging.info("File %s already exists, replacing file ..." % label_path)
        if label_path.suffix == ".json":
            with open(label_path, "w") as write_file:
                json.dump(data, write_file, indent="\t")
        elif label_path.suffix == ".txt" and isinstance(data, str):
            with open(label_path, "w") as write_file:
                write_file.write(data)
        else:
            raise ValueError("Received unknown label format/ type.")
        return label_path
    
    def get_filepath4(self, pcd_path: Path) -> dict:
        
        #logging.info("get_filepath4")
        label_path = self.label_folder.joinpath(pcd_path.stem + self.FILE_ENDING)
        #logging.info(f"label_path!! {label_path}!")
        
        data2 = dict()
        data2["logging"] = []
        
        if label_path.is_file():
            with self.label_path.open("r") as read_file:
                #logging.info("label_path!! is file()!")
                data2 = json.load(read_file)
        
        #logging.info(f"data2 path {self.data2}!")
        return data2
    

    @abstractmethod
    def import_labels(self, pcd_path: Path) -> List[BBox]:
        raise NotImplementedError

    @abstractmethod
    def export_labels(self, bboxes: List[BBox], pcd_path: Path) -> None:
        raise NotImplementedError


# ---------------------------------------------------------------------------- #
#                               Helper Functions                               #
# ---------------------------------------------------------------------------- #


def abs2rel_rotation(abs_rotation: float) -> float:
    """Convert absolute rotation 0..360° into -pi..+pi from x-Axis.

    :param abs_rotation: Counterclockwise rotation from x-axis around z-axis
    :return: Relative rotation from x-axis around z-axis
    """
    rel_rotation = np.deg2rad(abs_rotation)
    if rel_rotation > np.pi:
        rel_rotation = rel_rotation - 2 * np.pi
    return rel_rotation


def rel2abs_rotation(rel_rotation: float) -> float:
    """Convert relative rotation from -pi..+pi into 0..360° from x-Axis.

    :param rel_rotation: Rotation from x-axis around z-axis
    :return: Counterclockwise rotation from x-axis around z-axis
    """
    abs_rotation = np.rad2deg(rel_rotation)
    if abs_rotation < 0:
        abs_rotation = abs_rotation + 360
    return abs_rotation
