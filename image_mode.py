import cv2
from detector import detect_objects
from display import show_windows
from file_selector import select_file


def process_image(selected_colour):
    print("\nSelect an image...")
    file_path = select_file("image")

    if not file_path:
        print("No image selected.")
        return

    image = cv2.imread(file_path)

    if image is None:
        print("Unable to open image.")
        return

    output, mask, objects = detect_objects(
        image, selected_colour
    )

    print(f"\nObjects detected: {len(objects)}")

    show_windows(
        output, mask, "Colour Object Detection - Image"
    )

    print("\nPress any key on the window to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()