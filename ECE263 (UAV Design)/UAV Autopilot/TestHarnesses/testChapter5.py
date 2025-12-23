"""This file is a test harness for the module VehiclePerturbationModels. 

It is meant to be run from the Testharnesses directory of the repo with:

python ./TestHarnesses/testChapter5.py (from the root directory) -or-
python testChapter5.py (from inside the TestHarnesses directory)

at which point it will execute various tests on the VehiclePerturbationModels module"""

#%% Initialization of test harness and helpers:

import math

import sys
sys.path.append("..") #python is horrible, no?

import ece163.Utilities.MatrixMath as mm
import ece163.Utilities.Rotations as Rotations
import ece163.Modeling.VehicleDynamicsModel as VDM
import ece163.Controls.VehiclePerturbationModels as VPM
import ece163.Modeling.WindModel as WM
import ece163.Controls.VehicleTrim as VehicleTrim
import ece163.Containers.Inputs as Inputs
import ece163.Containers.States as States
import ece163.Constants.VehiclePhysicalConstants as VPC


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


#%% PUT A TEST HERE?
vTrim = VehicleTrim.VehicleTrim()
Vastar = 25.0
Gammastar = math.radians(6.0)
Kappastar = -1.0 / 150.0

check = vTrim.computeTrim(Vastar, Kappastar, Gammastar)
if check:
 print("Optimization successful")
else:
 print("Model converged outside of valid inputs, change parameters and try again")
	   
 
tF = VPM.CreateTransferFunction(
	vTrim.getTrimState(), 
	vTrim.getTrimControls())

#personal test
suc = 0
wind_model = WM.WindModel()
wind_state = wind_model.getWind()

if(isclose(wind_state.Wn, 0.0) and isclose(wind_state.We, 0.0) and isclose(wind_state.Wd, 0.0)):
	print("Passed Initial Condition Setup")
	suc +=1
else:
	print("Failed Initial Condition Setup")

wind_model.wind.Wn, wind_model.wind.We, wind_model.wind.Wd = 5,3,-2
wind_model.reset()
wind_state = wind_model.getWind()

if(isclose(wind_state.Wn, 0.0) and isclose(wind_state.We, 0.0) and isclose(wind_state.Wd, 0.0)):
	print("Passed Reset")
	suc +=1
else:
	print("Failed Reset")

Phi_u, Gamma_u, H_u, Phi_v, Gamma_v, H_v, Phi_w, Gamma_w, H_w = wind_model.getDrydenTransferFns()

#test a random variables to keep it short 
expected_Phi_u = [[1]]
expected_Gammav = [[0],[0]]
expected_Hw =  [[1,1]]
if(isclose(Phi_u[0][0],expected_Phi_u[0][0]) and isclose(Gamma_v[0][0], expected_Gammav[0][0]) and isclose(expected_Hw[0][0], H_w[0][0])):
	print("Passed GetDryden Transfer fn")
	suc +=1
else:
	print("Failed GetDryden Transfer fn")


#test wind update

wind_model.Update()
wind_state = wind_model.getWind()

if(isclose(wind_state.Wu, 0.0) and isclose(wind_state.Wv, 0.0) and isclose(wind_state.Ww, 0.0)):
	print("Passed Default Update")
	suc +=1
else:
	print("Failed Update")

#set para wind model
wind_model.setWindModelParameters(Wn=10, We= 2, Wd = 4)
wind_state = wind_model.getWind()

if(isclose(wind_state.Wn, 10) and isclose(wind_state.We, 2) and isclose(wind_state.Wd, 4)):
	print("Passed Set Wind Model Parameters")
	suc +=1
else:
	print("Failed Set Wind Model Parameters")

#test nonzero Va get tryden model, testing for arithmitic error or not
try:
	wind_model.CreateDrydenTransferFns(0.01, 30, VPC.DrydenNoWind)
	suc+=1
	print("Passed nonzero Va CreateTF")
except ArithmeticError:
	print("Failed nonzero Va CreateTF")

#test the raise of arithmeticerror
try:
	wind_model.CreateDrydenTransferFns(0.01, 0.0, VPC.DrydenNoWind)
	print("Failed zero Va CreateTF")
except ArithmeticError:
	print("Passed zero Va CreateTF")
	suc+=1



#%% Print results:
print("\nPersonalTest: " + str(suc), "/ 7" )
total = len(passed) + len(failed)
print(f"\n---\nPassed {len(passed)}/{total} tests")
[print("   " + test) for test in passed]

if failed:
	print(f"Failed {len(failed)}/{total} tests:")
	[print("   " + test) for test in failed]