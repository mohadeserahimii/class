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
fasele_ta_robot1=0
strength1=0
robotx1=0
roboty1=0
data={}
fasele_robot2_ta_robot1=0
to_boro=False
robot3DataValid=False
robot_num=0
ballx2=0
bally2=0
robotx2=0
roboty2=0
strength2=0
ballx1=0
bally1=0
robotx1=0
roboty1=0
strength1=0

class MyRobot3(RCJSoccerRobot):
    
    def send_data(self):

        if utils.ball_is_available==1:

            robot3DataValid=True
            data = {"robot_num": 3,'toop_be_zamin_x':utils.toop_be_zamin_x,'toop_be_zamin_y':utils.toop_be_zamin_y,'robot_x':utils.robotx,'robot_y':utils.roboty,'strength':utils.strength,'to_boro':to_boro,'robot3DataValid':robot3DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)
            
        else:

            robot3DataValid=False
            data = {"robot_num": 3,'robot_x':utils.robotx,'robot_y':utils.roboty,'to_boro':to_boro,'robot3DataValid':robot3DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)

    def receive_data(self): 

        global data
        global robot_num
        global robotx1
        global roboty1
        global strength1
        global fasele_ta_robot1  
        global fasele_robot2_ta_robot1
        global to_boro
        global ballx1
        global bally1
        global ballx2
        global bally2
        global robotx2
        global roboty2
        global strength2
        
        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key, value in data.items():
                if key=='robot_num':
                    robot_num=value
                if robot_num==1:
                    if key=='toop_be_zamin_x':
                        ballx1=value
                    elif key=='toop_be_zamin_y':
                        bally1=value
                    elif key=='robot_x':
                        robotx1=value
                    elif key=='robot_y':
                        roboty1=value
                    elif key=='strength':
                        strength1=value
                elif robot_num==2:
                    if key=='toop_be_zamin_x':
                        ballx2=value
                    elif key=='toop_be_zamin_y':
                        bally2=value
                    elif key=='robot_x':
                        robotx2=value
                    elif key=='robot_y':
                        roboty2=value
                    elif key=='strength':
                        strength2=value
                    elif key=='fasele_ta_robot1':
                        fasele_robot2_ta_robot1=value
                    

    def run(self):

        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():
                global to_boro
                
                utils.sensorUpdates(self)
                utils.toop_be_zamin_update(self)
                fasele_ta_robot1=math.sqrt((robotx1-utils.robotx)**2+(roboty1-utils.roboty)**2)
                

                if utils.ball_is_available==1:
                    utils.turn(self)
                else:
                    utils.go_to(self,0.3,0.4)

                '''if fasele_robot2_ta_robot1<fasele_ta_robot1:
                    to_boro=True
                else:
                    to_boro=False
                    if roboty1>0.69 and 0.23<robotx1<0.35:
                        utils.go_to(self,0.3,0.71)
                    elif roboty1>0.69 and -0.23>robotx1>-0.35:
                        utils.go_to(self,-0.3,0.71)'''

                self.send_data_to_team(self.player_id)
