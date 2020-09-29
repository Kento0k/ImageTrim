from PIL import Image
import matplotlib.pyplot as plt
import math
import numpy


def pixel_list(pix, width, height):
    pixels = []
    for i in range(height):
        for j in range(width):
            pixels.append(pix[i][j])
    return pixels


def build_hist(pix, width):
    hist = [0] * width
    for i in pix:
        hist[i] += 1
    return hist


def trim_hist(pix, percent):
    pix.sort()
    remove = math.floor(len(pix) / 100 * percent)
    return pix[remove:-remove]


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


def transform_hist(width, matrix):
    result = [0] * len(matrix)
    transform = transform_matrix(width, min(matrix), max(matrix))
    for i in range(len(matrix)):
        result[i] = transform[matrix[i]]
    return result


def transform_image(pix, width, height, matrix):
    image = [[0] * width for i in range(height)]
    transform = transform_matrix(width, min(matrix), max(matrix))
    for i in range(height):
        for j in range(width):
            image[i][j] = transform[pix[i][j]]
    return image


# Images loading and converting to gray tones

carImage = Image.open("car.jpg")
dogImage = Image.open("dog.jpg")
lainImage = Image.open("lain.jpg")

carImage = carImage.convert('L')
dogImage = dogImage.convert('L')
lainImage = lainImage.convert('L')

carPix = numpy.asarray(carImage)
dogPix = numpy.asarray(dogImage)
lainPix = numpy.asarray(lainImage)

carImage.show()
dogImage.show()
lainImage.show()

# Building base histograms

histogramCar = build_hist(pixel_list(carPix, carImage.size[0], carImage.size[1]), 256)
plt.plot(histogramCar)
plt.show()

histogramDog = build_hist(pixel_list(dogPix, dogImage.size[0], dogImage.size[1]), 256)
plt.plot(histogramDog)
plt.show()

histogramLain = build_hist(pixel_list(lainPix, lainImage.size[0], lainImage.size[1]), 256)
plt.plot(histogramLain)
plt.show()

# Histogram trimming

trimCarHist = trim_hist(pixel_list(carPix, carImage.size[0], carImage.size[1]), 5)
histogramCarTrimmed = build_hist(trimCarHist, 256)
plt.plot(histogramCarTrimmed)
plt.show()

trimDogHist = trim_hist(pixel_list(dogPix, dogImage.size[0], dogImage.size[1]), 5)
histogramDogTrimmed = build_hist(trimDogHist, 256)
plt.plot(histogramDogTrimmed)
plt.show()

trimLainHist = trim_hist(pixel_list(lainPix, lainImage.size[0], lainImage.size[1]), 5)
histogramLainTrimmed = build_hist(trimLainHist, 256)
plt.plot(histogramLainTrimmed)
plt.show()

# Histogram transformation

finalCarHist = transform_hist(256, trimCarHist)
histogramCarFinal = build_hist(finalCarHist, 256)
plt.plot(histogramCarFinal)
plt.show()

finalDogHist = transform_hist(256, trimDogHist)
histogramDogFinal = build_hist(finalDogHist, 256)
plt.plot(histogramDogFinal)
plt.show()

finalLainHist = transform_hist(256, trimLainHist)
histogramLainFinal = build_hist(finalLainHist, 256)
plt.plot(histogramLainFinal)
plt.show()

# Print new images

carImage = Image.fromarray(numpy.uint32(transform_image(carPix, carImage.size[0], carImage.size[1], trimCarHist)))
carImage.show()

dogImage = Image.fromarray(numpy.uint32(transform_image(dogPix, dogImage.size[0], dogImage.size[1], trimDogHist)))
dogImage.show()

lainImage = Image.fromarray(numpy.uint32(transform_image(lainPix, lainImage.size[0], lainImage.size[1], trimLainHist)))
lainImage.show()