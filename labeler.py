from turtle import up
import cv2
import json

class VideoLoader:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.frame = None
        self.original_frame = None
        if not self.cap.isOpened():
            print('Error opening video stream or file')
            exit()

    def load_frame(self):
        ret, self.original_frame = self.cap.read()
        self.frame = self.original_frame.copy()
        if not ret:
            print('Reached end of video')
            exit()

class JSONLoader:
    def __init__(self, json_path):
        self.json_path = json_path
        self.json_data = None
        self.load_json()
    def load_json(self):
        with open(self.json_path) as json_file:
            self.json_data = json.load(json_file)
    def saveJSON(self):
        with open(self.json_path, 'w') as json_file:
            json.dump(self.json_data, json_file)
    def add_label(self, bBx, ):
        self.json_data['boxes'].append(bBx.to_json())
        self.saveJSON()

class BoundingBoxes:
    def __init__(self):
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
    def popBoundingBoxes(self):
        if self.currentBox is not None:
            self.currentBox = None
            onclick.selected = False
        elif len(self.boundingBoxes) > 0:
                self.boundingBoxes.pop()
    def clearBoundingBoxes(self):
        self.boundingBoxes = []
        self.currentBox = None
    

def main():
    # Load the video from file
    video_path = 'videos/001.avi'
    video_loader = VideoLoader(video_path)

    # Create a window for displaying the video
    cv2.namedWindow('Video', cv2.WINDOW_GUI_NORMAL)
    bBx = BoundingBoxes()
    cv2.setMouseCallback('Video', onclick, bBx)
    
    # Display the first frame in the window
    video_loader.load_frame()
    cv2.imshow('Video', video_loader.frame)

    # Display the video in the window
    while video_loader.cap.isOpened():
        # Display the frame in the window
        updateFrame(video_loader, bBx)

        # Check if the user wants to quit
        keyPress = cv2.waitKey(1)
        if keyPress == 27:
            bBx.popBoundingBoxes()
        elif keyPress == ord('q'):
            break
        elif keyPress == ord('s'):
            bBx.clearBoundingBoxes()
            print('Saved')
            for i in range(10):
                video_loader.load_frame()
    
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

def updateFrame(VideoLoader, bBx):
    VideoLoader.frame = bBx.drawBoudingBoxes(VideoLoader.original_frame)
    cv2.imshow('Video', VideoLoader.frame)

if __name__ == '__main__':
    main()
