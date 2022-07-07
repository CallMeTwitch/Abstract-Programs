import cv2

ascii = '  .-^/+X0%@@@'
n = len(ascii) - 1

translate = lambda x:ascii[round(x / 255 * n)]
bound = lambda x:max(0, min(255, x))

numbers = [round(255 / n) * q for q in range(n)]
closest = lambda x:min(numbers, key = lambda q:abs(x - q))

def contrast(image):
    l, a, b = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2LAB))

    clahe = cv2.createCLAHE(clipLimit = 3, tileGridSize = (8, 8))
    cl = clahe.apply(l)

    return cv2.cvtColor((cv2.merge((cl, a, b))), cv2.COLOR_LAB2BGR)

def dither(image):
    h, w = image.shape[:2]

    for y in range(h):
        for x in range(w):
            old = image[y, x]
            new = closest(old)

            image[y, x] = new

            error = old - new

            if y < h - 1:
                image[y + 1, x] = bound(image[y + 1, x] + error * 5 / 16)

                if x > 0:
                    image[y + 1, x - 1] = bound(image[y + 1, x - 1] + error * 3 / 16)

                if x < w - 1:
                    image[y + 1, x + 1] = bound(image[y + 1, x + 1] + error * 1 / 16)

            if x < w - 1:
                image[y, x + 1] = bound(image[y, x + 1] + error * 7 / 16)
    
    return image

def pic2ascii(image):
    h, w = image.shape[:2]

    for y in range(h):
        for x in range(w):
            print(translate(image[y, x]), end = ' ')
        print()

image = cv2.imread('FILE_NAMEjpg', 1)

contrasted = contrast(image)
grey = cv2.resize(cv2.cvtColor(contrasted, cv2.COLOR_BGR2HSV), (160, 120))[:, :, 2]
dithered = dither(grey)

pic2ascii(dithered)
print()