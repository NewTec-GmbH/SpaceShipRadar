# Coordinate Measurements Overview

This document presents a collection of measurements related to my system's coordinate display. The table below outlines the following key components:

- my_system: These are the coordinates that are ultimately displayed in the graphical user interface (GUI) of the code.
- webots_coordinates / real_coordinates: These represent the corresponding measurements obtained from the Webots simulation and the real-world test table.
- deviation: This indicates the difference between the coordinates recorded in Webots or the real world and those displayed by my system.

It is important to note that all coordinates are relative, with (0, 0) defined by me based on the first measurement taken.

## webots

the coordinates are scaled in mm

my_system | webots_coordinates | deviation
---|---|---
(59, 1770) | (0, 0) | 0, 0 
(1062, 1769) | (1000, 0) | 3, -1
(58, 1272) | (0, -500) | -1, 2 
(912,1272) | (850, -500) | 3, 2
(58, 269) | (0, -1500) | -1, -1

## real_world

## top bottom paper
my_system | real_coordinates | deviation
---|---|---
(184, 930) | (0, 0) | 0, 0 
(471, 930) | (297, 0) | -10, 0

## top paper
my_system | real_coordinates | deviation 
---|---|---
(194, 0) | (0, 0) | 0, 0
(484, 0) | (297, 0)  | -7, 0

## right paper
my_system | real_coordinates | deviation
---|---|---
(590, 370) | (0, 0) | 0, 0
(589, 719) | (0, 297) | 0, 53

## right paper
my_system | real_coordinates | deviation
---|---|---
(0, 340) | (0, 0) | 0, 0
(0, 696) | (0, 297) | 0, 59

## middle paper
my_system | real_coordinates | deviation 
---|---|---
(236, 340) | (0, 0) | 0, 0 
(453, 684) | (210, 297) | 7, 47

## middle paper (median)
my_system | real_coordinates | deviation 
---|---|---
(448, 259) | (0, 0) | 0, 0 
(814, 500) | (297, 210) | 69, 31

## middle paper (scaled)
my_system | real_coordinates | deviation 
---|---|---
(525, 221) | (0, 0) | 0, 0 
(894, 450) | (297, 210) | 72, 19

## middle paper (scaled 96)
my_system | real_coordinates | deviation 
---|---|---
(512, 213) | (0, 0) | 0, 0 
(867, 436) | (297, 210) | 58, 13

## middle paper (fixed arm)
my_system | real_coordinates | deviation 
---|---|---
(405, 224) | (0, 0) | 0, 0 
(715, 443) | (297, 210) | 13, 9

## middle paper (fixed arm 4x3)
my_system | real_coordinates | deviation 
---|---|---
(360, 233) | (0, 0) | 0, 0 
(683, 460) | (297, 210) | 26, 17

## middle paper (fixed arm and scaled perimeter 4x3)
my_system | real_coordinates | deviation 
---|---|---
(429, 166) | (0, 0) | 0, 0 
(748, 398) | (297, 210) | 22, 22

## middle paper (fixed arm and scaled perimeter REMOVED 4x3)
my_system | real_coordinates | deviation 
---|---|---
(384, 284) | (0, 0) | 0, 0 
(691, 501) | (297, 210) | 10, 7
