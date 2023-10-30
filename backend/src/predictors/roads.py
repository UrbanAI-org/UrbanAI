# from src.database.singletonMeta import SingletonMeta
# from config import ROAD_DETECTION_MODEL
# import torch
# class RoadPredictor(metaclass=SingletonMeta):
#     detect_model = None
#     def __init__(self, detect_model_path = None) -> None:
#         self.detect_model  = torch.load(detect_model_path)
#     def predict(self, bgr_image):
#         return _predict(bgr_image, self.detect_model)
    
# def _predict(bgr_image, detect_model) -> None:
#     pred = detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=700,patch_overlap=0.3)
#     roads = []
#     if pred is None:
#         return roads
#     pred['width'] = pred['xmax'] - pred['xmin']
#     pred['height'] = pred['ymax'] - pred['ymin']
    
#     return {
#         "num_roads" : 1,
#         "roads" : [{
#             "seq_number" : 0,
#             "vertices" : [
#                 (245, 193),
#                 (266, 293),
#                 (245, 293),
#                 (266, 193),
#             ],
#         }]
#     }


# global road_predictor 
# road_predictor = RoadPredictor(ROAD_DETECTION_MODEL)