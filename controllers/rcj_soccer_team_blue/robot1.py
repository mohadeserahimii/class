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
robot3DataValid=False
robot2DataValid=False
robot_num=0
ballx2=0
bally2=0
robotx2=0
roboty2=0
strength2=0
ballx3=0
bally3=0
robotx3=0
roboty3=0
strength3=0
othersBallX=0
othersBallY=0
numbersOfValidData=0
othersBallXFinal=0
othersBallyFinal=0

class MyRobot1(RCJSoccerRobot):
    def send_data(self):
        data = {"robot_num": 1,'toop_be_zamin_x':utils.toop_be_zamin_x,'toop_be_zamin_y':utils.toop_be_zamin_y,'robot_x':utils.robotx,'robot_y':utils.roboty,'strength':utils.strength}
        packet = json.dumps(data)
        self.team_emitter.send(packet)

    def receive_data(self):

        global data
        global robot_num
        global ballx2
        global bally2
        global robotx2
        global roboty2
        global strength2
        global ballx3
        global bally3
        global robotx3
        global roboty3
        global strength3
        global robot3DataValid
        global robot2DataValid
       

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
                    elif key=='toop_be_zamin_y':
                        bally3=value
                    elif key=='robot_x':
                        robotx3=value
                    elif key=='robot_y':
                        roboty3=value
                    elif key=='strength':
                        strength3=value
                    elif key=="robot3DataValid":
                        robot3DataValid=value
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
                    elif key=='robot2DataValid':
                        robot2DataValid=value

    def run(self): 

        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():

                global othersBallX
                global othersBallY
                global numbersOfValidData
                global othersBallXFinal
                global othersBallyFinal
                
                utils.sensorUpdates(self)
                utils.toop_be_zamin_update(self)
                
                if utils.ball_is_available==1:
                    utils.goal_keeper(self)
                else:
                    
                    othersBallX=0
                    if robot2DataValid==True:
                        othersBallX = ballx2 + othersBallX
                        numbersOfValidData+=1
                    if robot3DataValid==True:
                        othersBallX = ballx3 + othersBallX
                        numbersOfValidData+=1
                    if numbersOfValidData>0:
                        othersBallXFinal= othersBallX / numbersOfValidData
                    
                    othersBallY=0
                    numbersOfValidData=0

                    if robot2DataValid==True:
                        othersBallY= bally2 + othersBallY
                        numbersOfValidData+=1
                    if robot3DataValid==True:
                        othersBallY = bally3 + othersBallY
                        numbersOfValidData+=1
                    if numbersOfValidData>0:
                        othersBallyFinal= othersBallY / numbersOfValidData


                    if othersBallyFinal<roboty:
                        if utils.robotx>0 and utils.robotx<0.3 or utils.robotx<0 and utils.robotx>-0.3 :
                            utils.go_to(self,othersBallX,0.6)
                        elif utils.robotx>0:
                            utils.go_to(self,0.3,0.6)
                        elif utils.robotx<0:
                            utils.go_to(self,-0.3,0.6)
                    elif othersBallyFinal>utils.roboty and utils.robotx>0:
                        utils.go_to(self,0.3,othersBallyFinal)
                    elif othersBallyFinal>utils.roboty and utils.robotx<0:
                        utils.go_to(self,-0.3,othersBallyFinal)
                    else:
                        utils.go_to(self,0,0.58)



                self.send_data_to_team(self.player_id)
