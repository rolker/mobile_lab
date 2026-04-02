
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace
from launch_ros.actions import SetParametersFromFile
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
   namespace = LaunchConfiguration('namespace')

   namespace_arg = DeclareLaunchArgument(
      "namespace", default_value=TextSubstitution(text="molab/johnny5")
   )

   hostname = LaunchConfiguration('hostname')

   hostname_arg = DeclareLaunchArgument(
      "hostname", default_value=TextSubstitution(text="johnny5")
   )

   return LaunchDescription([
      namespace_arg,
      hostname_arg,
      GroupAction(
         actions=[
            PushRosNamespace(namespace),
            IncludeLaunchDescription(
               AnyLaunchDescriptionSource(
                  PathJoinSubstitution([
                     FindPackageShare('axis_camera'),
                     'launch',
                     'axis_camera.launch'
                  ])
               ),
               launch_arguments={
                  'camera_name': 'johnny5',
                  'hostname': hostname,
                  'username': '',
                  'frame_width': '1920',
                  'frame_height': '1080',
                  'fps': '15',
                  'ptz_config': PathJoinSubstitution([
                     FindPackageShare('axis_camera'),
                     'config',
                     'axis_q62.yaml'
                  ]),
                  'enalble_ptz': 'true',
                  'enable_ir': 'true',
                  'enable_wiper': 'true',
                  'enable_defog': 'true',
               }.items()
            )

         ]
      )



   ])


# <launch>
#    <arg name="frame_id" default="johnny5"/>

#    <group ns="johnny5">

#       <node pkg="axis_tracker" type="axis_ptz.py" name="ptz">
#          <param name="url" value="http://192.168.50.55/"/>
#       </node>

#       <!-- launch video stream -->
#       <include file="$(find video_stream_opencv)/launch/camera.launch" >
#          <!-- node name and ros graph name -->
#          <arg name="camera_name" value="camera" />
#          <!-- means video device 0, /dev/video0 -->
#          <arg name="video_stream_provider" value="rtsp://192.168.50.55/axis-media/media.amp" />
#          <!-- throttling the querying of frames to -->
#          <arg name="fps" value="5" />
#          <!-- setting frame_id -->
#          <arg name="frame_id" value="$(arg frame_id)" />
#          <!-- camera info loading, take care as it needs the "file:///" at the start , e.g.:
#          "file:///$(find your_camera_package)/config/your_camera.yaml" -->
#          <arg name="camera_info_url" value="" />
#          <!-- flip the image horizontally (mirror it) -->
#          <arg name="flip_horizontal" value="false" />
#          <!-- flip the image vertically -->
#          <arg name="flip_vertical" value="false" />
#          <!-- visualize on an image_view window the stream generated -->
#          <arg name="visualize" value="false" />
#       </include>
#    </group>

# </launch>
