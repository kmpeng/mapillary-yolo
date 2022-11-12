"""
This script takes a subset of the Mapillary Traffic Sign Dataset, converts its annotations into yolo format, and
splits the subset into train/valid/test sets
"""
from utils.move_data import *
from utils.convert_yolo import *

if __name__ == '__main__':
    directory_path = 'C:/Users/Anton Lok/Desktop/Yolov7 Mapillary Project/mtsd_v2_fully_annotated'
    new_directory_path = directory_path + "/custom_dataset"
    dataset_percent = float(0.2)
    data_subset(directory_path, new_directory_path, dataset_percent)
    
    jsons = jsons_to_yolos(new_directory_path)
    # remove_jsons(jsons, directory_path)  # UNCOMMENT IF YOU WANT TO DELETE THE JSONS

    train_percent = float(0.6)
    dev_percent = float(0.2)
    split_train_valid_test(new_directory_path, train_percent, dev_percent)