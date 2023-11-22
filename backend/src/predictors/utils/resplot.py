import cv2
import numpy as np

def plot_coco_result(coco, image):
    """
    Plot the COCO results on the given image.

    Parameters:
    - coco (list): List of COCO results.
    - image (numpy.ndarray): Input image.

    Returns:
    - output_img (numpy.ndarray): Image with COCO results plotted.
    """
    output_img = np.zeros(image.shape)
    output_img.fill(255)
    for result in coco:
        for segmentation in result['segmentation']:
            cv2.polylines(image, [np.array(segmentation).reshape(-1,2)], True, (255, 0, 0), thickness=1)
            cv2.fillPoly(output_img, [np.array(segmentation).reshape(-1,2)], color=(0, 0, 0))
    return output_img


def plot_csv_result(csv, image):
    """
    Plot the bounding box results from a CSV file on an image.

    Parameters:
    csv (pandas.DataFrame): The CSV file containing the bounding box coordinates.
    image (numpy.ndarray): The image on which to plot the bounding boxes.

    Returns:
    numpy.ndarray: The image with the plotted bounding boxes.
    """
    output = np.zeros(image.shape)
    output.fill(255)
    for index, row in csv.iterrows():
        xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        width = xmax - xmin
        height = ymax - ymin
        cv2.rectangle(output,(int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 0), -1)
    return output

def merge_image(image, building, roads, trees):
    """
    Merge the given images of building, roads, and trees with the original image.

    Parameters:
    image (numpy.ndarray): The original image.
    building (numpy.ndarray): The image of buildings.
    roads (numpy.ndarray): The image of roads.
    trees (numpy.ndarray): The image of trees.

    Returns:
    numpy.ndarray: The merged image.
    """
    _merged_image = np.zeros((2 * image.shape[0], 2 * image.shape[1], 3), dtype=np.uint8)
    _merged_image[:image.shape[0], :image.shape[1], :] = image[:, :, ::-1]
    _merged_image[:building.shape[0], image.shape[1]:, :] = building
    _merged_image[image.shape[0]:, :roads.shape[1], :] = roads
    _merged_image[image.shape[0]:, roads.shape[1]:, :] = trees
    return _merged_image

def encode_image(image):
    """
    Encodes the given image as a PNG format.

    Parameters:
    image (numpy.ndarray): The input image to be encoded.

    Returns:
    bytes: The encoded image in PNG format.
    """
    return cv2.imencode('.png', image)