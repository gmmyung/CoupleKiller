Couple Killer, just because I hate couples
==========================================
This project intends to eliminate ALL COUPLES in the street.

![Alt Text](example.gif)

[Demo]

# Requirements

- Conda enviorment
- Python
- opencv2
- TBD

In order to set up your enviornment, follow these steps:

## 1. Install anaconda enviornment

 Refer to this [link](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

## 2. Create a new enviornment

```conda create --name CoupleKiller```

```conda activate CoupleKiller```

## 3. Install OpenCV and Pyav

```conda install -c conda-forge opencv```

```pip install av```

## 4. Clone yolov5

Refer to this [link](https://github.com/ultralytics/yolov5)

## 5. Label the data

```python labeler.py```

## 6. Format the data suitable for yolov5

```python formatter.py```

## 6. Train the model

```cd yolov5```

```python train.py --img 640 --batch 16 --epochs 100 --data ../CoupleKiller.yaml --weights yolov5n.pt```

