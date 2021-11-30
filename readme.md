Author: Joseph Cheng
Date: 27/11/2021
Language: Python3

### Purpose:
    1. Detecting Players & Basketball on the court
        How: Object Detection of people on the court
    2. Detecting Events such as ball posession, scoring, rebounding, free throw, assist, block, steal etc.

### How to run (Mac):
    1. Python Virtual Environment
        1.1. Python3 -m venv env
        1.2. source env/bin/activate (mac) or .\env\Scripts\activate for windows
        1.3. pip install -r requirement.txt
    2. youtube-dl python library
        Requirement: Brew - https://brew.sh/
        ffmpeg - brew install ffmpeg
    Note: Beware of Copyright!

### Questions to answer:
    1. Accuracy of the model
    2. Required hardware setting for the models
    3. Continuous improvement
### Appendix:
1. Holy Guacamole Seasion Play list
- [Season 2](https://www.youtube.com/playlist?list=PLVcnSCX19O4AwZHFaUfX21axVKY99KINn)
- [Season 3](https://www.youtube.com/playlist?list=PLVcnSCX19O4D6xiCO0XUEsH-f3AJqK_Yd)
- [Season 4](https://www.youtube.com/playlist?list=PLVcnSCX19O4AhuaHr5MIaJY4ql-GYQhGM)

2. YOLO object detection model

- [tutorial](https://www.r-bloggers.com/2021/09/object-detection-and-tracking-in-python/)
-  download the content within the yolov3 folder (coco.names, yolov3.cfg, and yolov3.weights)