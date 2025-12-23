"""This file is a test harness for the module VehicleDynamicsModel. 

It is meant to be run from the Testharnesses directory of the repo with:

python ./TestHarnesses/testChapter3.py (from the root directory) -or-
python testChapter3.py (from inside the TestHarnesses directory)

at which point it will execute various tests on the VehicleDynamicsModel module"""

#%% Initialization of test harness and helpers:

import math

import sys
sys.path.append("..") #python is horrible, no?

import ece163.Utilities.MatrixMath as mm
import ece163.Utilities.Rotations as Rotations
import ece163.Modeling.VehicleDynamicsModel as VDM
import ece163.Containers.Inputs as Inputs
import ece163.Containers.States as States

"""math.isclose doesn't work well for comparing things near 0 unless we 
use an absolute tolerance, so we make our own isclose:"""
isclose = lambda  a,b : math.isclose(a, b, abs_tol= 1e-12)

def compareVectors(a, b):
	"""A quick tool to compare two vectors"""
	el_close = [isclose(a[i][0], b[i][0]) for i in range(3)]
	return all(el_close)

#of course, you should test your testing tools too:
assert(compareVectors([[0], [0], [-1]],[[1e-13], [0], [-1+1e-9]]))
assert(not compareVectors([[0], [0], [-1]],[[1e-11], [0], [-1]]))
assert(not compareVectors([[1e8], [0], [-1]],[[1e8+1], [0], [-1]]))



failed = []
passed = []
def evaluateTest(test_name, boolean):
	"""evaluateTest prints the output of a test and adds it to one of two 
	global lists, passed and failed, which can be printed later"""
	if boolean:
		print(f"   passed {test_name}")
		passed.append(test_name)
	else:
		print(f"   failed {test_name}")
		failed.append(test_name)
	return boolean


#%% Derivative():
print("Beginning testing of VDM.Derivative(), subtest of [pe,pn,pd]")

cur_test = "Derivative test p_dot x dir"

testVDM = VDM.VehicleDynamicsModel()
testState = States.vehicleState()
testFm = Inputs.forcesMoments()
testState.pitch = 30*math.pi/180
testState.R = Rotations.euler2DCM(0.0,testState.pitch,0.0)
testState.u = 10
testDot = testVDM.derivative(testState, testFm)

print("With a velocity of u = 10 m/s, and pitch = 30deg:\n")
resultPdot = [[testDot.pn],[testDot.pe],[testDot.pd]]
expectedPdot = [[10*math.sqrt(3)/2],[0],[-10/2]]

if compareVectors(resultPdot,expectedPdot):
	print("passed!")
else:
	print("failed :(")



#%%  

"""
Students, add more tests here.  
You aren't required to use the testing framework we've started here, 
but it will work just fine.
"""

#%% Print results:
#test Derivative
#test PQR NED UVW
print("TESTING DERIVATIVE")
testPersonal = VDM.VehicleDynamicsModel()
derivResult = VDM.VehicleDynamicsModel()
count = 0
testPersonal.reset()
force = Inputs.forcesMoments()
force.Fx = 1
force.Fy = 1
force.Fz = 0.5
testPersonal.state.p = 1
testPersonal.state.q = 1
testPersonal.state.r = 0
testPersonal.state.u = 1
testPersonal.state.v = 0
testPersonal.state.w = 1
testPersonal.state.pitch = 1
testPersonal.state.roll = 0
testPersonal.state.yaw = 1

ERP = 0.12147151902172897
ERQ = -0.10607929515418502
ERR = -0.16826312058543708
derivResult.dot = derivResult.derivative(testPersonal.state,force)
if( isclose(derivResult.dot.p,ERP) and isclose(derivResult.dot.q, ERQ) and isclose(derivResult.dot.r, ERR)):
	count +=1
	print("Passed Simple PQR")
else:
	print("Failed Simple PQR")
if( isclose(derivResult.dot.pn,1) and isclose(derivResult.dot.pe, 0) and isclose(derivResult.dot.pd, 1)):
	count +=1
	print("Passed Simple PNED")
else:
	print("Failed Simple PNED")

if( isclose(derivResult.dot.pitch,1) and isclose(derivResult.dot.roll, 1) and isclose(derivResult.dot.yaw, 0)):
	count +=1
	print("Passed Simple EulerAngles")
else:
	print("Failed Simple EulerAngles")
u =-0.9090909090909091
v =1.0909090909090908
w =1.0454545454545454
if( math.isclose(derivResult.dot.u, u) and math.isclose(derivResult.dot.v,v) and math,isclose(derivResult.dot.w, w)):
	count +=1
	print("Passed Simple UVW")
else:
	print("Failed Simple UVW")


#test Integrate State
print("Testing Integrate State")
intS = VDM.VehicleDynamicsModel()
testPersonal.state.R = Rotations.euler2DCM(testPersonal.state.yaw, testPersonal.state.roll,testPersonal.state.roll)

intS.state = intS.IntegrateState(0.01, testPersonal.state,derivResult.dot)
p = 1.0012147151902173
q = 0.9989392070484582
r = -0.0016826312058543708
u = 0.990909090909091
v =  0.010909090909090908
w = 1.0104545454545455
pitch = 0.009994571341351068
roll =0.01000636472177866
yaw = 1.0000415922002681
pn = 0.01
pe = 0.0
pd = 0.01
if( isclose(intS.state.p,p) and isclose(intS.state.q, q) and isclose(intS.state.r, r)):
	count +=1
	print("Passed PQR")
else:
	print("Failed PQR")

if( isclose(intS.state.u,u) and isclose(intS.state.v,v) and isclose(intS.state.w, w)):
	count +=1
	print("Passed UVW")
else:
	print("Failed UVW")
if( isclose(intS.state.pitch, pitch) and isclose(intS.state.roll, roll) and isclose(intS.state.yaw,yaw)):
	count +=1
	print("Passed Euler Angle")
else:
	print("Failed Euler Angle")
if( isclose(intS.state.pn, pn) and isclose(intS.state.pe,pe) and isclose(intS.state.pd,pd)):
	count +=1
	print("Passed PNED")
else:
	print("Failed PNED")


'''print(intS.state.pitch)
print(intS.state.roll)
print(intS.state.yaw)
print(intS.state.pn)
print(intS.state.pe)
print(intS.state.pd)'''

#test rexp

stateEX = States.vehicleState()
dotEX = States.vehicleState()
stateEX.p = 1
stateEX.q = 90
stateEX.r = 30
#testPersonal.Rexp(0.01,stateEX,dotEX)
print("Testing REXP:")
expected = [[0.582757141 ,  0.26115000952,  -0.7695419332869],
 		[-0.2528051523 ,  0.95822935378 ,  0.13373877705],
 		[0.7723235523 , 0.116606938322 , 0.62443506662]]
testPersonal.Rexp(0.01,stateEX,dotEX)
test = testPersonal.Rexp(0.01,stateEX,dotEX)
if(isclose(expected[0][0],test[0][0]) and isclose(expected[1][0],test[1][0]) and isclose(expected[2][0],test[2][0])  and
   isclose(expected[0][1],test[0][1]) and isclose(expected[1][1],test[1][1]) and isclose(expected[2][1],test[2][1]) and
   isclose(expected[0][2],test[0][2]) and isclose(expected[1][2],test[1][2]) and isclose(expected[2][2],test[2][2])):
	count+=1
	print("Passed REXP w > 0.1")
else:
	print("Failed REXP w > 0.1")

stateEX.p = 1
stateEX.q = 0
stateEX.r = 0
testPersonal.Rexp(0.01,stateEX,dotEX)
test = testPersonal.Rexp(0.01,stateEX,dotEX)
expected = [[1.0 ,  0,  0],
 		   [0 ,  0.999950000416 ,  0.00999983333416],
 		   [0 ,-0.009999833334 , 0.9999500004166653]]
if(isclose(expected[0][0],test[0][0]) and isclose(expected[1][0],test[1][0]) and isclose(expected[2][0],test[2][0])  and
   isclose(expected[0][1],test[0][1]) and isclose(expected[1][1],test[1][1]) and isclose(expected[2][1],test[2][1]) and
   isclose(expected[0][2],test[0][2]) and isclose(expected[1][2],test[1][2]) and isclose(expected[2][2],test[2][2])):
	count+=1
	print("Passed REXP w < 0.1")
else:
	print("Failed REXP w < 0.1")



print("\nPersonalTest: " + str(count), "/ 10" )

total = len(passed) + len(failed)
print(f"\n---\nPassed {len(passed)}/{total} tests")
[print("   " + test) for test in passed]

if failed:
	print(f"Failed {len(failed)}/{total} tests:")
	[print("   " + test) for test in failed]