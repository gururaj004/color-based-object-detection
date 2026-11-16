
import cv2
import numpy as np
from colors import colour_ranges, box_colours


def normalize_brightness(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=1.0,
        tileGridSize=(8, 8)
    )

    l_channel = clahe.apply(l_channel)
    lab = cv2.merge((l_channel, a_channel, b_channel))

    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def detect_objects(frame, selected_colour):

    original = frame.copy()

    processed = normalize_brightness(original)

    hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)

    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for lower, upper in colour_ranges[selected_colour]:
        current_mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.bitwise_or(mask, current_mask)

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_OPEN, kernel
    )

    mask = cv2.morphologyEx(
        mask, cv2.MORPH_CLOSE, kernel
    )

    mask = cv2.dilate(
        mask, kernel, iterations=1
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detected_objects = []
    MIN_AREA = 800

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < MIN_AREA:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        if w < 20 or h < 20:
            continue

        detected_objects.append((x, y, w, h, area))

    detected_objects.sort(
        key=lambda obj: obj[4],
        reverse=True
    )

    output = processed.copy()
    colour = box_colours[selected_colour]

    for index, (x, y, w, h, area) in enumerate(
        detected_objects, start=1
    ):
        cv2.rectangle(
            output, (x, y), (x + w, y + h), colour, 3
        )

        cv2.putText(
            output,
            f"Object {index}",
            (x, max(y - 8, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            colour,
            1
        )

    count = len(detected_objects)

    cv2.rectangle(
        output, (10, 10), (350, 70), (0, 0, 0), -1
    )

    cv2.putText(
        output,
        f"Colour: {selected_colour.upper()}",
        (18, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        1
    )

    cv2.putText(
        output,
        f"Objects Detected: {count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    return output, mask, detected_objects
