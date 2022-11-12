"""
Contains functions to convert the MTSD json annotations format into txt files in yolo format and
delete json files
"""
import os
import json

class_to_id_map = {}
index = 0

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
        if os.path.exists(directory_path + "/" + json_name):
            os.remove(directory_path + "/" + json_name)