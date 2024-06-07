import cv2
import os

from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies

ocr_model = PaddleOCR(lang='en', use_angle_cls=True, use_gpu=False)

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    arr = os.listdir()
    if not ret:
        print("failed to grab frame")
        break
    
    cv2.imwrite('img{}.jpg'.format(img_counter), frame)
    
    getPlate = False
    imgName = ""
    for elem in arr:
        if(".jpg" in elem):
            imgName = elem
            getPlate = True

    showTarga = False
    if (getPlate):
        print("Scanning for plate...")
        getPlate = False
        result = ocr_model.ocr(imgName)

        if(type(result) != "NoneType"):
            targa = result[0][0][1][0]
            showTarga = True
            print(targa)

        else:
            showTarga = False
            print("Tasin Infame")
        os.remove(imgName)

    if(showTarga):
        cv2.putText(frame, targa, fontScale = 16)

    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
