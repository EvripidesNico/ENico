import math
from ..Containers import States
from ..Utilities import MatrixMath
from ..Utilities import Rotations
from ..Constants import VehiclePhysicalConstants as VPC


class VehicleDynamicsModel( ):
    

#at minimum the init should include an instance of the Containers.states.vehicleState class to maintain vechicle state and a second instance to maintain dervivative
    def __init__(self, dt = VPC.dT):
       # print("Initializing VehicleDynamicsModel...") 
        self.dt = dt
        self.state = States.vehicleState() #vechile state instance
        self.dot = States.vehicleState()   #vehicle dervivative instance
        
        return 

#should reset the state variables including the derivative variable to 0
    def reset(self):
        self.state = States.vehicleState() #vechile state instance
        self.dot = States.vehicleState()   #vehicle dervivative instance
        return

    def setVehicleState(self, state):
        if isinstance(state,States.vehicleState):
            self.state = state
        return

    def getVehicleState(self):
        return self.state #(from class vehicleState)

    def setVehicleDerivative(self, dot):
        if isinstance(dot,States.vehicleState):
            self.dot = dot
        return 

    def getVehicleDerivative(self, state):
        return self.dot #( an instance of Containers.States.vehicleState)

    def Update(self, forcesMoments):
        #compute derivativce
        #integrate state
        #forawrd euler
        #REXP
        #update everyhting
        #return new state with updates
        self.dot = self.derivative(self.state, forcesMoments)
        newState = self.IntegrateState(self.dt, self.state, self.dot)
        self.state = newState
        #is it just that simple
        return 

    def Rexp(self, dT, state, dot):

        I = [[1,0,0],[0,1,0],[0,0,1]]

        mid_p = state.p + (dT/2)* dot.p
        mid_q = state.q + (dT/2)* dot.q
        mid_r = state.r + (dT/2)* dot.r

        magW = math.hypot(mid_p,mid_q,mid_r)
        wCross = MatrixMath.skew(mid_p,mid_q,mid_r)
        wCross2 = MatrixMath.multiply(wCross,wCross)
        
        #check if ||w|| is within 0-0.2 which would require subsituation
        if magW > 0.1 :
            A = math.sin(magW * dT)/magW
            B = (1 - math.cos(magW* dT))/magW**2
        else:
            A = dT -(((dT**3) * (magW**2) )/6) +(((dT**5) * (magW**4))/120)
        
            B = (dT**2/2) - (((dT**4) * (magW**2) )/24) + (((dT**6) * (magW**4))/720)
        diff = MatrixMath.subtract(I,MatrixMath.scalarMultiply(A, wCross))
        Rexp =  MatrixMath.add(diff,MatrixMath.scalarMultiply(B,wCross2) )
      
        return Rexp #Rexp: the matrix exponential to update the state

    def derivative(self, state, forcesMoments):
        deriv = States.vehicleState() #set up output state for derivatives
        #d/dt Pned = R transpose * UVW
        Rt = MatrixMath.transpose(state.R)
        uvw = [[state.u],[state.v],[state.w]]
        Pned = MatrixMath.multiply(Rt,uvw)
        deriv.pn = Pned[0][0]
        deriv.pe = Pned[1][0]
        deriv.pd = Pned[2][0]

        #d/dt UVW = 1/m *F -wx*UVW
        wx = MatrixMath.skew(state.p,state.q,state.r) #set up cross product
        Force = [[forcesMoments.Fx],[forcesMoments.Fy],[forcesMoments.Fz]]

        DotUVW = MatrixMath.subtract(MatrixMath.scalarDivide(VPC.mass,Force),MatrixMath.multiply(wx, uvw)) 
        deriv.u = DotUVW[0][0]
        deriv.v = DotUVW[1][0]
        deriv.w = DotUVW[2][0]

        #d/dt φθψ = [....]*PQR
        PQR = [[state.p],[state.q],[state.r]]
        rotationMatrix = [[1, math.sin(state.roll)*math.tan(state.pitch),math.cos(state.roll)*math.tan(state.pitch)],
                          [0, math.cos(state.roll),-math.sin(state.roll)],
                          [0, math.sin(state.roll)/math.cos(state.pitch), math.cos(state.roll)/math.cos(state.pitch)]]
        #might need to change the rate of the divisions to sec instead of cos
        EulerAngles = MatrixMath.multiply(rotationMatrix, PQR)
        deriv.pitch = EulerAngles[1][0]
        deriv.roll = EulerAngles[0][0]
        deriv.yaw = EulerAngles[2][0]
        #PQR = 
        #J^-1 [-(wx)*J*PQR+(lmn)]
    
        M = [[forcesMoments.Mx],[forcesMoments.My],[forcesMoments.Mz]]
        Jw = MatrixMath.multiply(VPC.Jbody, PQR)
        Jwx = MatrixMath.multiply(wx, Jw)
        Jwx = MatrixMath.scalarMultiply(-1,Jwx)
        JwxM = MatrixMath.add(Jwx,M)
        PQRdot = MatrixMath.multiply(VPC.JinvBody,JwxM)
        deriv.p = PQRdot[0][0]
        deriv.q = PQRdot[1][0]
        deriv.r = PQRdot[2][0]
        
        #D/dtR = -wx*R
        deriv.R = MatrixMath.multiply(MatrixMath.scalarMultiply(-1,wx),state.R)

        return deriv  #the current time derivative, in the form of a States.vehicleState object

    def ForwardEuler(self, dT, state, dot):
        euler = States.vehicleState()

        euler.pn = state.pn + dot.pn*dT
        euler.pe = state.pe + dot.pe*dT
        euler.pd = state.pd + dot.pd*dT
        euler.u = state.u + dot.u*dT
        euler.v = state.v + dot.v*dT
        euler.w = state.w + dot.w*dT
        euler.p = state.p + dot.p*dT
        euler.q = state.q + dot.q*dT
        euler.r = state.r + dot.r*dT

        return euler #return new state, advanced by a timestep of dt (defined in states.vechicleState class)

    def IntegrateState(self, dT, state, dot):
        integ = States.vehicleState()
        integ = VehicleDynamicsModel.ForwardEuler(self, dT,state,dot)

        exp = VehicleDynamicsModel.Rexp(self, dT, state, dot)

        integ.R = MatrixMath.multiply(exp,state.R)
        integ.yaw,integ.pitch,integ.roll = Rotations.dcm2Euler(integ.R)

        integ.alpha = state.alpha
        integ.beta = state.beta
        integ.Va = state.Va
        integ.chi = math.atan2(dot.pe,dot.pn)


        return integ #new state, advanced by a timestep of dT, returned as an instance of the States.vehicleState class 
    """
        Defines the vehicle states to define the vehicle current position and orientation. Positions are in NED
        coordinates, velocity is ground speed in body coordinates, we carry both the Euler angles and the DCM together,
        and the rotation rates are in the body frame. If DCM is used in initialization then Euler angles are computed from
        the provided DCM, otherwise the DCM is computed from the Euler Angles (DCM will overwrite Euler Angles).

        :param pn: vehicle inertial north position [m]
        :param pe: vehicle inertial east position [m]
        :param pd: vehicle inertial down position [m] (Altitude is -pd)
        :param u: vehicle ground speed in body frame x [m/s]
        :param v: vehicle ground speed in body frame y [m/s]
        :param w: vehicle ground speed in body frame z [m/s]
        :param yaw: yaw angle [rad]
        :param pitch: pitch angle [rad]
        :param roll: roll angle [rad]
        :param p: body roll rate about body-x axis [rad/s]
        :param q: body pitch rate about body-y axis [rad/s]
        :param r: body yaw rate about body-z axis [rad/s]
        :param dcm: direction cosine matrix (R) which transforms from inertial to body frame

        :return: None
        """