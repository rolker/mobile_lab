cmake_minimum_required(VERSION 3.14.4)
project(molab_hardware)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS molab_hardware/heading_sender.py DESTINATION lib/${PROJECT_NAME})
install(PROGRAMS molab_hardware/position_sender.py DESTINATION lib/${PROJECT_NAME})

ament_package()

