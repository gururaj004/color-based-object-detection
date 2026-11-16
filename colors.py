import numpy as np 

colour_ranges = {
    "red": [
        (np.array([0, 100, 50]), np.array([10, 255, 255])),
        (np.array([170, 100, 50]), np.array([179, 255, 255]))
    ],
    "orange": [(np.array([10, 100, 50]), np.array([20, 255, 255]))],
    "yellow": [(np.array([20, 100, 50]), np.array([35, 255, 255]))],
    "green": [(np.array([35, 50, 50]), np.array([85, 255, 255]))],
    "cyan": [(np.array([85, 50, 50]), np.array([95, 255, 255]))],
    "blue": [(np.array([95, 50, 50]), np.array([135, 255, 255]))],
    "purple": [(np.array([135, 50, 50]), np.array([160, 255, 255]))],
    "pink": [(np.array([160, 50, 50]), np.array([170, 255, 255]))],
    "white": [(np.array([0, 0, 180]), np.array([179, 60, 255]))],
    "black": [(np.array([0, 0, 0]), np.array([179, 255, 60]))],
    "gray": [(np.array([0, 0, 60]), np.array([179, 50, 180]))]
}

box_colours = {
    "red": (0, 0, 255),
    "orange": (0, 165, 255),
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "cyan": (255, 255, 0),
    "blue": (255, 0, 0),
    "purple": (255, 0, 255),
    "pink": (203, 192, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (128, 128, 128)
}