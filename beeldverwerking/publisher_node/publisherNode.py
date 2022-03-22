import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class Publisher(Node):

    def __init__(self):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)

    def send_image(self, image):
        msg = String()
        msg.data = image
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)