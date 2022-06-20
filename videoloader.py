import cv2

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