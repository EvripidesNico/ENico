
"""This file is a test harness for the module VehicleAerodynamicsModel. 

It is meant to be run from the Testharnesses directory of the repo with:

python ./TestHarnesses/testChapter4.py (from the root directory) -or-
python testChapter4.py (from inside the TestHarnesses directory)

at which point it will execute various tests on the VehicleAerodynamicsModel module"""


import math

import sys
sys.path.append("..") #python is horrible, no?

import ece163.Utilities.MatrixMath as mm
import ece163.Utilities.Rotations as Rotations
import ece163.Modeling.VehicleDynamicsModel as VDM
import ece163.Modeling.VehicleAerodynamicsModel as VAM
import ece163.Modeling.WindModel as WM
import ece163.Containers.Inputs as Inputs
import ece163.Containers.States as States
import ece163.Constants.VehiclePhysicalConstants as VPC


isclose = lambda  a,b : math.isclose(a, b, abs_tol= 1e-12)


def compareVectors(a, b):
	"""A quick tool to compare two vectors"""
	el_close = [isclose(a[i][0], b[i][0]) for i in range(3)]
	return all(el_close)



passed = 0
#need to generate 12 test minimum 
#test initial values of height and speed
aero = VAM.VehicleAerodynamicsModel()
state = aero.getVehicleState()

if (isclose(state.u,25.0) and isclose(state.pd, -100)):
	print("Passed Initial Condition Setup")
	passed +=1
else:
	print("Failed Initial Condition Setup")
	

#Test reset returns height and speed back to normal
state.u, state.pd = 0,0
aero.reset()
state = aero.getVehicleState()
if (isclose(state.u,25.0) and isclose(state.pd, -100)):
	print("Passed Reset Condition Setup")
	passed +=1
else:
	print("Failed Reset Condition Setup")

#test gravity wiht rotation matrix I and returns gravity back

state.R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
grav = Inputs.forcesMoments()
grav = aero.gravityForces(state)

expected_grav = [[0],[0], [VPC.g0 * VPC.mass]]
if(isclose(grav.Fz,expected_grav[2][0]) and isclose(grav.Fy,expected_grav[1][0]) and isclose(grav.Fx,expected_grav[0][0]) ):
	print("Passed Gravity Forces")
	passed +=1
else:
	print("Failed Gravity Forces")

#test Coeff alpha function
CL, CD, CM = aero.CalculateCoeff_alpha(math.pi/6)
cl,cd,cm = 1.0224935239466217,0.4859094470618844,-1.4211606451393388

if(isclose(CL,cl) and isclose(cm,CM) and isclose(cd, CD)):
	print("Passed aeroCoeff Test")
	passed +=1
else:
	print("Failed aeroCoeff Test")

#testing propForce
fx_prop, mx_prop = aero.CalculatePropForces(20,0.8)
fxp, mxp = 24.614455319136255, -1.1761463309918336

if(isclose(fx_prop,fxp) and isclose(mx_prop,mxp)):
	print("Passed PropForce Test")
	passed +=1
else:
	print("Failed PropForce Test")
	
#testing control forces
cont_in = Inputs.controlInputs()
cont_in.Aileron = 0.2
cont_in.Elevator = 0.1
cont_in.Rudder = 0.04
aero.reset()
state = aero.getVehicleState()
force = Inputs.forcesMoments()
force = aero.controlForces(state,cont_in)

fx,fy,fz,mx,my,mz =21.817680754436033,0,0,-0.6194943564776727,0,0

if(isclose(force.Fx,fx) and isclose(force.Fy,fy) and isclose(force.Fz,fz)):
	print("Passed Forces ControlForces")
	passed+=1
else:
	print("Failed Forces ControlForces")

if(isclose(force.Mx,mx) and isclose(force.My,my) and isclose(force.Mz,mz)):
	print("Passed Moments ControlForces")
	passed+=1
else:
	print("Failed Moments ControlForces")
	

#testing Aeroforces
state.u = 30
state.alpha = 1
state.Va = 2
state.q = 1.2
state.r = 0.5
state.p = 0.1
force = aero.aeroForces(state)
fx,fy,fz,mx,my,mz =0.5317706902272736,0.0,-2.6891837400155714,0.21638606949796324,-1.2993556593270834,-0.1187199246164501

if(isclose(force.Fx,fx) and isclose(force.Fy,fy) and isclose(force.Fz,fz)):
	print("Passed Forces aeroForces")
	passed+=1
else:
	print("Failed Forces aeroForces")

if(isclose(force.Mx,mx) and isclose(force.My,my) and isclose(force.Mz,mz)):
	print("Passed Moments aeroForces")
	passed+=1
else:
	print("Failed Moments aeroForces")
	

print("\nPersonalTest: " + str(passed), "/ 9" )