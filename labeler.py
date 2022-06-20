import cv2
import json
import os
from jsonloader import JSONLoader, VideoLoader, BoundingBoxes

increment_frame = 50

def init_directories():
    if not os.path.exists('data'):
            os.makedirs('data')
    if not os.path.exists('data/photos'):
            os.makedirs('data/photos')
    if not os.path.isfile('data/label.json'):
        with open('data/label.json', 'w') as json_file:
            json.dump({}, json_file)

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
        if not bBx.onclick_selected:
            print('Selected')
            bBx.currentBox = (x, y, x, y)
        else:
            print('Unselected')
            bBx.finishCurrentBox()
        bBx.onclick_selected = ~bBx.onclick_selected
    if event == cv2.EVENT_MOUSEMOVE:
        if bBx.onclick_selected:
            bBx.currentBox = (bBx.currentBox[0], bBx.currentBox[1], x, y)

if __name__ == '__main__':
    main()
