# Colour-Based Object Detection Using Python and OpenCV

A computer vision application that detects and identifies objects based on their colour using Python and OpenCV.

The application supports image processing, video processing, and real-time webcam detection. Users can select a target colour, and the system identifies matching objects using HSV colour segmentation, contour detection, and image-processing techniques.

## Features

- Colour-based object detection
- Supports 11 different colours
- Image detection and processing
- Video detection frame by frame
- Real-time webcam detection
- Automatic object counting
- Bounding boxes around detected objects
- Detection mask visualization
- Brightness normalization using CLAHE
- Noise reduction using morphological operations
- Temporary object tracking when detection briefly disappears
- Supports common image and video formats
- Web-based interface for accessing detection features

## Technologies Used

- **Python** – Core programming language
- **OpenCV** – Image and video processing
- **NumPy** – Numerical and array operations
- **Flask** – Web application and backend
- **HTML, CSS, JavaScript** – Frontend interface
- **Tkinter** – Desktop file selection interface

## Supported Detection Colours

The application supports the following colours:

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

### 1. Image Detection

- Select an image from your computer.
- Choose the target colour.
- Detect matching objects.
- View the processed image and detection mask.

### 2. Video Detection

- Upload or select a video file.
- Process the video frame by frame.
- Detect and count objects matching the selected colour.
- View the detection results.

### 3. Real-Time Webcam Detection

- Access your computer's webcam.
- Process live video frames.
- Detect objects based on the selected colour.
- Display bounding boxes, object counts, and detection masks in real time.

## How It Works

The detection process follows these steps:

1. Capture an image, video frame, or webcam frame.
2. Normalize image brightness using CLAHE.
3. Convert the image from BGR to HSV colour space.
4. Apply colour thresholding using predefined HSV ranges.
5. Perform morphological operations to remove unwanted noise.
6. Detect contours of the selected colour.
7. Filter out small unwanted regions based on area.
8. Draw bounding boxes around detected objects.
9. Count the detected objects.
10. Generate and display the processed output and binary detection mask.

## Project Structure

```text
colour-based-object-detection/
│
├── app.py
├── main.py
├── detector.py
├── colors.py
├── display.py
├── file_selector.py
├── image_mode.py
├── video_mode.py
├── webcam_mode.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   ├── uploads/
│   └── results/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/gururaj004/color-based-object-detection.git
```

### 2. Navigate to the Project Directory

```bash
cd color-based-object-detection
```

### 3. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## Deployment

The Flask application can be deployed using a cloud hosting platform such as Render.

**Live Application:** Add your deployed application URL here after deployment.

## Future Improvements

- Improve detection accuracy under different lighting conditions.
- Add support for custom colour selection.
- Improve object tracking across video frames.
- Optimize processing performance for real-time applications.
- Add additional computer vision features.

## Author

**Gururaj**

GitHub: [@gururaj004](https://github.com/gururaj004)

---

If you find this project useful, consider giving the repository a star!