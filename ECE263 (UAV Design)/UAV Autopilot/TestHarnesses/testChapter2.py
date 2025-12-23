"""This file is a test harness for the module ece163.Utilities.Rotations,
and for the method ece163.Modeling.VehicleGeometry.getNewPoints(). 

It is meant to be run from the Testharnesses directory of the repo with:

python ./TestHarnesses/testChapter2.py (from the root directory) -or-
python testChapter2.py (from inside the TestHarnesses directory)

at which point it will execute various tests on the Rotations module"""

#%% Initialization of test harness and helpers:

import math
import sys
sys.path.append("..") #python is horrible, no?

import ece163.Utilities.MatrixMath as mm
import ece163.Utilities.Rotations as Rotations
import ece163.Modeling.VehicleGeometry as VG

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


#%% Euler2dcm():
print("Beginning testing of Rotations.Euler2dcm()")

cur_test = "Euler2dcm yaw test 1"
#we know that rotating [1,0,0] by 90 degrees about Z should produce [0,-1,0], so
R = Rotations.euler2DCM(90*math.pi/180, 0, 0)
orig_vec = [[1],[0],[0]]
expected_vec = [[0],[-1],[0]]
actual_vec = mm.multiply(R, orig_vec)
if not evaluateTest(cur_test, compareVectors(expected_vec, actual_vec) ):
	print(f"{expected_vec} != {actual_vec}")


#%%  


"""
Students, add more tests here.  
You aren't required to use the testing framework we've started here, 
but it will work just fine.
"""
#testing dcm2EULER
passedTest = 0
print("\nTesting Rotations.dcm2Euler(dcm):")
dcm = [[1,0,0],[0,1, 0],[0,0,1]] #we love some good old fashion identiy matrix
yaw, pitch, roll =  0, 0 ,0
results = Rotations.dcm2Euler(dcm)
#if(isclose([yaw,pitch,roll], results)):
if(isclose(yaw, results[0]) and isclose(pitch,results[1]) and isclose(roll,results[2])):
	print("Passed Simple")
	passedTest += 1
else:
	print("Failed Simple")

dcm = [  [ 0.612, 0.612, -0.500] ,[-0.047, 0.659, 0.751],[0.790 ,-0.435, 0.433]]
yaw, pitch, roll =  math.pi / 4, math.pi/6, math.pi/3
results = Rotations.dcm2Euler(dcm)
if(math.isclose(yaw, results[0],abs_tol=1e-3) and math.isclose(pitch,results[1],abs_tol=1e-3) and math.isclose(roll,results[2],abs_tol=1e-3)):
	print("Passed Complex")
	passedTest += 1
else:
	print("Failed Complex")
	



#testing euler2DCM
print("\nTesting Rotations.euler2DCM(yaw, pitch, roll):")
yaw,pitch,roll = 0,0,0 
expected = [[1,0,0],[0,1,0],[0,0,1]] #identiy or sm
result = Rotations.euler2DCM(yaw, pitch, roll)
if (isclose(expected[0][0],result[0][0]) and isclose(expected[0][1],result[0][1]) and isclose(expected[0][2],result[0][2]) 
	and isclose(expected[1][0],result[1][0]) and isclose(expected[1][1],result[1][1]) and isclose(expected[1][2],result[1][2])
	and isclose(expected[2][0],result[2][0]) and isclose(expected[2][1],result[2][1]) and isclose(expected[2][2],result[2][2])):
	print("Passed Simple")
	passedTest += 1
else:
	print("Failed Simple")


yaw,pitch,roll = math.pi / 4, math.pi/6, math.pi/3
expected = [  [ 0.612, 0.612, -0.500] ,[-0.047, 0.660, 0.750],[0.789 ,-0.436, 0.433]]
result = Rotations.euler2DCM(yaw, pitch, roll)
if (math.isclose(expected[0][0],result[0][0],abs_tol=1e-3) and math.isclose(expected[0][1],result[0][1],abs_tol=1e-3) and math.isclose(expected[0][2],result[0][2],abs_tol=1e-3) 
	and math.isclose(expected[1][0],result[1][0],abs_tol=1e-3) and math.isclose(expected[1][1],result[1][1],abs_tol=1e-3) and math.isclose(expected[1][2],result[1][2],abs_tol=1e-3)
	and math.isclose(expected[2][0],result[2][0],abs_tol=1e-3) and math.isclose(expected[2][1],result[2][1],abs_tol=1e-3) and math.isclose(expected[2][2],result[2][2],abs_tol=1e-3)):
	print("Passed Complex")
	passedTest += 1
else:
	print("Failed Complex")



#Testing ned2eenu
print("\nTesting rotations.ned2enu():")
points = [[1,2,3]]
expected = [[2,1,-3]]
result = Rotations.ned2enu(points)
if (result == expected):
	print("Passed Simple")
	passedTest += 1
else:
	print("Failed Simple")

points = [[10 ,-2, 4]]
expected = [[-2,10,-4]]
result = Rotations.ned2enu(points)
if (result == expected):
	print("Passed Complex")
	passedTest += 1
else:
	print("Failed Complex")

print("\nPersonalTest: " + str(passedTest), "/ 6" )


#%% Print results:

total = len(passed) + len(failed)
print(f"\n---\nPassed {len(passed)}/{total} tests")
[print("   " + test) for test in passed]

if failed:
	print(f"Failed {len(failed)}/{total} tests:")
	[print("   " + test) for test in failed]