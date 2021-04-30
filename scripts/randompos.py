#! /usr/bin/env python

#@package randompos
#it implements the service used to generate a random position for the goal
# import ros stuff
import rospy
import math
import random
from std_srvs.srv import *

#service callback
# @param des_pos_x and des_pos_y are set whit the random x and random y
def set_rand_pos (req):

	randpos = random.randint(1,6)
	print("The random number is:", randpos)
	print("The random number is: " + str(randpos) )

	if randpos == 1:
		x = -4
		y =-3

	elif randpos == 2:
		x = -4
		y = 2

	elif randpos == 3:
		x = -4
		y = 7

	elif randpos == 4:
		x = 5
		y = -7

	elif randpos == 5:
		x = 5
		y = -3

	elif randpos == 6:
		x = 5
		y = 1

	rospy.set_param("des_pos_x", x)
	rospy.set_param("des_pos_y", y)
	print("settati")
	print("The random x and y are: = " + str(x) + ", and = " + str(y))
	return []

def main():
	#initialization of the node and the service
	rospy.init_node ('randompos')
	srv = rospy.Service('randompos', Empty, set_rand_pos)
	rate = rospy.Rate(20)
    	while not rospy.is_shutdown():
		rate.sleep()

if __name__ == '__main__':
	main()

