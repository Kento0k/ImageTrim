import cv2
import matplotlib.pyplot as plt
import math


def build_hist(values, width, left, right):
    hist = [0] * width
    for line in values:
        for element in line:
            if element < left:
                continue
            if element > right:
                continue
            hist[element] += 1
    return hist


def trim_hist(original_hist, percent):
    left = 0
    right = 255
    total_space = sum(original_hist)
    new_space = total_space
    print(new_space / total_space)
    while True:
        left += 1
        new_space = sum(original_hist[left:right])
        print(new_space / total_space)
        print(str(left) + " - " + str(right))
        if new_space / total_space < 1.0 - percent:
            return [left, right]
        right -= 1
        new_space = sum(original_hist[left:right])
        print(new_space / total_space)
        print(str(left) + " - " + str(right))
        if new_space / total_space < 1.0 - percent:
            return [left, right]


def transform_matrix(width, a, b):
    c = 0
    d = width
    new_range = d-c
    old_range = b - a
    range_multiplier = new_range / old_range
    transform = [0] * width
    for i in range(len(transform)):
        new_color = (i - a) * range_multiplier + c
        transform[i] = max(min(math.floor(new_color), 255), 0)
    return transform


# Images loading and converting to gray tones

Image = cv2.imread("car.jpg")

Image = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Original_", Image)

# Building base histograms

baseHist = build_hist(Image, 256, 0, 255)
plt.plot(baseHist)
plt.show()


# Histogram trimming

trimmedBorders = trim_hist(baseHist, 0.05)
trimHist = build_hist(Image, 256, trimmedBorders[0], trimmedBorders[1])
plt.plot(trimHist)
plt.show()

# Histogram transformation

transformMatrix = transform_matrix(256, trimmedBorders[0], trimmedBorders[1])

for i in range(len(Image)):
        for j in range(len(Image[0])):
            Image[i][j] = transformMatrix[Image[i][j]]

finalHist = build_hist(Image, 256, 0, 255)
plt.plot(finalHist)
plt.show()

# Print new images
cv2.imshow("Result", Image)

cv2.waitKey(0)
