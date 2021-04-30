








# final_assignment


Graphic rapresentation of the components:
![rosgraph](https://user-images.githubusercontent.com/78663960/116706592-14aa6300-a9ce-11eb-839c-acc932621672.png)



How to run:

To launch it,  first download the repository from github, via git clone command https://github.com/Imdimark/Second_Assignmenty
 Then launch in this order the 2 launch files:
move_base.launch(it opens also simulation_gmapping.launch)
total.launch


content of the package

Nodes
bug_m.py:it is the main node, it uses the other nodes for the various services

randompos.py: It provides a service for setting a random position which the robot will achieve

user_interface.py  it implements the service used to choose the parameter stato and if stato == 2 it also acquires the user goal


wall_follow_service_m.py: m implements the algoritm that allows to follow the external wall.

Services

/wall_follower_switch implements the boolean switch for the option number 3 (follow the wall)


/user_interface implements the selection of the state and if state == 2 then also the manual choice of the next goal

/randompos implements the automatic choice of the next position




Parameters

des_x
des_y
stato
The first two are basically for the x and y poisition of the goal and stato is used to define the current state of the machine

Messages

publisher: 
move_base_msgs/MoveBaseActionGoal is used to send the goal to reach via the  move_base/goal topic
 geometry_msgs/twist is used to send linear and angular velocity via the topic "cmd/vel"

subscriber
nav_msgs/Odometry it is used by sub_odom in order to receive the position through the topic /Odom
		


robot behavior
The robot will have to locate itself in space via the move_base package and plan the path through the gmapping package. The user can select for keyboard options, depending on the choice made the behavior of the robot varies. The possible choices are:

Go to a random position: 6 possible combinations have been initialized in the randompos.py node, randomly one of the 6 options is chosen that will become the goal to be tagged.
Go to a location given by the user: in the user_interface.py node 6 locations have been initialized, the user can choose from keyboard a number from 1 to 6 that corresponds to the option.
Follow the wall
In options 1 and 2 you can enter a new goal only when the previous goal has been reached, option 3 instead can be blocked by typing 8, the robot will enter state 4 and return to the last position.

System’s limitations and possible improvements

It might be useful to try to improve the precision so as to reduce the threshold of goal achievement.

