import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class FsmListener(Node):
    def __init__(self):
        super().__init__('fsm_listener')        # this string is the node name on the ROS2 graph

        # Create a subscriber: (message_type, topic_name, queue_size)
        self.subscriber_ = self.create_subscription(Int32, '/led_state', self.listener_callback, 10)

        self.get_logger().info('FSM Listener node has started')
        self.state_names = {0: 'OFF', 1: 'ON', 2: 'BLINK'}

    def listener_callback(self, msg):
        # msg.data is already the integer (0, 1, or 2)
        name = self.state_names[msg.data]
        # look it up in a dictionary and log it
        self.get_logger().info(f'Received state: {msg.data} ({name})')

def main(args = None):
    rclpy.init(args=args)
    node = FsmListener()
    rclpy.spin(node)                            # keeps the node alive, processing callbacks
    node.destroy_node()
    rclpy.shutdown()