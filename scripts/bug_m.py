#! /usr/bin/env python
#@package bug_m
#This is the main node, it uses the other nodes for the various services


import rospy
import time
# import ros message
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations
# import ros service
from std_srvs.srv import *
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionGoal
import actionlib
import math

#publisher initialization
pub_vel = None
goal_pub = None


#service initialization
srv_client_wall_follower_ = None
srv_client_user_interface_ = None
srv_client_randompos_= None

yaw_error_allowed_ = 5 * (math.pi / 180)  # 5 degrees

#initialization of the message containing the position
position_ = Point()
desired_position_ = Point()
desired_position_.x = None
desired_position_.y = None
desired_position_.z = 0
#states that the user can choose
state_desc_ = ['Go to random point', 'Go to choosen', 'wall following', 'target reached']


#callback function used bthe subscriber in order to receive the position
# @var position stores the position
def clbk_odom(msg):
	global position_
	position_ = msg.pose.pose.position

# the function goal is used to initialize and fill the fields with the @param des_pos_x and des_pos_y
def goal():
	global goal_pub
	msg_goal = MoveBaseActionGoal()
	msg_goal.goal.target_pose.header.frame_id = "map"
	msg_goal.goal.target_pose.pose.position.x= rospy.get_param("des_pos_x")
	msg_goal.goal.target_pose.pose.position.y= rospy.get_param("des_pos_y")
	msg_goal.goal.target_pose.pose.orientation.w= 1
	goal_pub.publish(msg_goal)
	return[]

#this function implements the change state function
# @param stato is used to acquire the actual state of the machine
def change_state():
	global state_, state_desc_
	global srv_client_wall_follower_, srv_client_randompos_, srv_client_user_interface_
	state_= rospy.get_param('stato')
	#state_ stores the actual state of the machine
	log = "state changed: %s" % state_desc_[state_ - 1] 
	rospy.loginfo(log)
	if state_ == 1 :  #random input
		resp = srv_client_wall_follower_(False)
		resp = srv_client_randompos_()
		goal()

	if state_ == 2: #user input
		resp = srv_client_wall_follower_(False)
		goal()

	if state_ == 3: #wall follow

		resp = srv_client_wall_follower_(True)
			    
	if state_ == 4: #stop
		resp = srv_client_wall_follower_(False)
		twist_msg = Twist()
		twist_msg.linear.x = 0
		twist_msg.linear.y = 0
		twist_msg.angular.z = 0
		pub_vel.publish(twist_msg)
		resp = srv_client_user_interface_()

def main():
	time.sleep(2)
	rospy.init_node('bug_m')
	#initialization of bug_m node	
	global position_, desired_position_, state_
	global srv_client_wall_follower_, srv_client_user_interface_, srv_client_randompos_, pub_vel, goal_pub
	
	sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
	pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	goal_pub = rospy.Publisher ('move_base/goal', MoveBaseActionGoal, queue_size=1)

	srv_client_wall_follower_ = rospy.ServiceProxy('/wall_follower_switch', SetBool)

	srv_client_user_interface_ = rospy.ServiceProxy('/user_interface', Empty)
	
	srv_client_randompos_ = rospy.ServiceProxy('/randompos', Empty)

	change_state()
	rate = rospy.Rate(20)
    	
	while not rospy.is_shutdown():
		desired_position_.x = rospy.get_param('des_pos_x')
		desired_position_.y = rospy.get_param('des_pos_y')
		
		if state_ == 1 or state_ == 2 :
			err_pos = math.sqrt(pow(desired_position_.y - position_.y,2) + pow(desired_position_.x - position_.x, 2))
			print err_pos
			if(err_pos < 0.35): #0.35 ensures that the goal is achieved despite not being 100% accurate
				print ("goal reached")
				rospy.set_param("stato", 4)
				change_state()
		if state_ == 3:
			on_off_3 = input('Please insert 8 to STOP the "wall follower" and return to previus goal ')
			if (on_off_3 == 8):
				rospy.set_param("stato", 4)
				change_state()

		if state_ == 4:

			change_state()

		rate.sleep()
	


if __name__ == "__main__":
	main()
