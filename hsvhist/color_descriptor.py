"CBIR(Content-Base Image Retrieval)"  
import numpy as np  
import cv2  
  
class ColorDescriptor:  
    def __init__(self, bins):  
        # store the number of bins for the HSV histogram  
        self.bins = bins  
  
    def describe(self, image):  
        # convert the image into HSV color space  
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  
        features =[]  
        # grab the dimensions and compute the center of the image  
        (h,w) = image.shape[:2]  
        (cx,cy) = (int(w*0.5), int(h*0.5))  
  
        # segment the image  
        segments =[(0,cx,0,cy),(cx,w,0,cy),(cx,w,cy,h),(0,cx,cy,h)]  
  
        # construct an elliptical mask representing the center of the image  
        (axesX, axesY) =(int((w*0.75)/2), int((h*0.75)/2))  
        ellipMask = np.zeros(image.shape[:2], np.uint8)  
        cv2.ellipse(ellipMask,(cx,cy),(axesX,axesY),0,0,360,255,-1)         
  
        # loop over the segments  
        for(startX,endX, startY, endY) in segments:  
            cornerMask = np.zeros(image.shape[:2], np.uint8)  
            cv2.rectangle(cornerMask,(startX,startY),(endX,endY),255,-1)  
            cornerMask = cv2.subtract(cornerMask, ellipMask)  
  
            # compute the histogram  
            hist = self.histogram(image, cornerMask)  
            features.extend(hist)  
  
        # compute the ellipse histogram  
        hist = self.histogram(image, ellipMask)  
        features.extend(hist)  
  
        # return the feature vectr  
        return features  
  
    # define the function of histogram  
    def histogram(self, image, mask):  
        # extract the color histogram from the masked region  
        hist = cv2.calcHist([image],[0,1,2],mask, self.bins,[0,180,0,256,0,256])  
        hist = cv2.normalize(hist, hist).flatten()  
        return hist       