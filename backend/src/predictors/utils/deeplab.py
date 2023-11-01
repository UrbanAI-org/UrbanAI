from typing import Any, Dict, List, Optional

import numpy as np
import torch
import os
import numpy as np
import segmentation_models_pytorch as smp

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import albumentations as album

from sahi.models.base import DetectionModel
from sahi.prediction import ObjectPrediction
from sahi.utils.compatibility import fix_full_shape_list, fix_shift_amount_list
from sahi.utils.import_utils import check_requirements
from sahi.utils.cv import get_bbox_from_bool_mask
ENCODER = 'resnet50'
ENCODER_WEIGHTS = 'imagenet'

ACTIVATION = 'sigmoid' # could be None for logits or 'softmax2d' for multiclass segmentation
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)

class_names = ['road', 'background']

class_rgb_values = [[255, 255, 255], [0, 0, 0]]


select_classes = ['background', 'road']

# Get RGB values of required classes
select_class_indices = [class_names.index(cls.lower()) for cls in select_classes]
select_class_rgb_values =  np.array(class_rgb_values)[select_class_indices]


def reverse_one_hot(image):
    """
    Transform a 2D array in one-hot format (depth is num_classes),
    to a 2D array with only 1 channel, where each pixel value is
    the classified class key.
    # Arguments
        image: The one-hot format image

    # Returns
        A 2D array with the same width and hieght as the input, but
        with a depth size of 1, where each pixel value is the classified
        class key.
    """
    x = np.argmax(image, axis = -1)
    return x

def colour_code_segmentation(image, label_values):
    """
    Given a 1-channel array of class keys, colour code the segmentation results.
    # Arguments
        image: single channel array where each value represents the class key.
        label_values

    # Returns
        Colour coded image for segmentation visualization
    """
    colour_codes = np.array(label_values)
    x = colour_codes[image.astype(int)]

    return x

def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')

def get_preprocessing(preprocessing_fn=None):
    """Construct preprocessing transform
    Args:
        preprocessing_fn (callable): data normalization function
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose
    """
    _transform = []
    if preprocessing_fn:
        _transform.append(album.Lambda(image=preprocessing_fn))
    _transform.append(album.Lambda(image=to_tensor, mask=to_tensor))

    return album.Compose(_transform)

encode = get_preprocessing(preprocessing_fn)

class DeepLabRoadSeg(DetectionModel):
    def check_dependencies(self) -> None:
        # check_requirements(["ultralytics"])
        pass

    def load_model(self):
        """
        Detection model is initialized and set to self.model.
        """
          # TODO
        # from ultralytics import YOLO
        import torch

        try:
            model = torch.load(self.model_path, map_location=DEVICE)
            model.to(self.device)
            self.set_model(model)
        except Exception as e:
            raise TypeError("model_path is not a valid yolov8 model path: ", e)

    def set_model(self, model: Any):
        """
        Sets the underlying YOLOv8 model.
        Args:
            model: Any
                A YOLOv8 model
        """

        self.model = model

        # set category_mapping
        if not self.category_mapping:
            category_mapping = {str(ind): category_name for ind, category_name in enumerate(self.category_names)}
            self.category_mapping = category_mapping

    def perform_inference(self, image: np.ndarray):
        """
        Prediction is performed using self.model and the prediction result is set to self._original_predictions.
        Args:
            image: np.ndarray
                A numpy array that contains the image to be predicted. 3 channel image should be in RGB order.
        """
      # TODO
        # Confirm model is loaded
        if self.model is None:
            raise ValueError("Model is not loaded, load it by calling .load_model()")
        get_preprocessing(preprocessing_fn)
        sample = encode(image=image[:,:,::-1])
        x_tensor = torch.from_numpy(sample['image']).to(DEVICE).unsqueeze(0)
        pred_mask = self.model(x_tensor)  # YOLOv8 expects numpy arrays to have BGR

        pred_mask = pred_mask.detach().squeeze().cpu().numpy()
        pred_mask = np.transpose(pred_mask,(1,2,0))
        pred_mask = colour_code_segmentation(reverse_one_hot(pred_mask), select_class_rgb_values)
        self._original_predictions = pred_mask

    @property
    def category_names(self):
        # TODO
        return ["Road"]

    @property
    def num_categories(self):
        """
        Returns number of categories
        """
        # TODO
        return len(["Road"])

    @property
    def has_mask(self):
        """
        Returns if model output contains segmentation mask
        """
        return True  # fix when yolov5 supports segmentation models

    def _create_object_prediction_list_from_original_predictions(
        self,
        shift_amount_list: Optional[List[List[int]]] = [[0, 0]],
        full_shape_list: Optional[List[List[int]]] = None,
    ):
        """
        self._original_predictions is converted to a list of prediction.ObjectPrediction and set to
        self._object_prediction_list_per_image.
        Args:
            shift_amount_list: list of list
                To shift the box and mask predictions from sliced image to full sized image, should
                be in the form of List[[shift_x, shift_y],[shift_x, shift_y],...]
            full_shape_list: list of list
                Size of the full image after shifting, should be in the form of
                List[[height, width],[height, width],...]
        """
        original_predictions = self._original_predictions

        # print("aaa")
        # compatilibty for sahi v0.8.15
        shift_amount_list = fix_shift_amount_list(shift_amount_list)
        full_shape_list = fix_full_shape_list(full_shape_list)

        # handle all predictions
        object_prediction_list_per_image = []
        # for image_ind, result in enumerate(original_predictions):
        shift_amount = shift_amount_list[0]
        full_shape = None if full_shape_list is None else full_shape_list[0]
        # bool_mask = np.sum(original_predictions, axis=2)[:480, :592] /3 /255
        # rows = np.any(bool_mask, axis=1)
        # cols = np.any(bool_mask, axis=0)
        # print(rows)
        # print(cols)
        # ymin, ymax = np.where(rows)[0][[0, -1]]
        # xmin, xmax = np.where(cols)[0][[0, -1]]
        # print(np.where(rows)[0][[0, -1]])
        # print(np.where(cols)[0][[0, -1]])
        # width = xmax - xmin
        # height = ymax - ymin

        # if width == 0 or height == 0:
        #     return None

        # return [xmin, ymin, xmax, ymax]
        #     object_prediction_list = []

        #     # process predictions
        #     if result.masks is None or result.boxes is None:
        #         object_prediction_list_per_image.append(object_prediction_list)

        #         continue
        #     for box, mask in zip(result.boxes.data.cpu().detach().numpy(), result.masks.data.cpu().detach().numpy()):
        #         x1 = box[0]
        #         y1 = box[1]
        #         x2 = box[2]
        #         y2 = box[3]
        #         bbox = [x1, y1, x2, y2]
        #         score = box[4]
        #         category_id = int(box[5])
        #         category_name = self.category_mapping[str(category_id)]

        #         # fix negative box coords
        #         bbox[0] = max(0, bbox[0])
        #         bbox[1] = max(0, bbox[1])
        #         bbox[2] = max(0, bbox[2])
        #         bbox[3] = max(0, bbox[3])

        #         # fix out of image box coords
        #         if full_shape is not None:
        #             bbox[0] = min(full_shape[1], bbox[0])
        #             bbox[1] = min(full_shape[0], bbox[1])
        #             bbox[2] = min(full_shape[1], bbox[2])
        #             bbox[3] = min(full_shape[0], bbox[3])

        mask = np.sum(original_predictions, axis=2)[:480, :592] /3 /255
        # print(mask)

        object_prediction_list = []
        bbox = get_bbox_from_bool_mask(mask)
        if bbox is not None:
          # print("aaaa")
          object_prediction = ObjectPrediction(
              bbox=bbox,
              category_id=1,
              score=0.99,
              bool_mask=mask,
              category_name="Road",
              shift_amount=shift_amount,
              full_shape=full_shape,
          )
          object_prediction_list.append(object_prediction)
        object_prediction_list_per_image.append(object_prediction_list)

        self._object_prediction_list_per_image = object_prediction_list_per_image
