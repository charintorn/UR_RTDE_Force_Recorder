import sys
sys.path.append('')
import os
import time

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

# IP address and port of the robot
ROBOT_HOST = "127.0.0.1"
ROBOT_PORT = 30004

# Path to the RTDE configuration file
CONFIG_FILE = "rtde_config.xml"

def main():
    
    # con = rtde.RTDE(args.host, args.port)
    # Create an RTDE connection object
    rtde_connection = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)

    try:
        # Get the path of the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path to the RTDE configuration file
        config_path = os.path.join(current_dir, CONFIG_FILE)

        # Configure the RTDE communication
        conf = rtde_config.ConfigFile(config_path)


        state_names, state_types = conf.get_recipe('state')  # Define recipe for access to robot output ex. joints,tcp etc.
        setp_names, setp_types = conf.get_recipe('setp')  # Define recipe for access to robot input
        watchdog_names, watchdog_types= conf.get_recipe('watchdog')



        # -------------------- Establish connection--------------------
        rtde_connection = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
        rtde_connection.connect()
        print("---------------Successfully connected to the robot-------------\n")

        # -------------------- Get controller version --------------------
        controller_version = rtde_connection.get_controller_version()
        print(controller_version)

        # ------------------- setup recipes ----------------------------
        FREQUENCY = 50 # send data in 500 Hz instead of default 125Hz
        rtde_connection.send_output_setup(state_names, state_types, FREQUENCY)
        setp = rtde_connection.send_input_setup(setp_names, setp_types)  # Configure an input package that the external application will send to the robot controller
        watchdog = rtde_connection.send_input_setup(watchdog_names, watchdog_types)

        # setp.input_double_register_0 = 0
        # setp.input_double_register_1 = 0
        # setp.input_double_register_2 = 0
        # setp.input_double_register_3 = 0
        # setp.input_double_register_4 = 0
        # setp.input_double_register_5 = 0

        # setp.input_bit_registers0_to_31 = 0

        # watchdog.input_int_register_0 = 0

        # start data synchronization
        if not rtde_connection.send_start():
            sys.exit()

        # start_pose = [-0.18507570121045797, -0.43755157063468963, 0.21101969081827837, -0.06998478570599498, -3.0949971695297402, 0.10056260631290592]
        # desired_pose = [-0.41227681851594755, -0.553539320093064, 0.07077025734923525, -0.06990025901302169, -3.0949715741835195, 0.10065200008528846]

        # orientation_const = start_pose[3:]



        # # Read and write data using the RTDE connection
        while True:
            state = rtde_connection.receive()
            tcp1 = state.actual_TCP_pose
            print(tcp1)
            time.sleep(1/50)

        #     # Read robot joint positions
        #     joint_positions = rtde_connection.get_actual_joint_positions()
        #     print("Joint positions:", joint_positions)

        #     # Write new joint positions
        #     new_joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        #     rtde_connection.send_tool_joint_positions(new_joint_positions)

    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        # Stop and close the RTDE connection
        # rtde_connection.stop()
        rtde_connection.disconnect()

if __name__ == "__main__":
    main()