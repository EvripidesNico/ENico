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

isclose = lambda  a,b : math.isclose(a, b, abs_tol= 1e-12)

suc = 0

# Ensure computeTrim() Succeeds
vTrim = VehicleTrim.VehicleTrim()
Vastar, Gammastar, Kappastar = 25.0, math.radians(6.0), -1.0 / 150.0
trim_success = vTrim.computeTrim(Vastar, Kappastar, Gammastar)

if trim_success:
    print("Passed Compute Trim")
    suc += 1
else:
    print("Failed Compute Trim")

trim_state = vTrim.getTrimState()
if trim_state is not None:
    print("Passed Valid Trim State")
    suc += 1
else:
    print("Failed Valid Trim State")

controller = VCLC.VehicleClosedLoopControl()
testGains = Controls.controlGains(kp_roll=0.5, kd_roll=0.2, ki_roll=0.1)
controller.setControlGains(testGains)
gains = controller.getControlGains()

if isclose(gains.kp_roll, 0.5) and isclose(gains.kd_roll, 0.2) and isclose(gains.ki_roll, 0.1):
    print("Passed Control Gains Setting")
    suc += 1
else:
    print("Failed Control Gains Setting")


# Ensure VehicleClosedLoopControl.UpdateControlCommands()
referenceCommands = Controls.referenceCommands(altitudeCommand=1000, airspeedCommand=30, courseCommand=math.radians(90))
state = States.vehicleState(pd=950)  # Simulating slight altitude deviation
controller.UpdateControlCommands(referenceCommands, state)

if controller.mode == Controls.AltitudeStates.CLIMBING:
    print("Passed State Machine Climbing Mode")
    suc += 1
else:
    print("Failed State Machine Climbing Mode")


vehicle_model = VDM.VehicleDynamicsModel()
initial_state = vehicle_model.getVehicleState()
forceMoments = Inputs.forcesMoments()
vehicle_model.Update(forceMoments)
new_state = vehicle_model.getVehicleState()

if isclose(initial_state.Va, new_state.Va):
    print("Passed Vehicle Dynamics Model State Update")
    suc += 1
else:
    print("Failed Vehicle Dynamics Model State Update")

linearizedModel = Linearized.transferFunctions(a_phi2=1.0, a_theta2=1.2, a_theta3=0.8)
tuningParams = Controls.controlTuning(Wn_roll=1.0, Zeta_roll=0.7, Wn_pitch=1.5, Zeta_pitch=0.6)
reconstructed_tuning = VCG.computeTuningParameters(gains, linearizedModel)
if not isclose(reconstructed_tuning.Wn_roll, tuningParams.Wn_roll):
    print("Passed Tuning Parameters Reconstruction")
    suc += 1
else:
    print("Failed Tuning Parameters Reconstruction")


print(f"\nPersonalTest: {suc} / 6")


