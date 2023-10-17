
import math
from database.singletonMeta import SingletonMeta
from config import TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL
from deepforest import main
import pickle
import numpy as np
import joblib
import cv2
class TreePredictor(metaclass=SingletonMeta):
    detect_model = None
    cluster_model = None
    def __init__(self, detect_model_path = None, cluster_model_path = None) -> None:
        self.detect_model  = main.deepforest.load_from_checkpoint(detect_model_path)
        self.cluster_model = joblib.load(cluster_model_path)
        pass

    def predict(self, bgr_image):
        pred = self.detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=700,patch_overlap=0.3)
        trees = []
        for index, row in pred.iterrows():
            # get bounding box coordinates
            xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            # crop the image using the bounding box
            cropped_image = bgr_image[int(ymin):int(ymax), int(xmin):int(xmax)]
            feature = extract_features(bgr_image)
            label = self.cluster_model.predict(feature)
            tree = {
                'seq_number' : index,
                'position' : {'x' : np.average([row['xmin'], row['xmax']]), 'y' : np.average([row['ymin'], row['ymax']])},
                'size' : {'width': row['xmax'] - row['xmin'], 'height': row['ymax'] - row['ymin']},
                'model_type' : label
            }
            trees.append(tree)
        return trees

    def detect(self, bgr_image: np.ndarray):
        return self.detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=700,patch_overlap=0.3)

def extract_features(img, target_size = (100, 100)):
  height, width, channels = img.shape
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray = cv2.resize(gray, target_size)
  # Calculate basic statistics of pixel values
  mean_pixel_value = np.mean(gray)
  std_dev_pixel_value = np.std(gray)
  # Compute the histogram of pixel intensities
  hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
  # Flatten the histogram to a 1D array
  hist = hist.flatten()
  # Normalize the histogram
  hist /= hist.sum()
  # Concatenate the features into a single vector
  features = np.concatenate([hist, [mean_pixel_value, std_dev_pixel_value, height, width]])
  return features

def crop_trees(pred, image):
    imgs = []
    


global tree_predictor
tree_predictor = TreePredictor(TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL)