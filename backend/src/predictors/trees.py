
import math
from src.database.singletonMeta import SingletonMeta
from src.config import TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL, TREE_PCA_MODEL
from deepforest import main
import pickle
import numpy as np
import joblib
import cv2
# models
from src.predictors.utils.resplot import plot_csv_result

class TreePredictor(metaclass=SingletonMeta):
    detect_model = None
    cluster_model = None
    feature_extractor = None
    pca = None
    def __init__(self, detect_model_path=None, cluster_model_path=None, pca_path=None) -> None:
        """
        Initializes the Trees class.

        Args:
            detect_model_path (str): Path to the detect model checkpoint.
            cluster_model_path (str): Path to the cluster model.
            pca_path (str): Path to the PCA model.
        """
        self.detect_model = main.deepforest.load_from_checkpoint(detect_model_path)
        self.cluster_model = joblib.load(cluster_model_path)
        self.pca = joblib.load(pca_path)

    def predict(self, bgr_image):
        """
        Predicts the class label for a given BGR image.

        Args:
            bgr_image (numpy.ndarray): The BGR image to be predicted.

        Returns:
            The predicted class label.
        """
        return _predict(bgr_image, self.detect_model, self.cluster_model, self.pca)

    def detect(self, bgr_image: np.ndarray):
        """
        Detects trees in the given BGR image.

        Args:
            bgr_image (np.ndarray): The input BGR image.

        Returns:
            np.ndarray: The predicted tiles containing trees.
        """
        return self.detect_model.predict_tile(image=bgr_image, return_plot=False, patch_size=620, patch_overlap=0.3)
    def detect(self, bgr_image: np.ndarray):
        return self.detect_model.predict_tile(image = bgr_image, return_plot = False, patch_size=620,patch_overlap=0.3)

    def predict_image(self, bgr_image):
        """
        Predicts the class labels for a given BGR image.

        Args:
            bgr_image (numpy.ndarray): The input BGR image.

        Returns:
            numpy.ndarray: The image with predicted class labels plotted.

        """
        csv = self.detect(bgr_image)
        return plot_csv_result(csv, bgr_image)

def _predict(bgr_image, detect_model, cluster_model, pca):
    """
    Predicts the trees in the given image using the specified models.

    Args:
        bgr_image (numpy.ndarray): The input image in BGR format.
        detect_model: The detection model used to detect tree regions in the image.
        cluster_model: The clustering model used to classify the detected tree regions.
        pca: The PCA model used for feature extraction.

    Returns:
        tuple: A tuple containing two elements:
            - A list of dictionaries representing the detected trees, where each dictionary contains the following keys:
                - 'seq_number': The sequence number of the tree.
                - 'position': A dictionary with 'x' and 'y' keys representing the position of the tree.
                - 'size': A dictionary with 'width' and 'height' keys representing the size of the tree.
                - 'model_type': The type of the tree predicted by the clustering model.
                - 'height': The estimated height of the tree.
            - A set of unique tree types predicted by the clustering model.
    """
    pred = detect_model.predict_tile(image=bgr_image, return_plot=False, patch_size=620, patch_overlap=0.3)
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
        tree_type = _map_label_to_tree_type(label, row['width'], row['height'])

        tree = {
            'seq_number': index,
            'position': {'x': np.average([row['xmin'], row['xmax']]), 'y': np.average([row['ymin'], row['ymax']])},
            'size': {'width': row['width'], 'height': row['height']},
            'model_type': tree_type,
            'height': _map_height(label, row['width'], row['height'])
        }
        trees.append(tree)
        tree_types.add(tree_type)
    return trees, tree_types

def _extract_features(cropped_image, pca, target_size=(100, 100)):
    """
    Extracts features from a cropped image using PCA transformation.

    Parameters:
    - cropped_image: The input image to extract features from.
    - pca: The PCA object used for feature transformation.
    - target_size: The target size of the resized image (default: (100, 100)).

    Returns:
    - The transformed features of the input image.
    """
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


def _map_label_to_tree_type(label, width, height):
    """
    Maps the label to the corresponding tree type based on the given width and height.

    Args:
        label (int): The label of the tree.
        width (int): The width of the tree.
        height (int): The height of the tree.

    Returns:
        str: The tree type corresponding to the label.

    """
    maper = {
        0 : 'class1',
        1 : 'class4',
        2 : 'class5',
        3 : 'class10',
        4 : 'class3',
        5 : 'class1',
        6 : 'class8',
    }
    tree_type = maper[label]
    if label == 5:
        if width > 80 or height > 80:
            tree_type = 'class3'
    return tree_type

def _map_height(label, width, height):
    """
    Maps the height of a label to a value.
    Haven't implemented yet.
    Args:
        label (str): The label of the object.
        width (int): The width of the object.
        height (int): The height of the object.

    Returns:
        int: The mapped height value. 10 is the default value.
    """
    return 10


global tree_predictor
tree_predictor = TreePredictor(TREE_DETECTION_MODEL, TREE_CLUSTER_MODEL, TREE_PCA_MODEL)