from paddleocr import PaddleOCR
import cv2
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
img = cv2.imread('1.png')
ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
result = ocr.ocr(img, cls=True)

for pts, (text, conf) in result:
    pts[0] = [int(pts[0][0]), int(pts[0][1])]
    pts[2] = [int(pts[2][0]), int(pts[2][1])]
    pts[3] = [int(pts[3][0]), int(pts[3][1])]
    print(pts, text, conf)
    cv2.rectangle(img, pts[0], pts[2], (255,0,0), 2, 1)
    cv2.putText(img, text, pts[3], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

cv2.imshow('img',img)

cv2.waitKey()
cv2.destroyAllWindows()