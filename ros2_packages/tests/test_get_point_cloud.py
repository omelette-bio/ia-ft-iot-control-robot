import pyrealsense2 as rs
import time 

print("demarrage")
start_t = time.time()
pc = rs.pointcloud()
# points = rs.points()
pipe = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 424, 240, rs.format.z16, 6)
config.enable_stream(rs.stream.color, 424, 240, rs.format.bgr8, 6)

pipe.start(config)

decimate = rs.decimation_filter(8)
align = rs.align(rs.stream.color)
print(f"temps d'initialisation {time.time() - start_t} seconde")

start = time.time()
#end = time.time()
i = 0
print("debut de la boucle")
while (i < 6):
	frames = pipe.wait_for_frames()

# depth_raw = frames.get_depth_frame()

	# start_t = time.time()
	# print(f"temps de decimation magnitude 8 pour du 424x240 {time.time() - start_t} seconde")
	# depth = decimated.get_depth_frame()

# print(f"before : {depth_raw.get_width()}x{depth_raw.get_height()}")
# print(f"after : {depth.get_width()}x{depth.get_height()}")

	aligned_frames = align.process(frames)
	decimated = decimate.process(aligned_frames).as_frameset()

	aligned_depth = decimated.get_depth_frame()
	aligned_color = decimated.get_color_frame()

	print("Depth aligné :", aligned_depth.get_width(), aligned_depth.get_height())
	print("Color aligné :", aligned_color.get_width(), aligned_color.get_height())

	# print(f"===Frame {i} id: {depth.get_frame_number()}===")
	# print(f"TimeStamp : {depth.get_timestamp()}")
	# pointcloud=pc.calculate(depth)
	# print(pointcloud)
	end = time.time()
	i+=1

print(f"temps total pour 6 frames : {time.time()-start}")
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
