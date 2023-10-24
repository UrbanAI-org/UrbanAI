
import math
from database.singletonMeta import SingletonMeta
from config import TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL, TREE_PCA_MODEL
from deepforest import main
import pickle
import numpy as np
import joblib
import cv2
# models

class TreePredictor(metaclass=SingletonMeta):
    detect_model = None
    cluster_model = None
    feature_extractor = None
    pca = None
    def __init__(self, detect_model_path = None, cluster_model_path = None, pca_path = None) -> None:
        self.detect_model  = main.deepforest.load_from_checkpoint(detect_model_path)
        self.cluster_model = joblib.load(cluster_model_path)
        self.pca = joblib.load(pca_path)

    def predict(self, bgr_image):
        return _predict(bgr_image, self.detect_model, self.cluster_model, self.pca)

    def detect(self, bgr_image: np.ndarray):
        return self.detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=700,patch_overlap=0.3)

def _predict(bgr_image, detect_model, cluster_model, pca):
    pred = detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=700,patch_overlap=0.3)
    trees = []
    tree_types = set()
    if pred is None:
        return trees, tree_types
    pred['width'] = pred['xmax'] - pred['xmin']
    pred['height'] = pred['ymax'] - pred['ymin']
    pred = pred[~((pred['width'] > pred['height'] * 2) | (pred['width'] * 2 < pred['height']))]
    for index, row in pred.iterrows():
        xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        # crop the image using the bounding box
        cropped_image = bgr_image[int(ymin):int(ymax), int(xmin):int(xmax)]
        feature = _extract_features(cropped_image, pca)
        label = cluster_model.predict(feature)[0]
        tree_type = _map_label_to_tree_type(label)
        tree = {
            'seq_number' : index,
            'position' : {'x' : np.average([row['xmin'], row['xmax']]), 'y' : np.average([row['ymin'], row['ymax']])},
            'size' : {'width': row['xmax'] - row['xmin'], 'height': row['ymax'] - row['ymin']},
            'model_type' : tree_type
        }
        trees.append(tree)
        tree_types.add(tree_type)
    return trees, tree_types

def _extract_features(cropped_image, pca, target_size=(100, 100)):
    img = cv2.resize(cropped_image, target_size)
    blue_channel, green_channel, red_channel = cv2.split(img)
    mean_red = np.mean(red_channel)
    std_dev_red = np.std(red_channel)
    mean_green = np.mean(green_channel)
    std_dev_green = np.std(green_channel)
    mean_blue = np.mean(blue_channel)
    std_dev_blue = np.std(blue_channel)
    hist_red = cv2.calcHist([red_channel], [0], None, [256], [0, 256])
    hist_green = cv2.calcHist([green_channel], [0], None, [256], [0, 256])
    hist_blue = cv2.calcHist([blue_channel], [0], None, [256], [0, 256])
    hist_red = hist_red.flatten() / hist_red.sum()
    hist_green = hist_green.flatten() / hist_green.sum()
    hist_blue = hist_blue.flatten() / hist_blue.sum()
    features = np.concatenate([[mean_red, std_dev_red, mean_green, std_dev_green, mean_blue, std_dev_blue], hist_red])
    features = np.concatenate([features, hist_green])
    features = np.concatenate([features, hist_blue])
    return pca.transform(features.reshape(1, -1))


def _map_label_to_tree_type(label):
    # for example only
    # ['Pine', 'Oak', 'Palm']
    maper = {
        0 : 'Pine',
        1 : 'Pine',
        2 : 'Spruce',
        3 : 'Birch',
        4 : 'Oak',
        5 : 'Ash',
        6 : 'Maple',
    }
    return maper[label]




global tree_predictor
tree_predictor = TreePredictor(TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL, TREE_PCA_MODEL)