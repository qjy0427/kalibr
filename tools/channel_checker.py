import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

bag = rosbag.Bag('/home/jingye/Downloads/imu_image_1_2022-09-08-18-14-08.bag')
bridge = CvBridge()

for topic, msg, t in bag.read_messages(topics=['/zhz/driver/cam5/image_raw']):
    if 1 or isinstance(msg, Image):
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        channels = cv_image.shape[2] if len(cv_image.shape) == 3 else 1
        print(f"Number of channels: {channels}")
    else:
        print('Not an image message')
bag.close()
