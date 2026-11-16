
const modeCards = document.querySelectorAll(".mode-card");

const colours = [
    { name: "Red", value: "#EF4444" },
    { name: "Orange", value: "#F97316" },
    { name: "Yellow", value: "#EAB308" },
    { name: "Green", value: "#22C55E" },
    { name: "Cyan", value: "#06B6D4" },
    { name: "Blue", value: "#3B82F6" },
    { name: "Purple", value: "#A855F7" },
    { name: "Pink", value: "#EC4899" },
    { name: "White", value: "#FFFFFF" },
    { name: "Black", value: "#555555" },
    { name: "Gray", value: "#9CA3AF" }
];

let selectedMode = "image";
let selectedColour = "red";

const fileInput = document.getElementById("fileInput");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");

const outputPreview = document.getElementById("outputPreview");
const maskPreview = document.getElementById("maskPreview");
const resultInfo = document.getElementById("resultInfo");

const uploadHint = document.getElementById("uploadHint");
const webcamVideo = document.getElementById("webcamVideo");
const systemStatus = document.getElementById("systemStatus");
const downloadArea = document.getElementById("downloadArea");

const videoLivePanel = document.getElementById("videoLivePanel");
const liveFrame = document.getElementById("liveFrame");
const liveCount = document.getElementById("liveCount");
const liveTotal = document.getElementById("liveTotal");
const liveMaximum = document.getElementById("liveMaximum");
const livePercentage = document.getElementById("livePercentage");
const liveProgressBar = document.getElementById("liveProgressBar");
const videoProcessingStatus = document.getElementById("videoProcessingStatus");
const finalVideoArea = document.getElementById("finalVideoArea");

let webcamStream = null;
let webcamActive = false;
let webcamRequestInProgress = false;

let currentVideoJobId = null;
let videoPollingActive = false;

let imageAbortController = null;


// --------------------------------
// COLOUR SELECTION
// --------------------------------

const colourContainer = document.getElementById("colourOptions");

colours.forEach(colour => {

    const button = document.createElement("button");

    button.className = "colour-option";

    if (colour.name.toLowerCase() === selectedColour) {
        button.classList.add("selected");
    }

    button.innerHTML = `
        <span class="colour-circle"
              style="background-color: ${colour.value}">
        </span>
        <span>${colour.name}</span>
    `;

    button.addEventListener("click", () => {

        document.querySelectorAll(".colour-option").forEach(item => {
            item.classList.remove("selected");
        });

        button.classList.add("selected");
        selectedColour = colour.name.toLowerCase();

    });

    colourContainer.appendChild(button);
});


// --------------------------------
// COMMON HELPERS
// --------------------------------

function setStatus(message) {
    systemStatus.textContent = message;
}

function setPreviewMessage(message) {
    outputPreview.textContent = message;
    maskPreview.textContent = "No mask available.";
}

function clearDownloads() {
    downloadArea.innerHTML = "";
    finalVideoArea.innerHTML = "";
}

function resetVideoProgress() {

    videoLivePanel.style.display = "none";

    liveFrame.textContent = "0 / 0";
    liveCount.textContent = "0";
    liveTotal.textContent = "0";
    liveMaximum.textContent = "0";

    livePercentage.textContent = "0%";
    liveProgressBar.style.width = "0%";

    videoProcessingStatus.textContent = "Waiting for video...";
}


// --------------------------------
// IMAGE STOP
// --------------------------------

function stopImageDetection() {

    if (imageAbortController) {

        const controller = imageAbortController;

        imageAbortController = null;

        controller.abort();
    }
}


// --------------------------------
// WEBCAM STOP
// --------------------------------

function stopWebcam() {

    webcamActive = false;
    webcamRequestInProgress = false;

    if (webcamStream) {

        webcamStream.getTracks().forEach(track => {
            track.stop();
        });

        webcamStream = null;
    }

    webcamVideo.srcObject = null;
    webcamVideo.hidden = true;
}


// --------------------------------
// VIDEO STOP
// --------------------------------

async function stopVideoProcessing() {

    videoPollingActive = false;

    const jobId = currentVideoJobId;

    const liveOutput = outputPreview.querySelector("img");
    const liveMask = maskPreview.querySelector("img");

    if (liveOutput) {
        liveOutput.src = "";
    }

    if (liveMask) {
        liveMask.src = "";
    }

    if (jobId) {

        try {

            await fetch(`/stop-video/${jobId}`, {
                method: "POST"
            });

        } catch (error) {
            console.error("Unable to stop video:", error);
        }
    }

    currentVideoJobId = null;
}


// --------------------------------
// STOP CURRENT TASK
// --------------------------------

async function stopCurrentTask() {

    stopImageDetection();
    stopWebcam();

    if (currentVideoJobId) {
        await stopVideoProcessing();
    } else {
        videoPollingActive = false;
    }
}


// --------------------------------
// MODE SELECTION
// --------------------------------

function updateInputMode() {

    stopCurrentTask();

    fileInput.value = "";
    fileInput.disabled = selectedMode === "webcam";

    webcamVideo.hidden = true;

    clearDownloads();
    resetVideoProgress();

    if (selectedMode === "image") {

        fileInput.accept = "image/*";

        uploadHint.textContent =
            "Supported formats: JPG, JPEG, PNG, WEBP";

        resultInfo.textContent =
            "Upload an image and select a colour.";

    } else if (selectedMode === "video") {

        fileInput.accept =
            "video/mp4,video/avi,video/quicktime,video/x-matroska,video/webm,video/x-m4v,video/x-ms-wmv";

        uploadHint.textContent =
            "Supported formats: MP4, AVI, MOV, MKV, WEBM, M4V, WMV";

        resultInfo.textContent =
            "Upload a video and select a colour.";

    } else {

        fileInput.accept = "";

        uploadHint.textContent =
            "Allow camera access when your browser asks for permission.";

        resultInfo.textContent =
            "Press Start Detection to activate your webcam.";
    }

    setPreviewMessage("Your detection output will appear here.");

    setStatus("System Ready");

    startBtn.disabled = false;
    startBtn.textContent = "Start Detection";

    stopBtn.disabled = true;
}


modeCards.forEach(card => {

    card.addEventListener("click", () => {

        modeCards.forEach(item => item.classList.remove("active"));

        card.classList.add("active");

        selectedMode = card.dataset.mode;

        updateInputMode();
    });
});


// --------------------------------
// FILE SELECTION
// --------------------------------

fileInput.addEventListener("change", () => {

    const file = fileInput.files[0];

    if (file) {

        resultInfo.textContent = `Selected: ${file.name}`;

        clearDownloads();
        resetVideoProgress();
    }

});


// --------------------------------
// IMAGE DETECTION
// --------------------------------

async function detectImage() {

    const file = fileInput.files[0];

    if (!file) {
        resultInfo.textContent = "Please select an image first.";
        return;
    }

    const formData = new FormData();

    formData.append("image", file);
    formData.append("colour", selectedColour);

    const controller = new AbortController();

    imageAbortController = controller;

    startBtn.disabled = true;
    stopBtn.disabled = false;

    startBtn.textContent = "Processing...";

    resultInfo.textContent = "Detecting objects...";
    setStatus("Processing Image");

    try {

        const response = await fetch("/detect-image", {
            method: "POST",
            body: formData,
            signal: controller.signal
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Image detection failed.");
        }

        if (controller.signal.aborted) return;

        // Flask returns image URLs for image detection.
        outputPreview.innerHTML = `
            <img
                src="${data.output}"
                alt="Detection Output"
                style="width:100%; height:auto; display:block;"
            >
        `;

        maskPreview.innerHTML = `
            <img
                src="${data.mask}"
                alt="Detection Mask"
                style="width:100%; height:auto; display:block;"
            >
        `;

        resultInfo.textContent =
            `Successfully detected ${data.count} object(s) of ${selectedColour.toUpperCase()} colour.`;

        setStatus("Image Detection Complete");

    } catch (error) {

        if (error.name === "AbortError") {

            resultInfo.textContent = "Image detection stopped.";
            setStatus("Detection Stopped");

        } else {

            resultInfo.textContent = error.message;
            setStatus("Error");
        }

    } finally {

        if (imageAbortController === controller) {

            imageAbortController = null;

            startBtn.disabled = false;
            startBtn.textContent = "Start Detection";

            stopBtn.disabled = true;
        }
    }
}


// --------------------------------
// LIVE VIDEO DETECTION
// --------------------------------

async function detectVideo() {

    const file = fileInput.files[0];

    if (!file) {

        resultInfo.textContent = "Please select a video first.";
        videoPollingActive = false;
        return;
    }

    const formData = new FormData();

    formData.append("video", file);
    formData.append("colour", selectedColour);

    startBtn.disabled = true;
    stopBtn.disabled = false;

    startBtn.textContent = "Processing Video...";

    resultInfo.textContent =
        "Uploading video and starting live detection...";

    setStatus("Starting Video Detection");

    clearDownloads();
    resetVideoProgress();

    try {

        const response = await fetch("/start-video", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to start video detection.");
        }

        const jobId = data.job_id;

        if (!videoPollingActive) {

            await fetch(`/stop-video/${jobId}`, {
                method: "POST"
            });

            return;
        }

        currentVideoJobId = jobId;

        videoLivePanel.style.display = "block";

        outputPreview.innerHTML = `
            <img
                src="/video-stream/${jobId}/output"
                alt="Live Detection Output"
                style="width:100%; height:auto;"
            >
        `;

        maskPreview.innerHTML = `
            <img
                src="/video-stream/${jobId}/mask"
                alt="Live Detection Mask"
                style="width:100%; height:auto;"
            >
        `;

        resultInfo.textContent =
            "Live video detection is running...";

        setStatus("Video Detection Active");

        while (videoPollingActive) {

            await new Promise(resolve => setTimeout(resolve, 250));

            if (!videoPollingActive) break;

            const progressResponse = await fetch(
                `/video-progress/${jobId}`
            );

            const progress = await progressResponse.json();

            if (!progressResponse.ok) {
                throw new Error(
                    progress.error || "Unable to get video progress."
                );
            }

            if (!videoPollingActive) break;

            liveFrame.textContent =
                `${progress.frame} / ${progress.total_frames}`;

            liveCount.textContent = progress.count;
            liveTotal.textContent = progress.total_detections;
            liveMaximum.textContent = progress.max_objects;

            livePercentage.textContent =
                `${progress.progress}%`;

            liveProgressBar.style.width =
                `${progress.progress}%`;

            if (progress.status === "processing") {

                videoProcessingStatus.textContent =
                    `Processing frame ${progress.frame}...`;
            }

            if (progress.status === "error") {
                throw new Error(progress.error || "Video processing failed.");
            }

            if (progress.status === "stopped") {

                videoPollingActive = false;

                videoProcessingStatus.textContent =
                    "Video processing stopped.";

                resultInfo.textContent =
                    "Video processing was stopped.";

                setStatus("Video Stopped");

                break;
            }

            if (progress.status === "completed") {

                videoPollingActive = false;

                videoProcessingStatus.textContent =
                    "Video detection completed successfully!";

                const outputUrl =
                    `/static/results/processed_${jobId}.mp4`;

                finalVideoArea.innerHTML = `
                    <h3>Final Processed Video</h3>

                    <video controls playsinline preload="metadata"
                           style="width:100%; max-width:750px;">
                        <source src="${outputUrl}" type="video/mp4">
                        Your browser cannot play this video.
                    </video>
                `;

                downloadArea.innerHTML = `
                    <a class="download-btn"
                       href="/video-result/${jobId}/output"
                       download="processed_video.mp4">
                       Download Detection Video
                    </a>

                    <a class="download-btn secondary-download"
                       href="/video-result/${jobId}/mask"
                       download="detection_mask.mp4">
                       Download Mask Video
                    </a>
                `;

                resultInfo.textContent =
                    `Video processed successfully! Frames: ${progress.frame} | Maximum objects in one frame: ${progress.max_objects} | Total frame detections: ${progress.total_detections} | Colour: ${selectedColour.toUpperCase()}`;

                setStatus("Video Detection Complete");

                break;
            }
        }

    } catch (error) {

        if (videoPollingActive) {

            resultInfo.textContent = error.message;

            videoProcessingStatus.textContent =
                "Video detection failed.";

            setStatus("Error");
        }

    } finally {

        videoPollingActive = false;
        currentVideoJobId = null;

        startBtn.disabled = false;
        startBtn.textContent = "Start Detection";

        stopBtn.disabled = true;
    }
}


// --------------------------------
// WEBCAM DETECTION
// --------------------------------

async function startWebcam() {

    try {

        webcamStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "environment",
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        });

        webcamVideo.srcObject = webcamStream;
        webcamVideo.hidden = false;

        await webcamVideo.play();

        webcamActive = true;

        startBtn.disabled = true;
        startBtn.textContent = "Camera Running";

        stopBtn.disabled = false;

        resultInfo.textContent =
            "Live webcam detection is running.";

        setStatus("Webcam Active");

        processWebcamFrame();

    } catch (error) {

        stopWebcam();

        resultInfo.textContent =
            "Unable to access webcam. Allow camera permission and try again. " +
            error.message;

        setStatus("Camera Unavailable");

        startBtn.disabled = false;
        startBtn.textContent = "Start Detection";

        stopBtn.disabled = true;
    }
}


async function processWebcamFrame() {

    if (!webcamActive || webcamRequestInProgress) {
        return;
    }

    if (
        !webcamVideo.videoWidth ||
        !webcamVideo.videoHeight
    ) {
        setTimeout(processWebcamFrame, 200);
        return;
    }

    webcamRequestInProgress = true;

    const canvas = document.createElement("canvas");

    const scale = Math.min(
        1,
        640 / webcamVideo.videoWidth
    );

    canvas.width = Math.round(webcamVideo.videoWidth * scale);
    canvas.height = Math.round(webcamVideo.videoHeight * scale);

    const context = canvas.getContext("2d");

    context.drawImage(
        webcamVideo,
        0,
        0,
        canvas.width,
        canvas.height
    );

    const frame = canvas.toDataURL("image/jpeg", 0.75);

    try {

        const response = await fetch("/detect-frame", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                frame: frame,
                colour: selectedColour
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Webcam detection failed.");
        }

        if (!webcamActive) {
            return;
        }

        if (!data.output || !data.mask) {
            throw new Error("Processed frame or mask was not returned by Flask.");
        }

        // Flask returns Base64 strings for webcam frames.
      outputPreview.innerHTML = `
    <img
        src="data:image/jpeg;base64,${data.output}"
        alt="Live Detection Output"
        style="width:100%; height:auto; display:block;"
    >
`;
      maskPreview.innerHTML = `
    <img
        src="data:image/jpeg;base64,${data.mask}"
        alt="Live Detection Mask"
        style="width:100%; height:auto; display:block;"
    >
`;
        resultInfo.textContent =
            `Live detection: ${data.count} ${selectedColour.toUpperCase()} object(s) detected.`;

    } catch (error) {

        if (webcamActive) {
            resultInfo.textContent = error.message;
            console.error("Webcam processing error:", error);
        }

    } finally {

        webcamRequestInProgress = false;

        if (webcamActive) {
            setTimeout(processWebcamFrame, 150);
        }
    }
}


// --------------------------------
// START DETECTION
// --------------------------------

startBtn.addEventListener("click", () => {

    if (selectedMode === "image") {

        detectImage();

    } else if (selectedMode === "video") {

        videoPollingActive = true;
        detectVideo();

    } else if (selectedMode === "webcam") {

        startWebcam();

    }
});


// --------------------------------
// STOP DETECTION
// --------------------------------

stopBtn.addEventListener("click", async () => {

    stopBtn.disabled = true;

    if (selectedMode === "image") {

        stopImageDetection();

        resultInfo.textContent =
            "Image detection stopped.";

        setStatus("Detection Stopped");

        startBtn.disabled = false;
        startBtn.textContent = "Start Detection";

    } else if (selectedMode === "video") {

        videoProcessingStatus.textContent =
            "Stopping video processing...";

        resultInfo.textContent =
            "Stopping video detection...";

        await stopVideoProcessing();

        videoProcessingStatus.textContent =
            "Video processing stopped.";

        resultInfo.textContent =
            "Video detection stopped.";

        setStatus("Detection Stopped");

        startBtn.disabled = false;
        startBtn.textContent = "Start Detection";

    } else if (selectedMode === "webcam") {

        stopWebcam();

        resultInfo.textContent =
            "Webcam detection stopped.";

        setStatus("Detection Stopped");

        startBtn.disabled = false;
        startBtn.textContent = "Start Detection";
    }

    stopBtn.disabled = true;
});


// --------------------------------
// INITIALIZE
// --------------------------------

stopBtn.disabled = true;
resetVideoProgress();
