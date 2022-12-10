#!/bin/bash
# Train and test focal loss yolov7 model
# Run command: bash ./scripts/yolov7-focal-gamma.sh

python3 train.py --epochs 100 --workers 4 --batch-size 16 --data ../datasets/custom_full_dataset/data.yaml --img 640 640 --cfg cfg/training/yolov7.yaml --weights yolov7_training.pt --name yolov7-focal-gamma --hyp data/hyp.scratch.custom2.yaml

python3 test.py --batch-size 16 --data ../datasets/custom_full_dataset/data.yaml --img-size 640 --weights runs/train/yolov7-focal-gamma/weights/best.pt --name yolov7-focal-gamma --task test