import cv2
import json
import os

increment_frame = 100

def init_directories():
    if not os.path.exists('data'):
            os.makedirs('data')
    if not os.path.exists('data/photos'):
            os.makedirs('data/photos')
    if not os.path.isfile('data/label.json'):
        with open('data/label.json', 'w') as json_file:
            json.dump({}, json_file)

# Load the video from file, manages the frame number, and loads the frame with bounding boxes
class VideoLoader:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.frame = None
        self.original_frame = None
        self.frameNum = 1
        if not self.cap.isOpened():
            print('Error opening video stream or file')
            exit()
    def load_frame(self, frame_num = None):
        if frame_num is not None:
            self.frameNum = frame_num-1
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frameNum)
        ret, self.original_frame = self.cap.read()     
        if not ret:
            print('Reached end of video')
            exit()
        self.frame = self.original_frame.copy()
        self.frameNum += 1
    def updateFrame(self, bBx):
        self.frame = bBx.drawBoudingBoxes(self.original_frame)
        cv2.imshow('Video', self.frame)
    def __del__(self):
        self.cap.release()

# Load the JSON label file, add labels, and save the JSON file
class JSONLoader:
    def __init__(self, json_path):
        self.json_path = json_path
        self.json_data = None
        self.length = None
        self.decrement_once = False
        self.load_json()
    def load_json(self):
        with open(self.json_path) as json_file:
            self.json_data = json.load(json_file)
            print(self.json_data.keys())
        self.length = len(self.json_data)
        print(self.length)
    def add_label(self, bBx, videoLoader):
        self.decrement_once = False
        self.json_data[self.length] = {
            'boundingBoxes': bBx.boundingBoxes,
            'frame': videoLoader.frameNum,
            'fileName': videoLoader.video_path
        }
        self.length += 1
        print(self.length)
    def saveJSON(self):
        print('Saving JSON')
        with open(self.json_path, 'w') as json_file:
            json.dump(self.json_data, json_file)
    def decrement_frame(self):
        if self.length == 1:
            pass
        elif self.decrement_once:
            self.json_data.pop(self.length-1)
            self.length -= 1
        else:
            self.decrement_once = True

# Create a class for a set of bounding boxes for each frame
class BoundingBoxes:
    def __init__(self):
        self.id = 0
        self.boundingBoxes = []
        self.currentBox = None
    def drawBoudingBoxes(self, frame):
        ret = frame.copy()
        for boundingBox in self.boundingBoxes:
            ret = self.drawBoudingBox(ret, boundingBox)
        if self.currentBox is not None:
            ret = self.drawBoudingBox(ret, self.currentBox)
        return ret
    def drawBoudingBox(self, frame, boundingBox):
        cv2.rectangle(frame, boundingBox[0:2], boundingBox[2:4], (0, 255, 0), 2)
        return frame
    def updateCurrentBox(self, boundingBox):
        self.currentBox = boundingBox
    def finishCurrentBox(self):
        self.boundingBoxes.append(self.currentBox)
        self.currentBox = None
    def popBoundingBoxes(self, jsonLoader, videoLoader):
        if self.currentBox is not None:
            self.currentBox = None
            onclick.selected = False
        elif len(self.boundingBoxes) > 0:
            self.boundingBoxes.pop()
        elif len(self.boundingBoxes) == 0:
            jsonLoader.decrement_frame()
            self.boundingBoxes = jsonLoader.json_data[jsonLoader.length-1]['boundingBoxes']
            videoLoader.load_frame(jsonLoader.json_data[jsonLoader.length-1]['frame'])
    def clearBoundingBoxes(self):
        self.boundingBoxes = []
        self.currentBox = None

def main():
    init_directories()
    # Load the video from file
    video_path = 'videos/001.avi'
    video_loader = VideoLoader(video_path)

    # Create a window for displaying the video
    cv2.namedWindow('Video', cv2.WINDOW_GUI_NORMAL)
    bBx = BoundingBoxes()
    cv2.setMouseCallback('Video', onclick, bBx)

    # Load the JSON file
    data = JSONLoader('data/label.json')
    
    # Display the first frame in the window
    if data.length != 0:
        video_loader.load_frame(data.json_data[str(data.length-1)]['frame']+increment_frame)
    else:
        video_loader.load_frame()
    # cv2.imshow('Video', video_loader.frame)

    # Display the video in the window
    while video_loader.cap.isOpened():
        # Display the frame in the window
        video_loader.updateFrame(bBx)

        # Check if the user wants to quit
        keyPress = cv2.waitKey(1)
        if keyPress == 27:
            bBx.popBoundingBoxes(data, video_loader)
        elif keyPress == ord('q'):
            data.saveJSON()
            
            break
        elif keyPress == ord('s'):
            data.add_label(bBx, video_loader)
            # save image
            pathwithoutExtenstion = os.path.splitext(video_loader.video_path)[0]
            # print frame number
            print(video_loader.frameNum)
            cv2.imwrite('data/photos/'+os.path.basename(pathwithoutExtenstion)+'_'+str(data.length)+'.jpg', video_loader.original_frame)
            bBx.clearBoundingBoxes()
            print('Saved')
            video_loader.load_frame(video_loader.frameNum + increment_frame)

# Callback function for mouse events
def onclick(event, x, y, flags, bBx):
    if event == cv2.EVENT_FLAG_LBUTTON:
        if not onclick.selected:
            print('Selected')
            bBx.currentBox = (x, y, x, y)
        else:
            print('Unselected')
            bBx.finishCurrentBox()
        onclick.selected = ~onclick.selected
    if event == cv2.EVENT_MOUSEMOVE:
        if onclick.selected:
            bBx.currentBox = (bBx.currentBox[0], bBx.currentBox[1], x, y)

onclick.selected = False

if __name__ == '__main__':
    main()
