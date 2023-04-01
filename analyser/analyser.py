from PIL import Image
import os
import cv2


def color_load():
    name = 'data/map.png'
    im = Image.open(name).convert('RGB')
    result = Image.new('RGB', im.size)
    center = im.getpixel((325, 225))
    print(center)
    result.save('data/map.png')


def trafficlight(im1, im2):
    needle = cv2.imread(im1)
    haystack = cv2.imread(im2)

    result = cv2.matchTemplate(needle, haystack, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    return True if maxVal > 0.6 else False


if __name__ == "__main__":
    os.chdir(r'C:\Users\olegm\Documents\GitHub\road')
    # os.chdir(r'C:\Users\Олег\PycharmProjects\road')
