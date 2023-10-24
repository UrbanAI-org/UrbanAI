from database.singletonMeta import SingletonMeta

class BuildingPredictor(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass

    def predict(self, bgr_image):
        # return _predict(bgr_image)
        return {
            "num_buildings" : 1,
            "buildings" : [{
                "seq_number" : 0,
                "vertices" : [
                    (245, 193),
                    (266, 293),
                    (245, 293),
                    (266, 193),
                ],
                'height' : 3,
                'roof_color' : [255, 255, 255]
            }]
        }
global building_predictor
building_predictor = BuildingPredictor()
