#!/bin/bash  
cd ../../
rosdep install -i --from-path src --rosdistro foxy -y
colcon build --packages-select beeldverwerking
pip install svg_to_gcode
. install/setup.bash
