import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from . import BaseLabelFormat
from ...definitions import Point3D
from ...model import BBox
from ...utils import math3d
from ...__main__ import args

class VerticesFormat(BaseLabelFormat):
    FILE_ENDING = ".json"
    FILE_ENDING2 = ".ply"
    FILE_ENDING3 = ".log"
    ID = args.id

    def import_labels(self, pcd_path: Path) -> List[BBox]:
        labels = []
        
        
        if '0003_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            label_path = self.label_folder.joinpath('0003_00' + self.FILE_ENDING)
        elif '0011_00' in pcd_path.stem:    
            label_path = self.label_folder.joinpath('0011_00' + self.FILE_ENDING)
        elif '0047_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            label_path = self.label_folder.joinpath('0047_00' + self.FILE_ENDING)
        elif '0059_01' in pcd_path.stem:    
            label_path = self.label_folder.joinpath('0059_01' + self.FILE_ENDING)
        elif '0021_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            label_path = self.label_folder.joinpath('0021_00' + self.FILE_ENDING)
        elif '0013_00' in pcd_path.stem:    
            label_path = self.label_folder.joinpath('0013_00' + self.FILE_ENDING)
        else:    
            label_path = self.label_folder.joinpath(pcd_path.stem + self.FILE_ENDING)
        
        
        if label_path.is_file():
            with label_path.open("r") as read_file:
                data = json.load(read_file)

            for label in data["objects"]:
                vertices = label["vertices"]

                # Calculate centroid
                centroid: Point3D = tuple(  # type: ignore
                    np.add(np.subtract(vertices[4], vertices[2]) / 2, vertices[2])
                )

                # Calculate dimensions
                length = math3d.vector_length(np.subtract(vertices[0], vertices[3]))
                width = math3d.vector_length(np.subtract(vertices[0], vertices[1]))
                height = math3d.vector_length(np.subtract(vertices[0], vertices[4]))

                # Calculate rotations
                rotations = math3d.vertices2rotations(vertices, centroid)

                bbox = BBox(*centroid, length, width, height)
                bbox.set_rotations(*rotations)


                if label["name"] == 'refrigerator':
                    bbox.set_classname("냉장고")
                elif label["name"] == 'floor':
                    bbox.set_classname("바닥")
                elif label["name"] == 'table':
                    bbox.set_classname("탁자")
                elif label["name"] == 'sofa':
                    bbox.set_classname("소파")
                elif label["name"] == 'chair':
                    bbox.set_classname("의자")
                elif label["name"] == 'wall':
                    bbox.set_classname("벽")
                elif label["name"] == 'door':
                    bbox.set_classname("문")
                elif label["name"] == 'counter':
                    bbox.set_classname("카운터")
                elif label["name"] == 'window':
                    bbox.set_classname("창문")
                elif label["name"] == 'sink':
                    bbox.set_classname("싱크대")
                elif label["name"] == 'cabinet':
                    bbox.set_classname("캐비넷")
                elif label["name"] == 'otherprop':
                    bbox.set_classname("기타")
                else:    
                    bbox.set_classname(label["name"])
                #bbox.set_classname(label["name"])
                labels.append(bbox)
            #logging.info("Imported %s labels from %s." % (len(data["objects"]), label_path))
        return labels

    def export_labels(self, bboxes: List[BBox], pcd_path: Path) -> None:
        data: Dict[str, Any] = dict()
        # Header
        data["folder"] = pcd_path.parent.name
        data["filename"] = pcd_path.name
        data["path"] = str(pcd_path)


        data2 = dict()
        data2["logging"] = []
        
        # Labels
        data["objects"] = []
        for bbox in bboxes:
            label: Dict[str, Any] = dict()
            
            if bbox.get_classname() == '냉장고':
                label["name"] = "refrigerator"
            elif bbox.get_classname() == '캐비넷':
                label["name"] = "cabinet"
            elif bbox.get_classname() == '바닥':
                label["name"] = "floor"
            elif bbox.get_classname() == '탁자':
                label["name"] = "table"
            elif bbox.get_classname() == '소파':
                label["name"] = "sofa"
            elif bbox.get_classname() == '의자':
                label["name"] = "chair"
            elif bbox.get_classname() == '벽':
                label["name"] = "wall"
            elif bbox.get_classname() == '문':
                label["name"] = "door"
            elif bbox.get_classname() == '카운터':
                label["name"] = "counter"
            elif bbox.get_classname() == '창문':
                label["name"] = "window"
            elif bbox.get_classname() == '싱크대':
                label["name"] = "sink"
            elif bbox.get_classname() == '기타':
                label["name"] = "otherprop"
            else:    
                label["name"] = bbox.get_classname()
            
            
            label["vertices"] = self.round_dec(
                bbox.get_vertices().tolist()
            )  # TODO: Add option for axis-aligned vertices
            data["objects"].append(label)

        # Save to JSON
        
        if '0003_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0003_00.ply')
        elif '0011_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0011_00.ply')
        elif '0047_00' in pcd_path.stem: 
            pcd_path = pcd_path.parent.joinpath('0047_00.ply')
        elif '0059_01' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0059_01.ply')
        elif '0021_00' in pcd_path.stem: 
            pcd_path = pcd_path.parent.joinpath('0021_00.ply')
        elif '0013_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0013_00.ply')
        else:    
            pcd_path = pcd_path
            
        """    
        if '1b' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('1b.ply')
        elif '2b' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('2b.ply')
        """

        if len(data["objects"]) > 0:
            label_path = self.save_label_to_file(pcd_path, data)
        
        
        #logging.info(f"export_labels : ({label_path}).") #export_labels : (labels\TEST0212\0212.json).
        #logging.info(f"export_labels : ({pcd_path}).") #export_labels : (pointclouds\0212.ply).
        
        """
        logging.info(
            f"Exported {len(bboxes)} labels to {label_path} "
            f"in {self.__class__.__name__} formatting!"
        )
        """



    def export_labels2(self, logging_text: dict, pcd_path: Path) -> None:
        

        # for logging
        
        #logging.info(f"export_labels2!!") #export_labels : (pointclouds\0212.ply).
        
        #data2: Dict[str, Any] = dict()
        # Header
        #data2["folder"] = pcd_path.parent.name
        #data2["filename"] = pcd_path.name
        #data2["path"] = str(pcd_path)

        # Labels
        #data2["logging"]=logging_text
        

        # Save to JSON
        

        #if '1b' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
        #pcd_path = pcd_path.parent.joinpath('logging.ply')
        #elif '2b' in pcd_path.stem:    
        #pcd_path = pcd_path.parent.joinpath('2b_logging.ply')
        
        if '0003_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0003_00_logging.ply')
        elif '0011_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0011_00_logging.ply')
        elif '0047_00' in pcd_path.stem:
            pcd_path = pcd_path.parent.joinpath('0047_00_logging.ply')
        elif '0059_01' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0059_01_logging.ply')
        elif '0013_00' in pcd_path.stem:
            pcd_path = pcd_path.parent.joinpath('0013_00_logging.ply')
        elif '0021_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0021_00_logging.ply')
        else:    
            pcd_path =  pcd_path.parent.joinpath('logging_v2.ply')
        
        
        #export_labels2 : (pointclouds\b1_con02.ply).
        #File labels\TT2\b1_con02.json already exists, replacing file ...
        #export_labels2 : (labels\TT2\b1_con02.json).

        #logging.info(f"export_labels2 : ({pcd_path}).") #export_labels : (pointclouds\0212.ply).
        label_path = self.save_label_to_file(pcd_path, logging_text)
        
        #logging.info(f"export_labels2 : ({label_path}).") #export_labels : (labels\TEST0212\0212.json).
        
        

        #if not label_path.exists():
        #    label_path.mkdir(parents=True)
            
        #logging.info(f"pcd_path2 ({pcd_path2}).")
        #logging.info(f"export_labels : ({pcd_path}).") #export_labels : (pointclouds\0212.ply).
        

    def export_pers2(self, logging_text: dict, pcd_path: Path) -> None:
        
        #logging.info(f"export_labels2!!") #export_labels : (pointclouds\0212.ply).

        
        if '0003_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0003_00_logging.ply')
        elif '0011_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0011_00_logging.ply')
        elif '0047_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0047_00_logging.ply')
        elif '0059_01' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0059_01_logging.ply')
        elif '0013_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0013_00_logging.ply')
        elif '0021_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0021_00_logging.ply')
        else:    
            pcd_path =  pcd_path.parent.joinpath('logging_v2.ply')
        
        #logging.info(f"export_labels2 : ({pcd_path}).") #export_labels : (pointclouds\0212.ply).
        label_path = self.save_label_to_file(pcd_path, logging_text)        
        #logging.info(f"export_labels2 : ({label_path}).") #export_labels : (labels\TEST0212\0212.json).
        

      

    def get_filepath3(self, pcd_path: Path) -> dict:
        
        #logging.info(f"get_filepath3!!") #export_labels : (pointclouds\0212.ply).
        #logging.info(f"pcd_path : ({pcd_path})")
        
        if '0003_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0003_00_logging.ply')
        elif '0011_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0011_00_logging.ply')
        elif '0047_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0047_00_logging.ply')
        elif '0059_01' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0059_01_logging.ply')
        elif '0021_00' in pcd_path.stem: 
            pcd_path = pcd_path.parent.joinpath('0021_00_logging.ply')
        elif '0013_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0013_00_logging.ply')
        else:    
            pcd_path =  pcd_path.parent.joinpath('logging_v2.ply')
            
            
        # Save to JSON
        #pcd_path = pcd_path.parent.joinpath('logging.ply')
        #logging.info(f"pcd_path : ({pcd_path})") #pcd_path : (pointclouds\15913\0059_01_logging.ply)
        label_path = self.label_folder.joinpath(pcd_path.stem + self.FILE_ENDING)
        
        data2 = dict()
        data2["logging"] = []
        
        
        if label_path.is_file():
            with label_path.open("r") as read_file:
               #logging.info("file is...")
               #data2 = json.load(read_file)
               #return data2
               
               try:
                   data2 = json.load(read_file)
                   return data2
               except:
                   logging.info("except") #pcd_path : (pointclouds\15913\0059_01_logging.ply)
                   return data2
               
        return data2
        
    
    
    def get_filepath_real3(self, pcd_path: Path) -> Path:
        
        #logging.info(f"get_filepath_real3!!") #export_labels : (pointclouds\0212.ply).
        #logging.info(f"pcd_path : ({pcd_path})")
                
        if '0003_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0003_00_logging.ply')
        elif '0011_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0011_00_logging.ply')
        elif '0047_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0047_00_logging.ply')
        elif '0059_01' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0059_01_logging.ply')
        elif '0013_00' in pcd_path.stem: 
            pcd_path = pcd_path.parent.joinpath('0013_00_logging.ply')
        elif '0021_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0021_00_logging.ply')
        else:    
            pcd_path =  pcd_path.parent.joinpath('logging_v2.ply')
        
        #else:    
        #    pcd_path = pcd_path.parent.joinpath('logging_v2.ply')
            
        # Save to JSON
        #pcd_path = pcd_path.parent.joinpath('logging.ply')
        #logging.info(f"pcd_path : ({pcd_path})")
        label_path = self.label_folder.joinpath(pcd_path.stem + self.FILE_ENDING3)
        
        return label_path
       

    def get_pers2(self, pcd_path: Path) -> dict:
        
        #logging.info(f"get_filepath3!!") #export_labels : (pointclouds\0212.ply).
        #logging.info(f"pcd_path : ({pcd_path})")
        
        
        if '0003_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0003_00_pers.ply')
        elif '0011_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0011_00_pers.ply')
        elif '0047_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0047_00_pers.ply')
        elif '0059_01' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0059_01_pers.ply')
        elif '0013_00' in pcd_path.stem: #(pointclouds\scene0002_00_vh_clean_2.ply).
            pcd_path = pcd_path.parent.joinpath('0013_00_pers.ply')
        elif '0021_00' in pcd_path.stem:    
            pcd_path = pcd_path.parent.joinpath('0021_00_pers.ply')
        else:    
            pcd_path =  pcd_path.parent.joinpath('logging_pers.ply')
            
        # Save to JSON
        #pcd_path = pcd_path.parent.joinpath('logging.ply')
        #logging.info(f"pcd_path : ({pcd_path})") #pcd_path : (pointclouds\15913\0059_01_logging.ply)
        label_path = self.label_folder.joinpath(pcd_path.stem + self.FILE_ENDING)
        
        data2 = dict()
        data2["logging"] = []
        
        if label_path.is_file():
            with label_path.open("r") as read_file:
               #logging.info("file is...")
               data2 = json.load(read_file)
               return data2
        return data2
               


        