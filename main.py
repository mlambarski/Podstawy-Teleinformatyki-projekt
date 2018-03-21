import cv2


print(cv2.__version__)

img = cv2.imread('C:/Users/Ela/Desktop/A&A&N v2/50.jpg', cv2.IMREAD_GRAYSCALE)

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()