import math
from ece163.Modeling import VehicleAerodynamicsModel
from ece163.Constants import VehiclePhysicalConstants as VPC
from ece163.Containers import States
from ece163.Containers import Inputs
from ece163.Containers import Linearized
from ece163.Utilities import MatrixMath


"""Evripides Nicolaides, 
    enioclai@ucsc.edu
    VehiclePerturabationModel"""
def CreateTransferFunction(trimState, trimInputs):
    #transferFunction = Linearized.transferFunctions()

    #all definitions gotten from beard Chapter 5
    Aphi1 = (-1/4)*VPC.rho*trimState.Va *VPC.S *(VPC.b**2) * VPC.Cpp
    Aphi2 = (0.5) * VPC.rho * (trimState.Va**2) * VPC.S * VPC.b * VPC.CpdeltaA
    ABeta1 = ((-VPC.rho * trimState.Va * VPC.S)/ (2* VPC.mass) ) * VPC.CYbeta
    Abeta2 = ((VPC.rho * trimState.Va * VPC.S)/ (2* VPC.mass) ) * VPC.CYdeltaR
    A81 = ((-VPC.rho * trimState.Va**2 *VPC.c *VPC.S) / (2 * VPC.Jyy)) * ((VPC.CMq * VPC.c )/ (2 * trimState.Va))
    A82 = ((-VPC.rho * trimState.Va**2 *VPC.c *VPC.S * VPC.CMalpha) / (2 * VPC.Jyy))
    A83 = ((VPC.rho * trimState.Va**2 *VPC.c *VPC.S * VPC.CMdeltaE) / (2 * VPC.Jyy))

    #define variables needed for Av1-3
    Va = math.hypot(trimState.u, trimState.v, trimState.w)
    dt_Dva = dThrust_dVa(Va, trimInputs.Throttle, epsilon=0.5)
    dt_Dthrottle = dThrust_dThrottle(Va, trimInputs.Throttle,epsilon=0.01 )
    
    Av1 = ((VPC.rho* Va * VPC.S)/ VPC.mass) *( VPC.CD0  + VPC.CDalpha* trimState.alpha + VPC.CDdeltaE * trimInputs.Elevator)- (dt_Dva/VPC.mass)
    Av2 = (dt_Dthrottle/VPC.mass)
    Av3 = VPC.g0 * math.cos(trimState.pitch - trimState.alpha)
    #def __init__(self, Va_trim = Va, alpha_trim =trimState.alpha, beta_trim = trimState.beta, gamma_trim = (trimState.pitch- trimState.alpha), theta_trim =  trimState.roll, phi_trim = trimState.pitch, 
    # a_phi1 = Aphi1, a_phi2 =Aphi2, a_beta1 =ABeta1, a_beta2 = ABeta2, a_theta1 =A81, a_theta2 = A82, a_theta3 = A813, a_V1 = Av1, a_V2 = Av2, a_V3 =Av3):
    transferFunction = Linearized.transferFunctions(Va, trimState.alpha, trimState.beta, (trimState.pitch- trimState.alpha), trimState.pitch, trimState.roll, Aphi1, Aphi2, ABeta1, Abeta2, A81, A82, A83, 
                        Av1, Av2, Av3)

    return transferFunction

def dThrust_dThrottle(Va, Throttle, epsilon=0.01):
    VAM = VehicleAerodynamicsModel.VehicleAerodynamicsModel()
    Fxplus = VAM.CalculatePropForces(Va, Throttle + epsilon)[0] #only want the force not the moment
    Fx = VAM.CalculatePropForces(Va, Throttle)[0] #same here
    dTdDeltaT = (Fxplus - Fx) / epsilon

    return dTdDeltaT

def dThrust_dVa(Va, Throttle, epsilon=0.5):
    VAM = VehicleAerodynamicsModel.VehicleAerodynamicsModel()
    Fxplus = VAM.CalculatePropForces(Va + epsilon, Throttle)[0] #only want the force not the moment
    Fx = VAM.CalculatePropForces(Va, Throttle)[0] #same here
    dTdVa = (Fxplus - Fx) / epsilon
    return dTdVa