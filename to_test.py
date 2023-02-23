from NMwordDetection.filter3 import text_to_image
import cv2
from os import getcwd

a = 0
while True:
    string = ''
    for i in range(0, 10):
        for j in range(0,40):
            string+=chr(a+40*i+j)
        string+='\n'
    text_to_image("tmp", string)
    cv2.imshow(f"test{hex(a)}({a})~{hex(a+400)}({a+400})", cv2.imread(f"{getcwd()}\\NMwordDetection\\temp\\tmp.png"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    a+=400