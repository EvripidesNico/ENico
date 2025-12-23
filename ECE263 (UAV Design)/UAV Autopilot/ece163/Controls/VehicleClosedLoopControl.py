import math
import sys
import ece163.Containers.Inputs as Inputs
import ece163.Containers.Controls as Controls
import ece163.Containers.States as States
import ece163.Constants.VehiclePhysicalConstants as VPC
import ece163.Modeling.VehicleAerodynamicsModel as VAM
import ece163.Controls.VehicleEstimator as VehicleEstimator
import ece163.Sensors.SensorsModel as SensorsModel


class PDControl():

    def __init__(self, kp=0.0, kd=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.kp = kp
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        
        return
    
    def setPDGains(self, kp=0.0, kd=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.kp = kp
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        return
    
    def Update(self, command=0.0, current=0.0, derivative=0.0):
        err = command - current
        u = self.trim + (self.kp * err) - (self.kd * derivative)

        #check for saturation low and high
        #set to abosulute min or max depending on saturation
        if u > self.highLimit:
            u = self.highLimit
        elif u < self.lowLimit:
            u = self.lowLimit

        return u

class PIControl():
    def __init__(self, dT=VPC.dT, kp=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        self.accoumul = 0.0
        self.prevErr = 0.0 #initialize error for accoumul calc

        return
    def setPIGains(self, dT=VPC.dT, kp=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        return
    def Update(self, command=0.0, current=0.0):
        #method for PID but i am assuming it should be done here as well since we have an I term
        error = command - current

        self.accoumul += 0.5 * self.ki * self.dT  * (error + self.prevErr)

        u = self.trim + self.kp * error + self.accoumul

        if u > self.highLimit:
            u = self.highLimit
            # no additional error accumulation
            self.accoumul -= 0.5 * self.ki * self.dT  * (error + self.prevErr)
        elif u < self.lowLimit:
            u = self.lowLimit
            self.accoumul -= 0.5 * self.ki * self.dT  * (error + self.prevErr)
        #update error tracker for accumulation
        self.prevErr = error

        return u
    def resetIntegrator(self):
        self.accoumul = 0.0
        return
    

class PIDControl():
    def __init__(self, dT=VPC.dT, kp=0.0, kd=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        self.accoumul = 0.0
        self.prevErr = 0.0 #initialize error for accoumul calc
        return
    
    def setPIDGains(self, dT=VPC.dT, kp=0.0, kd=0.0, ki=0.0, trim=0.0, lowLimit=0.0, highLimit=0.0):
        self.dT = dT
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.trim = trim
        self.lowLimit = lowLimit
        self.highLimit = highLimit
        return
    
    def Update(self, command=0.0, current=0.0, derivative=0.0):
        error = command - current
        self.accoumul +=  0.5* self.dT * (error + self.prevErr)

        u = self.kp*error + self.ki * self.accoumul - self.kd * derivative + self.trim

        if u > self.highLimit:
            u = self.highLimit
            # no additional error accumulation
            self.accoumul -= 0.5  * self.dT  * (error + self.prevErr)
        elif u < self.lowLimit:
            u = self.lowLimit
            self.accoumul -= 0.5 * self.dT  * (error + self.prevErr)

        self.prevErr = error

        return u 
    
    def resetIntegrator(self):
        self.accoumul = 0.0
        return
    


class VehicleClosedLoopControl():
    def __init__(self, dT=0.01, rudderControlSource='SIDESLIP', useSensors=False, useEstimator=False  ):
        self.plant = VAM.VehicleAerodynamicsModel()
        self.controlGains = Controls.controlGains()
        self.trim = Inputs.controlInputs()
        self.control = Inputs.controlInputs()
        self.dt = dT
        self.mode = Controls.AltitudeStates.HOLDING
        self.rollFromCourse = PIControl()
        self.rudderFromSideslip = PIControl()
        self.throttleFromAirspeed = PIControl()
        self.pitchFromAltitude = PIControl()
        self.pitchFromAirspeed = PIControl()
        self.elevatorFromPitch = PDControl()
        self.aileronFromRoll = PIDControl()
        self.update = self.Update
        self.useSensors = useSensors
        if self.useSensors: 
            self.sensorsModel = SensorsModel.SensorsModel(aeroModel=self.plant)
        
        return
    def UpdateControlCommands(self, referenceCommands: Controls.referenceCommands, state: States.vehicleState):
        
        upper_thresh = referenceCommands.commandedAltitude + VPC.altitudeHoldZone 
        lower_thresh = referenceCommands.commandedAltitude - VPC.altitudeHoldZone
        #state machine or something

        #detrimine state
        if self.mode == Controls.AltitudeStates.HOLDING:
            #go to descending
            if -state.pd > upper_thresh:
                self.mode = Controls.AltitudeStates.DESCENDING
                self.pitchFromAltitude.resetIntegrator()
            #go to climbing
            elif -state.pd < lower_thresh:
                self.mode = Controls.AltitudeStates.CLIMBING
                self.pitchFromAltitude.resetIntegrator()
        
        #if in climnbing
        if self.mode == Controls.AltitudeStates.CLIMBING:
            if lower_thresh < -state.pd and -state.pd < upper_thresh:
                self.mode = Controls.AltitudeStates.HOLDING
                self.pitchFromAirspeed.resetIntegrator()
        
        #check descending
        elif self.mode == Controls.AltitudeStates.DESCENDING:
            if lower_thresh < -state.pd and -state.pd < upper_thresh:

                self.mode = Controls.AltitudeStates.HOLDING
                self.pitchFromAirspeed.resetIntegrator()

        #checking chi
        chi_error = referenceCommands.commandedCourse - state.chi
        if chi_error >= math.pi:
            state.chi += 2* math.pi
        elif chi_error <= -math.pi:
            state.chi -= 2*math.pi
                    
        #states have been determined  apply calculations based on state
        if self.mode == Controls.AltitudeStates.HOLDING:
            pitchCommand = self.pitchFromAltitude.Update(referenceCommands.commandedAltitude, -state.pd)
            throttleCommand = self.throttleFromAirspeed.Update(referenceCommands.commandedAirspeed, state.Va)
        
        elif self.mode == Controls.AltitudeStates.CLIMBING:
            pitchCommand = self.pitchFromAirspeed.Update(referenceCommands.commandedAirspeed, state.Va)
            throttleCommand = VPC.maxControls.Throttle
        
        elif self.mode == Controls.AltitudeStates.DESCENDING:
            pitchCommand = self.pitchFromAirspeed.Update(referenceCommands.commandedAirspeed, state.Va)
            throttleCommand = VPC.minControls.Throttle

        rollCommand = self.rollFromCourse.Update(referenceCommands.commandedCourse, state.chi)
        rudderCommand = self.rudderFromSideslip.Update(0.0, state.beta)
        aileronCommand = self.aileronFromRoll.Update(rollCommand, state.roll, state.p)
        elevatorCommand = self.elevatorFromPitch.Update(pitchCommand, state.pitch, state.q)

        #GUI update
        referenceCommands.commandedRoll = rollCommand
        referenceCommands.commandedPitch = pitchCommand

        autopilot = Inputs.controlInputs(Throttle= throttleCommand, Aileron= aileronCommand, Elevator= elevatorCommand, Rudder= rudderCommand)
        return autopilot
    

    def getControlGains(self):
        return self.controlGains
    
    def getSensorsModel(self):
        if self.sensorsModel:
            return self.sensorsModel
        return

    def getTrimInputs(self):
        return self.trim
    def getVehicleAerodynamicsModel(self):
        return self.plant
    def getVehicleControlSurfaces(self):
        return self.control
    
    #def getVehicleEstimator(self):
    #    return 
    
    def getVehicleState(self):
        return self.plant.getVehicleState()
    
    def reset(self):
        self.rollFromCourse.resetIntegrator()
        self.rudderFromSideslip.resetIntegrator()
        self.throttleFromAirspeed.resetIntegrator()
        self.pitchFromAltitude.resetIntegrator()
        self.pitchFromAirspeed.resetIntegrator()
        self.aileronFromRoll.resetIntegrator()
        self.plant.reset()
        if self.useSensors:
            self.sensorsModel.reset()

        return
    
    def setControlGains(self, controlGains=Controls.controlGains()):
        self.controlGains = controlGains # save for later use
        piCourseLow = -math.radians(VPC.bankAngleLimit)
        piCourseHigh = math.radians(VPC.bankAngleLimit)
        self.rollFromCourse.setPIGains(dT=VPC.dT,kp = controlGains.kp_course, ki= controlGains.ki_course, trim=0.0,lowLimit= piCourseLow, highLimit= piCourseHigh)
        
        piSideLow = VPC.minControls.Rudder
        piSideHigh = VPC.maxControls.Rudder
        self.rudderFromSideslip.setPIGains(kp= controlGains.kp_sideslip, ki= controlGains.ki_sideslip, trim= self.trim.Rudder, lowLimit= piSideLow, highLimit= piSideHigh)
        
        self.throttleFromAirspeed.setPIGains(kp = controlGains.kp_SpeedfromThrottle, ki= controlGains.ki_SpeedfromThrottle,trim=self.trim.Throttle, lowLimit= VPC.minControls.Throttle, highLimit=VPC.maxControls.Throttle)
        
        piheightMin = -math.radians(VPC.pitchAngleLimit)
        piheightMax = math.radians(VPC.pitchAngleLimit)
        self.pitchFromAltitude.setPIGains(kp= controlGains.kp_altitude, ki= controlGains.ki_altitude, lowLimit= piheightMin, highLimit= piheightMax)
        
        piairspeedLow = -math.radians(VPC.pitchAngleLimit)
        piairspeedHigh = math.radians(VPC.pitchAngleLimit)
        self.pitchFromAirspeed.setPIGains(kp= controlGains.kp_SpeedfromElevator, ki= controlGains.ki_SpeedfromElevator, lowLimit=piairspeedLow, highLimit= piairspeedHigh)
        
        self.elevatorFromPitch.setPDGains(kp = controlGains.kp_pitch, kd= controlGains.kd_pitch, trim = self.trim.Elevator,lowLimit= VPC.minControls.Elevator, highLimit= VPC.maxControls.Elevator)
        
        self.aileronFromRoll.setPIDGains(kp= controlGains.kp_roll, kd= controlGains.kd_roll, ki= controlGains.ki_roll,trim= self.trim.Aileron, lowLimit= VPC.minControls.Aileron, highLimit= VPC.maxControls.Aileron)
         
        return
    
    def setTrimInputs(self, trimInputs= Inputs.controlInputs(Throttle=0.5, Aileron=0.0, Elevator=0.0, Rudder=0.0)):
        self.trim = trimInputs
        return
    
    def setVehicleState(self, state):
        self.plant.setVehicleState(state)
        return
    
    def Update(self, referenceCommands=Controls.referenceCommands):
        self.controls = self.UpdateControlCommands(referenceCommands=referenceCommands, state=self.getVehicleState())
        self.plant.Update(self.controls)
        if self.useSensors:
            self.sensorsModel.update()
        return
    

    