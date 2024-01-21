import logging
import os
from pathlib import Path
from typing import List, Optional, Union, Dict, Any
import json

#from typing import Optional, Union

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPoint

import numpy as np

from ..definitions import BBOX_SIDES, Color, Context
from ..utils import oglhelper
from ..view.gui import GUI
from .alignmode import AlignMode
from .bbox_controller import BoundingBoxController
from .drawing_manager import DrawingManager
from .pcd_manager import PointCloudManger

from .startmode import StartMode
from ..__main__ import args


#! /usr/bin/env python
#import logging
import datetime
#from ..labeling_strategies import PickingStrategy, PickingStrategy_s, OnePointStrategy, SpanningStrategy, PolyStrategy

class Controller:
    MOVEMENT_THRESHOLD = 0.1
    
    ID = args.id
    FILE_ENDING = ".json"
    Condition = args.condition
    
    def __init__(self) -> None:
        """Initializes all controllers and managers."""
        #logging.info("Controller init...")
       
        self.view: "GUI"
        self.pcd_manager = PointCloudManger()
        self.bbox_controller = BoundingBoxController()

        # Drawing states
        self.drawing_mode = DrawingManager(self.bbox_controller)
        self.align_mode = AlignMode(self.pcd_manager)
        self.start_mode = StartMode(self.pcd_manager)

        # Control states
        self.curr_cursor_pos: Optional[QPoint] = None  # updated by mouse movement
        self.last_cursor_pos: Optional[QPoint] = None  # updated by mouse click
        self.ctrl_pressed = False
        self.shift_pressed = False
        self.v_pressed = False
        self.space_pressed = False

        self.shift_pre = 0
        self.space_pre = False
        self.scroll_mode = False  # to enable the side-pulling
        self.last_copy_bbox = -1

        # Correction states
        self.side_mode = False
        self.selected_side: Optional[str] = None
        
        #logger
        ## 가져오기
        self.data2: Dict[str, Any] = dict()
        self.data2["logging"] = []
        self.classname = "class0"
        #logging.info(f"self.pcd_manager.pcd_folder {self.pcd_manager.pcd_path}!")
        
        self.cnt = 0
        #logging.info(f"data2 {self.data2}!")
        self.label_path = Path()
        
        self.pre_active = ""
        
        

    def startup(self, view: "GUI") -> None:
        """Sets the view in all controllers and dependent modules; Loads labels from file."""
        
        #logging.info("STARTUP!")
        self.view = view
        self.bbox_controller.set_view(self.view)
        self.pcd_manager.set_view(self.view)
        
        self.drawing_mode.set_view(self.view)
        self.align_mode.set_view(self.view)
        
        self.view.gl_widget.set_bbox_controller(self.bbox_controller)
        self.bbox_controller.pcd_manager = self.pcd_manager

        # Read labels from folders
        self.pcd_manager.read_pointcloud_folder2()
        self.next_pcd(save=False)
        
        
        #self.data2["logging"] = []
        self.data2 =  self.pcd_manager.get_filepath()
        self.data3 =  self.pcd_manager.get_pers()
        
        """
        self.view.button_class1.setStyleSheet(css_pushButton())
        self.view.button_class2.setStyleSheet(css_pushButton())
        self.view.button_class3.setStyleSheet(css_pushButton())
        self.view.button_class4.setStyleSheet(css_pushButton())
        self.view.button_class5.setStyleSheet(css_pushButton())
        """
        """
        self.label_path = self.pcd_manager.get_filepath_real()
        f = open(self.label_path, 'a')
        
        logging.info(f"label_path = {self.label_path}")
        logging.basicConfig(filename=self.label_path, level=logging.DEBUG)
        logging.debug('TEST 03-02 12:00')
        
        if self.label_path.suffix == ".txt" and isinstance(data, str):
            with open(self.label_path, "a") as write_file:
                write_file.write(data)
        """        

    def timeOutFunc(self) -> None:
        self.view.button_finished.setEnabled(False)
        
        ###logging::start
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'timeOut'
                   ,'input': 'auto'
                   ,'input_detail': 'auto'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)    
        self.pre_active = 'button_class1'
        ###logging::end
        
        
    def button_class1(self) -> None:
        self.classname = '바닥'
        self.view.button_class1.setEnabled(False)
        self.view.button_class2.setEnabled(True)
        self.view.button_class3.setEnabled(True)
        self.view.button_class4.setEnabled(True)
        self.view.button_class5.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class7.setEnabled(True)
        self.view.button_class8.setEnabled(True)
        self.view.button_class9.setEnabled(True)
        self.view.button_class10.setEnabled(True)
        self.view.button_class11.setEnabled(True)
        self.view.button_class12.setEnabled(True)
        
        #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
        #self.pcd_manager.class_pcd(self.data2, 14)
            
        ###logging::start
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'button_class1'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_class1'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)    
        self.pre_active = 'button_class1'
        ###logging::end
        
    def button_class2(self) -> None:
        self.classname = '벽'
        self.view.button_class1.setEnabled(True)
        self.view.button_class2.setEnabled(False)
        self.view.button_class3.setEnabled(True)
        self.view.button_class4.setEnabled(True)
        self.view.button_class5.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class7.setEnabled(True)
        self.view.button_class8.setEnabled(True)
        self.view.button_class9.setEnabled(True)
        self.view.button_class10.setEnabled(True)
        self.view.button_class11.setEnabled(True)
        self.view.button_class12.setEnabled(True)
        
        #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
        #self.pcd_manager.class_pcd(self.data2, 2)
            
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'button_class2'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_class2'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)   
        self.pre_active = 'button_class2'
        
        
    def button_class3(self) -> None:
        self.classname = '문'
        self.view.button_class1.setEnabled(True)
        self.view.button_class2.setEnabled(True)
        self.view.button_class3.setEnabled(False)
        self.view.button_class4.setEnabled(True)
        self.view.button_class5.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class7.setEnabled(True)
        self.view.button_class8.setEnabled(True)
        self.view.button_class9.setEnabled(True)
        self.view.button_class10.setEnabled(True)
        self.view.button_class11.setEnabled(True)
        self.view.button_class12.setEnabled(True)
        
        #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
        #self.pcd_manager.class_pcd(self.data2, 0)
            
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'button_class3'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_class3'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'button_class3'

    def button_class4(self) -> None:
        self.classname = '의자'
       
        self.view.button_class1.setEnabled(True)
        self.view.button_class2.setEnabled(True)
        self.view.button_class3.setEnabled(True)
        self.view.button_class4.setEnabled(False)
        self.view.button_class5.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class7.setEnabled(True)
        self.view.button_class8.setEnabled(True)
        self.view.button_class9.setEnabled(True)
        self.view.button_class10.setEnabled(True)
        self.view.button_class11.setEnabled(True)
        self.view.button_class12.setEnabled(True)
        
        #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
        #self.pcd_manager.class_pcd(self.data2, 4)
            
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'button_class4'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_class4'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'button_class4'
   
    def button_class5(self) -> None:
        self.classname = '소파'
       
        self.view.button_class1.setEnabled(True)
        self.view.button_class2.setEnabled(True)
        self.view.button_class3.setEnabled(True)
        self.view.button_class4.setEnabled(True)
        self.view.button_class5.setEnabled(False)
        self.view.button_class6.setEnabled(True)
        self.view.button_class6.setEnabled(True)
        self.view.button_class7.setEnabled(True)
        self.view.button_class8.setEnabled(True)
        self.view.button_class9.setEnabled(True)
        self.view.button_class10.setEnabled(True)
        self.view.button_class11.setEnabled(True)
        self.view.button_class12.setEnabled(True)
        
        #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
        #self.pcd_manager.class_pcd(self.data2, 5)
            
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'button_class5'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_class5'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'button_class5'
        
    def button_class6(self) -> None:
            self.classname = '탁자'
           
            self.view.button_class1.setEnabled(True)
            self.view.button_class2.setEnabled(True)
            self.view.button_class3.setEnabled(True)
            self.view.button_class4.setEnabled(True)
            self.view.button_class5.setEnabled(True)
            self.view.button_class6.setEnabled(False)
            self.view.button_class7.setEnabled(True)
            self.view.button_class8.setEnabled(True)
            self.view.button_class9.setEnabled(True)
            self.view.button_class10.setEnabled(True)
            self.view.button_class11.setEnabled(True)
            self.view.button_class12.setEnabled(True)
            
            #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
            #self.pcd_manager.class_pcd(self.data2, 6)
                
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_class6'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_class6'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_class6'
            
    def button_class7(self) -> None:
            self.classname = '캐비넷'
           
            self.view.button_class1.setEnabled(True)
            self.view.button_class2.setEnabled(True)
            self.view.button_class3.setEnabled(True)
            self.view.button_class4.setEnabled(True)
            self.view.button_class5.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class7.setEnabled(False)
            self.view.button_class8.setEnabled(True)
            self.view.button_class9.setEnabled(True)
            self.view.button_class10.setEnabled(True)
            self.view.button_class11.setEnabled(True)
            self.view.button_class12.setEnabled(True)
            
            #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
            #self.pcd_manager.class_pcd(self.data2, 7)
                
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_class7'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_class7'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_class7'
            
    def button_class8(self) -> None:
            self.classname = '카운터'
           
            self.view.button_class1.setEnabled(True)
            self.view.button_class2.setEnabled(True)
            self.view.button_class3.setEnabled(True)
            self.view.button_class4.setEnabled(True)
            self.view.button_class5.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class7.setEnabled(True)
            self.view.button_class8.setEnabled(False)
            self.view.button_class9.setEnabled(True)
            self.view.button_class10.setEnabled(True)
            self.view.button_class11.setEnabled(True)
            self.view.button_class12.setEnabled(True)
            
            #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
            #self.pcd_manager.class_pcd(self.data2, 8)
                
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_class8'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_class8'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_class8'
            
    def button_class9(self) -> None:
            self.classname = '냉장고'
           
            self.view.button_class1.setEnabled(True)
            self.view.button_class2.setEnabled(True)
            self.view.button_class3.setEnabled(True)
            self.view.button_class4.setEnabled(True)
            self.view.button_class5.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class7.setEnabled(True)
            self.view.button_class8.setEnabled(True)
            self.view.button_class9.setEnabled(False)
            self.view.button_class10.setEnabled(True)
            self.view.button_class11.setEnabled(True)
            self.view.button_class12.setEnabled(True)
            
            #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
            #self.pcd_manager.class_pcd(self.data2, 9)
                
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_class9'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_class9'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_class9'
            
    def button_class10(self) -> None:
            self.classname = '창문'
           
            self.view.button_class1.setEnabled(True)
            self.view.button_class2.setEnabled(True)
            self.view.button_class3.setEnabled(True)
            self.view.button_class4.setEnabled(True)
            self.view.button_class5.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class7.setEnabled(True)
            self.view.button_class8.setEnabled(True)
            self.view.button_class9.setEnabled(True)
            self.view.button_class10.setEnabled(False)
            self.view.button_class11.setEnabled(True)
            self.view.button_class12.setEnabled(True)
            
            #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
            #self.pcd_manager.class_pcd(self.data2, 10)
                
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_class10'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_class10'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_class10'
            
    def button_class11(self) -> None:
            self.classname = '싱크대'
           
            self.view.button_class1.setEnabled(True)
            self.view.button_class2.setEnabled(True)
            self.view.button_class3.setEnabled(True)
            self.view.button_class4.setEnabled(True)
            self.view.button_class5.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class7.setEnabled(True)
            self.view.button_class8.setEnabled(True)
            self.view.button_class9.setEnabled(True)
            self.view.button_class10.setEnabled(True)
            self.view.button_class11.setEnabled(False)
            self.view.button_class12.setEnabled(True)
            
            #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
            #self.pcd_manager.class_pcd(self.data2, 11)
                
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_class11'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_class11'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_class11'
            
    def button_class12(self) -> None:
            self.classname = '기타'
           
            self.view.button_class1.setEnabled(True)
            self.view.button_class2.setEnabled(True)
            self.view.button_class3.setEnabled(True)
            self.view.button_class4.setEnabled(True)
            self.view.button_class5.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class6.setEnabled(True)
            self.view.button_class7.setEnabled(True)
            self.view.button_class8.setEnabled(True)
            self.view.button_class9.setEnabled(True)
            self.view.button_class10.setEnabled(True)
            self.view.button_class11.setEnabled(True)
            self.view.button_class12.setEnabled(False)
            
            #if args.condition == 'C0' or args.condition == 'D0' or args.condition == 'C1' or args.condition == 'D1' or args.condition == 'C2' or args.condition == 'D2' :
            #self.pcd_manager.class_pcd(self.data2, 12)
                
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_class12'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_class12'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_class12'
            
            
    def loop_gui(self) -> None:
        
        """Function collection called during each event loop iteration."""
        self.set_crosshair()
        self.set_selected_side()
        self.view.gl_widget.updateGL()
        
        
        #self.reload2()
    
    """
    def button_pick_bbox(self)-> None:
        lambda: self.controller.drawing_mode.set_drawing_strategy(
            PickingStrategy(self)
        )
    """
    
    def reload(self) -> None:
        #logging.info("RELOAD")
        self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
        
        #logging.info(f"!!!!!RELOAD ({self.pcd_manager.pointcloud.trans_x,self.pcd_manager.pointcloud.trans_y,self.pcd_manager.pointcloud.trans_z})")

        self.data2 =  self.pcd_manager.get_filepath()
        """
        if len(self.data2) == 1: 
            logging.info(f"CANNOT reloaded! ({len(self.data2)})")
        
        else:
        """
        if True:
            self.pcd_manager.get_reload_pcd(self.data2)
            self.reset()
            self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
        
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'button_reload'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'button_reload'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'button_reload'
            
    def reload2(self) -> None:
        #logging.info("RELOAD")
        self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
        self.data2 =  self.pcd_manager.get_filepath()

    
        self.pcd_manager.get_reload_pcd(self.data2)
        self.reset()
        self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
    
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'button_reload'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_reload'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)

            
    # POINT CLOUD METHODS
    def next_pcd(self, save: bool = True) -> None:
        if save:
            self.save()
        if self.pcd_manager.pcds_left():
            self.data2 =  self.pcd_manager.get_filepath()
            self.pcd_manager.get_next_pcd(self.data2)
            self.reset()
            self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
            
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'next_pcd'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'next_pcd'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            #logging.info(f"data2{self.data2}")
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'next_pcd'
    
        else:
            self.view.update_progress(len(self.pcd_manager.pcds))
            self.view.button_next_pcd.setEnabled(False)

    def prev_pcd(self) -> None:
        self.save()
        if self.pcd_manager.current_id > 0:
            self.data2 =  self.pcd_manager.get_filepath()
            self.pcd_manager.get_prev_pcd(self.data2)
            self.reset()
            self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'prev_pcd'
                       ,'input': 'button_clicked'
                       ,'input_detail': 'prev_pcd'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)  
            self.pre_active = 'prev_pcd'
    """
    def transparency_pcd(self) -> None:
        self.save()
        self.pcd_manager.get_transparency_pcd()
        #self.reset()
        #self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
    """  
    """
    def test(self) -> None:
        #Saves all bounding boxes in the label file.
        logging.info("TEST...")
        
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'test'
                   ,'input': 'test'
                   ,'input_detail': 'test'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
    """    
        
    def custom_pcd(self, custom: int) -> None:
        self.save()
        self.pcd_manager.get_custom_pcd(custom)
        self.reset()
        self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())


    ##############################################################
    # BBOX CONTROL
    def button_bbox_up(self) -> None:
        self.bbox_controller.translate_along_z()
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'translate_along_z'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_up'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'translate_along_z'
        
    def button_bbox_down(self) -> None:
        self.bbox_controller.translate_along_z(down=True)
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'translate_along_z_down'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_down'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'translate_along_z_down'
        
    def button_bbox_left(self) -> None:
        self.bbox_controller.translate_along_x(left=True)
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'translate_along_x_left'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_left'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'translate_along_x_left'

    def button_bbox_right(self) -> None:
        self.bbox_controller.translate_along_x()
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'translate_along_x'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_right'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'translate_along_x'
        
    def button_bbox_forward(self) -> None:
        self.bbox_controller.translate_along_y(forward=True)
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'translate_along_y_forward'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_forward'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'translate_along_y_forward'
        
    def button_bbox_backward(self) -> None:
        self.bbox_controller.translate_along_y()
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'translate_along_y'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_backward'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'translate_along_y_forward'
        
    """
    def dial_bbox_z_rotation(self) -> None:
        self.bbox_controller.rotate_around_z(x, absolute=True)
        
        logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'translate_along_y_forward'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'dial_bbox_z_rotation'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   }
        self.data2["logging"].append(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        """
        
    def button_bbox_decrease_dimension(self) -> None:
        self.bbox_controller.scale(decrease=True)
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'scale_decrease'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_decrease_dimension'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'scale_decrease'
        
    def button_bbox_increase_dimension(self) -> None:
        self.bbox_controller.scale()
        
        #logging.info('button_bbox_up...')
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'scale_increase'
                   ,'input': 'button_pressed'
                   ,'input_detail': 'button_bbox_increase_dimension'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'scale_increase'
    
        """
    def edit_current_class(self) -> None:
        self.bbox_controller.set_classname()

        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'set_classname'
                   ,'input': 'textChanged'
                   ,'input_detail': 'edit_current_class'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   }
        self.data2["logging"].append(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        """
        
    def button_deselect_label(self) -> None:
        self.bbox_controller.deselect_bbox()

        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'deselect_bbox'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_deselect_label'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'deselect_bbox'
        
    def button_delete_label(self) -> None:
        self.bbox_controller.delete_current_bbox()

        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'delete_current_bbox'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_delete_label'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'delete_current_bbox'
        
    def label_list(self) -> None:
        self.bbox_controller.set_active_bbox()

        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'set_active_bbox'
                   ,'input': 'mouse_clicked'
                   ,'input_detail': 'label_list'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'set_active_bbox'
        
        
    def button_start(self) -> None:
        self.data2 =  self.pcd_manager.get_filepath()
        self.view.button_start.setEnabled(False)
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'start'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_start'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'start'
        
        self.view.timer3.start()

        #self.GUI().timer3.start()
        
        
        
    def button_finished(self) -> None:
        self.view.button_finished.setEnabled(False)
        
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'finished'
                   ,'input': 'button_clicked'
                   ,'input_detail': 'button_finished'
                   ,'mouse_position_x': ''
                   ,'mouse_position_y': ''
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'finished'
    ##############################################################

    # CONTROL METHODS
    def save(self) -> None:
        """Saves all bounding boxes in the label file."""
        #logging.info("saving saving saving...")
        self.pcd_manager.save_labels_into_file(self.bbox_controller.bboxes)
        
        
        
    ##############################################################
    # CONTROL METHODS
    def save2(self, logtext: str) -> None:
        """Saves all bounding boxes in the label file."""
        #logging.info("SAVE2...")
        #self.pcd_manager.save_labels_into_file2('TEST FOR ')
        
     ##############################################################

    def reset(self) -> None:
        """Resets the controllers and bounding boxes from the current screen."""
        self.bbox_controller.reset()
        self.drawing_mode.reset()
        self.align_mode.reset()

    # CORRECTION METHODS
    def set_crosshair(self) -> None:
        """Sets the crosshair position in the glWidget to the current cursor position."""
        if self.curr_cursor_pos:
            self.view.gl_widget.crosshair_col = Color.GREEN.value
            self.view.gl_widget.crosshair_pos = (
                self.curr_cursor_pos.x(),
                self.curr_cursor_pos.y(),
            )

    def set_selected_side(self) -> None:
        """Sets the currently hovered bounding box side in the glWidget."""
        if (
            (not self.side_mode)
            and self.curr_cursor_pos
            and self.bbox_controller.has_active_bbox()
            and (not self.scroll_mode)
        ):
            _, self.selected_side = oglhelper.get_intersected_sides(
                self.curr_cursor_pos.x(),
                self.curr_cursor_pos.y(),
                self.bbox_controller.get_active_bbox(),  # type: ignore
                self.view.gl_widget.modelview,
                self.view.gl_widget.projection,
            )
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'set_bbox_side'
                       ,'input': 'mouse_point'
                       ,'input_detail': 'mouse_point'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'set_bbox_side'
            
        if (
            self.selected_side
            and (not self.ctrl_pressed)
            and self.bbox_controller.has_active_bbox()
        ):
            self.view.gl_widget.crosshair_col = Color.RED.value
            side_vertices = self.bbox_controller.get_active_bbox().get_vertices()  # type: ignore
            self.view.gl_widget.selected_side_vertices = side_vertices[
                BBOX_SIDES[self.selected_side]
            ]
            self.view.status_manager.set_message(
                "Scroll to change the bounding box dimension.",
                context=Context.SIDE_HOVERED,
            )
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'change_bbox_side'
                       ,'input': 'mouse_scroll'
                       ,'input_detail': 'mouse_scroll'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'change_bbox_side'
            
            
        else:
            self.view.gl_widget.selected_side_vertices = np.array([])
            self.view.status_manager.clear_message(Context.SIDE_HOVERED)

    # EVENT PROCESSING
    def mouse_clicked(self, a0: QtGui.QMouseEvent) -> None:
        """Triggers actions when the user clicks the mouse."""
        self.last_cursor_pos = a0.pos()

        ########################################################## 
        if (
            self.drawing_mode.is_active()
            and 
            (a0.buttons() & QtCore.Qt.LeftButton)
            and (not self.ctrl_pressed)
        ):
            #if(self.shift_pressed):
            if(self.v_pressed):
                #logging.info("V pressed!!")
                self.drawing_mode.register_point(a0.x(), a0.y(), correction=True, cntinue=True, Right=False, className=self.classname)
                
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'create_plus_bbox_continuous'
                           ,'input': 'mouse_left_clicked, v_pressed'
                           ,'input_detail': 'mouse_left_clicked, v_pressed'
                           ,'mouse_position_x': a0.x()
                           ,'mouse_position_y': a0.y()
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                print(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                self.pre_active = 'create_plus_bbox_continuous'
                
            else: 
                self.drawing_mode.register_point(a0.x(), a0.y(), correction=True, cntinue=False, Right=False, className=self.classname)
                
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'create_plus_bbox'
                           ,'input': 'mouse_left_clicked'
                           ,'input_detail': 'mouse_left_clicked'
                           ,'mouse_position_x': a0.x()
                           ,'mouse_position_y': a0.y()
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                print(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                self.pre_active = 'create_plus_bbox'
                
        ########################################################## 
        elif (
            self.drawing_mode.is_active()
            and 
            (a0.buttons() & QtCore.Qt.RightButton)
            and (not self.ctrl_pressed)
        ):
            if(self.v_pressed):
            #if(self.space_pressed):
                self.drawing_mode.register_point(a0.x(), a0.y(), correction=True, cntinue=True, Right=True, className=self.classname)

                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'create_minus_bbox_continuous'
                           ,'input': 'mouse_right_clicked, v_pressed'
                           ,'input_detail': 'mouse_right_clicked, v_pressed'
                           ,'mouse_position_x': a0.x()
                           ,'mouse_position_y': a0.y()
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                print(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                self.pre_active = 'create_minus_bbox_continuous'
            else: 
                self.drawing_mode.register_point(a0.x(), a0.y(), correction=True, cntinue=False, Right=True, className=self.classname)
                
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'create_minus_bbox'
                           ,'input': 'mouse_right_clicked'
                           ,'input_detail': 'mouse_right_clicked'
                           ,'mouse_position_x': a0.x()
                           ,'mouse_position_y': a0.y()
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                print(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                self.pre_active = 'create_minus_bbox'
                
        ##########################################################  
        elif self.align_mode.is_active and (not self.ctrl_pressed):
            self.align_mode.register_point(
                self.view.gl_widget.get_world_coords(a0.x(), a0.y(), correction=False, className=self.classname)
            )
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                        ,'active': 'align_mode'
                        ,'input': 'mouse_clicked'
                        ,'input_detail': 'mouse_clicked'
                       ,'mouse_position_x': a0.x()
                       ,'mouse_position_y': a0.y()
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'align_mode'

        elif self.selected_side:
            self.side_mode = True
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'selected_side'
                       ,'input': 'mouse_point'
                       ,'input_detail': 'mouse_point'
                       ,'mouse_position_x': a0.x()
                       ,'mouse_position_y': a0.y()
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'selected_side'

    def mouse_double_clicked(self, a0: QtGui.QMouseEvent) -> None:
        """Triggers actions when the user double clicks the mouse."""
        
        """if self.drawing_mode.is_active() and (self.drawing_mode.drawing_strategy is not None) and (args.id is not None):
            logging.info(f"drawing_strategy is {self.drawing_mode.drawing_strategy}!")
            self.drawing_mode.register_point(
                a0.x(), a0.y(), correction=True, is_temporary=False, is_finished=True
            )
            
        else :
            self.bbox_controller.select_bbox_by_ray(a0.x(), a0.y())"""
        self.bbox_controller.select_bbox_by_ray(a0.x(), a0.y())
        
        self.data2 =  self.pcd_manager.get_filepath()
        self.cnt = self.cnt+1
        new_row = {'index': self.cnt
                   ,'id': args.id
                   ,'condition': args.condition
                   ,'pcd': self.pcd_manager.pcd_name
                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                   ,'active': 'select_bbox_by_ray'
                   ,'input': 'mouse_double_clicked'
                   ,'input_detail': 'mouse_double_clicked'
                   ,'mouse_position_x': a0.x()
                   ,'mouse_position_y': a0.y()
                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                   }
        self.data2["logging"].append(new_row)
        print(new_row)
        self.pcd_manager.save_labels_into_file2(self.data2)
        self.pre_active = 'select_bbox_by_ray'

    def mouse_move_event(self, a0: QtGui.QMouseEvent) -> None:
        """Triggers actions when the user moves the mouse."""
        self.curr_cursor_pos = a0.pos()  # Updates the current mouse cursor position
    

        # Methods that use absolute cursor position
        if self.drawing_mode.is_active():
            if (not self.ctrl_pressed):
                self.drawing_mode.register_point(a0.x(), a0.y(), correction=True, is_temporary=True, copied_id=self.last_copy_bbox , className=self.classname)
                #self.drawing_mode.register_point(4, 4, correction=True, is_temporary=True)
            

        elif self.align_mode.is_active and (not self.ctrl_pressed):
            self.align_mode.register_tmp_point(
                self.view.gl_widget.get_world_coords(a0.x(), a0.y(), correction=False)
            )


        if self.last_cursor_pos:
            dx = (
                self.last_cursor_pos.x() - a0.x()
            ) / 5  # Calculate relative movement from last click position
            dy = (self.last_cursor_pos.y() - a0.y()) / 5

            if (
                self.ctrl_pressed
                and (not self.drawing_mode.is_active())
                and (not self.align_mode.is_active)
                and (not self.shift_pressed)
            ):
                if a0.buttons() & QtCore.Qt.LeftButton:  # bbox rotation
                    self.bbox_controller.rotate_with_mouse(-dx, -dy)
                    
                    if self.pre_active != 'bbox_rotation':
                        self.data2 =  self.pcd_manager.get_filepath()
                        self.cnt = self.cnt+1
                        new_row = {'index': self.cnt
                                   ,'id': args.id
                                   ,'condition': args.condition
                                   ,'pcd': self.pcd_manager.pcd_name
                                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                                   ,'active': 'bbox_rotation'
                                   ,'input': 'mouse_move_event'
                                   ,'input_detail': 'mouse_left_move'
                                   ,'mouse_position_x': a0.x()
                                   ,'mouse_position_y': a0.y()
                                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                                   }
                        self.data2["logging"].append(new_row)
                        print(new_row)
                        self.pcd_manager.save_labels_into_file2(self.data2)
                        self.pre_active = 'bbox_rotation'
                        #self.reload2()
                    
                elif a0.buttons() & QtCore.Qt.RightButton:  # bbox translation
                    new_center = self.view.gl_widget.get_world_coords(
                        a0.x(), a0.y(), correction=True
                    )
                    self.bbox_controller.set_center(*new_center)  # absolute positioning
                    
                    if self.pre_active != 'bbox_translation':
                        self.data2 =  self.pcd_manager.get_filepath()
                        self.cnt = self.cnt+1
                        new_row = {'index': self.cnt
                                   ,'id': args.id
                                   ,'condition': args.condition
                                   ,'pcd': self.pcd_manager.pcd_name
                                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                                   ,'active': 'bbox_translation'
                                   ,'input': 'mouse_move_event'
                                   ,'input_detail': 'mouse_right_move'
                                   ,'mouse_position_x': a0.x()
                                   ,'mouse_position_y': a0.y()
                                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                                   }
                        self.data2["logging"].append(new_row)
                        print(new_row)
                        self.pcd_manager.save_labels_into_file2(self.data2)
                        self.pre_active = 'bbox_translation'
                        #self.reload2()
            else:
                if (self.start_mode.is_active) :
                    True
                    #logging.info("starmode is active and mouse is moving...")
                elif a0.buttons() & QtCore.Qt.LeftButton:  # pcd rotation
                    self.pcd_manager.rotate_around_x(dy)
                    self.pcd_manager.rotate_around_z(dx)
                    
                    if self.pre_active != 'pcd_rotation' :
                        self.data2 =  self.pcd_manager.get_filepath()
                        self.cnt = self.cnt+1
                        new_row = {'index': self.cnt
                                   ,'id': args.id
                                   ,'condition': args.condition
                                   ,'pcd': self.pcd_manager.pcd_name
                                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                                   ,'active': 'pcd_rotation'
                                   ,'input': 'mouse_move_event'
                                   ,'input_detail': 'mouse_left_move'
                                   ,'mouse_position_x': a0.x()
                                   ,'mouse_position_y': a0.y()
                                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                                   }
                        self.data2["logging"].append(new_row)
                        print(new_row)
                        self.pcd_manager.save_labels_into_file2(self.data2)
                        self.pre_active = 'pcd_rotation'
                       #self.reload2()
                        
                elif a0.buttons() & QtCore.Qt.RightButton:  # pcd translation
                    self.pcd_manager.translate_along_x(dx)
                    self.pcd_manager.translate_along_y(dy)
                    
                    if self.pre_active != 'pcd_translation':
                        self.data2 =  self.pcd_manager.get_filepath()
                        self.cnt = self.cnt+1
                        new_row = {'index': self.cnt
                                   ,'id': args.id
                                   ,'condition': args.condition
                                   ,'pcd': self.pcd_manager.pcd_name
                                   ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                                   ,'active': 'pcd_translation'
                                   ,'input': 'mouse_move_event'
                                   ,'input_detail': 'mouse_right_move'
                                   ,'mouse_position_x': a0.x()
                                   ,'mouse_position_y': a0.y()
                                   ,'rot_x': self.pcd_manager.pointcloud.rot_x
                                   ,'rot_y': self.pcd_manager.pointcloud.rot_y
                                   ,'rot_z': self.pcd_manager.pointcloud.rot_z
                                   ,'trans_x': self.pcd_manager.pointcloud.trans_x
                                   ,'trans_y': self.pcd_manager.pointcloud.trans_y
                                   ,'trans_z': self.pcd_manager.pointcloud.trans_z
                                   }
                        self.data2["logging"].append(new_row)
                        print(new_row)
                        self.pcd_manager.save_labels_into_file2(self.data2)
                        self.pre_active = 'pcd_translation'
                        #self.reload2()

            # Reset scroll locks of "side scrolling" for significant cursor movements
            if dx > Controller.MOVEMENT_THRESHOLD or dy > Controller.MOVEMENT_THRESHOLD:
                if self.side_mode:
                    self.side_mode = False
                else:
                    self.scroll_mode = False
        self.last_cursor_pos = a0.pos()

    def mouse_scroll_event(self, a0: QtGui.QWheelEvent) -> None:
        """Triggers actions when the user scrolls the mouse wheel."""
        if self.selected_side:
            self.side_mode = True

        if (
            self.drawing_mode.is_active()
            and (not self.ctrl_pressed)
            and self.drawing_mode.drawing_strategy is not None
        ):
            self.drawing_mode.drawing_strategy.register_scrolling(a0.angleDelta().y())
            
            if self.pre_active != 'register_scrolling':
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'register_scrolling'
                           ,'input': 'mouse_scroll_event'
                           ,'input_detail': 'mouse_scroll'
                           ,'mouse_position_x': ''
                           ,'mouse_position_y': ''
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                print(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                self.pre_active = 'register_scrolling'
            
        elif self.side_mode and self.bbox_controller.has_active_bbox():
            self.bbox_controller.get_active_bbox().change_side(  # type: ignore
                self.selected_side, -a0.angleDelta().y() / 4000  # type: ignore
            )  # ToDo implement method
            
            if self.pre_active != 'change_side':
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'change_side'
                           ,'input': 'mouse_scroll_event'
                           ,'input_detail': 'mouse_scroll'
                           ,'mouse_position_x': ''
                           ,'mouse_position_y': ''
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                print(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                self.pre_active = 'change_side'
            
            
        else:
            self.pcd_manager.zoom_into(a0.angleDelta().y())
            self.scroll_mode = True
            
            if self.pre_active != 'zoom_into' :
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'zoom_into'
                           ,'input': 'mouse_scroll_event'
                           ,'input_detail': 'mouse_scroll'
                           ,'mouse_position_x': ''
                           ,'mouse_position_y': ''
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                print(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                self.pre_active = 'zoom_into'

    def key_press_event(self, a0: QtGui.QKeyEvent) -> None:
        """Triggers actions when the user presses a key."""

        #########################
        if a0.key() == QtCore.Qt.Key_V:
            #logging.info("V")
            self.v_pressed = True
        
        
        if a0.key() == QtCore.Qt.Key_Shift:
            #logging.info("Shift")
            self.shift_pressed = True
        
            """
            self.view.status_manager.set_message(
                ".."
                "..",
                context=Context.CONTROL_PRESSED,
            )
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'change_pcd'
                       ,'input': 'key_shift'
                       ,'input_detail': 'key_shift'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            self.pre_active = 'change_pcd'

            if self.shift_pre < 1:
                if self.pcd_manager.pcds_left():
                    self.save()
                    self.data2 =  self.pcd_manager.get_filepath()
                    self.pcd_manager.get_next_pcd(self.data2)
                    self.reset()
                    self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
                    self.shift_pre = self.shift_pre+1
                    
                    
            else:
                if self.pcd_manager.current_id > 0:
                    
                    self.data2 =  self.pcd_manager.get_filepath()
                    self.pcd_manager.get_prev_pcd(self.data2)
                    #self.data2 =  self.pcd_manager.get_filepath()
                    #self.pcd_manager.get_prev_pcd(self.data2)
                    self.reset()
                    self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
                    self.shift_pre = 0
            """
                    
        """
        if a0.key() == QtCore.Qt.Key_Space:
            logging.info("Space")
            self.space_pressed = True

            if self.space_pre == False:
                if self.pcd_manager.pcds_left():
                    self.data2 =  self.pcd_manager.get_filepath()
                    self.pcd_manager.get_next_pcd2(self.data2)
                    self.reset()
                    self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
                    self.space_pre = True
            else:
                if self.pcd_manager.current_id > 0:
                    self.data2 =  self.pcd_manager.get_filepath()
                    self.pcd_manager.get_prev_pcd2(self.data2)
                    self.reset()
                    self.bbox_controller.set_bboxes(self.pcd_manager.get_labels_from_file())
                    self.space_pre = False
        """
        
        #########################
        
        
        # Reset position to intial value
        if a0.key() == QtCore.Qt.Key_Control:
            self.ctrl_pressed = True
            self.view.status_manager.set_message(
                "Hold right mouse button to translate or left mouse button to rotate "
                "the bounding box.",
                context=Context.CONTROL_PRESSED,
            )
            

        # Reset point cloud pose to intial rotation and translation
        elif (a0.key() == QtCore.Qt.Key_R): #or (a0.key() == QtCore.Qt.Key_Home):
            self.pcd_manager.reset_transformations()
            #logging.info("Reseted position to default.")
            
            """
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'reset_transformations'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_R'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
            
        elif a0.key() == QtCore.Qt.Key_Delete:  # Delete active bbox
            self.bbox_controller.delete_current_bbox()
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'delete_current_bbox'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_Delete'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)

        # Save labels to file
        elif (a0.key() == QtCore.Qt.Key_S) and self.ctrl_pressed:
            self.save()
            #self.save2('TEST SAVE?')
           
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'save'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_S, ctrl_pressed'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                        ,'rot_x': self.pcd_manager.pointcloud.rot_x
                        ,'rot_y': self.pcd_manager.pointcloud.rot_y
                        ,'rot_z': self.pcd_manager.pointcloud.rot_z
                        ,'trans_x': self.pcd_manager.pointcloud.trans_x
                        ,'trans_y': self.pcd_manager.pointcloud.trans_y
                        ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
        

        elif a0.key() == QtCore.Qt.Key_Escape:
            True
            #logging.info("not use!")
            """
            if self.drawing_mode.is_active():
                self.drawing_mode.reset()
                logging.info("Resetted drawn points!")
                
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'drawing_mode_reset'
                           ,'input': 'key_press_event'
                           ,'input_detail': 'Key_Escape'
                           ,'mouse_position_x': ''
                           ,'mouse_position_y': ''
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                
            elif self.align_mode.is_active:
                self.align_mode.reset()
                logging.info("Resetted selected points!")
                
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'align_mode_reset'
                           ,'input': 'key_press_event'
                           ,'input_detail': 'Key_Escape'
                           ,'mouse_position_x': ''
                           ,'mouse_position_y': ''
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                """
        # BBOX MANIPULATION
        #elif (a0.key() == QtCore.Qt.Key_Y) or (a0.key() == QtCore.Qt.Key_Comma):
        elif (a0.key() == QtCore.Qt.Key_Z): #or (a0.key() == QtCore.Qt.Key_Comma):
            True
            #logging.info("not use!")
            """
            # z rotate counterclockwise
            self.bbox_controller.rotate_around_z()

            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'rotate_around_z'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_Z'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
        elif (a0.key() == QtCore.Qt.Key_X): #or (a0.key() == QtCore.Qt.Key_Period):
            True
            #logging.info("not use!")
            """
            # z rotate clockwise
            self.bbox_controller.rotate_around_z(clockwise=True)
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'rotate_around_z_clockwise'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_X'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
        
        elif a0.key() == QtCore.Qt.Key_C:
            if self.ctrl_pressed:
                #logging.info("C !!")
                self.last_copy_bbox = self.bbox_controller.active_bbox_id
                #self.bbox_controller.copied_bbox(2) # 현재 active 되어있는 bbox에 한에 변함
                
                """
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'BBOX_copy'
                           ,'input': 'key_press_event'
                           ,'input_detail': 'Key_C, ctrl_pressed'
                           ,'mouse_position_x': ''
                           ,'mouse_position_y': ''
                           }
                self.data2["logging"].append(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
                """
            """
            else:
                # y rotate counterclockwise
                self.bbox_controller.rotate_around_y()
                
                self.data2 =  self.pcd_manager.get_filepath()
                self.cnt = self.cnt+1
                new_row = {'index': self.cnt
                           ,'id': args.id
                           ,'condition': args.condition
                           ,'pcd': self.pcd_manager.pcd_name
                           ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                           ,'active': 'rotate_around_y'
                           ,'input': 'key_press_event'
                           ,'input_detail': 'Key_C'
                           ,'mouse_position_x': ''
                           ,'mouse_position_y': ''
                           ,'rot_x': self.pcd_manager.pointcloud.rot_x
                           ,'rot_y': self.pcd_manager.pointcloud.rot_y
                           ,'rot_z': self.pcd_manager.pointcloud.rot_z
                           ,'trans_x': self.pcd_manager.pointcloud.trans_x
                           ,'trans_y': self.pcd_manager.pointcloud.trans_y
                           ,'trans_z': self.pcd_manager.pointcloud.trans_z
                           }
                self.data2["logging"].append(new_row)
                self.pcd_manager.save_labels_into_file2(self.data2)
             """
        elif a0.key() == QtCore.Qt.Key_V:
            # y rotate clockwise
            self.bbox_controller.rotate_around_y(clockwise=True)
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'rotate_around_y_clockwise'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_V'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            print(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            
        elif a0.key() == QtCore.Qt.Key_B:
            True
            #logging.info("not use!")
            """
            # x rotate counterclockwise
            self.bbox_controller.rotate_around_x()
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'rotate_around_x'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_B'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
            
        elif a0.key() == QtCore.Qt.Key_N:
            True
            #logging.info("not use!")
            """
            # x rotate clockwise
            self.bbox_controller.rotate_around_x(clockwise=True)
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'rotate_around_x_clockwise'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_N'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
            
        elif (a0.key() == QtCore.Qt.Key_W): #or (a0.key() == QtCore.Qt.Key_Up):
            True
            #logging.info("not use!")
            """
            # move backward
            self.bbox_controller.translate_along_y()
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'translate_along_y'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_W'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
        elif (a0.key() == QtCore.Qt.Key_S): #or (a0.key() == QtCore.Qt.Key_Down):
            True
            #logging.info("not use!")
            """
            # move forward
            self.bbox_controller.translate_along_y(forward=True)
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'translate_along_y_forward'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_S'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
        elif (a0.key() == QtCore.Qt.Key_A): #or (a0.key() == QtCore.Qt.Key_Left):
            True
            #logging.info("not use!")
            """
            # move left
            self.bbox_controller.translate_along_x(left=True)
            #self.bbox_controller.translate_along_y(forward=True)
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'translate_along_x_left'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_A'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
        elif (a0.key() == QtCore.Qt.Key_D): #or (a0.key() == QtCore.Qt.Key_Right):
            True
            #logging.info("not use!")
            """
            # move right
            self.bbox_controller.translate_along_x()
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'translate_along_x'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_D'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
        elif (a0.key() == QtCore.Qt.Key_Q): #or (a0.key() == QtCore.Qt.Key_PageUp):
            True
            #logging.info("not use!")
            """
            # move up
            self.bbox_controller.translate_along_z()
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'translate_along_z'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_Q'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """
        elif (a0.key() == QtCore.Qt.Key_E): #or (a0.key() == QtCore.Qt.Key_PageDown):
            True
            #logging.info("not use!")
            """
            # move down
            self.bbox_controller.translate_along_z(down=True)
            #self.bbox_controller.translate_along_z()
            
            self.data2 =  self.pcd_manager.get_filepath()
            self.cnt = self.cnt+1
            new_row = {'index': self.cnt
                       ,'id': args.id
                       ,'condition': args.condition
                       ,'pcd': self.pcd_manager.pcd_name
                       ,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                       ,'active': 'translate_along_z_down'
                       ,'input': 'key_press_event'
                       ,'input_detail': 'Key_E'
                       ,'mouse_position_x': ''
                       ,'mouse_position_y': ''
                       ,'rot_x': self.pcd_manager.pointcloud.rot_x
                       ,'rot_y': self.pcd_manager.pointcloud.rot_y
                       ,'rot_z': self.pcd_manager.pointcloud.rot_z
                       ,'trans_x': self.pcd_manager.pointcloud.trans_x
                       ,'trans_y': self.pcd_manager.pointcloud.trans_y
                       ,'trans_z': self.pcd_manager.pointcloud.trans_z
                       }
            self.data2["logging"].append(new_row)
            self.pcd_manager.save_labels_into_file2(self.data2)
            """

    def key_release_event(self, a0: QtGui.QKeyEvent) -> None:
        """Triggers actions when the user releases a key."""
        if a0.key() == QtCore.Qt.Key_V:
            self.v_pressed = False
            #self.drawing_mode.reset()
            #self.view.status_manager.clear_message(Context.CONTROL_PRESSED)
        
        if a0.key() == QtCore.Qt.Key_Shift:
            self.shift_pressed = False
            self.drawing_mode.reset()
            self.view.status_manager.clear_message(Context.CONTROL_PRESSED)
            
        if a0.key() == QtCore.Qt.Key_Control:
            self.ctrl_pressed = False
            self.view.status_manager.clear_message(Context.CONTROL_PRESSED)
        
        if a0.key() == QtCore.Qt.Key_Space:
            self.space_pressed = False
            self.view.status_manager.clear_message(Context.CONTROL_PRESSED)


def css_pushButton():
    css = '''
        QPushButton {
                        font-size: 10px;
                        background-color: green;
                        color: black;
                        border: 2px green;
                        border-radius: 22px;
                        border-style: outset;
                            }
        QPushButton:hover {
                        background: qradialgradient(
                            cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                            radius: 1.35, stop: 0 grey, stop: 1 lightgray
                            );
                        }
        QPushButton:enabled{
                        color: black;
                        font:  10px;
                        background: green;
                        background-color: red;
                        border: 1px black;
                        border-style: outset;
                        }
        QPushButton:pressed {
                        color: white;
                        background: yellow;
                        }
        QPushButton:disabled {
                        color: gray;
                        background-color: gray;
                        border: 1px black;
                        border-style: outset;                
                    }
        QPushButton:checked{
                    color: black; 
                    font:  12px;   
                    font: bold;
                    background-color: red;
                    border: 1px black;
                    border-style: outset;
                    }
        QPushButton:!checked{
                    color: black; 
                    font:  12px;   
                    font: bold;
                    background-color: green;
                    border: 1px black;
                    border-style: outset;
        }
    
        '''
    return css
