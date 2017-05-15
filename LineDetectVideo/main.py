#-*- coding: utf-8 -*-
'''
Created on 07.05.2017

@author: Michał Stypczyński
'''

import cv2
import numpy as np

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('output.avi',fourcc, 20.0, (800,600))
    line_color = [([210,210,210], [255,255,255])]
    while(True):
        
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,1)
        for (lower, upper) in line_color:
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            mask = cv2.inRange(frame, lower, upper)
            output = cv2.bitwise_and(frame, frame, mask = mask)
            
        gray = cv2.cvtColor(output,cv2.COLOR_RGB2RGBA)    
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        lines = cv2.HoughLines(edges,1,np.pi/180,100)
        if lines is not None:   
            for x in range(0, len(lines)):
                for rho,theta in lines[x]:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a*rho
                    y0 = b*rho
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0 + 1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 - 1000*(a))
                    cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)  
        
        cv2.imshow('frame',frame)
       # out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    #out.release()
    cv2.destroyAllWindows()