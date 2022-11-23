import cv2
import pytesseract

img = cv2.imread('1.png')
text = pytesseract.image_to_string(img, config='')
print(text)

print(pytesseract.image_to_boxes(img))

# for b in boxes.splitlines():
#     b = b.split(' ')
#     roi = cv2.rectangle(roi, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), 0)

cv2.imshow('img',img)
cv2.waitKey()
cv2.destroyAllWindows()
