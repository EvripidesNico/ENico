import math
from ..Containers import States
from ..Containers import Inputs
from ..Modeling import VehicleDynamicsModel
from ..Modeling import WindModel
from ..Utilities import MatrixMath
from ..Utilities import Rotations
from ..Constants import VehiclePhysicalConstants as VPC


class VehicleAerodynamicsModel():

    def __init__(self, initialSpeed = 25.0, initialHeight =-100):
         # print("Initializing VehicleDynamicsModel...") 
        #self.dt = dt
        self.AerodynamicsState = VehicleDynamicsModel.VehicleDynamicsModel() #vechile state instance
        
        self.AerodynamicsState.state.u = initialSpeed
        self.AerodynamicsState.state.pd = initialHeight

        self.initialSpeed = initialSpeed
        self.initialHeight = initialHeight
        #i think we need this for later
        self.WindModel = WindModel.WindModel()

        return
    
    def reset(self):
        #vechile state instance
        self.AerodynamicsState.reset()
        self.AerodynamicsState.state.u =self.initialSpeed
        self.AerodynamicsState.state.pd =self.initialHeight
        self.WindModel = WindModel.WindModel()

        return
    
    def getVehicleState(self):
        return self.AerodynamicsState.state
    
    def getVehicleDynamicsModel(self):
        return self.AerodynamicsState
    
 
    
    def setVehicleState(self,state):
        self.AerodynamicsState.state = state    
        return
    
    
    def getWindModel(self):
        return self.WindModel
   
    def setWindModel(self, windModel):
        self.WindModel = windModel
        return
    #Dont do the this
    #we do this now :-)
    def CalculateAirspeed(self, state, wind = States.windState()):
        Va, alpha, beta = 0, 0, 0
        #get velocities and winds into a vector
        UVW = [[state.u],[state.v],[state.w]]
        Wned = [[wind.Wn], [wind.We], [wind.Wd]]
        Wuvw = [[wind.Wu],[wind.Wv],[wind.Ww]]

        #need to establish 2 rotation matrixs and then we can math up
        XiW = math.atan2(wind.We,wind.Wn)
        Ws = math.hypot(wind.Wn,wind.We,wind.Wd)
        #check for division by 0
        if(Ws != 0):
            
            GammaW = -math.asin(wind.Wd/Ws)
        else:
            GammaW = 0
        #get DCM from gamma and xi
        #i believe this sohuld do the trick for the DCM
        #GX_DCM = Rotations.euler2DCM(yaw = XiW, pitch = Ws, roll=0 )
        GX_DCM = [[math.cos(XiW)*math.cos(GammaW), math.sin(XiW)*math.cos(GammaW),-math.sin(GammaW)],
                  [-math.sin(XiW), math.cos(XiW), 0],
                  [math.cos(XiW)*math.sin(GammaW), math.sin(XiW)*math.sin(GammaW), math.cos(GammaW)]]
        GX_DCM = MatrixMath.transpose(GX_DCM)
        #math time
        #VaVec = MatrixMath.subtract(UVW,MatrixMath.multiply(state.R, MatrixMath.add(Wned, MatrixMath.multiply(GX_DCM, Wuvw))))
        Wintertial = MatrixMath.add(Wned, MatrixMath.multiply(GX_DCM,Wuvw))
        Wbody = MatrixMath.multiply(state.R, Wintertial)
        VaVec = MatrixMath.subtract(UVW,Wbody)
        #check for 0
        
        alpha = math.atan2(VaVec[2][0],VaVec[0][0])
    
        Va = math.hypot(VaVec[0][0],VaVec[1][0],VaVec[2][0])
        #check for 0
        if(Va == 0):
            beta = 0
        else:
            beta = math.asin(VaVec[1][0]/Va)
            
        return Va, alpha, beta
    

    #takes in alpha value and generates CL, CM, CD alpha coefficients
    def CalculateCoeff_alpha(self, alpha):
        CL, CD, CM = 0,0,0
        CL0, CLalpha = VPC.CL0, VPC.CLalpha
        CM0, CMalpha = VPC.CM0, VPC.CMalpha
        CDp =VPC.CDp
        AR = VPC.AR
        e = VPC.e
        M = VPC.M
        alpha0 = VPC.alpha0
        #pre and post stall models
        CLattached = CL0 + CLalpha * alpha
        CDattached = CDp + ((CLattached)**2)/(math.pi *AR*e)
        CLseperated = 2*math.sin(alpha)*math.cos(alpha)
        CDseperated = 2*(math.sin(alpha)**2)

        #blending fn to combine pre and post stall models
        sigma = ((1 + math.exp(-M*(alpha- alpha0))) + (math.exp(M*(alpha + alpha0)))) / ((1+math.exp(-M*(alpha- alpha0)))*(1+math.exp(M*(alpha+ alpha0))))

        #Coefficient of Lift, CL_alpha (unitless), Coefficient of Drag, CD_alpha (unitless), Coefficient of Moment, CM_alpha (unitless)
        CL = (1- sigma) * CLattached + (sigma*CLseperated)
        CD = (1- sigma) * CDattached + (sigma*CDseperated)

        CM = CM0 + CMalpha * alpha

        return CL, CD, CM
    
    #takes in Va, and Throttle and Fx propeller force and Mx Propeller
    def CalculatePropForces(self, Va, Throttle):
        Fx_prop, Mx_prop = 0,0
        #VPC variables
        Dprop, rho = VPC.D_prop, VPC.rho, 
        CT0, CT1, CT2 = VPC.C_T0, VPC.C_T1, VPC.C_T2
        CQ0, CQ1, CQ2 = VPC.C_Q0, VPC.C_Q1, VPC.C_Q2
        Vin = Throttle*VPC.V_max
        KT = 60 / (2*math.pi*VPC.KV)
        KE = KT
        #Omega = uadradic formula
        a = (rho*(Dprop**5)*CQ0)/(4*math.pi**2)
        b = (rho* (Dprop**4)*Va*CQ1)/(2*math.pi) + ((KT*KE)/VPC.R_motor)
        c = (rho * (Dprop**3)*(Va**2)*CQ2) - (KT*(Vin / VPC.R_motor)) + (KT * VPC.i0)

        #check imaginary
        dis = b**2 - 4*a*c
        if dis < 0:
            omega = 100
        else:
            omega = ((-b) + math.sqrt(dis)) / (2*a)

        #lets calculate J = 2piVa/omegaDprop
        J = (2*math.pi*Va)/ (omega*Dprop)
        #calculate Ct(J) and Cq(J)

        CT = CT0 + (CT1*J)+ (CT2 * J**2)
        CQ = CQ0 + (CQ1*J)+ (CQ2 *J**2)

        #caluclate MX and FX
        Fx_prop = (rho*(omega**2)*(Dprop**4)*CT)/(4*math.pi**2)
        Mx_prop = -(rho*(omega**2)*(Dprop**5)*CQ)/(4*math.pi**2)
        return Fx_prop, Mx_prop
    
    #update state and forcemoments
    def Update(self, controls):
        wind = self.WindModel.getWind()
        state = self.getVehicleState()

        forceMoments =  self.updateForces(state,controls, wind = wind)
        self.AerodynamicsState.Update(forceMoments)
        #need to update windmodel as well
        
        return
    
    #Update all forces based on our 3 force functions (aero,grav, control)
    def updateForces(self, state, controls, wind=None):
        #calculate alpha,beta, and Va
        if(wind != 0):
            self.AerodynamicsState.state.Va,  self.AerodynamicsState.state.alpha,  self.AerodynamicsState.state.beta = self.CalculateAirspeed(state,wind)


        else:
            self.AerodynamicsState.state.alpha = math.atan2(state.w,state.u)
            self.AerodynamicsState.state.Va = math.hypot(state.u,state.v,state.w)
            
            #confirm Va != 0 to make sure no division by 0 happens
            if self.AerodynamicsState.state.Va != 0.0 :
                self.AerodynamicsState.state.beta = math.asin(state.v/self.AerodynamicsState.state.Va)
            else:
                self.AerodynamicsState.state.beta = 0

        #get all forces and sum them up
        force = Inputs.forcesMoments()
        grav = Inputs.forcesMoments()
        con = Inputs.forcesMoments()
        aero = Inputs.forcesMoments()
    
        aero = self.aeroForces(state)
        con = self.controlForces(state,controls)
        grav = self.gravityForces(state)

        force.Fx = grav.Fx + con.Fx + aero.Fx 
        force.Fy = grav.Fy + con.Fy + aero.Fy 
        force.Fz = grav.Fz + con.Fz + aero.Fz
        force.Mx = grav.Mx + con.Mx + aero.Mx 
        force.My = grav.My + con.My + aero.My 
        force.Mz = grav.Mz + con.Mz + aero.Mz 

        return force #return total forces
    
    #calulating forces and moments for the aero part of the equation only, control will be done in ControlForces
    def aeroForces(self, state):
        #set constants
        force = Inputs.forcesMoments()
        S = VPC.S
        CL , CD , CM = self.CalculateCoeff_alpha(state.alpha)
        CDq, CLq, Myq = VPC.CDq, VPC.CLq, VPC.CMq
        c, b = VPC.c, VPC.b
        
        rho = VPC.rho
        Va = state.Va

        #check for div by 0, return force
        if Va == 0.0:
            return force
        
        beta = state.beta

        #calculate force drag and lift
        Fdrag = ((0.5)*rho*(Va**2)*S)* (CD + (CDq*(c/(2*Va))*state.q) )
        Flift = ((0.5)*rho*(Va**2)*S)* (CL+ (CLq*(c/(2*Va))*state.q) ) 
       
        
        #set up variables for Fy,Mx,Mz
        Cyb,Cyp, Cyr = VPC.CYbeta, VPC.CYp, VPC.CYr
        Clb, Clp, Clr = VPC.Clbeta, VPC.Clp, VPC.Clr
        Cnb, Cnp, Cnr = VPC.Cnbeta, VPC.Cnp, VPC.Cnr
        pBar = (b/(2*Va))*state.p
        rBar = (b/(2*Va))*state.r


       
        #calucalte FX and FY based on the drag and lift forces
        force.Fx = (math.cos(state.alpha) * (-Fdrag) ) + (-math.sin(state.alpha)*(-Flift))
        force.Fz = (math.sin(state.alpha) * (-Fdrag) ) + (math.cos(state.alpha)*(-Flift))
        #the rest of the forces and moments are calculated based of text book equations
        force.Fy = ((0.5)*rho*(Va**2)*S)* ((Cyb * beta)+ (Cyp * pBar) + (Cyr * rBar))
        force.My = ((0.5)*rho*(Va**2)*S*c) * (VPC.CM0 + (VPC.CMalpha * state.alpha) +  (Myq * (c/(2*Va)) * state.q))
        force.Mx = ((0.5)*rho*(Va**2)*S * b) * (VPC.Cl0 + (Clb *beta) + (Clp * pBar) + (Clr * rBar)) 
        force.Mz = ((0.5)*rho*(Va**2)*S * b) * (VPC.Cn0 +(Cnb *beta) + (Cnp * pBar) + (Cnr * rBar)) 

        return force #return aero forces/moments
    

    #Calculate force and moments for the control portion of the equations
    def controlForces(self, state, controlInputs):
        #set up constants
        force = Inputs.forcesMoments()
        S = VPC.S
        rho = VPC.rho
        Va = state.Va
        c, b = VPC.c, VPC.b
        fxprop, mxprop = self.CalculatePropForces(Va ,controlInputs.Throttle)

        #calculate drag and lift forces
        Flift =  ((0.5)*rho*(Va**2)*S)* (VPC.CLdeltaE * controlInputs.Elevator)
        Fdrag = ((0.5)*rho*(Va**2)*S)* (VPC.CDdeltaE *controlInputs.Elevator)

        #FX and Fz are based on lift and drag forces
        #Fx and Mx get propForces added to them, calculated in PropForces()
        #the rest of the variables are based on text book equations
        force.Fx = (math.cos(state.alpha) * (-Fdrag) ) + (-math.sin(state.alpha)*(-Flift)) + fxprop
        force.Fy = ((0.5)*rho*(Va**2)*S)* ((VPC.CYdeltaA * controlInputs.Aileron) + (VPC.CYdeltaR * controlInputs.Rudder))
        force.Fz = (math.sin(state.alpha) * (-Fdrag) ) + (math.cos(state.alpha)*(-Flift))
        force.Mx = ((0.5)*rho*(Va**2)*S * b) * ((VPC.CldeltaA * controlInputs.Aileron) + (VPC.CldeltaR * controlInputs.Rudder)) + mxprop
        force.My = ((0.5)*rho*(Va**2)*S*c) * (VPC.CMdeltaE * controlInputs.Elevator ) 
        force.Mz =((0.5)*rho*(Va**2)*S * b) * ((VPC.CndeltaA * controlInputs.Aileron) + (VPC.CndeltaR * controlInputs.Rudder))

        return force #returns control forces
    
    #generate gravity forces by multiplying DCM (R) by computed gravity force
    def gravityForces(self, state): 
        forceG = Inputs.forcesMoments()
        [[forceG.Fx],[forceG.Fy], [forceG.Fz]] = MatrixMath.multiply( state.R , [[0],[0],[ VPC.mass *VPC.g0]])
        
        return forceG
