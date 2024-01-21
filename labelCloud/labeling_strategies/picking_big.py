import logging
from typing import TYPE_CHECKING, Optional

import numpy as np

from . import BaseLabelingStrategy
from ..control.config_manager import config
from ..definitions import Mode, Point3D
from ..definitions.types import Point3D
from ..model import BBox
from ..utils import oglhelper as ogl

if TYPE_CHECKING:
    from ..view.gui import GUI

from ..__main__ import args
import datetime

class PickingStrategy_big(BaseLabelingStrategy):
    POINTS_NEEDED = 1
    PREVIEW = True

    def __init__(self, view: "GUI") -> None:
        super().__init__(view)
        #logging.info("Enabled drawing mode.")
        self.view.status_manager.update_status(
            "Please pick the location for the bounding box front center.",
            mode=Mode.DRAWING,
        )
        self.tmp_p1: Optional[Point3D] = None
        self.bbox_z_rotation: float = 0
        
        self.copied_id: float=-1
        self.copied_length: float = 0.7
        self.copied_width: float = 0.7
        self.copied_height: float = 0.7
        self.copied_x_rotation: float = 0
        self.copied_y_rotation: float = 0
        self.copied_z_rotation: float = 0
        
        self.className = 'class0'
    
    
    ##########################################
    def save_copied_id(self, copied_id: float
                       , length: float = None, width: float = None, height: float = None
                       , x_rotation: float = None, y_rotation: float = None, z_rotation: float = None) -> None:
        self.copied_id = copied_id
        self.copied_length=length
        self.copied_width=width
        self.copied_height=height
        self.copied_x_rotation=x_rotation
        self.copied_y_rotation=y_rotation
        self.copied_z_rotation=z_rotation
        #logging.info(f"save_copied_id ({x_rotation})")
    ##########################################
    
    ##########################################
    def get_strategy(self)->None:
        return True
    ##########################################
    
    def register_point(self, new_point: Point3D) -> None:
        self.point_1 = new_point
        self.points_registered += 1

    def register_tmp_point(self, new_tmp_point: Point3D) -> None:
        self.tmp_p1 = new_tmp_point

    def register_scrolling(self, distance: float) -> None:
        self.bbox_z_rotation += distance // 30

    def draw_preview(self) -> None:  # TODO: Refactor
        if self.tmp_p1:
            
            #logging.info("draw_preview!!!")
            
            
            """
            if self.className == '냉장고':
                tmp_bbox = BBox(
                    length=1, width=0.25, height=1.6,
                    *np.add(self.tmp_p1,[0, 0, 0],))
                tmp_bbox.set_z_rotation(self.bbox_z_rotation) 
                ogl.draw_cuboid(
                    tmp_bbox.get_vertices(), draw_vertices=True, vertex_color=(1, 1, 0, 1)
                )
            elif self.className == '캐비넷':
                tmp_bbox = BBox(
                    length=0.8, width=0.5, height=0.8,
                    *np.add(self.tmp_p1,[0, 0, 0],))
                tmp_bbox.set_z_rotation(self.bbox_z_rotation) 
                ogl.draw_cuboid(
                    tmp_bbox.get_vertices(), draw_vertices=True, vertex_color=(1, 1, 0, 1)
                )
            elif self.className == '바닥':
                tmp_bbox = BBox(
                    length=2.5, width=2, height=0.15,
                    *np.add(self.tmp_p1,[0, 0, 0],))
                tmp_bbox.set_z_rotation(self.bbox_z_rotation) 
                ogl.draw_cuboid(
                    tmp_bbox.get_vertices(), draw_vertices=True, vertex_color=(1, 1, 0, 1)
                )
            elif self.className == '의자':
                tmp_bbox = BBox(
                    length=0.5, width=0.5, height=1,
                    *np.add(self.tmp_p1,[0, 0, 0],))
                tmp_bbox.set_z_rotation(self.bbox_z_rotation) 
                ogl.draw_cuboid(
                    tmp_bbox.get_vertices(), draw_vertices=True, vertex_color=(1, 1, 0, 1)
                )
            elif self.className == '소파':
                tmp_bbox = BBox(
                    length=1, width=2, height=1,
                    *np.add(self.tmp_p1,[0, 0, 0],))
                tmp_bbox.set_z_rotation(self.bbox_z_rotation) 
                ogl.draw_cuboid(
                    tmp_bbox.get_vertices(), draw_vertices=True, vertex_color=(1, 1, 0, 1)
                )
            elif self.className == '기본':
                tmp_bbox = BBox(
                    length=0.1, width=0.1, height=0.1,
                    *np.add(self.tmp_p1,[0, 0, 0],))
                tmp_bbox.set_z_rotation(self.bbox_z_rotation) 
                ogl.draw_cuboid(
                    tmp_bbox.get_vertices(), draw_vertices=True, vertex_color=(1, 1, 0, 1)
                )
            """
            if True:
                tmp_bbox = BBox(
                    #cx=self.copied_x_rotation,
                    #cy=self.copied_y_rotation,
                    #cz=self.copied_z_rotation,
                    length=self.copied_length,
                    width=self.copied_width,
                    height=self.copied_height,
                    *np.add(
                        self.tmp_p1,
                        [
                            0,
                            0,
                            0
                            #config.getfloat("LABEL", "STD_BOUNDINGBOX_WIDTH") / 2,
                            #-config.getfloat("LABEL", "STD_BOUNDINGBOX_HEIGHT") / 3,
                        ],
                    )
                )
                tmp_bbox.set_z_rotation(self.bbox_z_rotation)
                #tmp_bbox.set_length(length=5)
                
                ogl.draw_cuboid(
                    tmp_bbox.get_vertices(), draw_vertices=True, vertex_color=(1, 1, 0, 1)
                )
                
            new_row = {'index': ''
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': ''
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_big_bbox_preview'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_big_bbox'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': ''
                       ,'rot_y': ''
                       ,'rot_z': ''
                       ,'trans_x': ''
                       ,'trans_y': ''
                       ,'trans_z': ''
                       }
            print(new_row)

    # Draw bbox with fixed dimensions and rotation at x,y in world space
    def get_bbox(self) -> BBox:  # TODO: Refactor
        assert self.point_1 is not None
        #logging.info(f"get_bbox ({self.copied_length})")
        final_bbox = BBox(
            #cx=self.copied_x_rotation,
            #cy=self.copied_y_rotation,
            #cz=self.copied_z_rotation,
            length=self.copied_length,
            width=self.copied_width,
            height=self.copied_height,
            *np.add(
                self.point_1,
                [
                    0,
                    0,
                    0
                    #config.getfloat("LABEL", "STD_BOUNDINGBOX_WIDTH") / 2,
                    #-config.getfloat("LABEL", "STD_BOUNDINGBOX_HEIGHT") / 3,
                ],
            )
        )
        final_bbox.set_z_rotation(self.bbox_z_rotation)
        
        new_row = {'index': ''
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': ''
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'button_big_bbox_draw'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'draw_big_bbox'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': ''
                   ,'rot_y': ''
                   ,'rot_z': ''
                   ,'trans_x': ''
                   ,'trans_y': ''
                   ,'trans_z': ''
                   }
        print(new_row)
        return final_bbox

    def reset(self) -> None:
        super().reset()
        self.tmp_p1 = None
        self.view.button_pick_bbox_big.setChecked(False)