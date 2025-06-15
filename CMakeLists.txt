cmake_minimum_required(VERSION 3.0.2)
project(molab_description)

find_package(catkin REQUIRED COMPONENTS
  xacro
)

catkin_package(
  CATKIN_DEPENDS xacro
)
