#getting all the libraries
import imageio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from skimage import color, filters


def get_intensity_along_line(image, x1, y1, x2, y2):
    # Get line points
    x, y = np.linspace(x1, x2, num=100), np.linspace(y1, y2, num=100)
    z = image[np.round(y).astype(int), np.round(x).astype(int)]

    return x, y, z


def onclick(event):
    global x, y
    x.append(event.xdata)
    y.append(event.ydata)
    if len(x) == 2:
        # Get the intensity along the line defined by the selected points
        x, y, z = get_intensity_along_line(gray_image, x[0], y[0], x[1], y[1])

        # Binarize the image using Otsu's method
        binary_image = filters.apply_hysteresis_threshold(gray_image, z.mean() - 0.1, z.mean() + 0.1)

        # Get the line points in the binary image
        bx, by = np.round(x).astype(int), np.round(y).astype(int)
        bz = binary_image[by, bx]

        # Set the intensity to 1 where the hand is present, and 0 elsewhere
        z = bz.astype(float)

        # Check if there is a hand in the image
        if np.count_nonzero(z) > 0:
            print("Hand detected!")
        else:
            print("No hand detected.")

        # Plot the intensity along the line
        fig, ax = plt.subplots()
        ax.plot(z)

        plt.show()


# Read the image
image = imageio.imread("biometrics.jpeg")

# Convert the image to grayscale
gray_image = color.rgb2gray(image)

# Plot the image
fig, ax = plt.subplots()
ax.imshow(gray_image, cmap='gray')

cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

x, y = [], []

plt.connect('button_press_event', onclick)

plt.show()
