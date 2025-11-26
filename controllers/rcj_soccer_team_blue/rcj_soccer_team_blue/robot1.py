# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import math  # noqa: F401
import json

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
robot_num=0
ballx3=0

class MyRobot1(RCJSoccerRobot):
    def send_data(self):
        data = {"robot_num": 1,'toop_be_zamin_x':utils.toop_be_zamin_x,'toop_be_zamin_y':utils.toop_be_zamin_y,'robot_x':utils.robotx,'robot_y':utils.roboty,'strength':utils.strength}
        packet = json.dumps(data)
        self.team_emitter.send(packet)

    def receive_data(self):
        global data
        global robot_num
        global ballx3

        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key, value in data.items():
                if key=='robot_num':
                    robot_num=value
                if robot_num==3:
                    if key=='toop_be_zamin_x':
                        ballx3=value
                elif robot_num==2:
                    if key=='toop_be_zamin_x':
                        ballx2=value

    def run(self): 

        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():
                
                utils.sensorUpdates(self)
                utils.toop_be_zamin_update(self)
                
                if utils.ball_is_available==1:
                    utils.goal_keeper(self) 
                else:
                    utils.go_to(self,0,0.58)


                self.send_data_to_team(self.player_id)
