from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint,VehicleCommand
import rclpy
from rclpy.node import Node
class OffboardControlNode(Node):
    def __init__(self):
        super().__init__('offboard_control_node')
        self.offboard_setpoint_counter = 0
        self.offboard_mode_publisher = self.create_publisher(OffboardControlMode,'/fmu/in/offboard_control_mode',10)
        self.trajectory_publisher = self.create_publisher(TrajectorySetpoint,'/fmu/in/trajectory_setpoint',10)
        self.vehicle_command_publisher = self.create_publisher(VehicleCommand,'/fmu/in/vehicle_command',10)
        self.timer = self.create_timer(0.02, self.timer_callback)
    def publish_offboard_mode(self):
        msg = OffboardControlMode()
        msg.timestamp=self.get_clock().now().nanoseconds//1000
        msg.position = True
        msg.velocity = False
        msg.acceleration=False
        msg.attitude = False
        msg.body_rate=False
        self.offboard_mode_publisher.publish(msg=msg)
    def publish_trajectory_setpoint(self):
        msg= TrajectorySetpoint()
        msg.timestamp = self.get_clock().now().nanoseconds//1000
        msg.position = [0.0,0.0,-3.0]
        msg.yaw = 0.0
        self.trajectory_publisher.publish(msg=msg)
    def publish_vehicle_command(self,command, param1=0.0, param2= 0.0):
        msg = VehicleCommand()
        msg.timestamp = self.get_clock().now().nanoseconds//1000
        msg.param1 = param1
        msg.param2 = param2
        msg.command=command
        self.vehicle_command_publisher.publish(msg=msg)
    
    def timer_callback(self):
        if self.offboard_setpoint_counter<10:
            self.publish_offboard_mode()
            self.publish_trajectory_setpoint()
            self.offboard_setpoint_counter = self.offboard_setpoint_counter + 1
        elif self.offboard_setpoint_counter == 10:
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE,1.0,6.0)
            self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,1.0)
            self.offboard_setpoint_counter= self.offboard_setpoint_counter + 1
        else:
            self.publish_trajectory_setpoint()

def main():
    rclpy.init()
    controlnode = OffboardControlNode()
    rclpy.spin(controlnode)
    controlnode.destroy_node()
    rclpy.shutdown()
main()