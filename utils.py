import json
import cv2
import av

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
        self.length = len(self.json_data)
        print(self.length)
    def add_label(self, bBx, videoLoader):
        self.decrement_once = False
        self.json_data[str(self.length)] = {
            'boundingBoxes': bBx.boundingBoxes,
            'frame': videoLoader.frameNum,
            'fileName': videoLoader.video_path
        }
        self.length += 1
    def saveJSON(self):
        print('Saving JSON')
        with open(self.json_path, 'w') as json_file:
            json.dump(self.json_data, json_file)
    def decrement_frame(self):
        if self.length <= 1:
            pass
        elif self.decrement_once:
            self.json_data.pop(str(self.length-1))
            self.length -= 1
        else:
            self.decrement_once = True


class VideoLoader:
    def __init__(self, video_path):
        self.video_path = video_path
        self.container = av.container.open(self.video_path)
        self.frameNum = 0
        self.frame = None
        self.original_frame = None
        self.stream = self.container.streams.video[0]
        self.total_frames = self.stream.frames
        self.seek(0)

    def iter_frames(self):
        for packet in self.container.demux(self.stream):
            if packet.dts is None:
                continue
            for frame in packet.decode():
                yield frame

    def __del__(self):
        self.container.close()

    def load_frame(self, frameNum=None):
        if frameNum is not None:
            self.seek(frameNum)
        try:
            frame = next(self.iter)
        except StopIteration:
            self.end = True
            return None
        self.frameNum += 1
        self.original_frame = frame.to_ndarray(format='bgr24')
    def seek(self, frame):
        pts = int(frame * self.stream.duration / self.stream.frames)
        self.container.seek(pts, stream=self.stream)
        for j, f in enumerate(self.iter_frames()):
            if f.pts >= pts - 1:
                break
        self.end = False
        self.frameNum = frame
        self.iter = iter(self.iter_frames())
    def updateFrame(self, bBx):
        self.frame = bBx.drawBoudingBoxes(self.original_frame)
        cv2.imshow('Video', self.frame)

# Create a class for a set of bounding boxes for each frame
class BoundingBoxes:
    def __init__(self):
        self.id = 0
        self.boundingBoxes = []
        self.currentBox = None
        self.onclick_selected = False
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
            self.onclick_selected = False
        elif len(self.boundingBoxes) > 0:
            self.boundingBoxes.pop()
        elif len(self.boundingBoxes) == 0:
            jsonLoader.decrement_frame()
            self.boundingBoxes = jsonLoader.json_data[str(jsonLoader.length-1)]['boundingBoxes']
            videoLoader.load_frame(jsonLoader.json_data[str(jsonLoader.length-1)]['frame'])
    def clearBoundingBoxes(self):
        self.boundingBoxes = []
        self.currentBox = None
