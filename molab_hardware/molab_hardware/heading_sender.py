#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import QuaternionStamped
import math
import numpy as np

# From: https://raw.githubusercontent.com/ros/geometry_tutorials/ros2/turtle_tf2_py/turtle_tf2_py/turtle_tf2_broadcaster.py
#
# This function is a stripped down version of the code in
# https://github.com/matthew-brett/transforms3d/blob/f185e866ecccb66c545559bc9f2e19cb5025e0ab/transforms3d/euler.py
# Besides simplifying it, this version also inverts the order to return x,y,z,w, which is
# the way that ROS prefers it.
def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = np.empty((4, ))
    q[0] = cj*sc - sj*cs
    q[1] = cj*ss + sj*cc
    q[2] = cj*cs - sj*sc
    q[3] = cj*cc + sj*ss

    return q

class HeadingSender(Node):
    def __init__(self):
        super().__init__('heading_sender')
        self.publisher_ = self.create_publisher(QuaternionStamped, 'heading', 10)
        self.declare_parameter('heading', 0.0)
        self.declare_parameter('frame_id', '')
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):

        q = QuaternionStamped()
        q.header.stamp = self.get_clock().now().to_msg()
        q.header.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value

        heading =  self.get_parameter('heading').get_parameter_value().double_value
        quat = quaternion_from_euler(0, 0, math.radians(90.0-heading))
        q.quaternion.x = quat[0]
        q.quaternion.y = quat[1]
        q.quaternion.z = quat[2]
        q.quaternion.w = quat[3]
        self.publisher_.publish(q)

def main(args=None):
    rclpy.init(args=args)

    heading_sender = HeadingSender()

    rclpy.spin(heading_sender)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    heading_sender.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()