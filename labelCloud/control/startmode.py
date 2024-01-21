"""
A module for aligning point clouds with the floor. The user has to span a triangle with
three points on the plane that serves as the ground. Then the old point cloud will be
saved up and the aligned current will overwrite the old.
"""
import logging
from typing import TYPE_CHECKING, Optional

import numpy as np

from ..definitions import Mode, Point3D
from ..utils import oglhelper as ogl
from .pcd_manager import PointCloudManger

if TYPE_CHECKING:
    from ..view.gui import GUI


class StartMode(object):
    def __init__(self, pcd_manager: PointCloudManger) -> None:
        #logging.info("startmode.py StartMode init...")
        self.pcd_manager = pcd_manager
        self.view: GUI
        self.is_active = False
        self.point_color = (1, 1, 0, 1)
        self.area_color = (1, 1, 0, 0.6)
        self.plane1: Optional[Point3D] = None
        self.plane2: Optional[Point3D] = None
        self.plane3: Optional[Point3D] = None

        self.tmp_p2: Optional[Point3D] = None
        self.tmp_p3: Optional[Point3D] = None
        

    def change_activation(self) -> None:
        if self.is_active :
            self.is_active = False
        else :
            self.is_active = True
        #logging.info(f"StartMode was changed to {self.is_active}!")
