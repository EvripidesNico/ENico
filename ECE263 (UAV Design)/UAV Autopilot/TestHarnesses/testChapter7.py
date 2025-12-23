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
import ece163.Controls.VehicleClosedLoopControl as VCLC
import ece163.Containers.Controls as Controls
from ece163.Containers import Linearized
import ece163.Controls.VehicleControlGains as VCG
import ece163.Sensors.SensorsModel as SM 
import ece163.Containers.Sensors as Sensors
import ece163.Constants.VehicleSensorConstants as VSC

# For floating‐point comparisons
isclose = lambda a, b: math.isclose(a, b, abs_tol=1e-12)

suc = 0
total = 0

print("\n-- SensorsModel Testing --")


# Test 1: GaussMarkov update vnoise 
total += 1
gm = SM.GaussMarkov(dT=1, tau=1, eta=0)
gm.v = 0  
result = gm.update(vnoise=2)
expected = 2  
if isclose(result, expected):
    print("Passed GaussMarkov update with provided vnoise")
    suc += 1
else:
    print("Failed GaussMarkov update with provided vnoise")


# Test 2: GaussMarkov update without vnoise 
total += 1
gm.reset()
_ = gm.update(vnoise=2) 
result2 = gm.update()  
expected2 = math.e**(-1) * 2
if isclose(result2, expected2):
    print("Passed GaussMarkov update without vnoise")
    suc += 1
else:
    print("Failed GaussMarkov update without vnoise")


# Test 3: GaussMarkovXYZ update
total += 1
gmxyz = SM.GaussMarkovXYZ(dT=1, tauX=1, etaX=0, tauY=1, etaY=0, tauZ=1, etaZ=0)
vx, vy, vz = gmxyz.update(vXnoise=1, vYnoise=2, vZnoise=3)
if isclose(vx, 1) and isclose(vy, 2) and isclose(vz, 3):
    print("Passed GaussMarkovXYZ update")
    suc += 1
else:
    print("Failed GaussMarkovXYZ update")

# Test 4: updateAccelsTrue
state = States.vehicleState()
dot = States.vehicleState()
state.q = 0.1
state.w = 20.0
state.r = 0.05
state.v = 30.0
state.p = 0.2
state.pitch = math.radians(10)
state.roll = math.radians(5)   
dot.u = 2.0
dot.v = 3.0
dot.w = 4.0

total += 1
# Expected output:
ax_exp = dot.u + state.q * state.w - state.r * state.v + VPC.g0 * math.sin(state.pitch)
ax, ay, az = SM.SensorsModel().updateAccelsTrue(state, dot)
if isclose(ax, ax_exp):
    print("Passed updateAccelsTrue")
    suc += 1
else:
    print("Failed updateAccelsTrue")
    print(f"Expected: {ax_exp}")
    print(f"Got: {ax}")

# ------------------------------
# Test 5: updateMagsTrue
total += 1

state.R = [[1,0,0],[0,1,0],[0,0,1]]
mx_exp = VSC.magfield[0][0]
my_exp = VSC.magfield[1][0]
mz_exp = VSC.magfield[2][0]
mmx, mmy, mmz = SM.SensorsModel().updateMagsTrue(state)
if isclose(mmx, mx_exp) and isclose(mmy, my_exp) and isclose(mmz, mz_exp):
    print("Passed updateMagsTrue")
    suc += 1
else:
    print("Failed updateMagsTrue")
    print(f"Expected: {mx_exp}, {my_exp}, {mz_exp}")
    print(f"Got: {mmx}, {mmy}, {mmz}")


# Test 6: updateGyrosTrue
total += 1

state.p = 0.2
state.q = 0.1
state.r = 0.05
p_exp, q_exp, r_exp = state.p, state.q, state.r
p_out, q_out, r_out = SM.SensorsModel().updateGyrosTrue(state)
if isclose(p_out, p_exp) and isclose(q_out, q_exp) and isclose(r_out, r_exp):
    print("Passed updateGyrosTrue")
    suc += 1
else:
    print("Failed updateGyrosTrue")
    print(f"Expected: {p_exp}, {q_exp}, {r_exp}")
    print(f"Got: {p_out}, {q_out}, {r_out}")


# Test 7: updatePressureSensorsTrue
total += 1

state.pd = -10.0 
state.Va = 20.0
baro_exp = VSC.Pground - VPC.rho * VPC.g0 * (-state.pd)
pinto_exp = (VPC.rho * state.Va**2) / 2
baro_out, pinto_out = SM.SensorsModel().updatePressureSensorsTrue(state)
if isclose(baro_out, baro_exp) and isclose(pinto_out, pinto_exp):
    print("Passed updatePressureSensorsTrue")
    suc += 1
else:
    print("Failed updatePressureSensorsTrue")
    print(f"Expected: {baro_exp}, {pinto_exp}")
    print(f"Got: {baro_out}, {pinto_out}")

# Test 8: updateGPSTrue
total += 1
state.pn = 100.0
state.pe = 200.0
state.pd = -5.0   
dot.pn = 1.0
dot.pe = 2.0
n_exp = state.pn
e_exp = state.pe
d_exp = -state.pd  
sog_exp = math.hypot(dot.pn, dot.pe)
cog_exp = math.atan2(dot.pe, dot.pn)
model_instance = SM.SensorsModel()
n_out, e_out, d_out, sog_out, cog_out = model_instance.updateGPSTrue(state, dot)
if isclose(n_out, n_exp) and isclose(e_out, e_exp) and isclose(d_out, d_exp) and isclose(sog_out, sog_exp) and isclose(cog_out, cog_exp):
    print("Passed updateGPSTrue")
    suc += 1
else:
    print("Failed updateGPSTrue")
    print(f"Expected: {n_exp}, {e_exp}, {d_exp}, {sog_exp}, {cog_exp}")
    print(f"Got: {n_out}, {e_out}, {d_out}, {sog_out}, {cog_out}")


# Test 9: updateSensorsTrue
total += 1
prevSensors = Sensors.vehicleSensors()
prevSensors.gps_n = 111.0
prevSensors.gps_e = 222.0
prevSensors.gps_alt = 333.0
prevSensors.gps_sog = 44.0
prevSensors.gps_cog = 0.5

model_instance.updateTicks = 0
sensors_true = model_instance.updateSensorsTrue(prevSensors, state, dot)
if (isclose(sensors_true.gps_n, state.pn) and
    isclose(sensors_true.gps_e, state.pe) and
    isclose(sensors_true.gps_alt, -state.pd)):
    print("Passed updateSensorsTrue")
    suc += 1
else:
    print("Failed updateSensorsTrue")
    print(f"Expected GPS: {state.pn}, {state.pe}, {-state.pd}")
    print(f"Got: {sensors_true.gps_n}, {sensors_true.gps_e}, {sensors_true.gps_alt}")


# Test 10: updateSensorsNoisy
total += 1

zeroBias = Sensors.vehicleSensors()
zeroSigma = Sensors.vehicleSensors()

zeroBias.gyro_x = zeroBias.gyro_y = zeroBias.gyro_z = 0.0
zeroBias.accel_x = zeroBias.accel_y = zeroBias.accel_z = 0.0
zeroBias.mag_x = zeroBias.mag_y = zeroBias.mag_z = 0.0
zeroBias.baro = zeroBias.pitot = 0.0
zeroBias.gps_n = zeroBias.gps_e = zeroBias.gps_alt = zeroBias.gps_sog = zeroBias.gps_cog = 0.0

zeroSigma.gyro_x = zeroSigma.gyro_y = zeroSigma.gyro_z = 0.0
zeroSigma.accel_x = zeroSigma.accel_y = zeroSigma.accel_z = 0.0
zeroSigma.mag_x = zeroSigma.mag_y = zeroSigma.mag_z = 0.0
zeroSigma.baro = zeroSigma.pitot = 0.0
zeroSigma.gps_n = zeroSigma.gps_e = zeroSigma.gps_alt = zeroSigma.gps_sog = zeroSigma.gps_cog = 0.0


model_instance.gyro = SM.GaussMarkovXYZ(dT=1, tauX=1, etaX=0, tauY=1, etaY=0, tauZ=1, etaZ=0)
model_instance.GPS = SM.GaussMarkovXYZ(dT=1, tauX=1, etaX=0, tauY=1, etaY=0)
noisy_out = model_instance.updateSensorsNoisy(sensors_true, Sensors.vehicleSensors(), zeroBias, zeroSigma)


pass_test = True
for field in ['accel_x','accel_y','accel_z','mag_x','mag_y','mag_z','gyro_x','gyro_y','gyro_z','baro','pitot']:
    if not isclose(getattr(noisy_out, field), getattr(sensors_true, field)):
        pass_test = False
        print(f"Mismatch in {field}: expected {getattr(sensors_true, field)}, got {getattr(noisy_out, field)}")
if model_instance.updateTicks % model_instance.gpsTickUpdate == 0:
    for field in ['gps_n','gps_e','gps_alt','gps_sog','gps_cog']:
        if not isclose(getattr(noisy_out, field), getattr(sensors_true, field)):
            pass_test = False
            print(f"Mismatch in {field}: expected {getattr(sensors_true, field)}, got {getattr(noisy_out, field)}")
if pass_test:
    print("Passed updateSensorsNoisy")
    suc += 1
else:
    print("Failed updateSensorsNoisy")

print(f"\nSensorsModel Test: {suc} / {total}\n")