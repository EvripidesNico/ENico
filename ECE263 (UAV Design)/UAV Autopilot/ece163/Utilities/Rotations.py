import math
from . import MatrixMath

def dcm2Euler(DCM): #dcm 3x3 matrix
    ##return yaw, pitch, roll
    yaw = math.atan2(DCM[0][1], DCM[0][0])

    pitch = -math.asin(max(-1, min(1, DCM[0][2])))

    roll = math.atan2(DCM[1][2], DCM[2][2])

    return yaw, pitch, roll

#Parameters:
# yaw(roattion along the z axis)
# pitch(roation aobu the y axis)
# roll (roation along the x axis)
#return: DCM 3x3 matrix
def euler2DCM(yaw, pitch, roll):
    cy = math.cos(yaw)
    sy = math.sin(yaw)
    cp = math.cos(pitch)
    sp = math.sin(pitch)
    cr = math.cos(roll)
    sr = math.sin(roll)
    return [[cp*cy, cp*sy, -sp], 
            [(sr*sp*cy)-(cr*sy), (sr*sp*sy)+(cr*cy), sr*cp],
              [(cr*sp*cy)+(sr*sy), (cr*sp*sy)-(sr*cy), cr*cp]]

def ned2enu(points):
    #return same points but in enu from ned 
    translation_matrix = [[0,1,0],[1,0,0],[0,0,-1]]
    #enu_points = [points[1],points[0], -points[2]]
    
    return MatrixMath.multiply(points, translation_matrix)