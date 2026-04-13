from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
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

    heading = LaunchConfiguration('heading')

    heading_arg = DeclareLaunchArgument('heading', default_value=TextSubstitution(text="0.0"))

    latitude_arg = DeclareLaunchArgument('latitude', default_value=TextSubstitution(text="43.07202674"))
    longitude_arg = DeclareLaunchArgument('longitude', default_value=TextSubstitution(text="-70.71174829"))
    altitude_arg = DeclareLaunchArgument('altitude', default_value=TextSubstitution(text="-19.3"))

    enable_bridge = LaunchConfiguration('enable_bridge')
    enable_bridge_arg = DeclareLaunchArgument(
        "enable_bridge", default_value="false"
    )


    return LaunchDescription([
        namespace_arg,
        heading_arg,
        latitude_arg,
        longitude_arg,
        altitude_arg,
        enable_bridge_arg,
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
                                    name = 'ais_nmea_relay'
                                ),
                                Node(
                                    package = 'marine_ais_tools',
                                    executable = 'ais_parser',
                                    name = 'parser'
                                ),
                                Node(
                                    package = 'marine_ais_tools',
                                    executable = 'ais_contact_tracker',
                                    name = 'tracker',
                                    respawn = True,
                                    respawn_delay = 2.0
                                ),
                                Node(
                                    package = 'nmea_navsat_driver',
                                    executable = 'nmea_topic_driver',
                                    name = 'ais_navsat',
                                    remappings= [
                                        ('nmea_sentence', 'nmea')
                                    ]
                                ),
                                # Node(
                                #     package='molab_hardware',
                                #     executable='heading_sender.py',
                                #     name='heading_sender',
                                #     parameters=[{
                                #         'heading': heading
                                #     }]
                                # )
                            ]
                        ),
                        GroupAction(
                            actions=[
                                PushRosNamespace('gps'),
                                Node(
                                    package = 'marine_ais_tools',
                                    executable = 'nmea_relay',
                                    name = 'gps_nmea_relay'
                                ),
                                # Node(
                                #     package = 'nmea_navsat_driver',
                                #     executable = 'nmea_topic_driver',
                                #     name = 'gps_navsat',
                                #     remappings= [
                                #         ('nmea_sentence', 'nmea')
                                #     ]
                                # ),
                                Node(
                                    package='molab_hardware',
                                    executable='heading_sender.py',
                                    name='heading_sender',
                                    parameters=[{
                                        'heading': heading
                                    }],
                                    
                                ),
                                Node(
                                    package='molab_hardware',
                                    executable='position_sender.py',
                                    name='position_sender',
                                    parameters=[{
                                        'latitude': LaunchConfiguration('latitude'),
                                        'longitude': LaunchConfiguration('longitude'),
                                        'altitude': LaunchConfiguration('altitude')
                                    }],
                                    remappings=[('position','fix'),('velocity', 'vel')]
                                )

                            ]
                        ),
                        GroupAction(
                            actions=[
                                PushRosNamespace('radar'),
                                Node(
                                    package='simrad_halo_radar',
                                    executable = 'simrad_halo_radar',
                                    name = 'radar'
                                ),
                                GroupAction(
                                    actions=[
                                        PushRosNamespace('halo_a'),
                                        Node(
                                            package='marine_radar_tracker',
                                            executable='marine_radar_tracker',
                                            name='marine_radar_tracker',
                                            parameters=[{
                                                'map_frame': 'molab/map_tide'}],
                                            remappings=[('radar_data', 'data')],
                                            respawn=True,
                                            respawn_delay=2.0
                                        )
                                        # Node(
                                        #     package='echoflow',
                                        #     executable = 'radar_grid_map',
                                        #     name = 'echoflow_a',
                                        #     parameters=[{
                                        #         'map.frame_id': 'molab/map',
                                        #         'map.resolution': 2.0,
                                        #         'map.width': 2000.0,
                                        #         'map.length': 2000.0,
                                        #         'filter.near_clutter_range': 1.5,
                                        #     }]
                                        # ),
                                        # Node(
                                        #     package='echoflow',
                                        #     executable='flow_tracker',
                                        #     name= 'flow_tracker',
                                        #     # parameters=[{
                                        #     #     'map.width': 2000.0,
                                        #     #     'map.length': 2000.0,
                                        #     #     'particle_filter_statistics.frame_id': 'molab/map',
                                        #     # }]
                                        # ),
                                        # Node(
                                        #     package='rviz2',
                                        #     executable='rviz2',
                                        #     name='rviz_echoflow',
                                        #     arguments = [
                                        #         '-d',
                                        #         PathJoinSubstitution([
                                        #             FindPackageShare('molab_hardware'),
                                        #             'config',
                                        #             'echoflow.rviz'
                                        #         ])

                                        #     ]
                                        # )
                                    ]
                                )
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
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        PathJoinSubstitution([
                            FindPackageShare('udp_bridge'),
                        'launch',
                        'udp_bridge_launch.py'
                    ])
                    ),
                    condition = IfCondition(enable_bridge)
                ),
                Node(
                    package='mru_transform',
                    executable='mru_transform_node',
                    name='mru_transform',
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        PathJoinSubstitution([
                            FindPackageShare('mru_transform'),
                            'launch',
                            'tide_copier_launch.py'])
                    ),
                    launch_arguments={
                        'name': namespace
                    }.items()
                ),
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        PathJoinSubstitution([
                            FindPackageShare('marine_autonomy'),
                            'launch',
                            'platform_sender_launch.py'])
                    ),
                    launch_arguments={
                        'name': namespace
                    }.items()
                ),

            ]
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('molab_description'),
                    'launch',
                    'publish_state_launch.py'])
            ),
            launch_arguments={
                'namespace': namespace
            }.items()
        ),
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



