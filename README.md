<div align="center">
<br>
<h1>
Traffic Sign Localization and Classification
</h1>
<h4>
Anton Lok, Kaitlin Peng, Victoria Wu
</h4>
<p>
<i>CS230: Deep Learning, Fall 2022, Stanford University</i>
</p>
</div>

The scripts used to train and test our models are in  ```src/yolov5/scripts``` and ```src/yolov7/scripts```. They are run from the ```src/yolov5``` and ```src/yolov7``` directories respectively, using ```bash ./scripts/*.sh```.

The folder ```src``` includes the python script ```process_dataset.py``` which was used to convert our dataset labels to YOLO txt form and split the dataset into train/val/test sets. ```process_dataset.py``` calls helper scripts in ```src/utils```.

The training runs for all our models are under ```src/yolov5/runs/train``` and ```src/yolov7/runs/train```. They include the hyperparameters used ```hyp.yaml```, options used ```opt.yaml```, and the best and last weights for the training, ```weights/best.pt``` and ```weights/last.pt```.

```
.
|-- sample_dataset/
|-- src/
    |-- process_dataset.py
    |-- utils/
        |-- convert_yolo.py
        |-- move_data.py
    |-- yolov5/
        |-- scripts/
            ...
        |-- runs/
            |-- train/
                |-- *
                    |-- hyp.yaml
                    |-- opt.yaml
                    |-- weights/
                        |-- best.pt
                        |-- last.pt
        ...
    |-- yolov7/
        |-- scripts/
            ...
        |-- runs/
            |-- train/
                |-- *
                    |-- hyp.yaml
                    |-- opt.yaml
                    |-- weights/
                        |-- best.pt
                        |-- last.pt
        ...
        
```

![image](https://lh4.googleusercontent.com/LMvR8q_GYbLZaThOqZlDO7KuwoBVzwnO5kqrjXVGRpkNKa53UbWfGONtBrDMLme9lks=w2400)