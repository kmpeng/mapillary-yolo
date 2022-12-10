#!/bin/bash
# Train and test adam yolov7 model
# Run command: bash ./scripts/yolov7-adam.sh

python3 train.py --epochs 100 --workers 4 --batch-size 16 --data ../datasets/custom_full_dataset/data.yaml --img 640 640 --cfg cfg/training/yolov7.yaml --weights yolov7_training.pt --name yolov7-adam --hyp data/hyp.scratch.custom.yaml --adam

python3 test.py --batch-size 16 --data ../datasets/custom_full_dataset/data.yaml --img-size 640 --weights runs/train/yolov7-adam/weights/best.pt --name yolov7-adam --task test