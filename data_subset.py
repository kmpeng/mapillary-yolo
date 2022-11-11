"""
This script takes a subset of the Mapillary Traffic Sign Dataset and splits it into train/dev/test sets
"""
import os
import random

# set paths
DIRECTORY_IMAGES = 'C:/Users/Anton Lok/Desktop/Yolov7 Mapillary Project/mtsd_v2_fully_annotated/images'
TARGET_DIRECTORY_IMAGES = 'C:/Users/Anton Lok/Desktop/Yolov7 Mapillary Project/mtsd_v2_fully_annotated/custom_dataset/images'
DIRECTORY_LABELS = 'C:/Users/Anton Lok/Desktop/Yolov7 Mapillary Project/mtsd_v2_fully_annotated/annotations'
TARGET_DIRECTORY_LABELS = 'C:/Users/Anton Lok/Desktop/Yolov7 Mapillary Project/mtsd_v2_fully_annotated/custom_dataset/labels'
directory_images = str(DIRECTORY_IMAGES)
target_directory_images = str(TARGET_DIRECTORY_IMAGES)
directory_labels = str(DIRECTORY_LABELS)
target_directory_labels = str(TARGET_DIRECTORY_LABELS)

dataset_percentage = float(0.2)

# make a list of all files in 'directory_images' that are jpgs
files = [f for f in os.listdir(directory_images) if f.endswith('.jpg')]

# randomly select 'dataset_percentage' percent of the image files
random_files = random.sample(files, int(len(files) * dataset_percentage))

# move the randomly selected images to 'target_directory_images'
for file in random_files:      
    os.rename(directory_images + '/' + file, target_directory_images + '/' + file)
    continue

# move the matching annotations to 'target_directory_labels'
for annotations in random_files:
    # strip .jpg extension and add .json to find corellating annotations file
    os.rename(directory_labels + '/' + (os.path.splitext(annotations)[0] + '.json'), target_directory_labels + '/' + (os.path.splitext(annotations)[0] + '.json'))
    continue