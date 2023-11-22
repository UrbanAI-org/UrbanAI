import cv2
import numpy as np

def plot_coco_result(coco, image):
    output_img = np.zeros(image.shape)
    output_img.fill(255)
    for result in coco:
#         xmin, ymin, xmax, ymax = result['bbox']
        
#         pt1 = (int(xmin), int(ymin))
#         pt2 = (int(xmax), int(ymax))
#         image = cv2.rectangle(image, pt1, pt2, (255, 255, 255), 2)
        for segmentation in result['segmentation']:
            cv2.polylines(image, [np.array(segmentation).reshape(-1,2)], True, (255, 0, 0), thickness=1)
            cv2.fillPoly(output_img, [np.array(segmentation).reshape(-1,2)], color=(0, 0, 0))
    return output_img


def plot_csv_result(csv, image):
    output = np.zeros(image.shape)
    output.fill(255)
    for index, row in csv.iterrows():
        xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        width = xmax - xmin
        height = ymax - ymin
        cv2.rectangle(output,(int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 0, 0), -1)
    return output

def merge_image(image, building, roads, trees):
    _merged_image = np.zeros((2 * image.shape[0], 2 * image.shape[1], 3), dtype=np.uint8)
    _merged_image[:image.shape[0], :image.shape[1], :] = image[:, :, ::-1]
    _merged_image[:building.shape[0], image.shape[1]:, :] = building
    _merged_image[image.shape[0]:, :roads.shape[1], :] = roads
    _merged_image[image.shape[0]:, roads.shape[1]:, :] = trees
    return _merged_image

def encode_image(image):
    return cv2.imencode('.png', image)