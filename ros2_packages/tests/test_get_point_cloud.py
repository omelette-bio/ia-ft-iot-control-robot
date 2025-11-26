import pyrealsense2 as rs

pc = rs.pointcloud()
points = rs.points()
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 6)
pipe.start(config)

for i in range(3):
	frames = pipe.wait_for_frames()
	depth = frames.get_depth_frame()
	print(f"===Frame {i} id: {depth.get_frame_number()}===")
	print(f"TimeStamp : {depth.get_timestamp()}")
	pointcloud=pc.calculate(depth)
	print(pointcloud)

pipe.stop()

# faudra que je set un timer 1/6 self.timer_callback

'''
verts = np.asanyarray(points.get_vertices())
xyz = verts.view(np.float32).reshape(-1, 3)

# Build ROS2 message
msg = self.numpy_to_pointcloud2(xyz, frame_id="camera_link")

# Publish
self.pub.publish(msg)
'''
