#!/bin/bash
# Train and test cbam nms yolov7 model
# Run command: bash ./scripts/yolov7-cbam-nms.sh

python3 train.py --epochs 100 --workers 4 --batch-size 16 --data ../datasets/custom_full_dataset/data.yaml --img 640 640 --cfg cfg/training/cbam.yaml --weights yolov7_training.pt --name yolov7-cbam-nms --hyp data/hyp.scratch.custom.yaml

python3 test.py --batch-size 16 --data ../datasets/custom_full_dataset/data.yaml --img-size 640 --weights runs/train/yolov7-cbam-nms/weights/best.pt --name yolov7-cbam-nms --task test