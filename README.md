# FaiyazAzizRizwi_21JE0335_OpenCV

This project is about pasting Aruco marker(of specified id) on the square that is present in the image CVtask.jpg file.
The Aruco is to be pasted as follows:
               |-------------------------|----------------------|
               |    colour of square     |       Marker ID      |
               |-------------------------|----------------------|
               |        green            |           1          |
               |        orange           |           2          |
               |        black            |           3          |
               |        pink peach       |           4          |
               |-------------------------|----------------------|

For this I written a python script using opencv library in which i defined four function which are as:-
    1) rotate()   :-This funtion is created to rotate the aruco marker so that it can be cropped.
                     in this I used :
                        a)  cv2.getRotationMatrix2D()= to get the matrix used for rotating a image.
                        b)  cv2.warpAffine() = this is used to do transformation in image(Here we do rotation)
    2) augmented() :-This function is created to paste the aruco in the square in proper orientation
                      in this I used :
                         a) cv2.findHomaography() = provide the matrix for transsformation when points of both image is provided.
                         b) cv2.warpPerspective() = it is used for planting marker in the CVtask image using the points matrix of detected sqaure and aruco marker.
                                                    it gives marker at required point but outside this was blak.
                         c) cv2.fillConvexPoly()  =this is used to fill the outer portion of polygon with particular colour
                                                   this gives inside the marker aquare portion black.
                         d) thus on adding image obtained from about we get clear fully placed marker image.
    3) findAruco() :-This function is used to get the id, and the co-ordinate of the marker.
                          a) aruco.detectMarker()= It give us the array of co-ordinates of aruco marker ,marker id. 
    4) findSquare():- This function id created to find if the detected contour is square.
                         a) cv.findContours()=it provide us the contour where there is the change in pixel(i.e. getting the boundary)
                         b) cv.approxPolyDP()=used to get a approx polygon from the corner of contour of minimum length
                         c) cv.minAreaRect() = used to get a rectangle of minimum area containing the contour.
                         d) cv.boxPoints() = provide the coordinate of the co-ordinate
                         
