
import math
from database.singletonMeta import SingletonMeta
from config import TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL, TREE_PCA_MODEL
from deepforest import main
import pickle
import numpy as np
import joblib
import cv2
# models
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.applications.vgg16 import preprocess_input

class TreePredictor(metaclass=SingletonMeta):
    detect_model = None
    cluster_model = None
    feature_extractor = None
    pca = None
    def __init__(self, detect_model_path = None, cluster_model_path = None, pca = None) -> None:
        self.detect_model  = main.deepforest.load_from_checkpoint(detect_model_path)
        self.cluster_model = joblib.load(cluster_model_path)
        self.pca = joblib.load(pca)
        model = VGG16()
        model = Model(inputs = model.inputs, outputs = model.layers[-2].output)
        self.feature_extractor = model
        pass

    def predict(self, bgr_image):
        pred = self.detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=700,patch_overlap=0.3)
        trees = []
        if pred is None:
            return trees
        for index, row in pred.iterrows():
            # get bounding box coordinates
            xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            # crop the image using the bounding box
            cropped_image = bgr_image[int(ymin):int(ymax), int(xmin):int(xmax)]
            feature = extract_features(cropped_image, self.feature_extractor, self.pca)
            label = self.cluster_model.predict(feature)
            #  this class is highly likely not to be a tree
            if label == 8:
                continue
            tree = {
                'seq_number' : index,
                'position' : {'x' : np.average([row['xmin'], row['xmax']]), 'y' : np.average([row['ymin'], row['ymax']])},
                'size' : {'width': row['xmax'] - row['xmin'], 'height': row['ymax'] - row['ymin']},
                'model_type' : map_label_to_tree_type(label)
            }
            trees.append(tree)
        return trees

    def detect(self, bgr_image: np.ndarray):
        return self.detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=700,patch_overlap=0.3)

def extract_features(image, model, pca):
    img = cv2.resize(image, (224, 224))
    reshaped_img = img.reshape(1,224,224,3)
    imgx = preprocess_input(reshaped_img)
    features = model.predict(imgx, use_multiprocessing=True)
    features = features.flatten()
    return pca.transform(features)


def map_label_to_tree_type(label):
    # for example only
    maper = {
        1 : 'Pine',
        2 : 'Spruce',
        3 : 'Birch',
        4 : 'Oak',
        5 : 'Ash',
        6 : 'Maple',
        7 : 'Aspen',
        9 : 'Willow',
        10 : 'Alder',
        11 : 'Poplar',
        12 : 'Fir',
        13 : 'Cedar',
        14 : 'Hemlock',
    }
    return maper[label]




global tree_predictor
tree_predictor = TreePredictor(TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL, TREE_PCA_MODEL)