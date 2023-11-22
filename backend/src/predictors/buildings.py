import imp
from src.database.singletonMeta import SingletonMeta
from src.config import BUILDING_SEGMENTATION_MODEL
from src.predictors.utils.predict import my_get_sliced_prediction
from src.predictors.utils.yolo import Yolov8BuildingSegModel
from src.predictors.utils.resplot import plot_coco_result
class BuildingPredictor(metaclass=SingletonMeta):
    def __init__(self, model_path=None) -> None:
        """
        Initializes the Buildings predictor.

        Args:
            model_path (str): The path to the YOLOv8 building segmentation model. Defaults to None.
        """
        self.model = Yolov8BuildingSegModel(model_path)
        pass
    
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
            list: A list of dictionaries representing the predicted buildings. Each dictionary contains the following keys:
                - 'seq_number': The sequence number of the building.
                - 'vertices': The vertices of the building's segmentation.
                - 'height': The height of the building.
                - 'roof_color': The color of the building's roof.
        """
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

