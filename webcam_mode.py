import cv2
from colors import box_colours
from detector import detect_objects
from display import show_windows


def process_webcam(selected_colour):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to access webcam.")
        return

    last_box = None
    missing_frames = 0
    MAX_MISSING_FRAMES = 8

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        output, mask, objects = detect_objects(
            frame, selected_colour
        )

        if len(objects) > 0:
            x, y, w, h, area = objects[0]
            last_box = (x, y, w, h)
            missing_frames = 0
        else:
            missing_frames += 1

        if (
            len(objects) == 0
            and last_box is not None
            and missing_frames <= MAX_MISSING_FRAMES
        ):
            x, y, w, h = last_box
            colour = box_colours[selected_colour]

            cv2.rectangle(
                output, (x, y), (x + w, y + h), colour, 3
            )

            cv2.putText(
                output,
                "Tracking...",
                (x, max(y - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                colour,
                2
            )

        elif missing_frames > MAX_MISSING_FRAMES:
            last_box = None

        show_windows(
            output, mask, "Colour Object Detection - Webcam"
        )

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()