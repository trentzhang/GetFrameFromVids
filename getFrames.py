import cv2
import random
import os
import numpy as np
import re
import sys


# Define a list of common video file extensions
video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".mpeg", ".mpg"]


class getVidsFrames:
    def __init__(self, path, n=16, debug=False):
        self.path = path
        self.n = n
        self.debug = debug

    def layout(self, n: int):
        nrow = int(np.round(np.sqrt(n)))
        ncol = int(np.ceil(n / nrow))
        return nrow, ncol

    def stackImgs(self, images, nrow, ncol):
        # Create an empty canvas to stack the images
        canvas = np.zeros(
            (nrow * images[0].shape[0], ncol * images[0].shape[1], images[0].shape[2]),
            dtype=np.uint8,
        )

        # Iterate through the images and place them on the canvas
        for i, img in enumerate(images):
            row_idx = i // ncol
            col_idx = i % ncol
            x_start = col_idx * img.shape[1]
            x_end = (col_idx + 1) * img.shape[1]
            y_start = row_idx * img.shape[0]
            y_end = (row_idx + 1) * img.shape[0]

            canvas[y_start:y_end, x_start:x_end, :] = img
        return canvas

    def getImages(self, cap):
        # get total number of frames
        totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        quantile_indices = [int(i * (totalFrames - 1) / 15) for i in range(16)]

        frames = []
        for index in quantile_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        return frames

    def getFileThumnail(self, path):
        parpath, filename = os.path.split(path)
        filename, _ = os.path.splitext(filename)

        # Check if the thumnailsDir directory exists; if not, create it
        thumnailsDir = os.path.join(parpath, "Thumnails")
        if not os.path.exists(thumnailsDir):
            os.makedirs(thumnailsDir)

        thumnailpath = os.path.join(parpath, "Thumnails", f"{filename}.png")
        # generate thumbnail only if thumbnail doesn't exist and video file is open
        cap = cv2.VideoCapture(path)
        if not os.path.exists(thumnailpath) and cap.isOpened():
            imgs = self.getImages(cap)
            nrow, ncol = self.layout(self.n)
            result = self.stackImgs(imgs, nrow, ncol)

            cv2.imwrite(
                thumnailpath,
                self.compressImage(result),
            )
        cap.release()

    def compressImage(self, original_array, max_dim_size=2000):
        if original_array.shape[0] < 2000 and original_array.shape[1] < 2000:
            return original_array

        scale_factor = min(
            max_dim_size / original_array.shape[0],
            max_dim_size / original_array.shape[1],
        )

        # Calculate the new shape
        new_height = int(original_array.shape[0] * scale_factor)
        new_width = int(original_array.shape[1] * scale_factor)

        # Downsample the original array
        downsampled_array = cv2.resize(
            original_array, (new_width, new_height), interpolation=cv2.INTER_AREA
        )
        return downsampled_array

    def run(self):
        path = os.path.normpath(self.path.replace(r"\ ", " ").replace("'", ""))
        if os.path.exists(path):
            if os.path.isfile(path):
                print(f"{path} is a file.")
                self.getFileThumnail(path)
            elif os.path.isdir(path):
                print(f"{path} is a directory.")
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_extension = os.path.splitext(file_path)[1].lower()

                        # Check if the file extension is in the list of video extensions
                        if file_extension in video_extensions and not os.path.basename(
                            file
                        ).startswith("."):
                            self.getFileThumnail(file_path)
                            print(f"Generated thumnails for '{file_path}'.")
        else:
            print(f"{path} does not exist.")


# path = input("Please input video location:")
# getVidsFrames(path).run()


import cProfile


def main():
    path = input("Please input video location:")
    getVidsFrames(path).run()


if __name__ == "__main__":
    # Profile the main() function
    # cProfile.run("main()")
    main()
