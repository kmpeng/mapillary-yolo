"""
Contains functions for moving images and their labels from one directory to another, taking a subset of the dataset,
and splitting the dataset into train/valid/test sets
"""
import os
import random

def move_img_labels(files, directory_images, directory_labels, target_directory_images, target_directory_labels, type):
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
    move_img_labels(random_files, directory_images, directory_labels, target_directory_images, target_directory_labels, ".json")

def split_train_valid_test(directory_path, train_percent, valid_percent):
    """ Splits the dataset at the given path into train/valid/test sets

    :param directory_path: path to directory with the data
    :param train_percent: percentage of data that will be for training
    :param valid_percent: percentage of data that will be for validation
    """
    assert(train_percent + valid_percent < 1)

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
    random.shuffle(files)
    split_1 = int(train_percent * len(files))
    split_2 = int((train_percent + valid_percent) * len(files))
    train_files = files[:split_1]
    valid_files = files[split_1:split_2]
    test_files = files[split_2:]

    # move split dataset into respective directories
    move_img_labels(train_files, directory_images, directory_labels, directory_train_images, directory_train_labels, ".txt")
    move_img_labels(valid_files, directory_images, directory_labels, directory_valid_images, directory_valid_labels, ".txt")
    move_img_labels(test_files, directory_images, directory_labels, directory_test_images, directory_test_labels, ".txt")