import numpy as np

def GeneralEquation(first_x,first_y,second_x,second_y):
    # Ax+By+C=0
    A=second_y-first_y
    B=first_x-second_x
    C=second_x*first_y-first_x*second_y
    return A,B,C

def GetIntersectPointofLines(x1,y1,x2,y2,x3,y3,x4,y4):
    '''
    Calculate the intersection point of two lines, defined by {(x1,y1), (x2,y2)} and {(x3,y3), (x4,y4)}
    '''
    A1,B1,C1 = GeneralEquation(x1,y1,x2,y2)
    A2,B2,C2 = GeneralEquation(x3,y3,x4,y4)
    if (B1 == 0 and B2 == 0): # both vertical lines
        return None, None
    elif (B1 != 0 and B2 != 0): # both are not vertical lines
        if np.abs(A1/B1 - A2/B2) <= 1e-9: # parallel
            if (np.abs(((y2-y1)/(x2-x1))*(x3-x1)+y1 - y3) <= 1e-5 or np.abs(((y2-y1)/(x2-x1))*(x4-x1)+y1 - y4) <= 1e-5):
                # if two parallel lines overlap
                return 0.5*(x2+x3), y2
            else:
                return None, None
        else:
            m=A1*B2-A2*B1
            if m==0:
                if x1 == x4:
                    x = x1
                    y = y1
                if x2 == x3:
                    x = x2
                    y = y2
            else:
                x=(C2*B1-C1*B2)/m
                y=(C1*A2-C2*A1)/m
            return x,y