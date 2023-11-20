from src.database.singletonMeta import SingletonMeta
from src.predictors.utils.deeplab import DeepLabRoadSeg
from src.predictors.utils.predict import my_get_sliced_prediction
from src.config import ROAD_DETECTION_MODEL
from src.predictors.utils.plot import plot_coco_result
import torch
class RoadPredictor(metaclass=SingletonMeta):
    detect_model = None
    def __init__(self, detect_model_path = None) -> None:
        self.detect_model  = DeepLabRoadSeg(detect_model_path)

    def predict_image(self, bgr_image):
        result = my_get_sliced_prediction(
            bgr_image,
            self.model,
            slice_height=640,
            slice_width=640,
            overlap_height_ratio=0.3,
            overlap_width_ratio=0.3
            
        ).object_prediction_list
        return plot_coco_result(result, bgr_image)

    def predict(self, bgr_image):
        result = my_get_sliced_prediction(
            bgr_image,
            self.detect_model,
            slice_height=480,
            slice_width=592,
            overlap_height_ratio=0.2,
            overlap_width_ratio=0.2
            
        ).object_prediction_list

        buildings = []
        for index, pred in enumerate(result):
            building = {
                'seq_number' : index,
                'vertices' : pred['segmentation']
            }
            buildings.append(building)
        return buildings

global road_predictor 
road_predictor = RoadPredictor(ROAD_DETECTION_MODEL)