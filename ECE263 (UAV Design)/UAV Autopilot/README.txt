Enicolai
Evripides Nicolaides:

Lab 0:
Setting up rotation functions:
def ned2enu(points):
def euler2DCM(yaw, pitch, roll):
def dcm2Euler(DCM): #dcm 3x3 matrix
and the get points functions
def getNewPoints(self, x, y, z, yaw, pitch, roll):

Lab 1:
Class: VehicleDynamicsModel(dT=0.01)
    Variables:
        state – States.vehicleState (current vehicle state)
        dot – States.vehicleState (time derivative of state)
        dT – float (time step)
Methods:
    Parameters: dT (float, defaults to VPC.dT)
    Returns: None
    __init__(dT=0.01)

   Parameters:dT (float)
    state (States.vehicleState)
    dot (States.vehicleState) 
    Returns: States.vehicleState
ForwardEuler(dT, state, dot)

    Parameters:
    dT (float)
    state (States.vehicleState)
    dot (States.vehicleState)
    Returns: States.vehicleState
IntegrateState(dT, state, dot)

    Parameters:
    dT (float)
    state (States.vehicleState)
    dot (States.vehicleState)
    Returns: Rexp (matrix)
Rexp(dT, state, dot)


    Parameters:
    forcesMoments (Inputs.forcesMoments)
    Returns: None
    derivative(state, forcesMoments)
    Parameters:
    state (States.vehicleState)
    forcesMoments (Inputs.forcesMoments)
    Returns: States.vehicleState
Update(forcesMoments)

    Returns: States.vehicleState
getVehicleDerivative()

    Returns: States.vehicleState
getVehicleState()

    Returns: None
reset()

    Parameters:
    dot (States.vehicleState)
    Returns: None
setVehicleDerivative(dot)

    Parameters:
    state (States.vehicleState)
    Returns: None
setVehicleState(state)
