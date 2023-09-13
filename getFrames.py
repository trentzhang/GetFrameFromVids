import cv2
import random
import os
import numpy as np
import re
import sys

def getVidsFrames(path):
    

vidPath = input("Please input video location:")
vidPath = vidPath.replace("'", "").replace("\\", "").rstrip()
print(vidPath)
if not os.path.exists(vidPath):
    print("file exists?", os.path.exists(vidPath), vidPath)
else:
    vidcap = cv2.VideoCapture(vidPath)
    # get total number of frames
    totalFrames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    n = 12
    FrameNumbers = random.sample(range(1, int(totalFrames)), n - 2)
    FrameNumbers += [0, int(totalFrames - 1)]

    imgs = []
    for i, FrameNumber in enumerate(np.linspace(0, int(totalFrames - 1), n, dtype=int)):
        # set frame position
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, FrameNumber)
        success = False
        while success == False:
            success, image = vidcap.read()
            FrameNumber = random.randint(0, int(totalFrames - 1))
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, FrameNumber)

        imgs.append(image)
        cv2.imwrite(f"/Users/trent/Downloads/pics/img-{i}.jpg", image)

    result = np.vstack(
        [np.hstack((imgs[i], imgs[i + 1], imgs[i + 2])) for i in range(0, n, 3)]
    )
    # result =
    cv2.imwrite(re.sub(r"\.[A-Za-z0-9]{3,5}$", "-fanart.jpg", vidPath), result)
    cv2.imwrite("/Users/trent/Downloads/img.jpg", result)
