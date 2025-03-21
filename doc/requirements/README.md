# Glossary

Abbreviation | Meaning
--- | ---
ArUco | Augmented Reality University of Cordoba
mm | millimeters

The text inside the square bracket ([]) describes the requirement-ID

# Requirements

SSR = Space Ship Radar

---

The system shall locate the position, rotation and speed of every robot in its designated field of view [GEN-02]

---

The system shall measure the position in mm [GEN-03]

---

The system shall define the coordinate origin by an ArUco-tracker (dict= cv2.aruco.DICT_5X5_50, id=6) [GEN-04]

---


The system shall measure the rotation in mrad, with 0 representing the angle pointing straight up (y-direction) [GEN-05]

---

The system shall measure speed in mm/s and is split into a x- and y-direction [GEN-06]

---

The system can limit the visible area by 4 ArUco-markers [GEN-07]

---

The GUI may make an image if the "Create picture"-button is pressed [GEN-08]

---

## ArUco-Marker

The ArUco-markers shall be the following from the dictionary DICT_ARUCO_ORIGINAL with the IDs [ARUCO-01]:
- 6 = top-left  
![pink_6](../../webots/protos/pink_6.png)
- 13 = top-right  
![pink_13](../../webots/protos/pink_13.png)
- 35 = bottom-right  
![pink_35](../../webots/protos/pink_35.png)
- 49 = bottom-left  
![pink_49](../../webots/protos/pink_49.png)

---

The designated field of view shall be restricted by the 4 ArUco-markers and is orientated to match the markers (the top-left marker needs to be in the top-left corner) [ARUCO-02]

---

Pixel coordinates shall be translated to real world coordinates by using the size of the ArUco-markers or the distance between the markers
The resulting translation can have a deviation of 10% to the "real" size [ARUCO-03]


## Miscellaneous

---

SSR shall be simulated in Webots [MISC-01]

---

SSR shall communicate with a real esp-32-cam [MISC-02]

---

SSR shall send the position, rotation and speed with the MQTT-protocol to each robot [MISC-03]

---

A picture of the tracked objects may be provided under src/img folder [MISC-04]

---

