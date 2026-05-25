import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial

class FsmTalker(Node):
    def __init__(self):
        super().__init__('fsm_talker')          # this string is the node name on the ROS2 graph

        # Create a publisher: (message_type, topic_name, queue_size)
        self.publisher_ = self.create_publisher(Int32, '/led_state', 10)

        self.get_logger().info('FSM Talker node has started')

        # Retry serial connection (Arduino resets on connect)
        import time
        for attempt in range(5):
            try:
                self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
                self.get_logger().info('Serial port opened')
                break
            except Exception:
                self.get_logger().warn(f'Serial port not ready, attempt {attempt + 1}/5...')
                time.sleep(2)
        else:
            self.get_logger().error('Could not open serial port after 5 attempts')
            raise SystemExit(1)

        self.create_timer(0.1, self.timer_callback)
    
    def timer_callback(self):
        if self.ser.in_waiting:
            # read a line, decode it, strip whitespace
            line = self.ser.readline()          # b'1\r\n'  (raw bytes)
            text = line.decode('utf-8').strip() # '1'   (clean string)
            # parse to int
            value = int(text)                   # 1 (integer)
            # create Int32 message, set .data
            msg = Int32()
            msg.data = value                    # put the integer into the message
            # publish it
            self.publisher_.publish(msg)        # send it out on /led_state
            # log it
            self.get_logger().info(f'Published state: {value}')

def main(args = None):
    rclpy.init(args=args)
    node = FsmTalker()
    rclpy.spin(node)                            # keeps the node alive, processing callbacks
    node.destroy_node()
    rclpy.shutdown()