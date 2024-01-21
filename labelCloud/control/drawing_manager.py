import logging
from typing import TYPE_CHECKING, Union

from ..labeling_strategies import BaseLabelingStrategy
from .bbox_controller import BoundingBoxController

if TYPE_CHECKING:
    from ..view.gui import GUI


class DrawingManager(object):
    def __init__(self, bbox_controller: BoundingBoxController) -> None:
        #logging.info("DrawingManager init...")
        self.view: "GUI"
        self.bbox_controller = bbox_controller
        self.drawing_strategy: Union[BaseLabelingStrategy, None] = None

    def set_view(self, view: "GUI") -> None:
        self.view = view
        self.view.gl_widget.drawing_mode = self

    def is_active(self) -> bool:
        return self.drawing_strategy is not None and isinstance(
            self.drawing_strategy, BaseLabelingStrategy
        )

    def has_preview(self) -> bool:
        if self.is_active():
            return self.drawing_strategy.__class__.PREVIEW  # type: ignore
        return False

    def set_drawing_strategy(self, strategy: BaseLabelingStrategy) -> None:
        if self.is_active() and self.drawing_strategy == strategy:
            self.reset()
            #logging.info("Deactivated drawing!")
        else:
            if self.is_active():
                self.reset()
                #logging.info("Resetted previous active drawing mode!")

            self.drawing_strategy = strategy

    def register_point(
        self, x: float, y: float, correction: bool = False, is_temporary: bool = False, is_finished=False, cntinue=False, Right=False, copied_id=-1, className="class0"
    ) -> None:
        assert self.drawing_strategy is not None
        world_point = self.view.gl_widget.get_world_coords(x, y, correction=correction)
        
        self.drawing_strategy.className = className
        
        #if self.drawing_strategy.get_strategy == True:
        if copied_id>-1:
            tmp_copied_box = self.bbox_controller.bboxes[copied_id]
            self.drawing_strategy.save_copied_id(copied_id=copied_id
                                                 ,length=tmp_copied_box.length, width=tmp_copied_box.width, height=tmp_copied_box.height
                                                 ,x_rotation=tmp_copied_box.x_rotation, y_rotation=tmp_copied_box.y_rotation, z_rotation=tmp_copied_box.z_rotation)
    
        
        if is_finished:
            # Register bbox to bbox controller when finished
            #logging.info(f"finished?")
            self.bbox_controller.add_bbox(self.drawing_strategy.get_bbox())
            self.drawing_strategy.reset()
            self.drawing_strategy = None
              
        elif is_temporary:
            #logging.info(f"is_temporary? ({world_point})") #world point는 포인터가 가르키는 위치인데
            self.drawing_strategy.register_tmp_point(world_point)
        else:
            #logging.info(f"??") # 클릭하면 박스 등록
            self.drawing_strategy.register_point(world_point)
            if (
                self.drawing_strategy.is_bbox_finished()
            ):  # Register bbox to bbox controller when finished
                
                if(Right==True):
                    self.bbox_controller.add_bbox(self.drawing_strategy.get_bbox(), True, className)
                else:
                    self.bbox_controller.add_bbox(self.drawing_strategy.get_bbox(), False, className)
                
                if(cntinue==False):
                    #logging.info(f"not shifted")
                    self.drawing_strategy.reset()
                    self.drawing_strategy = None

    def draw_preview(self) -> None:
        if self.drawing_strategy is not None:
            self.drawing_strategy.draw_preview()

    def reset(self, points_only: bool = False) -> None:
        if self.is_active():
            self.drawing_strategy.reset()  # type: ignore
            if not points_only:
                self.drawing_strategy = None
