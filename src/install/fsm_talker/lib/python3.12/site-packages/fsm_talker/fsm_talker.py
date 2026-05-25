import rclpy
from rclypy.node import Node
from std_msgs.msg import Int32

class FsmTalker(Node):
    def __init__(self):
        super().__init__('fsm_talker') # this string is the node name on the ROS2 graph

        # Create a publisher: (message_type, topic_name, queue_size)
        self.publisher_ = self.create_publisher(Int32, '/led_state', 10)

        self.get_logger().info('FSM Talker node has started')

def main(args = None):
    rclpy.init(args=args)
    node = FsmTalker()
    rclpy.spin(node)    # keeps the node alive, processing callbacks
    node.destroy_node()
    rclpy.shutdown()