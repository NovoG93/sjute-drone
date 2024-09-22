import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

class JoystickControlNode(Node):
    def __init__(self):
        super().__init__('joystick_control_node')
        
        # Declare and get parameters for joystick mappings
        self.declare_parameter('axis_linear_x', 1)
        self.declare_parameter('axis_linear_y', 0)
        self.declare_parameter('axis_linear_z', 3)
        self.declare_parameter('axis_angular_z', 2)
        self.declare_parameter('button_takeoff', 0)
        self.declare_parameter('button_land', 1)
        
        self.axis_linear_x = self.get_parameter('axis_linear_x').get_parameter_value().integer_value
        self.axis_linear_y = self.get_parameter('axis_linear_y').get_parameter_value().integer_value
        self.axis_linear_z = self.get_parameter('axis_linear_z').get_parameter_value().integer_value
        self.axis_angular_z = self.get_parameter('axis_angular_z').get_parameter_value().integer_value
        self.button_takeoff = self.get_parameter('button_takeoff').get_parameter_value().integer_value
        self.button_land = self.get_parameter('button_land').get_parameter_value().integer_value

        # Subscribers
        self.joy_subscriber = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        
        # Publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.takeoff_publisher = self.create_publisher(Empty, 'takeoff', 10)
        self.land_publisher = self.create_publisher(Empty, 'land', 10)

    def joy_callback(self, msg: Joy):
        twist = Twist()
        
        # Map joystick axes to drone velocity commands
        twist.linear.x = msg.axes[self.axis_linear_x]
        twist.linear.y = msg.axes[self.axis_linear_y]
        twist.linear.z = msg.axes[self.axis_linear_z]
        twist.angular.z = msg.axes[self.axis_angular_z]
        
        self.cmd_vel_publisher.publish(twist)
        
        # Check for takeoff and land button presses
        if msg.buttons[self.button_takeoff]:
            self.takeoff_publisher.publish(Empty())
        if msg.buttons[self.button_land]:
            self.land_publisher.publish(Empty())

def main(args=None):
    rclpy.init(args=args)
    node = JoystickControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()