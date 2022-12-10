#!/bin/bash
# Train and test baseline yolov5l model
# Run command: bash ./scripts/yolov5_baseline.sh

python3 train.py --epochs 100 --workers 4 --batch-size 16 --data /home/ubuntu/datasets/custom_full_dataset/data.yaml --img 640 --cfg models/yolov5l.yaml --weights 'yolov5l.pt' --name yolov5_baseline --hyp data/hyps/hyp.scratch-low.yaml

python3 val.py --data /home/ubuntu/datasets/custom_full_dataset/data.yaml --imgsz 640 --weights runs/train/yolov5_baseline/weights/best.pt --name yolov5_baseline --task test