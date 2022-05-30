import cv2
import funcs as cm
import random
import string
"""
    BGR Encoding
"""

def stg_encoding(text):

    binarytext = cm.str2binary(text)
    bt_Length = len(binarytext)
    img = cv2.imread("images/logo.png")
    height, width, channels = img.shape
    i = 0
    flag = False
    for y in range(height):
        for x in range(width):
            for z in range(channels):
                binaryValue = cm.decimal2Binary(img[y][x][z])
                LSB = int(binaryValue[-1:])
                if (i < bt_Length) and (LSB != int(binarytext[i])):
                    LSB = binarytext[i]
                    binaryValue = binaryValue[:7] + str(LSB)
                    decimalValue = int(binaryValue, 2)
                    img[y][x][z] = decimalValue
                elif i >= bt_Length:
                    flag = True
                    break
                i += 1
            if flag:
                break
        if flag:
            break
    cv2.imwrite("images/logo.png", img)

    return True

"""
    BGR Decoding
"""

def stg_decoding():
    img = cv2.imread("images/logo.png")
    height, width, channels = img.shape
    binarytext = ''
    i = 0
    flag = False
    for y in range(height):
        for x in range(width):
            for z in range(channels):
                if (i % 8 == 0) and (binarytext[-8:] == '00000000'):
                    flag = True
                    break
                binaryValue = cm.decimal2Binary(img[y][x][z])
                binarytext += binaryValue[-1:]
                i += 1
            if flag:
                break
        if flag:
            break
    text = cm.binary2str(binarytext[:-8])
    return text
