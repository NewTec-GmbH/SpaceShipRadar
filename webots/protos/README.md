# Zumo robot proto-files documentation

This documentation provides an overview of the .proto files used to define and render Zumo robots within the Webots simulation environment. The setup includes a base robot definition and several variants distinguished by unique ArUco markers.

### Components:
- Zumo32U4.proto: Defines the base Zumo robot structure.
- Zumo32U4_0.proto, Zumo32U4_1.proto, Zumo32U4_2.proto, Zumo32U4_3.proto, Zumo32U4_4.proto: Variants of the base robot, each  with a distinct ArUco marker on top.

### ArUco markers:
Each variant has an ArUco marker from the dictionary cv.aruco.DICT_4X4_50. The marker's ID corresponds to the suffix number in the filename:

File name |	Marker ID |	Description
--- | --- | ---
Zumo32U4_0.proto |	0 |	Marker ID 0 on top of the robot
Zumo32U4_1.proto |	1 |	Marker ID 1 on top of the robot
Zumo32U4_2.proto |	2 |	Marker ID 2 on top of the robot
Zumo32U4_3.proto |	3 |	Marker ID 3 on top of the robot
Zumo32U4_4.proto |	4 |	Marker ID 4 on top of the robot
