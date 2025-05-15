from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace
from launch_ros.actions import SetParameter
from launch_ros.actions import SetParametersFromFile
from launch_ros.actions import SetRemap
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    namespace = LaunchConfiguration('namespace')

    namespace_arg = DeclareLaunchArgument(
        "namespace", default_value=TextSubstitution(text="molab")
    )

    return LaunchDescription([
        namespace_arg,
            GroupAction(
                actions=[
                    PushRosNamespace(namespace),
                    SetParametersFromFile(
                        filename=PathJoinSubstitution([
                            FindPackageShare('molab_hardware'),
                            'config',
                            'molab.yaml'
                        ])                
                    ),
                    GroupAction(
                        actions=[
                            PushRosNamespace('sensors'),
                            GroupAction(
                                actions=[
                                    PushRosNamespace('ais'),
                                    Node(
                                        package = 'marine_ais_tools',
                                        executable = 'nmea_relay',
                                        name = 'nmea_relay'
                                    ),
                                    Node(
                                        package = 'marine_ais_tools',
                                        executable = 'ais_parser',
                                        name = 'parser'
                                    ),
                                    Node(
                                        package = 'marine_ais_tools',
                                        executable = 'ais_contact_tracker',
                                        name = 'tracker'
                                    ),
                                    Node(
                                        package = 'nmea_navsat_driver',
                                        executable = 'nmea_topic_driver',
                                        name = 'navsat',
                                        remappings= [
                                            ('nmea_sentence', 'nmea')
                                        ]
                                    ),
                                    # todo: add heading sender if needed
                                ]
                            ),
                            IncludeLaunchDescription(
                                PythonLaunchDescriptionSource(
                                    PathJoinSubstitution([
                                        FindPackageShare('molab_hardware'),
                                        'launch',
                                        'johnny5_launch.py'
                                    ])
                                ),
                                launch_arguments={
                                    'namespace': 'johnny5'
                                }.items()
                            ),
                        ]

                    ),
                    # todo add optional udp bridge
                    Node(
                        package='mru_transform',
                        executable='mru_transform_node',
                        name='mru_transform',
                    ),
                    IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(
                            PathJoinSubstitution([
                                FindPackageShare('project11'),
                                'launch',
                                'platform_sender_launch.py'])
                        ),
                        launch_arguments={
                            'name': namespace
                        }.items()
                    ),

                ]
            )
    ])


# <launch>
#   <arg name="namespace" default="molab"/>
#   <arg name="operator_namespace" default="operator"/>
#   <arg name="logDirectory" default="$(find project11)/logs/ais/"/>
#   <arg name="udp_bridge" default="True"/>

#   <arg name="send_heading" default="True"/>
#   <arg name="heading" default="0"/>

#   <group ns="$(arg namespace)">

#     <group ns="sensors">

#       <group ns="ais">
#         <node pkg="marine_ais_tools" type="nmea_relay.py" name="nmea">
#           <param name="input_type" value="udp"/>
#           <param name="input_port" value="8010"/>
#           <param name="frame_id" value="$(arg namespace)/ais"/>
#         </node>
        
#         <node pkg="marine_ais_tools" type="ais_parser.py" name="parser">
#         </node>

#         <node pkg="marine_ais_tools" type="ais_contact_tracker.py" name="tracker">
#         </node>

#         <node pkg="nmea_navsat_driver" type="nmea_topic_driver" name="navsat">
#           <remap from="nmea_sentence" to="nmea"/>
#         </node>

#         <node if="$(arg send_heading)" pkg="molab_hardware" type="heading_sender.py" name="heading_sender">
#           <param name="frame_id" value="$(arg namespace)/ais"/>
#           <param name="heading" value="$(arg heading)"/>
#           <remap from="orientation" to="heading"/>
#         </node>

#       </group>

#       <include file="$(find molab_hardware)/launch/johnny5.launch">
#         <arg name="frame_id" value="$(arg namespace)/johnny5"/>
#       </include>

#     </group>

#     <node if="$(arg udp_bridge)" pkg="udp_bridge" type="udp_bridge_node" name="udp_bridge">
#       <param name="maxPacketSize" value="1400"/>
#     </node>

#     <node pkg="mru_transform" type="mru_transform_node" name="mru_transform">
#       <param name="base_frame" value="$(arg namespace)/base_link"/>
#       <param name="map_frame" value="$(arg namespace)/map"/>
#       <param name="odom_frame" value="$(arg namespace)/odom"/>
#     </node>

#     <node pkg="project11" type="platform_send.py" name="platform_sender"/>

#     <rosparam command="load" file="$(find molab_hardware)/config/molab.yaml"/>
#   </group>

# </launch>



