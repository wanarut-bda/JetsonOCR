import cv2
import easyocr

img = cv2.imread('1.png')
reader = easyocr.Reader(['en']) 
# result = reader.readtext(img, allowlist ='0123456789/()', min_size=10)
result = reader.readtext(img, min_size=10)

for pts, text, conf in result:
    print(pts, text, conf)
    cv2.rectangle(img, pts[0], pts[2], (255,0,0), 2, 1)
    cv2.putText(img, text, pts[3], cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

cv2.imshow('img',img)

cv2.waitKey()
cv2.destroyAllWindows()