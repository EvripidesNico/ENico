import math
from ..Containers import Controls
from ..Containers import Sensors
from ..Containers import States
from ..Constants import VehiclePhysicalConstants as VPC
from ..Constants import VehicleSensorConstants as VSC
from ..Modeling import VehicleDynamicsModel as VDM
from ..Sensors import SensorsModel
from ..Utilities import MatrixMath as MM



class LowPassFilter():

    def __init__(self, dT=VPC.dT, cutoff=1):
        self.dT = dT
        self.cutoff = cutoff
        self.output = 0.0
        self.alpha = 2 * math.pi * cutoff
        return
    
    def reset(self):
        self.output = 0
        return
    
    def update(self, input):
        e = math.e**(-self.alpha*self.dT)
        yk1 = e * self.output + (1-e)*input
        self.output = yk1
        return self.output
    

class VehicleEstimator():

    def __init__(self, dT=VPC.dT, gains=Controls.VehicleEstimatorGains(), sensorsModel= SensorsModel.SensorsModel()):
        self.dT  = dT
        self.gains =gains
        self.sensorsModel = sensorsModel

        #estimate states
        self.estimateState = States.vehicleState()
        self.estimateState.pd = VPC.InitialDownPosition
        self.estimateState.Va = VPC.InitialSpeed
        self.estimateState.R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        #not sure about the cuttoff but oh well for now 
        self.LFbaro = LowPassFilter(self.dT, cutoff= gains.lowPassCutoff_h)
        #biasses
        self.gyroBias = [[0], [0], [0]]
        self.magBias = [[VSC.mag_bias],[VSC.mag_bias],[VSC.mag_bias]]
        self.baroBias = 0.0
        self.accelBias = VSC.accel_bias
        self.pitotBias = 0
        self.GPSalt = 0 #VSC.GPS_etaHorizontal
        self.ChiBias = 0
        self.AscentRate = 0
        #Might need more
        return
    
    def reset(self):
        self.gyroBias = [[0], [0], [0]]
        self.magBias = [[0],[0],[0]]
        self.accelBias = 0
        self.pitotBias = 0
        self.GPSalt = 0
        self.ChiBias = 0
        self.AscentRate = 0
        return
    

    def getEstimatedState(self):
        return self.estimateState
    def getEstimatorGains(self):
        return self.gains
    def setEstimatorGains(self, gains):
        self.gains = gains
        return 
    def setEstimatedState(self, state):
        self.estimateState = state
        return
    def setEstimatorBiases(self, estimatedGyroBias=[[0], [0], [0]], estimatedPitotBias=0, estimatedChiBias=0, estimatedAscentRate=0, estimatedAltitudeGPSBias=0):
        self.gyroBias = estimatedGyroBias
        self.pitotBias = estimatedPitotBias
        self.ChiBias = estimatedChiBias
        self.AscentRate = estimatedAscentRate
        self.GPSalt = estimatedAltitudeGPSBias
        return


    def estimateAttitude(self, sensorData = Sensors.vehicleSensors(), estimatedState = States.vehicleState()):
        #setting these up so i can return the right size variables
        '''print("estimateAttitude(self, sensorData=Sensors.vehicleSensors(gyro_x=", sensorData.gyro_x, ", gyro_y=", sensorData.gyro_y, ", gyro_z=", sensorData.gyro_z, ", accel_x=", sensorData.accel_x, ", accel_y=", sensorData.accel_y, ", accel_z=", sensorData.accel_z, ", mag_x=", sensorData.mag_x, ", mag_y=", sensorData.mag_y, ", mag_z=", sensorData.mag_z, "), estimatedState=States.vehicleState(pn=", estimatedState.pn, ", pe=", estimatedState.pe, ", pd=", estimatedState.pd, ", u=", estimatedState.u, ", v=", estimatedState.v, ", w=", estimatedState.w, ", yaw=", estimatedState.yaw, ", pitch=", estimatedState.pitch, ", roll=", estimatedState.roll, ", p=", estimatedState.p, ", q=", estimatedState.q, ", r=", estimatedState.r, ", dcm=", estimatedState.R, "))")
        print("vehicleEstimator.setEstimatedGains(Controls.VehicleEstimatorGains(Kp_acc=", self.gains.Kp_acc, ", Ki_acc=", self.gains.Ki_acc, ", Kp_mag=", self.gains.Kp_mag, ", Ki_mag=", self.gains.Ki_mag, "))")
        print("self.gyro_bias = ", self.gyroBias)'''
        self.estimateState = estimatedState
        est_b = self.gyroBias
        est_R = self.estimateState.R
        gyro = [[sensorData.gyro_x], [sensorData.gyro_y], [sensorData.gyro_z]]
        #normalize accel and mag
        accel = [[sensorData.accel_x], [sensorData.accel_y],[sensorData.accel_z]]
        accel_mag = math.sqrt(accel[0][0]**2 + accel[1][0]**2 + accel[2][0]**2)
        #check to see if accel is on a turn or not
        use_accel = (0.9 * VPC.g0) < accel_mag < (1.1 * VPC.g0)
        normAccel = [[0], [0], [0]] #accel body norm

        g_NED = MM.vectorNorm([[0],[0],[VPC.g0]]) if MM.vectorNorm([[0],[0],[VPC.g0]]) != 0 else [[0],[0],[VPC.g0]] #accel inirtial norm
        
        g_body = MM.multiply(est_R, g_NED) #R*mi

        mag = [[sensorData.mag_x],[sensorData.mag_y], [sensorData.mag_z]]
        normMag = MM.vectorNorm(mag) if MM.vectorNorm(mag) != 0 else mag # mag body norm
        B_NED = MM.vectorNorm(VSC.magfield) if MM.vectorNorm(VSC.magfield) != 0  else VSC.magfield
        if use_accel:
            normAccel= MM.vectorNorm(accel) #mb
            error_acc = MM.crossProduct(normAccel, g_body) # mb x R*mi
            bias_dot = MM.scalarMultiply(self.dT,MM.scalarMultiply(-self.gains.Ki_acc, error_acc))
            est_b = MM.add(est_b, bias_dot)
        else: 
            error_acc =[[0], [0], [0]]
        
        error_mag = MM.crossProduct(normMag,MM.multiply(est_R, B_NED)) # mb x R*mi
        bias_dot = MM.scalarMultiply(self.dT,MM.scalarMultiply(-self.gains.Ki_mag, error_mag))
        est_b = MM.add(est_b, bias_dot)

        #compute est_w
        est_w = MM.subtract(gyro,est_b)

        #dcm stuff, make empty dot state
        dot = States.vehicleState()
        sure = VDM.VehicleDynamicsModel()
        temp = MM.subtract(gyro,est_b) #might just have to be just gyro
        temp = MM.add(temp, MM.scalarMultiply(self.gains.Kp_acc, error_acc))
        temp = MM.add(temp, MM.scalarMultiply(self.gains.Kp_mag, error_mag))
        next_R = sure.Rexp(state = States.vehicleState(p=temp[0][0],q = temp[1][0], r = temp[2][0]), dT=self.dT,dot= dot)

        
        est_R = MM.multiply(next_R, est_R)

        #self.estimateState.R = est_R

        return est_b, est_w, est_R 

    def estimateAirspeed(self, sensorData = Sensors.vehicleSensors(), estimatedState = States.vehicleState()):
        '''print("estimateAttitude(self, sensorData=Sensors.vehicleSensors(gyro_x=", sensorData.gyro_x, ", gyro_y=", sensorData.gyro_y, ", gyro_z=", sensorData.gyro_z, ", accel_x=", sensorData.accel_x, ", accel_y=", sensorData.accel_y, ", accel_z=", sensorData.accel_z, ", mag_x=", sensorData.mag_x, ", mag_y=", sensorData.mag_y, ", mag_z=", sensorData.mag_z,"Pitot =" ,sensorData.pitot, "), estimatedState=States.vehicleState(pn=", estimatedState.pn, ", pe=", estimatedState.pe, ", pd=", estimatedState.pd, ", u=", estimatedState.u, ", v=", estimatedState.v, ", w=", estimatedState.w, ", yaw=", estimatedState.yaw, ", pitch=", estimatedState.pitch, ", roll=", estimatedState.roll, ", p=", estimatedState.p, ", q=", estimatedState.q, ", r=", estimatedState.r, ", dcm=", estimatedState.R, "))")
        print("vehicleEstimator.setEstimatedGains(Controls.VehicleEstimatorGains(Kp_acc=", self.gains.Kp_acc, ", Ki_acc=", self.gains.Ki_acc, ", Kp_mag=", self.gains.Kp_mag, ", Ki_mag=", self.gains.Ki_mag, "))")'''
        b_est = self.pitotBias
        #airspeed from pitot
        Va_est = estimatedState.Va
        Va_pitot = math.sqrt(2*sensorData.pitot / VPC.rho) 
        #get bias from accel with gravity 
        g_ned = [[0],[0],[VPC.g0]]
        g_body = MM.multiply( estimatedState.R,g_ned)
        accel_x_corrected = sensorData.accel_x + g_body[0][0]

        #bias pitot
        b_dot = -self.gains.Ki_Va*(Va_pitot - Va_est)
        b_est = b_est + b_dot*self.dT
        #compute Va estimation
        Va_dot = (accel_x_corrected - b_est) + self.gains.Kp_Va*(Va_pitot - Va_est)
        Va_est = Va_est + (Va_dot)*self.dT
        
        return b_est, Va_est
    
    def estimateAltitude(self, sensorData = Sensors.vehicleSensors(), estimatedState = States.vehicleState()):
        '''print("estimateAttitude(self, sensorData=Sensors.vehicleSensors(gyro_x=", sensorData.gyro_x, ", gyro_y=", sensorData.gyro_y, ", gyro_z=", sensorData.gyro_z, ", accel_x=", sensorData.accel_x, ", accel_y=", sensorData.accel_y, ", accel_z=", sensorData.accel_z, "Baro =" ,sensorData.baro, "), estimatedState=States.vehicleState(pn=", estimatedState.pn, ", pe=", estimatedState.pe, ", pd=", estimatedState.pd, ", u=", estimatedState.u, ", v=", estimatedState.v, ", w=", estimatedState.w, ", yaw=", estimatedState.yaw, ", pitch=", estimatedState.pitch, ", roll=", estimatedState.roll, ", p=", estimatedState.p, ", q=", estimatedState.q, ", r=", estimatedState.r, ", dcm=", estimatedState.R, "))")
        print("vehicleEstimator.setEstimatedGains(Controls.VehicleEstimatorGains(Kp_h=", self.gains.Kp_h, ", Ki_h=", self.gains.Ki_h, ", Kp_h_gps=", self.gains.Kp_h_gps, ", Ki_h_gps=", self.gains.Ki_h_gps, "))")'''
        #initial variables
        bh_hat = self.AscentRate
        h_hat = -estimatedState.pd
        b_gps_prev = self.GPSalt
        b_gps = b_gps_prev 
        h_baro = (sensorData.baro - VSC.Pground)/ (VPC.rho*VPC.g0)
        hlpf = self.LFbaro.update(-h_baro)
        bh_dot = -self.gains.Ki_h*(hlpf + h_hat)

        bh_hat = bh_hat+ bh_dot*self.dT
        #set up aup
        accel_body = [[sensorData.accel_x],[sensorData.accel_y], [sensorData.accel_z]]
        a = MM.multiply(MM.transpose(estimatedState.R), accel_body)
        a_up = a[2][0] + VPC.g0

        h_dot_under = a_up*self.dT +bh_hat

        h_hat =h_hat+ (self.gains.Kp_h*(hlpf - h_hat) + h_dot_under)*self.dT

        #check for gps update
        if self.sensorsModel.updateTicks % self.sensorsModel.gpsTickUpdate == 1:
            #do more math
            b_gps_dot = -self.gains.Ki_h_gps*(sensorData.gps_alt - h_hat)
            b_gps= b_gps + b_gps_dot*self.dT
            h_dot = self.gains.Kp_h_gps*(sensorData.gps_alt - h_hat) + h_hat + (-b_gps)
            h_hat += h_dot*self.dT
        else:
            h_hat = h_hat - b_gps

        return  h_hat, h_dot_under, b_gps 
    
    def estimateCourse(self, sensorData = Sensors.vehicleSensors(), estimatedState = States.vehicleState()):
        bx_prev = self.ChiBias
        X_hat_prev = estimatedState.chi
        bx_hat = 0
        X_hat = estimatedState.chi
        #course rate estimate
        X_dot = (1/math.cos(estimatedState.pitch))*(estimatedState.q*math.sin(estimatedState.roll)+ estimatedState.r*math.cos(estimatedState.roll)) - bx_prev

        X_hat += X_dot*self.dT #integrate

         #check for gps update
        if self.sensorsModel.updateTicks % self.sensorsModel.gpsTickUpdate == 1:
            b_dot = -self.gains.Ki_chi*(sensorData.gps_cog - X_hat_prev) #cours rate estimate
            bx_hat = bx_prev + b_dot*self.dT #integrate bias
            X_dot = self.gains.Kp_chi*(sensorData.gps_cog - X_hat_prev) - (bx_hat - bx_prev) #encorporate error
            X_hat += X_dot*self.dT #comp filter new course update

            bx_prev = bx_hat


        return bx_prev ,  X_hat
    
    def Update(self):
        sensor = self.sensorsModel.getSensorsNoisy()
        self.gyroBias, estimated_w, estimated_R = self.estimateAttitude(sensor,estimatedState=self.estimateState)
        h_est, h_dot_est, b_gps_est = self.estimateAltitude(sensor, estimatedState=self.estimateState)

        pitot_bias, Va_est = self.estimateAirspeed(sensor,estimatedState = self.estimateState)
        chi_bias, chi_est = self.estimateCourse(sensor,estimatedState= self.estimateState)

       
        self.estimateState.pd = -h_est  
        self.estimateState.Va = Va_est
        self.estimateState.chi = chi_est
        self.estimateState.R = estimated_R  
        self.pitotBias = pitot_bias
        self.GPSalt = b_gps_est
        self.ChiBias = chi_bias

        return
