import imageio

# Read the video file
reader = imageio.get_reader('output.avi')
fps = reader.get_meta_data()['fps']

# Write the frames to a GIF file
writer = imageio.get_writer('output.gif', fps=fps)
for frame in reader:
    writer.append_data(frame)
writer.close()