# multi-robot-control

## Multiple robots and drones control with obstacle avoidance

[readme](https://github.com/SummerOf15/multi-robot-control/blob/main/multi-robot/ReadMe.md)

![image-20210310213208143](README.assets/image-20210310213208143.png)



## YOLO object detection

### Environment

- ubuntu 18.04
- ros-melodic
- python 2.7
- pytorch 1.4

For the dependence of other libraries, please visit the `requirements.txt`

### Installation

Download the weights file and put it under `model` directory.

```bash
wget http://pjreddie.com/media/files/yolov3.weights
```

#### Create environment

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
source devel/setup.bash
cd src/
git clone https://github.com/SummerOf15/multi-robot-control.git
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

#### Run

```bash
rosrun yolo yolo_ros.py
```

### Topics

#### input images

- /husky/front_cam/camera/image (you can modify it in `yolo_ros.py` )

#### output detection results

- /result (you can modify it in `yolo_ros.py`)

