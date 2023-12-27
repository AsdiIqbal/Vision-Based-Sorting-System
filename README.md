# Vision-Based-Sorting-System

This project is concerned with the development of a high-speed sorting system based on Machine Vision that can segregate carton boxes on the main belt conveyor. This technology will benefit the industry in a variety of ways. The technology has a big potential in the various FMCG sectors, from saving labor costs and effort of recognizing (a product in a carton box) and then relocating that carton to another conveyor or workbench to saving a lot of time and eliminating human mistake. As a result, our objective is to create a low-cost Automated sorting system that can be used in local companies to assist them enhance production. Local industry development is essential for each country's economic progress.

<img src="https://github.com/AsdiIqbal/Vision-Based-Sorting-System/blob/main/Resources/intro.PNG">

## Requirements

You need to have basic knowledge of the following to catch up:

- [openCV](https://opencv.org/releases/)
- [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)
- [PyQt5](https://www.pythonguis.com/pyqt5-tutorial/)
- [Threading](https://docs.python.org/3/library/threading.html)

## About this Repo

This Repo provides access to the SDK end of this project. It consist of:

- Imaging
    - Frame Acquistion
    - Image Processing
    - Feature Extraction
- Connecting with controller interface

The vision-based high-speed sorting system will make use of a Vision Camera connected to a Raspberry Pi microcontroller. The arriving carton box on the conveyor will be detected by the camera. An ArUco Marker will be printed on the side of the Carton box, which the camera will detect. A box will be sorted based on the product identified by the camera. Soring mechanisms can be of several forms. Pneumatic sorting is commonly utilized because to its low cost, which is a crucial concern for any company. The carton box will be sorted by a pneumatic sorting system consisting of a cylinder, valves, and an end effector after being detected by the camera.

An `Aruco Marker` carrying some information about the cartoon is detected and processed from the captured frames to help in the algorithm ahead. A detailed Library of aruco markers can be accessed from `openCV` module. Frames and extracted features is displayed on a GUI. 

<img src="https://github.com/AsdiIqbal/Vision-Based-Sorting-System/blob/main/Resources/Capture.PNG">

GUI features the monitoring of the frames, Data extracted from the markers, Status of sensors, image processing settings and inventory management system.

<img src="https://github.com/AsdiIqbal/Vision-Based-Sorting-System/blob/main/Resources/1.PNG"><img src="https://github.com/AsdiIqbal/Vision-Based-Sorting-System/blob/main/Resources/2.PNG"><img src="https://github.com/AsdiIqbal/Vision-Based-Sorting-System/blob/main/Resources/3.PNG">
