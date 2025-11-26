import rclpy # the ros2 python client library
from rclpy.node import Node # A base class from rclpy that represents a ROS2 node
from sensor_msgs.msg import PointCloud2, PointField
# from std_msgs.msg import PointCloud2
import pyrealsense2 as rs
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
from std_msgs.msg import Header

class PointCloudPublisher(Node):
	def __init__(self):
		# publisher config
		super().__init__('pointcloudpublisher')
		self.publisher_ = self.create_publisher(PointCloud2, 'RealsensePointCloud', 10)
		self.timer = self.create_timer(1/6, self.timer_callback)
		
		# realsense pipeline config
		self.pc = rs.pointcloud()
		self.points = rs.points()
		self.pipe = rs.pipeline()
		self.config = rs.config()
		self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 6)
		self.pipe.start(self.config)
		
		# extra data init
		self.i = 0

	def timer_callback(self):
		frames = self.pipe.wait_for_frames()
		depth = frames.get_depth_frame()
		
		if not depth:
			return
			
		points = self.pc.calculate(depth)
		
		verts = np.asanyarray(points.get_vertices())
		xyz = verts.view(np.float32).reshape(-1, 3)
		msg = self.numpy_to_pointcloud2(xyz, frame_id="camera_link")
		self.publisher_.publish(msg)
		self.get_logger().info(f'Sent pointcloud "{msg}"')
		
		self.i+=1
	
	def numpy_to_pointcloud2(self, points, frame_id="camera_link"):
		header = Header()
		header.stamp = self.get_clock().now().to_msg()
		header.frame_id = frame_id

		msg = pc2.create_cloud_xyz32(header, points)
		return msg

def main(args=None):
	rclpy.init(args=args) # Initialize the ROS2 Python system
	node = PointCloudPublisher() # Create an instance of the Listener node
	rclpy.spin(node) # Keep the node running, listening for messages
	node.destroy_node() # Cleanup when the node is stopped
	rclpy.shutdown() # It cleans up all ROS2 resources used by the node

if __name__ == '__main__':
	main()
