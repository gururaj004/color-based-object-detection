import cv2


def show_windows(output, mask, output_title):
    display_width = 800
    display_height = 600

    output_display = cv2.resize(
        output, (display_width, display_height)
    )

    mask_display = cv2.resize(
        mask, (display_width, display_height)
    )

    cv2.namedWindow(output_title, cv2.WINDOW_NORMAL)
    cv2.namedWindow("Detection Mask", cv2.WINDOW_NORMAL)

    cv2.resizeWindow(
        output_title, display_width, display_height
    )
    cv2.resizeWindow(
        "Detection Mask", display_width, display_height
    )

    cv2.moveWindow(output_title, 20, 50)
    cv2.moveWindow("Detection Mask", 840, 50)

    cv2.imshow(output_title, output_display)
    cv2.imshow("Detection Mask", mask_display)