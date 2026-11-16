from image_mode import process_image
from video_mode import process_video
from webcam_mode import process_webcam


colours = [
    "red", "orange", "yellow", "green", "cyan",
    "blue", "purple", "pink", "white", "black", "gray"
]


def main():
    print("\n===================================")
    print(" COLOUR BASED OBJECT DETECTION")
    print("===================================")

    # Colour selection
    print("\nAvailable Colours:")
    for i, colour in enumerate(colours, start=1):
        print(f"{i}. {colour.capitalize()}")

    colour_choice = input(
        "\nEnter colour name or number: "
    ).strip().lower()

    if colour_choice.isdigit():
        number = int(colour_choice)
        if 1 <= number <= len(colours):
            selected_colour = colours[number - 1]
        else:
            print("Invalid colour choice!")
            return
    elif colour_choice in colours:
        selected_colour = colour_choice
    else:
        print("Invalid colour! Please enter a valid colour name or number.")
        return

    print(f"\nSelected Colour: {selected_colour.upper()}")

    # Input mode selection
    print("\nSelect Input Mode:")
    print("1. Image Detection")
    print("2. Video Detection")
    print("3. Webcam Detection")

    mode = input(
        "\nEnter your choice (number or word): "
    ).strip().lower()

    if mode in ["1", "image", "photo", "picture"]:
        process_image(selected_colour)

    elif mode in ["2", "video", "movie", "clip"]:
        process_video(selected_colour)

    elif mode in ["3", "webcam", "camera", "cam"]:
        process_webcam(selected_colour)

    else:
        print("Invalid mode! Enter 1/image, 2/video, or 3/webcam.")


if __name__ == "__main__":
    main()