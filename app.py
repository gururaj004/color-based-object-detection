
from flask import (
    Flask, render_template, request, jsonify,
    url_for, send_file, Response
)
import cv2
import numpy as np
import os
import uuid
import base64
import threading
import time

from detector import detect_objects
from colors import colour_ranges, box_colours


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024

RESULT_FOLDER = os.path.join("static", "results")
UPLOAD_FOLDER = os.path.join("static", "uploads")

os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

video_jobs = {}
video_jobs_lock = threading.Lock()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# IMAGE DETECTION
# --------------------------------------------------

@app.route("/detect-image", methods=["POST"])
def detect_image():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    selected_colour = request.form.get("colour", "red")

    if selected_colour not in colour_ranges:
        return jsonify({"error": "Invalid colour selected"}), 400

    image_bytes = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Invalid image file"}), 400

    output, mask, objects = detect_objects(frame, selected_colour)

    image_id = str(uuid.uuid4())

    output_path = os.path.join(
        RESULT_FOLDER, f"processed_{image_id}.jpg"
    )
    mask_path = os.path.join(
        RESULT_FOLDER, f"mask_{image_id}.png"
    )

    cv2.imwrite(output_path, output)
    cv2.imwrite(mask_path, mask)

    return jsonify({
        "success": True,
        "output": url_for(
            "static", filename=f"results/processed_{image_id}.jpg"
        ),
        "mask": url_for(
            "static", filename=f"results/mask_{image_id}.png"
        ),
        "count": len(objects),
        "objects": objects
    })


# --------------------------------------------------
# START VIDEO PROCESSING
# --------------------------------------------------

@app.route("/start-video", methods=["POST"])
def start_video():

    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    file = request.files["video"]
    selected_colour = request.form.get("colour", "red")

    if selected_colour not in colour_ranges:
        return jsonify({"error": "Invalid colour selected"}), 400

    if not file.filename:
        return jsonify({"error": "No video selected"}), 400

    extension = os.path.splitext(file.filename)[1].lower()

    allowed_extensions = {
        ".mp4", ".avi", ".mov", ".mkv", ".webm"
    }

    if extension not in allowed_extensions:
        return jsonify({"error": "Unsupported video format"}), 400

    job_id = str(uuid.uuid4())

    input_path = os.path.join(
        UPLOAD_FOLDER, f"input_{job_id}{extension}"
    )

    output_path = os.path.join(
        RESULT_FOLDER, f"processed_{job_id}.mp4"
    )

    mask_path = os.path.join(
        RESULT_FOLDER, f"mask_{job_id}.mp4"
    )

    file.save(input_path)

    job = {
        "input": input_path,
        "output": output_path,
        "mask": mask_path,
        "colour": selected_colour,
        "status": "waiting",
        "error": None,
        "frame": 0,
        "total_frames": 0,
        "count": 0,
        "max_objects": 0,
        "total_detections": 0,
        "progress": 0,
        "latest_output": None,
        "latest_mask": None,
        "sequence": 0,
        "cancel": threading.Event(),
        "lock": threading.Lock()
    }

    with video_jobs_lock:
        video_jobs[job_id] = job

    thread = threading.Thread(
        target=process_video,
        args=(job_id,),
        daemon=True
    )

    thread.start()

    return jsonify({
        "success": True,
        "job_id": job_id
    })


# --------------------------------------------------
# VIDEO PROCESSING BACKGROUND THREAD
# --------------------------------------------------

def process_video(job_id):

    job = video_jobs[job_id]

    cap = None
    output_writer = None
    mask_writer = None

    try:
        cap = cv2.VideoCapture(job["input"])

        if not cap.isOpened():
            raise RuntimeError("Unable to open uploaded video.")

        fps = cap.get(cv2.CAP_PROP_FPS)

        if not fps or fps <= 0:
            fps = 25

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width <= 0 or height <= 0:
            raise RuntimeError("Invalid video dimensions.")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        output_writer = cv2.VideoWriter(
            job["output"], fourcc, fps, (width, height)
        )

        mask_writer = cv2.VideoWriter(
            job["mask"], fourcc, fps, (width, height), False
        )

        if not output_writer.isOpened():
            raise RuntimeError("Could not create processed video.")

        if not mask_writer.isOpened():
            raise RuntimeError("Could not create mask video.")

        with job["lock"]:
            job["status"] = "processing"
            job["total_frames"] = total_frames

        missing_frames = 0
        tracking_text = ""

        while not job["cancel"].is_set():

            frame_start = time.time()

            ret, frame = cap.read()

            if not ret:
                break

            output, mask, objects = detect_objects(
                frame, job["colour"]
            )

            count = len(objects)

            if count > 0:
                largest_object = max(
                    objects, key=lambda item: item[4]
                )

                x, y, w, h, area = largest_object

                missing_frames = 0
                tracking_text = "Tracking..."

            else:
                missing_frames += 1

                if missing_frames <= 8:
                    tracking_text = "Tracking..."
                else:
                    tracking_text = ""

            if tracking_text:
                cv2.putText(
                    output,
                    tracking_text,
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            output_writer.write(output)

            # Ensure mask has the same dimensions as source video.
            if len(mask.shape) == 3:
                mask = cv2.cvtColor(
                    mask, cv2.COLOR_BGR2GRAY
                )

            if mask.shape[:2] != (height, width):
                mask = cv2.resize(mask, (width, height))

            mask_writer.write(mask)

            # Encode frames for live browser preview.
            success_out, output_buffer = cv2.imencode(
                ".jpg", output
            )

            success_mask, mask_buffer = cv2.imencode(
                ".jpg", cv2.cvtColor(
                    mask, cv2.COLOR_GRAY2BGR
                )
            )

            if success_out and success_mask:

                with job["lock"]:
                    job["latest_output"] = output_buffer.tobytes()
                    job["latest_mask"] = mask_buffer.tobytes()
                    job["sequence"] += 1

            with job["lock"]:
                job["frame"] += 1
                job["count"] = count
                job["max_objects"] = max(
                    job["max_objects"], count
                )
                job["total_detections"] += count

                if total_frames > 0:
                    job["progress"] = min(
                        99,
                        int(
                            job["frame"] / total_frames * 100
                        )
                    )

            # Keep processing close to the video's original FPS.
            elapsed = time.time() - frame_start
            remaining = max(0, (1 / fps) - elapsed)

            if job["cancel"].wait(remaining):
                break

    except Exception as error:

        with job["lock"]:
            job["status"] = "error"
            job["error"] = str(error)

    finally:

        # Release resources before marking the job completed.
        if cap is not None:
            cap.release()

        if output_writer is not None:
            output_writer.release()

        if mask_writer is not None:
            mask_writer.release()

        # Remove temporary uploaded video.
        try:
            if os.path.exists(job["input"]):
                os.remove(job["input"])
        except OSError:
            pass

        # Set final status only after video files are closed.
        with job["lock"]:

            if job["status"] != "error":

                if job["cancel"].is_set():
                    job["status"] = "stopped"

                elif job["frame"] == 0:
                    job["status"] = "error"
                    job["error"] = (
                        "The video contains no readable frames."
                    )

                else:
                    job["status"] = "completed"
                    job["progress"] = 100


# --------------------------------------------------
# LIVE VIDEO AND MASK STREAM
# --------------------------------------------------

@app.route("/video-stream/<job_id>/<kind>")
def video_stream(job_id, kind):

    if kind not in ("output", "mask"):
        return "Invalid stream type", 400

    with video_jobs_lock:
        job = video_jobs.get(job_id)

    if job is None:
        return "Video job not found", 404

    def generate():

        last_sequence = -1

        while True:

            with job["lock"]:
                sequence = job["sequence"]

                if kind == "output":
                    frame_data = job["latest_output"]
                else:
                    frame_data = job["latest_mask"]

                status = job["status"]

            if frame_data is not None and sequence != last_sequence:

                last_sequence = sequence

                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + frame_data
                    + b"\r\n"
                )

            elif status in ("completed", "stopped", "error"):
                break

            else:
                time.sleep(0.03)

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# --------------------------------------------------
# VIDEO PROGRESS
# --------------------------------------------------

@app.route("/video-progress/<job_id>")
def video_progress(job_id):

    with video_jobs_lock:
        job = video_jobs.get(job_id)

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    with job["lock"]:

        return jsonify({
            "status": job["status"],
            "error": job["error"],
            "frame": job["frame"],
            "total_frames": job["total_frames"],
            "count": job["count"],
            "max_objects": job["max_objects"],
            "total_detections": job["total_detections"],
            "progress": job["progress"]
        })


# --------------------------------------------------
# STOP VIDEO PROCESSING
# --------------------------------------------------

@app.route("/stop-video/<job_id>", methods=["POST"])
def stop_video(job_id):

    with video_jobs_lock:
        job = video_jobs.get(job_id)

    if job is None:
        return jsonify({"error": "Job not found"}), 404

    job["cancel"].set()

    return jsonify({
        "success": True,
        "message": "Video processing stopped."
    })


# --------------------------------------------------
# DOWNLOAD PROCESSED VIDEO / MASK
# --------------------------------------------------

@app.route("/video-result/<job_id>/<kind>")
def video_result(job_id, kind):

    with video_jobs_lock:
        job = video_jobs.get(job_id)

    if job is None:
        return "Video job not found", 404

    if kind == "output":
        path = job["output"]
        filename = "processed_video.mp4"

    elif kind == "mask":
        path = job["mask"]
        filename = "colour_mask.mp4"

    else:
        return "Invalid result type", 400

    with job["lock"]:
        if job["status"] != "completed":
            return "Video processing is not complete.", 409

    if not os.path.exists(path):
        return "Result file not found.", 404

    return send_file(
        path,
        as_attachment=True,
        download_name=filename
    )



# --------------------------------------------------
# WEBCAM DETECTION
# --------------------------------------------------

@app.route("/detect-frame", methods=["POST"])
def detect_frame():

    data = request.get_json(silent=True)

    if not data or "frame" not in data:
        return jsonify({"error": "No frame received"}), 400

    selected_colour = data.get("colour", "red")

    if selected_colour not in colour_ranges:
        return jsonify({"error": "Invalid colour selected"}), 400

    try:
        encoded_data = data["frame"].split(",", 1)[1]

        image_bytes = base64.b64decode(encoded_data)

        image_array = np.frombuffer(
            image_bytes, np.uint8
        )

        frame = cv2.imdecode(
            image_array, cv2.IMREAD_COLOR
        )

        if frame is None:
            return jsonify({"error": "Invalid frame"}), 400

        output, mask, objects = detect_objects(
            frame, selected_colour
        )

        # Convert mask to 3-channel image for JPEG encoding.
        if len(mask.shape) == 2:
            mask_display = cv2.cvtColor(
                mask, cv2.COLOR_GRAY2BGR
            )
        else:
            mask_display = mask

        success_out, output_buffer = cv2.imencode(
            ".jpg", output
        )

        success_mask, mask_buffer = cv2.imencode(
            ".jpg", mask_display
        )

        if not success_out or not success_mask:
            return jsonify({
                "error": "Frame encoding failed"
            }), 500

        output_base64 = base64.b64encode(
            output_buffer
        ).decode("utf-8")

        mask_base64 = base64.b64encode(
            mask_buffer
        ).decode("utf-8")

        return jsonify({
            "success": True,
            "output": output_base64,
            "mask": mask_base64,
            "count": len(objects),
            "objects": objects
        })

    except Exception as error:

        app.logger.exception("Webcam detection failed")

        return jsonify({
            "error": str(error)
        }), 500


# --------------------------------------------------
# FILE SIZE ERROR
# --------------------------------------------------

@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "error": "File is too large. Maximum upload size is 200 MB."
    }), 413


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        threaded=True
    )
