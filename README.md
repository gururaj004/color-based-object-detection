# Colour-Based Object Detection Using Python and OpenCV

A computer vision application that detects and identifies objects based on their colour using Python and OpenCV.

The application supports image processing, video processing, and real-time webcam detection. Users can select a target colour, and the system identifies matching objects using HSV colour segmentation and image-processing techniques.

## Live Demo

**Try the application here:**

🌐 https://color-based-object-detection.onrender.com

The application is hosted on Render and can be accessed through a web browser.

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
- Web-based interface

## Technologies Used

- **Python** – Core programming language
- **OpenCV** – Image and video processing
- **NumPy** – Numerical and array operations
- **Flask** – Backend web framework
- **HTML, CSS, JavaScript** – Frontend development
- **Tkinter** – Desktop file selection interface
- **Render** – Cloud deployment

## Supported Detection Colours

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

- Upload an image from your device.
- Select the target colour.
- Detect matching objects.
- View the processed image and detection mask.

### 2. Video Detection

- Select or upload a video file.
- Process the video frame by frame.
- Detect objects matching the selected colour.
- View the detection results and object count.

### 3. Real-Time Webcam Detection

- Access your device's webcam.
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

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

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

Open your browser and visit:

```text
http://127.0.0.1:5000
```

## Deployment

The Flask application is deployed using **Render**.

**Live Application:** https://color-based-object-detection.onrender.com

## Future Improvements

- Improve detection accuracy under different lighting conditions.
- Add custom colour selection.
- Improve object tracking across video frames.
- Optimize processing performance for real-time applications.
- Introduce additional computer vision features.

## Author

**Gururaj**

GitHub: https://github.com/gururaj004

---

If you find this project useful, consider giving the repository a ⭐!
