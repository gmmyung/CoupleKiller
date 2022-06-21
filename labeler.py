import cv2
import json
import os
from utils import JSONLoader, VideoLoader, BoundingBoxes

increment_frame = 100

def init_directories():
    if not os.path.exists('data'):
            os.makedirs('data')
    if not os.path.exists('data/images'):
            os.makedirs('data/images')
    if not os.path.isfile('data/label.json'):
        with open('data/label.json', 'w') as json_file:
            json.dump({}, json_file)

def main():
    init_directories()
    video_path = 'videos/001.avi'
    video_loader = VideoLoader(video_path)

    cv2.namedWindow('Video', cv2.WINDOW_GUI_NORMAL)
    bBx = BoundingBoxes()
    cv2.setMouseCallback('Video', onclick, bBx)
    data = JSONLoader('data/label.json')
    
    # Display the first frame in the window
    if data.length != 0:
        video_loader.load_frame(data.json_data[str(data.length-1)]['frame']+increment_frame)
    else:
        video_loader.load_frame()

    # Display the video in the window
    while True:
        video_loader.updateFrame(bBx)
        keyPress = cv2.waitKey(1)
        if keyPress == 27:
            bBx.popBoundingBoxes(data, video_loader)
        elif keyPress == ord('q'):
            data.saveJSON()
            break
        elif keyPress == ord('s'):
            data.add_label(bBx, video_loader)
            pathwithoutExtenstion = os.path.splitext(video_loader.video_path)[0]
            cv2.imwrite('data/images/'+os.path.basename(pathwithoutExtenstion)+'_'+str(data.length)+'.jpg', video_loader.original_frame)
            bBx.clearBoundingBoxes()
            video_loader.load_frame(video_loader.frameNum + increment_frame)

def onclick(event, x, y, flags, bBx):
    if event == cv2.EVENT_FLAG_LBUTTON:
        if not bBx.onclick_selected:
            bBx.currentBox = (x, y, x, y)
        else:
            bBx.finishCurrentBox()
        bBx.onclick_selected = ~bBx.onclick_selected
    if event == cv2.EVENT_MOUSEMOVE:
        if bBx.onclick_selected:
            bBx.currentBox = (bBx.currentBox[0], bBx.currentBox[1], x, y)

if __name__ == '__main__':
    main()
