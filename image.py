# all functions expect float image
def minmax(img):
    minv = np.min(img)
    maxv = np.max(img)
    return (img - minv) / (maxv - minv)

def threshold(img, rate):
    ind = img > rate
    temp = np.zeros(img.shape)
    temp[ind] = 1
    return temp

def erode(img, size):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(size,size))
    temp = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
    return temp

def dilate(img, size):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(size,size))
    temp = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)
    return temp

def denoise(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    temp = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    temp = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel)
    return temp

def high_pass(img, value):
    ind = img < value
    temp = img + 0
    temp[ind] = 0
    return temp

def normalize_thickness(img, target_thickness, rec_depth=0):
    temp1 = erode(img, target_thickness)
    temp2 = erode(img, target_thickness + 1)
    temp = img + 0

    if rec_depth > 5:
        return temp

    #too thin
    if np.sum(temp1) < 20:
        temp = dilate(img, target_thickness)
        temp = normalize_thickness(temp, target_thickness, rec_depth + 1)

    #too thick
    if np.sum(temp2) > 20:
        temp = erode(img, 2)
        temp = normalize_thickness(temp, target_thickness, rec_depth + 1)

    return temp