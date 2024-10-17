import rosbag
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

# 初始化 CvBridge
bridge = CvBridge()

# 打开 rosbag 文件
bag = rosbag.Bag('/home/jingye/Downloads/imu_image_1_2022-09-08-18-14-08.bag', 'r')
new_bag = rosbag.Bag('/home/jingye/Downloads/corrected_1.bag', 'w')

# 读取 rosbag 中的图像 topic
for topic, msg, t in bag.read_messages():
    if topic in ['/zhz/driver/cam4/image_raw', '/zhz/driver/cam5/image_raw']:
        # 使用 CvBridge 将 ROS Image 转为 OpenCV 图像
        msg.width = 768
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')  # 单通道图像
        cv_image = cv_image[:, :640]

        # # 使用 cv2 将单通道图像转换为三通道
        # cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2RGB)

        # 将 OpenCV 图像转换回 ROS Image 消息
        img_msg = bridge.cv2_to_imgmsg(cv_image, encoding='mono8')
        img_msg.header = msg.header

        # 将转换后的图像保存到新的 rosbag 文件
        new_bag.write(topic, img_msg, t)
    else:
        new_bag.write(topic, msg, t)

# 关闭 bag 文件
bag.close()
new_bag.close()
