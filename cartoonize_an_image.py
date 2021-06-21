"""
Cartoonize an Image
Two operations we should make:
    -> Reduce the color palette.
        - Bileteral filter
            - Gaussian blur
    -> Identify the edges.
        - Adaptive threshold
            - Median blur
Blur is reducing the noise in an image.
"""
import cv2 as cv
import numpy as np

img = cv.imread("dean_winchester2.jpg")

# smooth the image 5 times
"""
d -> Diameter of each pixel neighborhood that is used during filtering
sigmaColor -> Filter sigma in the color space. A larger value of the parameter means that
farther colors within the pixel neighborhood (see sigmaSpace) will be mixed together,
resulting in larger areas of semi-equal color.
sigmaSpace -> Filter sigma in the coordinate space. A larger value of the parameter means
that farther pixels will influence each other as long as their colors are close enough.
When d>0, it specifies the neighborhood size regardless of sigmaSpace.
Otherwise, d is proportional to sigmaSpace.
"""
num_iter = 5
for _ in range(num_iter):
    new_img = cv.bilateralFilter(img, d = 9, sigmaColor = 9, sigmaSpace = 7)

# converts bgr to gray scale
img_gray = cv.cvtColor(new_img, cv.COLOR_BGR2GRAY)
# apply medium blur
img_blur = cv.medianBlur(img_gray, 7)

"""
adaptiveThreshold -> the algorithm determines the threshold for a pixel based on a small
region around it. So we get different thresholds for different regions of the same image
which gives better results for images with varying illumination.
cv.ADAPTIVE_THRESH_GAUSSIAN_C: The threshold value is a gaussian-weighted sum of the
neighbourhood values minus the constant C.
"""
img_edge = cv.adaptiveThreshold(img_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv.THRESH_BINARY, 7, 2)
img_edge = cv.cvtColor(img_edge, cv.COLOR_GRAY2BGR)

# take only region of img from img_edge image
cartoon = cv.bitwise_and(img, img_edge)
cv.imshow("Cartoon Image", cartoon)
cv.imwrite("cartoon_dean2.jpg", cartoon)

cv.waitKey(0)
cv.destroyAllWindows()
