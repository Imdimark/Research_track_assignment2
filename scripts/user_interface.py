#! /usr/bin/env python

#@package user_interface
#it implements the service used to choose the @param stato 
#if stato == 2 it also acquires the user goal

# import ros stuff
import rospy
from std_srvs.srv import *

# service callback
#callback of the service user_interface
def set_new_user_pos(req):
	print("Please, insert the status:")
	print("1:Go to random point, 2:Go to choosen, 3:wall following, 4:target reached")
	stato = int(raw_input('status :'))
		
	while not stato == 1 or not stato == 2 or not stato == 3 or not stato == 4: #repeat loop until you have typed allowed values
		if stato == 1 or stato == 2 or stato == 3 or stato == 4:	
			print("You chose: "+ str(stato))
			rospy.set_param("stato", stato) #set @param stato
	
			if stato == 2:
				print("Please, digit a number to choose one of the six possible position (x,y) 1:(-4,-3) 2:(-4,2) 3:(-4,7) 4:(5,-7) 5:(5,-3) 6:(5,1)")
				posnotok = True

				while posnotok == True:
					userpos = int(raw_input('Inserisci la scelta :'))
					posnotok = False
					if userpos == 1:
						x = -4
						y =-3

					elif userpos == 2:
						x = -4
						y = 2

					elif userpos == 3:
						x = -4
						y = 7

					elif userpos == 4:
						x = 5
						y = -7

					elif userpos == 5:
						x = 5
						y = -3

					elif userpos == 6:
						x = 5
						y = 1
					else:
						posnotok = True
						print ("Your choose is not valid")

					rospy.set_param("des_pos_x", x)
					rospy.set_param("des_pos_y", y)
				print("Hi! We are reaching the chosen position: x = " + str(x) + ", y = " + str(y))
			break
		else:
			print("Wrong choise,please insert the status (1 or 2 or 3 or 4")
			print("1:Go to random point, 2:Go to choosen, 3:wall following, 4:target reached")
			stato = int(raw_input('status :'))
			#Break
	return []

def main():
	#initalization of the node
	rospy.init_node('user_interface')
	srv = rospy.Service('user_interface', Empty, set_new_user_pos)
	rate = rospy.Rate(20)
	while not rospy.is_shutdown(): 
		rate.sleep()
if __name__ == '__main__':
	main()


