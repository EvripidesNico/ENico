import math
import random
from ece163.Modeling import VehicleAerodynamicsModel
from ece163.Utilities import MatrixMath
from ..Containers import Sensors
from ..Constants import VehiclePhysicalConstants as VPC
from ..Constants import VehicleSensorConstants as VSC
from ..Modeling import VehicleAerodynamicsModel
from ..Containers import States


class GaussMarkov():

    def __init__(self,dT=VPC.dT, tau=1e6, eta=0.0):
        self.tau = tau
        self.eta = eta
        self.v = 0
        self.dT = dT
        self.dt = self.dT
        return
    def reset(self):
        self.v = 0
        return
    def update(self, vnoise = None):
        
        if vnoise == None:

            self.v = math.e**(-self.dt/self.tau)*self.v + random.gauss(0, self.eta)
        else:
            self.v = math.e**(-self.dt/self.tau)*self.v + vnoise
        return self.v
    
class GaussMarkovXYZ():

    def __init__(self, dT=VPC.dT, tauX=1e6, etaX=0.0, tauY=None, etaY=None, tauZ=None, etaZ=None):
        self.dT = dT
        self.dt = self.dT
        self.vx = GaussMarkov(dT, tauX, etaX)

        if tauY == None and etaY == None:
            self.vy = GaussMarkov(dT, tauX, etaX)
        else:
            self.vy = GaussMarkov(dT, tauY, etaY)

        #check same for z
        if tauZ == None and etaZ == None:
            if tauY == None and etaY == None:
                self.vz = GaussMarkov(dT, tauX, etaX)
            else:
                self.vz = GaussMarkov(dT, tauY, etaY)
        else:
            self.vz = GaussMarkov(dT, tauZ, etaZ)
  
        return
    
    #reset each individual v value for each axis
    def reset(self):
        self.vx.reset()
        self.vy.reset()
        self.vz.reset()
        return
    
    def update(self, vXnoise=None, vYnoise=None, vZnoise=None ):
        vx = self.vx.update(vXnoise)
        vy = self.vy.update(vYnoise)
        vz = self.vz.update(vZnoise)
        return vx, vy, vz
    

class SensorsModel():

    def __init__(self, aeroModel=VehicleAerodynamicsModel.VehicleAerodynamicsModel(), taugyro=VSC.gyro_tau, etagyro=VSC.gyro_eta, tauGPS=VSC.GPS_tau, etaGPSHorizontal=VSC.GPS_etaHorizontal, etaGPSVertical=VSC.GPS_etaVertical, gpsUpdateHz=VSC.GPS_rate):
        #as given in the lab manual, i am scared to change names of anything due to the test harnesses
        self.aero = aeroModel
        self.sensorsTrue = Sensors.vehicleSensors()
        self.sensorsBiases = Sensors.vehicleSensors()
        self.sensorsSigmas = Sensors.vehicleSensors()
        self.sensorsNoisy = Sensors.vehicleSensors()

        #call initialize functions
        self.sensorsBiases = self.initializeBiases()
        self.sensorsSigmas = self.initializeSigmas()

        self.gyro = GaussMarkovXYZ(tauX= taugyro, etaX=etagyro)
        self.GPS = GaussMarkovXYZ(tauX= tauGPS, etaX=etaGPSHorizontal, tauY= tauGPS, etaY= etaGPSVertical)
        #needs to match dynamic models
        self.dT = aeroModel.getVehicleDynamicsModel().dt
        

        self.updateTicks = 0
        self.gpsTickUpdate = (1/gpsUpdateHz)/self.dT

        return
    def initializeBiases(self, gyroBias=0.08726646259971647, accelBias=0.0, magBias=0.0, baroBias=0.0, pitotBias=20.0):
        #settiong up bias values based on a random unifrom range of given values
        bias = Sensors.vehicleSensors()
        bias.gyro_x = random.uniform(-gyroBias,gyroBias)
        bias.gyro_y = random.uniform(-gyroBias,gyroBias)
        bias.gyro_z = random.uniform(-gyroBias,gyroBias)

        bias.accel_x = random.uniform(-accelBias,accelBias)
        bias.accel_y = random.uniform(-accelBias,accelBias)
        bias.accel_z = random.uniform(-accelBias,accelBias)

        bias.mag_x = random.uniform(-magBias,magBias)
        bias.mag_y = random.uniform(-magBias,magBias)
        bias.mag_z = random.uniform(-magBias,magBias)
        
        bias.baro = random.uniform(-baroBias, baroBias)

        bias.pitot = random.uniform(-pitotBias, pitotBias)
        return bias
    def initializeSigmas(self, gyroSigma=0.002617993877991494, accelSigma=0.24525000000000002, magSigma=25.0, baroSigma=10.0, pitotSigma=2.0, gpsSigmaHorizontal=0.4, gpsSigmaVertical=0.7, gpsSigmaSOG=0.05, gpsSigmaCOG=0.002):
        #create all instances of sigma and assign to appropriate value
        sig = Sensors.vehicleSensors()
        sig.gyro_x =gyroSigma
        sig.gyro_z =gyroSigma
        sig.gyro_y =gyroSigma

        sig.accel_x =accelSigma
        sig.accel_z = accelSigma
        sig.accel_y =accelSigma

        sig.mag_x = magSigma
        sig.mag_z = magSigma
        sig.mag_y = magSigma

        sig.baro = baroSigma

        sig.pitot = pitotSigma

        sig.gps_e = gpsSigmaHorizontal
        sig.gps_n = gpsSigmaHorizontal
        sig.gps_alt = gpsSigmaVertical
        sig.gps_sog = gpsSigmaSOG
        sig.gps_cog = gpsSigmaCOG

        return sig

    def updateGPSTrue(self,state:States.vehicleState, dot):
        #beard chapter 7 eq 7.18, .19, .20
        n, e ,d = 0,0,0
        sog, cog = 0, 0
        n = state.pn
        e = state.pe
        d = -state.pd
        sog = math.hypot(dot.pn, dot.pe)
        cog = math.atan2(dot.pe, dot.pn)
        return n, e, d, sog, cog

    #equations found in beard chapter 7 page 122
    def updateAccelsTrue(self,state:States.vehicleState, dot: States.vehicleState):
        ax ,ay, az = 0,0,0
        ax = dot.u + state.q*state.w - state.r*state.v + VPC.g0*math.sin(state.pitch)
        ay = dot.v + state.r*state.u - state.p*state.w - VPC.g0*math.cos(state.pitch)*math.sin(state.roll)
        az = dot.w + state.p*state.v - state.q*state.u - VPC.g0*math.cos(state.pitch)*math.cos(state.roll)
        return ax,ay,az

    def updateMagsTrue(self,state):
        #beard chapter 7 eq 7.12
        MagT = MatrixMath.multiply(state.R,VSC.magfield)
        mx, my, mz = MagT[0][0], MagT[1][0],  MagT[2][0]
        return mx, my, mz
    
    def updateGyrosTrue(self, state):
        #lecture notes, lecture 6
        return state.p, state.q, state.r

    def updatePressureSensorsTrue(self,state:States.vehicleState):
        #beard chapter 7, eq7.7
        baro = VSC.Pground -VPC.rho *VPC.g0*(-state.pd)
        #beard chapter 7 eq7.1
        pinto = (VPC.rho*state.Va**2)/2
        return baro, pinto
    
    def updateSensorsTrue(self, prevTrueSensors, state, dot):
        #update all the sensors with their own update functions
        true = Sensors.vehicleSensors()
        true.accel_x, true.accel_y, true.accel_z = self.updateAccelsTrue(state, dot)
        true.mag_x, true.mag_y, true.mag_z = self.updateMagsTrue(state)
        true.gyro_x, true.gyro_y, true.gyro_z = self.updateGyrosTrue(state)
        true.baro, true.pitot = self.updatePressureSensorsTrue(state)

        #check for previous integer multiple of the update threshold else use previous gps values
        if self.updateTicks % self.gpsTickUpdate == 0:
            true.gps_n, true.gps_e, true.gps_alt, true.gps_sog, true.gps_cog = self.updateGPSTrue(state, dot)
        else:
            true.gps_n, true.gps_e, true.gps_alt, true.gps_sog, true.gps_cog = prevTrueSensors.gps_n, prevTrueSensors.gps_e, prevTrueSensors.gps_alt, prevTrueSensors.gps_sog, prevTrueSensors.gps_cog
        self.sensorsTrue = true

        return self.sensorsTrue
    
    def updateSensorsNoisy(self, trueSensors=Sensors.vehicleSensors(), noisySensors=Sensors.vehicleSensors(), sensorBiases=Sensors.vehicleSensors(), sensorSigmas=Sensors.vehicleSensors()):
        noisy = self.sensorsNoisy
        bias = sensorBiases
        true = trueSensors
        sig = sensorSigmas
        #need to add noise too all of the sensors now
        #add noise accel
        noisy.accel_x =  trueSensors.accel_x + bias.accel_x + random.gauss(0, sig.accel_x)
        noisy.accel_y =  trueSensors.accel_y + bias.accel_y + random.gauss(0, sig.accel_y)
        noisy.accel_z  = trueSensors.accel_z + bias.accel_z + random.gauss(0, sig.accel_z)
        #add noise mag
        noisy.mag_x = true.mag_x + bias.mag_x + random.gauss(0, sig.mag_x)
        noisy.mag_y = true.mag_y + bias.mag_y + random.gauss(0, sig.mag_y)
        noisy.mag_z = true.mag_z + bias.mag_z + random.gauss(0, sig.mag_z)
        #add noise gyro
        noisy.gyro_x = true.gyro_x + bias.gyro_x + self.gyro.vx.update()
        noisy.gyro_y = true.gyro_y + bias.gyro_y + self.gyro.vy.update()
        noisy.gyro_z = true.gyro_z + bias.gyro_z + self.gyro.vz.update()
        #add noise pressure
        noisy.baro = true.baro + bias.baro + random.gauss(0, sig.baro)
        noisy.pitot = true.pitot + bias.pitot + random.gauss(0,sig.pitot)

        #add noise gps check same condition from update true to apply ZOH
        if self.updateTicks % self.gpsTickUpdate == 0:
            noisy.gps_n = true.gps_n +self.GPS.vx.update() + random.gauss(0, sig.gps_n)
            noisy.gps_e = true.gps_e +self.GPS.vy.update() + random.gauss(0, sig.gps_e)
            noisy.gps_alt = true.gps_alt +self.GPS.vz.update() + random.gauss(0, sig.gps_alt)
            noisy.gps_sog = true.gps_sog + random.gauss(0,sig.gps_sog)
            noisy.gps_cog = true.gps_cog + random.gauss(0,sig.gps_cog)
        #already puts in previous values of gps if the statement above is not met
        self.sensorsNoisy = noisy
        return self.sensorsNoisy
    
    def update(self):
        state = self.aero.getVehicleState()
        dot = self.aero.getVehicleDynamicsModel().getVehicleDerivative(state)
        self.updateSensorsTrue(self.sensorsTrue, state, dot)
        self.updateSensorsNoisy(self.sensorsTrue, self.sensorsNoisy, self.sensorsBiases, self.sensorsSigmas)
        self.updateTicks +=1
        return
    
    def setSensorsTrue(self,sensorsTrue=Sensors.vehicleSensors()):
        self.sensorsTrue = sensorsTrue
        return
    def getSensorsTrue(self):
        return self.sensorsTrue
    def setSensorsNoisy(self, sensorsNoisy=Sensors.vehicleSensors()):
        self.sensorsNoisy = sensorsNoisy
        return
    def getSensorsNoisy(self):
        return self.sensorsNoisy
    
    def reset(self): 
        self.sensorsTrue = Sensors.vehicleSensors()
        self.sensorsBiases = Sensors.vehicleSensors()
        self.sensorsSigmas = Sensors.vehicleSensors()
        self.sensorsNoisy = Sensors.vehicleSensors()
        self.sensorsBiases = self.initializeBiases()
        self.sensorsSigmas = self.initializeSigmas()
        self.gyro = GaussMarkovXYZ.reset()
        self.GPS = GaussMarkovXYZ.reset()
        return