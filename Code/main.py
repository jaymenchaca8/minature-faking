
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

# Read source and mask (if exists) for a given id
# Taken from assignment 5
def Read(id, path = ""):
    source = plt.imread(path + "image_" + id + ".jpg") / 255
    maskPath = path + "mask_" + id + ".jpg"
    
    if os.path.isfile(maskPath):
        mask = plt.imread(maskPath)
        assert(mask.shape == source.shape), 'size of mask and image does not match'
        mask = (mask > 128)[:, :, 0].astype(int)
    else:
        mask = np.zeros_like(source)[:, :, 0].astype(int)

    return source, mask

#set were the focus plane will be
#focus plane assumed horizontal
def getPoints(image):

    plt.imshow(image)
    plt.axis('image')
    points = plt.ginput(1, timeout=-1) #right click to add
    plt.close()

    return points

#obtain gradient "mask"
#larger values mean farther row to focus plane
def getGradient(image, point, H):
    mask = np.ones((image.shape[0],),dtype = int)
    (x_p,y_p) = point[0]
    for y in range(image.shape[0]):
        mask[y] = int((abs(y_p - y) / image.shape[0]) * H)
    return mask

def applyBlur(image, k, focus, point, gradient, F):
    output = image
    height = image.shape[0]
    (x_p,y_p) = point[0]
    gradRev = np.flip(gradient)

    #apply filter to ROI respective to gradient values
    for i in range(F):
        #collect first and last instance of gradient change respective to i
        t = next((top for top in range(int(y_p)) if gradient[top] == i) , -1)
        b = next((bot for bot in range(gradRev.shape[0] - int(y_p)) if gradRev[bot] == i), -1)
        
        if t > 0:
            output[0:t,:] = cv2.GaussianBlur(output[0:t,:],(k,k),0)
        if b > 0:
            output[height-b:height,:] = cv2.GaussianBlur(output[height - b:height,:],(k,k),0)
        k = k + 2

    #simple approach
    #for y in range(F):
    #    k = gradient[y]
    #    output[y,:] = cv2.GaussianBlur(image[y,:],(k,k),0)

    return output

# Setting up the input output paths
inputDir = '../Images/'
outputDir = '../Results/'
initialKernel = 3
F = 10 #number times applied filter
N = 1  #image number to use
H = 20 #how large focus plane is, higher numbers mean shallower depth of field 

for index in range(N,N+1):

    image, mask = Read(str(index).zfill(2), inputDir)

    points = getPoints(image)

    gradient = getGradient(image, points, H)

    output = applyBlur(image, initialKernel, focus, points, gradient, F)

    (x_p,y_p) = points[0]

    # Writing the result
    plt.imsave("{}/result_{}_gradient_F_{}_H_{}_{}X{}_recur.jpg".format(outputDir, 
                                            str(index).zfill(2), str(F).zfill(2), str(H).zfill(2), str(int(x_p)).zfill(2), str(int(y_p)).zfill(2)), output)