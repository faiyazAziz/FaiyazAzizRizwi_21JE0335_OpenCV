import cv2 as cv
import numpy as np
import math
import cv2.aruco as aruco


    #  Function for the roytaion of aruco marker which is to be cropped.
def rotate(img,ang,rotPoint):
    (y,x)=img.shape[:2]
    rotMat=cv.getRotationMatrix2D(rotPoint,ang,1.0)
    dimension=(x,y)
    return cv.warpAffine(img,rotMat,dimension)


    # Function for pasting the aruco marker over the shapes.
def augmented(bbox,img,imgAug):
    tl=bbox[0][0],bbox[0][1]          #bbox is the list of co-ordinates of the square
    tr=bbox[1][0],bbox[1][1]
    br=bbox[2][0],bbox[2][1]
    bl=bbox[3][0],bbox[3][1]

    h,w,c=imgAug.shape
    pts1=np.array([tl,tr,br,bl])
    pts2=np.float32([[0,0],[w,0],[w,h],[0,h]])

    matrix,_=cv.findHomography(pts2,pts1)
    imgOut=cv.warpPerspective(imgAug,matrix,(img.shape[1],img.shape[0]))
    cv.fillConvexPoly(img,pts1.astype(int),(0,0,0))
    imgOut=img+imgOut

    return imgOut


    #   Function for finding the presence of aruco marker
def findArucoMarker(img,markerSize=5,totalMarker=250):
    imgGray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_{markerSize}X{markerSize}_{totalMarker}')
    arucoDict=aruco.Dictionary_get(key)
    parameters=aruco.DetectorParameters_create()
    bboxs,ids,rejected=aruco.detectMarkers(imgGray,arucoDict,parameters=parameters)

    x1, y1 = (int(bboxs[0][0][0][0]), int(bboxs[0][0][0][1]))         # co-ordinates of detected aruco marker
    x2, y2 = (int(bboxs[0][0][1][0]), int(bboxs[0][0][1][1]))

    y_net = y2 - y1
    x_net = x2 - x1
    sideLength = ((y_net) ** 2 + (x_net) ** 2) ** (1 / 2)            # length of sides of Aruco marker
    tanx = float(y_net) / x_net
    angle = math.atan(tanx) * (180 / 3.142)                          # Angle by which aruco marker is rotated from ideal position

    return bboxs,ids[0][0],angle,(x1,y1),sideLength


 # Function for finding the square
def findSquare(img):
    _, thresh = cv.threshold(img, 245, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    i = 0
    for contour in contours:
        if i == 0:
            i = 1                                                   # this is to neglect the detection of image boundary as a contour
            continue

        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)

        if len(approx) == 4:                                       # Condition for being a Quadrilateral
            x1, y1, w, h = cv.boundingRect(approx)
            aspect_Ratio = float(w) / h

            if aspect_Ratio>= 0.98 and aspect_Ratio <= 1.02:       # Condition for being square or rhombus
                rect = cv.minAreaRect(contour)
                cbox = cv.boxPoints(rect)                          # It will give list of co-ordinates of detected square
                return cbox


# Reading the image containing shapes
shapes=cv.imread("CVtask.jpg",1)
shapes=cv.resize(shapes,(int(shapes.shape[1]/2),int(shapes.shape[0]/2)),interpolation=cv.INTER_AREA)
gray=cv.cvtColor(shapes,cv.COLOR_BGR2GRAY)

# Detection of color
         # green
hsv=cv.cvtColor(shapes,cv.COLOR_BGR2HSV)
lower_green=np.array([40,100,100])
upper_green=np.array([70,255,255])            # Range detected using trackbar
green=cv.inRange(hsv,lower_green,upper_green)

        # Orange
lower_orange=np.array([10,40,40])
upper_orange=np.array([30,255,255])
orange=cv.inRange(hsv,lower_orange,upper_orange)

        # Black
lower_black=np.array([0,0,0])
upper_black=np.array([10,210,210])
black=cv.inRange(hsv,lower_black,upper_black)
black=cv.bilateralFilter(black,10,25,25)              # done for neglected some extra dots detected
black=cv.GaussianBlur(black,(3,3),0)

        # Pink Peach
lower_pink=np.array([0,8,54])
upper_pink=np.array([30,57,240])
pink=cv.inRange(hsv,lower_pink,upper_pink)

# Reading Aruco Marker Image
aruco_1=cv.imread("1.jpg")
aruco_2=cv.imread("2.jpg")
aruco_3=cv.imread("3.jpg")
aruco_4=cv.imread("4.jpg")

arucos=[aruco_1,aruco_2,aruco_3,aruco_4]          # List of Aruco markers

for arc in arucos:

    bbox,id,angle,point,L=findArucoMarker(arc)
    rotated=rotate(arc,angle,point)
    crop=rotated[point[1]:point[1]+int(L),point[0]:point[0]+int(L)]

    if id==1:
        box=findSquare(green)                     # Getting co-ordinate of contour having of green square
    elif id==2:
        box=findSquare(orange)
    elif id==3:
        box=findSquare(black)
    elif id==4:
        box=findSquare(pink)
    shapes = augmented(box,shapes,crop)

cv.imwrite("final.jpg",shapes)
cv.imshow("shapes",shapes)
cv.waitKey(0)
cv.destroyAllWindows()