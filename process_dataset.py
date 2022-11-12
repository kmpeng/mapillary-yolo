"""
This script takes a subset of the Mapillary Traffic Sign Dataset, converts its annotations into yolo format, and
splits the subset into train/valid/test sets
"""
import os
import random
import json

class_to_id_map = {}
index = 0

def move_img_annot(files, directory_images, directory_labels, target_directory_images, target_directory_labels, type):
    """Moves images and labels from one directory to another.

    :param files: list of filenames for the images that will be moved (all end in .jpg)
    :param directory_images: path to directory with the images
    :param directory_labels: path to directory with the labels
    :param target_directory_images: path to directory the images will be moved to
    :param target_directory_labels: path to directory the labels will be moved to
    :param type: .json or .txt
    """
    # move image files to `target_directory_images`
    for file in files:      
        os.rename(directory_images + '/' + file, target_directory_images + '/' + file)
        continue

    # move the matching annotations to `target_directory_labels`
    for annotations in files:
        # strip .jpg extension and add .json to find corellating annotations file
        file_name = os.path.splitext(annotations)[0] + type
        os.rename(directory_labels + '/' + file_name, target_directory_labels + '/' + file_name)
        continue

def data_subset(directory_path, target_directory_path, percent):
    """ Takes a subset of the dataset and moves it to the target directory.

    :param directory_path: path to directory with the images/annotations
    :param target_directory_path: path to directory the images/labels will be moved to
    :param percentage: percentage of the dataset we want to take
    """
    # set paths
    directory_images = str(directory_path + "/images")
    directory_labels = str(directory_path + "/annotations")
    target_directory_images = str(target_directory_path + "/images")
    target_directory_labels = str(target_directory_path + "/labels")

    # make a list of all files in `directory_images` that are jpgs
    files = [f for f in os.listdir(directory_images) if f.endswith('.jpg')]

    # randomly select `percent` percent of the image files
    random_files = random.sample(files, int(len(files) * percent))

    # move randomly selected images and annotations to the target directory
    move_img_annot(random_files, directory_images, directory_labels, target_directory_images, target_directory_labels, ".json")

def split_train_valid_test(directory_path, train_percent, valid_percent):
    """ Splits the dataset at the given path into train/valid/test sets

    :param directory_path: path to directory with the data
    :param train_percent: percentage of data that will be for training
    :param valid_percent: percentage of data that will be for validation
    """
    assert(train_percent + dev_percent < 1)

    # set paths
    directory_images = str(directory_path + "/images")
    directory_labels = str(directory_path + "/labels")
    directory_train_images = str(directory_path + "/train/images")
    directory_train_labels = str(directory_path + "/train/labels")
    directory_valid_images = str(directory_path + "/valid/images")
    directory_valid_labels = str(directory_path + "/valid/labels")
    directory_test_images = str(directory_path + "/test/images")
    directory_test_labels = str(directory_path + "/test/labels")

    # make a list of all files in `directory_images` that are jpgs
    files = [f for f in os.listdir(directory_images) if f.endswith('.jpg')]
    
    # split `files` into trian, valid, test
    # code adapted from https://cs230.stanford.edu/blog/split/
    # files.sort()
    # random.seed(182)
    random.shuffle(files)
    split_1 = int(train_percent * len(files))
    split_2 = int((train_percent + valid_percent) * len(files))
    train_files = files[:split_1]
    valid_files = files[split_1:split_2]
    test_files = files[split_2:]

    # move split dataset into respective directories
    move_img_annot(train_files, directory_images, directory_labels, directory_train_images, directory_train_labels, ".txt")
    move_img_annot(valid_files, directory_images, directory_labels, directory_valid_images, directory_valid_labels, ".txt")
    move_img_annot(test_files, directory_images, directory_labels, directory_test_images, directory_test_labels, ".txt")

def extract_from_json(json_name, directory_path):
    """ Extract info from json into a dictionary and return it.

    :param json_name: name of the json file we want to extract info from
    :param directory_path: path to directory with the json file
    :returns: a dictionary with the json filename, image size, and all classified objects in the image
    along with info about their labels, xmins, ymins, xmaxs, and ymaxs
    """
    # code adapted from https://blog.paperspace.com/train-yolov5-custom-data/

    # open json file and load it
    f = open(directory_path + "/" + json_name)
    data = json.load(f)

    # copy relevant json info about the image into a dictionary
    info_dict = {}
    info_dict['filename'] = json_name
    info_dict['image_size'] = tuple([data['width'], data['height']])

    # make a list of all identified objects' info and append it to `info_dict`
    info_dict['objects'] = []
    for object in data['objects']:
        object_dict = {}
        object_dict['label'] = object['label']
        object_dict['xmin'] = object['bbox']['xmin']
        object_dict['ymin'] = object['bbox']['ymin']
        object_dict['xmax'] = object['bbox']['xmax']
        object_dict['ymax'] = object['bbox']['ymax']
        info_dict['objects'].append(object_dict)

    # close file
    f.close()
    # print(info_dict)
    return info_dict

def convert_to_yolo(info_dict, directory_path):
    """ Convert extracted json info into a txt file in yolo format.

    :param info_dict: a dictionary with the relevant json info
    :param directory_path: path to directory the txts will be saved in
    """
    # code adapted from https://blog.paperspace.com/train-yolov5-custom-data/

    print_buffer = []
    
    # loop through all identified objects in `info_dict`
    for object in info_dict['objects']:
        try:  # get class id from `class_to_id_map`
            class_id = class_to_id_map[object['label']]
        except:  # add object label to the `class_to_id_map` dict if it does not exist
            global index
            class_to_id_map[object['label']] = index
            class_id = index
            index += 1
        # print(class_to_id_map)

        # convert coordinates to yolo format
        center_x = (object['xmin'] + object['xmax']) / 2
        center_y = (object['ymin'] + object['ymax']) / 2
        width = object['xmax'] - object['xmin']
        height = object['ymax'] - object['ymin']

        # normalize new coordinates
        image_w, image_h = info_dict['image_size']
        center_x /= image_w
        center_y /= image_h
        width /= image_w
        height /= image_h

        print_buffer.append("{} {} {} {} {}".format(class_id, center_x, center_y, width, height))

    save_file_name = os.path.join(directory_path, info_dict["filename"].replace("json", "txt"))
    print("\n".join(print_buffer), file=open(save_file_name, "w"))

def jsons_to_yolos(directory_path):
    """ Convert the dataset labels from json to yolo format.

    :param directory_path: path to directory with the labels directory
    """
    # make a list of all files in `directory_path` that are jsons
    directory_path = str(directory_path)
    directory_labels =  str(directory_path + "/labels")
    jsons = [f for f in os.listdir(directory_labels) if f.endswith('.json')]

    # convert each json file to a txt file in yolo format
    for json_name in jsons:
        info_dict = extract_from_json(json_name, directory_labels)
        convert_to_yolo(info_dict, directory_labels)
    
    # write the updated `class_to_id_map` dictionary to a txt file as a list
    global class_to_id_map
    class_to_id_map = dict(sorted(class_to_id_map.items(), key=lambda x: x[1]))
    with open(directory_path + '/class_to_id_map.txt', 'w') as file:
        file.write(json.dumps(list(class_to_id_map.keys())))
        file.write("\n" + json.dumps(class_to_id_map))
        file.write("\n" + str(len(class_to_id_map)))
    
    return jsons
    
def remove_jsons(jsons, directory_path):
    """ Removes all jsons in the given list from the given directory

    :param jsons: list of json filenames
    :param directory_path: path to directory with the json files
    """
    for json_name in jsons:
        # print(json_name)
        if os.path.exists(directory_path + "/" + json_name):
            os.remove(directory_path + "/" + json_name)


if __name__ == '__main__':
    directory_path = 'C:/Users/Anton Lok/Desktop/Yolov7 Mapillary Project/mtsd_v2_fully_annotated'
    new_directory_path = directory_path + "/custom_dataset"
    dataset_percent = float(0.2)
    # directory_path = '/Users/kaitlinpeng/Kaitlin/School/CS 230/mapillary-yolo/mapillary_tiny_sample'
    # new_directory_path = directory_path + "/custom_dataset"
    # dataset_percentage = float(1)
    data_subset(directory_path, new_directory_path, dataset_percent)
    
    jsons = jsons_to_yolos(new_directory_path)
    # remove_jsons(jsons, directory_path)  # UNCOMMENT IF YOU WANT TO DELETE THE JSONS

    train_percent = float(0.6)
    dev_percent = float(0.2)
    split_train_valid_test(new_directory_path, train_percent, dev_percent)