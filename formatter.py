import json
from utils import JSONLoader
import os

json_path = 'data/label.json'
jsonloader = JSONLoader(json_path)
if not os.path.exists('data/labels/'):
    os.makedirs('data/labels/')
for data in jsonloader.json_data:
    pathwithoutExtenstion = os.path.splitext(jsonloader.json_data[data]['fileName'])[0]
    filename = os.path.basename(pathwithoutExtenstion)+'_'+str(int(data)+1)+'.txt'
    # write new txt file
    with open('data/labels/'+filename, 'w') as f:
        for boundingBox in jsonloader.json_data[data]["boundingBoxes"]:
            x_center = (boundingBox[0] + boundingBox[2]) / 2
            y_center = (boundingBox[1] + boundingBox[3]) / 2
            x_width = abs(boundingBox[2] - boundingBox[0])
            y_height = abs(boundingBox[3] - boundingBox[1])
            # normalize with width 854 and height 480
            x_center = x_center / 854
            y_center = y_center / 480
            x_width = x_width / 854
            y_height = y_height / 480
            f.write("0 %f %f %f %f\n" % (x_center, y_center, x_width, y_height))
