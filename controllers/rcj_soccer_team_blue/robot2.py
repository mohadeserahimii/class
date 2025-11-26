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
is_turning=0
robot_num=0
strength1=0
robotx1=0
roboty1=0
data={}
fasele_ta_robot1=0
to_boro=False
robot2DataValid=False
robot_num=0
ballx1=0
bally1=0
robotx1=0
roboty1=0
strength1=0
ballx3=0
bally3=0
robotx3=0
roboty3=0
strength3=0


class MyRobot2(RCJSoccerRobot):

    def send_data(self):

        if utils.ball_is_available==1:
            
            robot2DataValid=True 
            data = {"robot_num":2,'toop_be_zamin_x':utils.toop_be_zamin_x,'toop_be_zamin_y':utils.toop_be_zamin_y,'robot_x':utils.robotx,'robot_y':utils.roboty,'strength':utils.strength,'fasele_ta_robot1':fasele_ta_robot1,'robot2DataValid':robot2DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)

        else:

            robot2DataValid=False
            data = {"robot_num":2,'robot_x':utils.robotx,'robot_y':utils.roboty,'fasele_ta_robot1':fasele_ta_robot1,'robot2DataValid':robot2DataValid}
            packet = json.dumps(data)
            self.team_emitter.send(packet)



    def receive_data(self):

        global robot_num
        global robotx1
        global roboty1
        global strength1
        global data
        global fasele_ta_robot1  
        global to_boro
        global ballx1
        global bally1
        global robotx3
        global roboty3
        global strength3
        global ballx3
        global bally3

        while self.team_receiver.getQueueLength() > 0:
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)

            for key, values in data.items():
                if key=='robot_num':
                    robot_num=values
                if robot_num==1:
                    if key=='toop_be_zamin_x':
                        ballx1=values
                    elif key=='toop_be_zamin_y':
                        bally1=values
                    elif key=='robot_x':
                        robotx1=values
                    elif key=='robot_y':
                        roboty1=values
                    elif key=='strength':
                        strength1=values
                elif robot_num==3:
                    if key=='toop_be_zamin_x':
                        ballx3=values
                    elif key=='toop_be_zamin_y':
                        bally3=values
                    elif key=='robot_x':
                        robotx3=values
                    elif key=='robot_y':
                        roboty3=values
                    elif key=='strength':
                        strength3=values
                    elif key=='to_boro':
                        to_boro=values
                

    def run(self):
 
        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():            
                global fasele_ta_robot1

                utils.sensorUpdates(self) 
                utils.toop_be_zamin_update(self)

                fasele_ta_robot1=math.sqrt((robotx1-utils.robotx)**2+(roboty1-utils.roboty)**2)

                if utils.ball_is_available==1:
                    utils.turn(self)
                else:
                    utils.go_to(self,-0.3,0.4)


                '''if to_boro==True:
                    if roboty1>0.69 and 0.23<robotx1<0.35:
                        utils.go_to(self,0.3,0.71)
                    elif roboty1>0.69 and -0.23>robotx1>-0.35:
                        utils.go_to(self,-0.3,0.71)
                    else:
                        utils.turn(self)'''
                

                self.send_data_to_team(self.player_id)
