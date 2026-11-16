# Colour-Based Object Detection Using Python

A computer vision project that detects and identifies objects based on their colour using Python and OpenCV.

The system can process images, videos, and live webcam input. Users can select a target colour, and the system detects objects matching that colour using HSV colour segmentation.

## Features

- Detect objects based on selected colour
- Supports multiple colours
- Image detection
- Video detection
- Real-time webcam detection
- Object counting
- Bounding boxes around detected objects
- Detection mask visualization
- Brightness normalization using CLAHE
- Noise removal using morphological operations
- Temporary object tracking when detection briefly disappears
- Supports common image and video formats

## Technologies Used

- Python
- OpenCV
- NumPy
- Tkinter

## Detection Colours

The system supports:

- Red
- Orange
- Yellow
- Green
- Cyan
- Blue
- Purple
- Pink
- White
- Black
- Gray

## Input Modes

### 1. Image

Select an image from your computer.

The system processes the image and detects objects matching the selected colour.

### 2. Video

Select a video file from your computer.

The system processes the video frame by frame and detects objects based on the selected colour.

### 3. Webcam

Use the computer's webcam for real-time colour-based object detection.

## How It Works

The project follows these main steps:

1. Capture an image, video frame, or webcam frame.
2. Normalize the brightness of the frame.
3. Convert the image from BGR colour space to HSV.
4. Apply colour thresholding using predefined HSV ranges.
5. Perform morphological operations to remove noise.
6. Detect contours of the selected colour.
7. Filter small unwanted regions.
8. Draw bounding boxes around detected objects.
9. Count the detected objects.
10. Display the detection result and binary mask.

