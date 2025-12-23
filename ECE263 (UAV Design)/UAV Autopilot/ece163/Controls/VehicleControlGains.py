import math
import pickle
from ece163.Modeling import VehicleAerodynamicsModel
from ece163.Constants import VehiclePhysicalConstants as VPC
from ece163.Containers import States
from ece163.Containers import Inputs
from ece163.Containers import Controls
from ece163.Containers import Linearized
from ece163.Utilities import MatrixMath
from ece163.Utilities import Rotations

"""
    Computes control gains using the tuning parameters outlined in Beard Chapter 6.
    Both the lateral and longitudinal gains are calculated.
    
    Parameters:
        tuningParameters (controlTuning): Contains desired bandwidth and damping.
        linearizedModel (transferFunctions): Contains the linearized UAV model.
    
    Returns:
        controlGains: An instance of controlGains with computed gain values.

        
		:param kp_roll: roll proportional gain
		:param kd_roll: roll derivative gain
		:param ki_roll: roll integral gain
		:param kp_sideslip: sideslip proportional gain
		:param ki_sideslip: sideslip integral gain
		:param kp_course: course proportional gain
		:param ki_course: course integral gain
		:param kp_pitch: pitch proportional gain
		:param kd_pitch: pitch derivative gain
		:param kp_altitude: altitude proportional gain
		:param ki_altitude: altitude integral gain
		:param kp_SpeedfromThrottle: airspeed (from throttle) proportional gain
		:param ki_SpeedfromThrottle: airspeed (from throttle) integral gain
		:param kp_SpeedfromElevator: airspeed (from elevator) proportional gain
		:param ki_SpeedfromElevator: airspeed (from elevator) integral gain
    """

def computeGains(tuningParameters=Controls.controlTuning(), linearizedModel=Linearized.transferFunctions()):
    gains = Controls.controlGains()

    gains.kp_roll = tuningParameters.Wn_roll**2/ linearizedModel.a_phi2
    gains.kd_roll= (2* (tuningParameters.Wn_roll* tuningParameters.Zeta_roll) - linearizedModel.a_phi1) / linearizedModel.a_phi2
    gains.ki_roll = 1e-3 #not sure why but its what is asked

    gains.kp_course = (2*tuningParameters.Zeta_course *tuningParameters.Wn_course * linearizedModel.Va_trim) / VPC.g0
    gains.ki_course = (tuningParameters.Wn_course**2) * linearizedModel.Va_trim / VPC.g0

    gains.ki_sideslip = (tuningParameters.Wn_sideslip**2)/ linearizedModel.a_beta2
    gains.kp_sideslip = ((2* tuningParameters.Zeta_sideslip * tuningParameters.Wn_sideslip) -linearizedModel.a_beta1) / linearizedModel.a_beta2
    
    gains.kp_pitch = (tuningParameters.Wn_pitch**2 - linearizedModel.a_theta2)/ linearizedModel.a_theta3
    gains.kd_pitch = ((2 * tuningParameters.Zeta_pitch * tuningParameters.Wn_pitch) - linearizedModel.a_theta1) / linearizedModel.a_theta3
    K_pitch_DC = (gains.kp_pitch * linearizedModel.a_theta3) / ( linearizedModel.a_theta2 + (gains.kp_pitch* linearizedModel.a_theta3))

    gains.kp_altitude = (2 * tuningParameters.Zeta_altitude * tuningParameters.Wn_altitude)/ (K_pitch_DC * linearizedModel.Va_trim)
    gains.ki_altitude = (tuningParameters.Wn_altitude**2)/ (K_pitch_DC* linearizedModel.Va_trim)

    gains.kp_SpeedfromElevator = (linearizedModel.a_V1 - (2 * tuningParameters.Zeta_SpeedfromElevator * tuningParameters.Wn_SpeedfromElevator))/ (K_pitch_DC * VPC.g0)
    gains.ki_SpeedfromElevator = -(tuningParameters.Wn_SpeedfromElevator**2)/ (K_pitch_DC* VPC.g0)

    gains.kp_SpeedfromThrottle = (( 2* tuningParameters.Zeta_SpeedfromThrottle* tuningParameters.Wn_SpeedfromThrottle) - linearizedModel.a_V1) / linearizedModel.a_V2
    gains.ki_SpeedfromThrottle = (tuningParameters.Wn_SpeedfromThrottle**2)/linearizedModel.a_V2

    return gains

"""     self.Wn_roll  = Wn_roll 
		self.Zeta_roll  = Zeta_roll 
		self.Wn_course  = Wn_course 	# Wn_roll should be 5-10x larger
		self.Zeta_course  = Zeta_course 
		self.Wn_sideslip  = Wn_sideslip 
		self.Zeta_sideslip  = Zeta_sideslip 
		#tuning knobs for longitudinal control
		self.Wn_pitch  = Wn_pitch 
		self.Zeta_pitch  = Zeta_pitch 
		self.Wn_altitude  = Wn_altitude 	# Wn_pitch should be 5-10x larger
		self.Zeta_altitude  = Zeta_altitude 
		self.Wn_SpeedfromThrottle  = Wn_SpeedfromThrottle 
		self.Zeta_SpeedfromThrottle  = Zeta_SpeedfromThrottle 
		self.Wn_SpeedfromElevator  = Wn_SpeedfromElevator 
		self.Zeta_SpeedfromElevator  = Zeta_SpeedfromElevator """
def computeTuningParameters(controlGains=Controls.controlGains(), linearizedModel=Linearized.transferFunctions()):

    try: 
        tuning = Controls.controlTuning()

        tuning.Wn_roll = math.sqrt(controlGains.kp_roll * linearizedModel.a_phi2)
        tuning.Zeta_roll = (linearizedModel.a_phi1 + (linearizedModel.a_phi2* controlGains.kd_roll))/ (tuning.Wn_roll*2)
         
        tuning.Wn_course = math.sqrt(VPC.g0/linearizedModel.Va_trim *controlGains.ki_course)
        tuning.Zeta_course = (controlGains.kp_course * VPC.g0) / (2 * linearizedModel.Va_trim * tuning.Wn_course)
        
        tuning.Wn_sideslip = math.sqrt(linearizedModel.a_beta2 * controlGains.ki_sideslip)
        tuning.Zeta_sideslip = (linearizedModel.a_beta1 + (linearizedModel.a_beta2* controlGains.kp_sideslip))/ (2* tuning.Wn_sideslip)
         
        tuning.Wn_pitch = math.sqrt(linearizedModel.a_theta2 + (linearizedModel.a_theta3 * controlGains.kp_pitch))
        tuning.Zeta_pitch = (linearizedModel.a_theta1 + (controlGains.kd_pitch * linearizedModel.a_theta3))/ (2 * tuning.Wn_pitch)
       
        #K_pitch_DC = (gains.kp_pitch * linearizedModel.a_theta3) / ( linearizedModel.a_theta2 + (gains.kp_pitch* linearizedModel.a_theta3))
        K_pitch_DC = (controlGains.kp_pitch * linearizedModel.a_theta3)/ (linearizedModel.a_theta2 + (controlGains.kp_pitch * linearizedModel.a_theta3))

        tuning.Wn_altitude = math.sqrt(K_pitch_DC * linearizedModel.Va_trim * controlGains.ki_altitude)
        tuning.Zeta_altitude = (K_pitch_DC * linearizedModel.Va_trim * controlGains.kp_altitude) / (2 * tuning.Wn_altitude)
         
        tuning.Wn_SpeedfromElevator = math.sqrt(- K_pitch_DC * VPC.g0 * controlGains.ki_SpeedfromElevator)
        tuning.Zeta_SpeedfromElevator = (linearizedModel.a_V1- (K_pitch_DC* VPC.g0 * controlGains.kp_SpeedfromElevator))/ (2 * tuning.Wn_SpeedfromElevator)
         
        tuning.Wn_SpeedfromThrottle = math.sqrt( linearizedModel.a_V2 * controlGains.ki_SpeedfromThrottle)
        tuning.Zeta_SpeedfromThrottle = (linearizedModel.a_V1 + (linearizedModel.a_V2 * controlGains.kp_SpeedfromThrottle)) / (2 * tuning.Wn_SpeedfromThrottle)

        
        return tuning
    
    except:
        tuning = Controls.controlTuning()
        return tuning

    