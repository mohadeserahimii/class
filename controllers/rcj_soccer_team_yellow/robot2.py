# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import math  # noqa: F401

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

robotx=0 
roboty=0
heading=0
robot_pos=''
robot_angle=0 
data = ""
team_data = ""
ball_data = ""
heading = ""
direction = ""
zavie_maghsad=0
error_zavie=0
error=0
error_fasele=0
state=1
is_turning=0

class MyRobot2(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1 :
            if self.is_new_data():                
                
                utils.sensorUpdates(self) 
                utils.toop_be_zamin_update(self)

                if utils.ball_is_available==1:
                    utils.turn(self)
                else:
                    utils.go_to(self,0.2,0.3)

                self.send_data_to_team(self.player_id)
