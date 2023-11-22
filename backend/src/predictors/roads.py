from src.database.singletonMeta import SingletonMeta
from src.predictors.utils.deeplab import DeepLabRoadSeg
from src.predictors.utils.predict import my_get_sliced_prediction
from src.config import ROAD_DETECTION_MODEL
from src.predictors.utils.resplot import plot_coco_result
import torch
class RoadPredictor(metaclass=SingletonMeta):
    detect_model = None
    def __init__(self, detect_model_path=None) -> None:
        """
        Initialize the RoadsPredictor object.

        Args:
            detect_model_path (str): The path to the road detection model.

        Returns:
            None
        """
        self.detect_model = DeepLabRoadSeg(detect_model_path)

    def predict_image(self, bgr_image):
        """
        Predicts the objects in the given BGR image using the model.

        Args:
            bgr_image (numpy.ndarray): The BGR image to predict objects in.

        Returns:
            numpy.ndarray: The BGR image with the predicted objects plotted.
        """
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
        """
        Predicts the buildings in the given BGR image.

        Args:
            bgr_image (numpy.ndarray): The input BGR image.

        Returns:
            list: A list of dictionaries containing the predicted buildings.
                    Each dictionary contains the sequence number and vertices of a building.
        """
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