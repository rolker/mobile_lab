#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geographic_msgs.msg import GeoPointStamped
from geometry_msgs.msg import TwistStamped

class PositionSender(Node):
    def __init__(self):
        super().__init__('heading_sender')
        self.publisher_ = self.create_publisher(GeoPointStamped, 'position', 10)
        self.velocity_publisher_ = self.create_publisher(TwistStamped, 'velocity', 10)  
        self.declare_parameter('latitude', 0.0)
        self.declare_parameter('longitude', 0.0)
        self.declare_parameter('altitude', 0.0)
        self.declare_parameter('frame_id', '')
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        position = GeoPointStamped()
        position.header.stamp = self.get_clock().now().to_msg()
        position.header.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        position.position.latitude = self.get_parameter('latitude').get_parameter_value().double_value
        position.position.longitude = self.get_parameter('longitude').get_parameter_value().double_value
        position.position.altitude = self.get_parameter('altitude').get_parameter_value().double_value
        self.publisher_.publish(position)

        velocity = TwistStamped()
        velocity.header = position.header

        self.velocity_publisher_.publish(velocity)


def main(args=None):
    rclpy.init(args=args)

    position_sender = PositionSender()

    rclpy.spin(position_sender)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    position_sender.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()