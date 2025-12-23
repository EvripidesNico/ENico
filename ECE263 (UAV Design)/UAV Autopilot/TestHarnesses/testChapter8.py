import math

import sys
sys.path.append("..") #python is horrible, no?

import ece163.Utilities.MatrixMath as MM
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
import ece163.Controls.VehicleEstimator as VE

import math
import ece163.Utilities.MatrixMath as MM
import ece163.Controls.VehicleEstimator as VE
import ece163.Containers.States as States
import ece163.Containers.Sensors as Sensors
import ece163.Containers.Controls as Controls
import ece163.Constants.VehiclePhysicalConstants as VPC
import ece163.Constants.VehicleSensorConstants as VSC

def test_estimateAttitude():
    """
    Test estimateAttitude 
    """

    print("Running Attitude Estimation Test")

    estimator = VE.VehicleEstimator()
    estimator.setEstimatorGains(Controls.VehicleEstimatorGains(Kp_acc=2.5, Ki_acc=0.25, Kp_mag=10, Ki_mag=1))
    estimator.gyroBias = [[0], [0], [0]]
    sensorData = Sensors.vehicleSensors(
        gyro_x=3, gyro_y=2, gyro_z=-1,
        accel_x=20, accel_y=10, accel_z=-10,
        mag_x=15000, mag_y=7000, mag_z=10000
    )
    estimatedState = States.vehicleState(
        pn=-4, pe=0.0, pd=0.0, u=3, v=0.0, w=0.0,
        yaw=0.5235987755982988, pitch=-0.3490658503988659, roll=-0.5235987755982988,
        p=0.0, q=2, r=0.0,
        dcm=[
            [0.8137976813493738, 0.46984631039295416, 0.3420201433256687],
            [-0.2849136355292074, 0.8355050358314172, -0.46984631039295416],
            [-0.5065151074942515, 0.2849136355292074, 0.8137976813493738]
        ]
    )
    est_b, est_w, est_R = estimator.estimateAttitude(sensorData, estimatedState)


    print("\nEstimated Gyro Bias:")
    MM.matrixPrint(est_b)
    print("\nCorrected Angular Rates:")
    MM.matrixPrint(est_w)
    print("\nEstimated DCM (Rotation Matrix):")
    MM.matrixPrint(est_R)  

    assert len(est_b) == 3, "Gyro bias should be a 3x1 list"
    assert len(est_w) == 3, "Angular rate correction should be a 3x1 list"
    assert len(est_R) == 3 and len(est_R[0]) == 3, "DCM should be a 3x3 matrix"

    print("\n Test Completed Successfully ")

# Run the test
def test_estimateAirspeed():
    """
    Test estimateAirspeed
    """
    print("Running Airspeed Estimation Test ")
    estimator = VE.VehicleEstimator()
    estimator.setEstimatorGains(Controls.VehicleEstimatorGains(Kp_acc=0.0, Ki_acc=0.0, Kp_mag=0.0, Ki_mag=0.0))

    sensorData = Sensors.vehicleSensors(
        gyro_x=0.0, gyro_y=0.0, gyro_z=0.0,  
        accel_x=20, accel_y=10, accel_z=-10,  
        mag_x=0.0, mag_y=0.0, mag_z=0.0,  
        pitot=10  
    )

    estimatedState = States.vehicleState(
        pn=-4, pe=0.0, pd=0.0, u=3, v=0.0, w=0.0,
        yaw=0.5235987755982988, pitch=-0.3490658503988659, roll=-0.5235987755982988,
        p=0.0, q=2, r=0.0,
        dcm=[
            [0.8137976813493738, 0.46984631039295416, 0.3420201433256687],
            [-0.2849136355292074, 0.8355050358314172, -0.46984631039295416],
            [-0.5065151074942515, 0.2849136355292074, 0.8137976813493738]
        ]
    )
    estimatedState.Va = 3.0

    b_est, Va_est = estimator.estimateAirspeed(sensorData, estimatedState)

    # Print results
    print("\nEstimated Airspeed Bias (b_est) -5.6:")
    print(b_est)
    print("\nEstimated Airspeed (Va_est) 3.289552:")
    print(Va_est)
    print("\n===== Test Completed Successfully =====")



def test_estimateAltitude():
    """
    TestestimateAltitude
    """

    print("Running Altitude Estimation Test ")

  
    estimator = VE.VehicleEstimator()

    estimator.setEstimatorGains(Controls.VehicleEstimatorGains(
        Kp_h=0.0, Ki_h=0.0, Kp_h_gps=0.0, Ki_h_gps=0.0
    ))
    sensorData = Sensors.vehicleSensors(
        gyro_x=0.0, gyro_y=0.0, gyro_z=0.0,  
        accel_x=20, accel_y=10, accel_z=-10,  
        baro=0.0 
    )
    estimatedState = States.vehicleState(
        pn=-4, pe=0.0, pd=0.0, u=3, v=0.0, w=0.0,
        yaw=0.5235987755982988, pitch=-0.3490658503988659, roll=-0.5235987755982988,
        p=0.0, q=2, r=0.0,
        dcm=[
            [0.8137976813493738, 0.46984631039295416, 0.3420201433256687],
            [-0.2849136355292074, 0.8355050358314172, -0.46984631039295416],
            [-0.5065151074942515, 0.2849136355292074, 0.8137976813493738]
        ]
    )
    bh_hat, bh_gps, h_hat = estimator.estimateAltitude(sensorData, estimatedState)

    # Print results
    print("\nEstimated Accelerometer Bias (bh_hat/h_estimate):")
    print(bh_hat)

    print("\nEstimated GPS Bias (bh_gps/h_dot_estimate):")
    print(bh_gps)

    print("\nEstimated Altitude (h_hat/b_est):")
    print(h_hat)

    print("\nTest Completed Successfully")

# Run test function
test_estimateAltitude()
test_estimateAttitude()
test_estimateAirspeed()

