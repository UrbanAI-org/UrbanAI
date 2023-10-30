import imp
from src.database.singletonMeta import SingletonMeta
from src.config import BUILDING_SEGMENTATION_MODEL
from src.predictors.utils.predict import my_get_sliced_prediction
from src.predictors.utils.yolo import Yolov8BuildingSegModel

class BuildingPredictor(metaclass=SingletonMeta):
    def __init__(self, model_path = None) -> None:
        self.model = Yolov8BuildingSegModel(model_path)
        pass

    def predict(self, bgr_image):
        # return _predict(bgr_image)
        result = my_get_sliced_prediction(
            bgr_image,
            self.model,
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.3,
            overlap_width_ratio=0.3
            
        ).object_prediction_list

        buildings = []
        for index, pred in enumerate(result):
            building = {
                'seq_number' : index,
            }
            building['vertices'] = pred['segmentation']
            building['height'] = 3
            building['roof_color'] = [253, 253, 253]
            buildings.append(building)
        return buildings
    
global building_predictor
building_predictor = BuildingPredictor(BUILDING_SEGMENTATION_MODEL)

