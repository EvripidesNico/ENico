import math
import random
from ..Containers import States
from ..Utilities import MatrixMath as MM
from ..Containers import Inputs
from ..Constants import VehiclePhysicalConstants as VPC

#wind :')

class WindModel():

    def __init__(self, dT = VPC.dT, Va = VPC.InitialSpeed, drydenParameters= VPC.DrydenNoWind ):
        """
        Initalize  Dryden Wind Model
        Param dT
        Param Va
        Param Dryden Parameters
        """      
        self.dt = dT
        self.Va = Va
        self.Xu = [[0]]
        self.Xv = [[0],[0]]
        self.Xw = [[0],[0]]
        if(drydenParameters is None):

            self.drydenParameters = Inputs.drydenParameters()
        else:
            self.drydenParameters = drydenParameters

        self.wind = States.windState()
        
        self.Gamma_u = [[0]] 
        self.Gamma_v = [[0],[0]] 
        self.Gamma_w = [[0],[0]] 
    
        self.Phi_u = [[1]]
        self.Phi_v = [[1,0],[0,1]]
        self.Phi_w = [[1,0],[0,1]] 

        self.H_u = [[1]]
        self.H_v = [[1,1]]
        self.H_w = [[1,1]]
        self.CreateDrydenTransferFns(dT, Va, drydenParameters)


        return
    
    def CreateDrydenTransferFns(self, dT, Va, drydenParameters):
        #checking cases before equations if none return 0 if Va < 0 return error
        
        if(Va <= 0):
            raise ArithmeticError("Va is less than or equal to 0")
 
        #if Lv is no wind
        if(drydenParameters.Lv != 0):
            #setting up all the V parameters
            expo = math.exp((-(Va/drydenParameters.Lv))*dT) #used for both phi and gammaV
            Hscal = drydenParameters.sigmav * math.sqrt((3*Va)/(math.pi*drydenParameters.Lv))
            phiV_matrix = [[(1-((Va/drydenParameters.Lv))*dT), (-(Va/drydenParameters.Lv)**2)*dT],[dT, (1+((Va/drydenParameters.Lv))*dT)],]
            gammaV_matrix = [[dT],[((drydenParameters.Lv/Va)**2)* (math.exp((Va/drydenParameters.Lv)*dT) - 1) - ((drydenParameters.Lv/Va)*dT)]]
            HV_matrix = [[1, Va/(math.sqrt(3)*drydenParameters.Lv)]]
            self.Phi_v = MM.scalarMultiply(expo, phiV_matrix)
            self.Gamma_v = MM.scalarMultiply(expo,gammaV_matrix)
            self.H_v = MM.scalarMultiply(Hscal,HV_matrix)
        else:
            self.Gamma_v = [[0],[0]] 
            self.H_v = [[1,1]]
            self.Phi_v = [[1,0],[0,1]]
        #if Lu is no windd
        if(drydenParameters.Lu != 0):
            Us = math.exp((-Va * dT) / drydenParameters.Lu) #used in γu as well as φu
            self.Phi_u = [[Us]]
            self.H_u = [[drydenParameters.sigmau* math.sqrt((2*Va)/(math.pi*drydenParameters.Lu))]]
            self.Gamma_u = [[(drydenParameters.Lu/Va) * (1 - Us)]]
        else:
            self.Gamma_u = [[0]] 
            self.Phi_u = [[1]]
            self.H_u = [[1]]


        #if Lw is no wind
        if(drydenParameters.Lw != 0):
            #setting up all W parameteres, should be the same a V but using W instead
            expow = math.exp(-(Va/drydenParameters.Lw)*dT) #used for both phi and gammaV
            Hscalw = drydenParameters.sigmaw * math.sqrt((3*Va)/(math.pi*drydenParameters.Lw))
            phiw_matrix = [[(1-((Va/drydenParameters.Lw))*dT), (-(Va/drydenParameters.Lw)**2)*dT],[dT, (1+((Va/drydenParameters.Lw))*dT)],]
            gammaw_matrix = [[dT],[((drydenParameters.Lw/Va)**2)* (math.exp((Va/drydenParameters.Lw)*dT)-1) - ((drydenParameters.Lw/Va)*dT)]]
            Hw_matrix = [[1, Va/(math.sqrt(3)*drydenParameters.Lw)]]

            self.Phi_w = MM.scalarMultiply(expow, phiw_matrix)
            self.Gamma_w = MM.scalarMultiply(expow,gammaw_matrix)
            self.H_w = MM.scalarMultiply(Hscalw,Hw_matrix)
        else:
            self.Gamma_w = [[0],[0]]  
            self.Phi_w = [[1,0],[0,1]] 
            self.H_w = [[1,1]]

        
        return 
    

    
    def Update(self, uu = None, uv = None, uw =None):
        #the fun part :')
        #need randoms
        #then get transfer
        #then do the maths
        #then should be gucci
        if uu is None:
            uu = random.gauss(0,1)
        if uv is None:
            uv = random.gauss(0,1)
        if uw is None:
            uw = random.gauss(0,1)
        self.CreateDrydenTransferFns(self.dt, self.Va, self.drydenParameters)
        #in essence from my understanding we are computing Xuvw and Wuvw(gust)
        #with the given variables that we calcedd earlier
        #Xuvw =  φ*Xuvw + ΓUvuw(white noise)
        #compute gust = HXuvw
        #self.Xu = self.Phi_u *self.Xu + self.Gamma_u*uu

        self.Xu = MM.add(MM.multiply(self.Phi_u, self.Xu),MM.scalarMultiply(uu, self.Gamma_u))
        self.Xv = MM.add(MM.multiply(self.Phi_v, self.Xv),MM.scalarMultiply(uv, self.Gamma_v))
        self.Xw = MM.add(MM.multiply(self.Phi_w, self.Xw),MM.scalarMultiply(uw, self.Gamma_w))

        #self.wind.Wu = self.H_u*self.Xu\
        #need to make sure to just get a value out of the matrix
        self.wind.Wu = MM.multiply(self.H_u,self.Xu)[0][0]
        self.wind.Wv = MM.multiply(self.H_v,self.Xv)[0][0]
        self.wind.Ww = MM.multiply(self.H_w, self.Xw)[0][0]

        return
    
    def getDrydenTransferFns(self):
        return self.Phi_u , self.Gamma_u , self.H_u , self.Phi_v , self.Gamma_v , self.H_v , self.Phi_w , self.Gamma_w , self.H_w
    
    def getWind(self):
        return self.wind
    
    def reset(self):
        self.wind = States.windState()
        self.Xu = [[0]]
        self.Xv = [[0],[0]]
        self.Xw = [[0],[0]]
        self.Va = VPC.InitialSpeed
        self.dt = VPC.dT

        return
    
    def setWind(self, windState):
        self.wind = windState
        return
    
    def setWindModelParameters(self, Wn = 0.0, We = 0.0, Wd = 0.0, drydenParameters = VPC.DrydenNoWind):
        self.drydenParameters, self.wind.Wn, self.wind.We, self.wind.Wd = drydenParameters, Wn, We, Wd
        #not sure if i need to run create dryden transder function here?

        return