#!/usr/bin/env python2
# racecar AI for Driver

import rospy
import math
from race.msg import drive_param
from sensor_msgs.msg import LaserScan

import constants

# useful functions
def average(array):
    total = 0
    for value in array:
        total += value
    return total / len(array)

def dist_between(pos1, pos2):
    return math.sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 )


class Car:
    def __init__(self):
        self.lidar = []
        self._angle = 0 # used by turningProgram
        self._position = 0 # used by turningProgram
        self.motorSpeed = 0
        self.turnAngle = 0
        self.velocity = 0
        self.fricCoeff = 10 # coefficient of friction between ground and tires
        self.carLength = 0.5 # length of car determines smallest turn radius
        self.reading_number = 1 # ray casts per degree (2 = 360 readings)
        # must be 0.25, 0.5, 1, 2, or 4
        self.lidar = [10.0]*(180*self.reading_number+1) #want lidar range to be 0 to 180 inclusive

    def changeMotorSpeed(self, val):
        self.motorSpeed = val

    def changeTurnAngle(self, ang):
        # clip turn angle to +/- pi/4
        if (ang > math.pi/4):
            self.turnAngle = math.pi/4
            return
        if (ang < -math.pi/4):
            self.turnAngle = -math.pi/4
            return
        self.turnAngle = ang

    def __del__(self):
        self.changeMotorSpeed(0)
        self.changeTurnAngle(0)

class RacecarAI:
    '''This is the Driver module that controls the car's basic functions
    It is designed to operate with or without a codriver.
    Without a codriver, the driver will simply drive slowly and safely, avoiding
    obstances and performing turns when necessary. It is designed to be lightweight
    and free of hardcoding.
    '''

    def __init__(self, car, codriver, dumb):
        # codriver - bool that enables codriver
        # dumb - bool that indicates that driver should only avoid collisions
        self.dumb = dumb
        self.state = "auto"
        self.car = car
        self.codriver = None
        self.fricCoeff = 10 # this will have to be adjusted to a realistic value
        self.safetyMode = False
        
        ''' Variables for collision avoidance'''
        self.collisionAvoid = False
        self.obsDist = 0
        self.obsAngle = 0
        
        self.start_angle = self.car._angle # used to keep track of how much the car has turned at nodes, updated in autoProgram
        self.start_pos = self.car._position # used to record distance traveled by car during collision avoidance mode

        self.pub = rospy.Publisher('drive_parameters', drive_param, queue_size=1) # ros publisher
        self.listener()

    #-------------------------------------------------------------------------------------

    def moveTowardsLongestDist(self, scope, right_bound, left_bound):
        ''' Uses the lidar to find the angle with the longest distance reading, and returns that angle. The angle is
        relative to the direction the car is facing. 0 degrees should be straight forward. Left angles are negative and
        right angles are positive.
        scope - limits the band of view which that car is using to make its decisions
        right_bound, left_bound - bottom and top boundary on the lidar indices that are taken into consideration 
        '''
        angle = math.pi / len(self.car.lidar)
        maximum = 0
        max_index = 0
        for reading in range(right_bound+scope, left_bound-scope):
            if(self.car.lidar[reading] >= maximum):
                maximum = self.car.lidar[reading]
                max_index = reading
            
        new_angle = angle*max_index - math.pi/2 # subtract PI/2 to make angle=0 -> angle=-PI/2
        return new_angle

    #-------------------------------------------------------------------------------------

    def _moveAwayFromWall(self, dist, angle):
        #if car is too close to a wall, modify angle to pull away
        left = self.car.lidar[0]
        right = self.car.lidar[len(self.car.lidar)-1]
        # dist will be scaled by number of carLengths (currently 1x)
        if(left < dist):
            rospy.loginfo("Too close to left wall: %f", left)
            return angle + math.pi/12
        if(right < dist):
            rospy.loginfo("Too close to right wall: %f", right)
            return angle - math.pi/12
        return angle

    def _getFrontDist(self, angle=0):
        middle = len(self.car.lidar)//2
        # relative angle ranges from -pi/2 to pi/2
        lidar_beam_angle = (math.pi / len(self.car.lidar))
        #determine the range of values to scan
        scope = int(math.atan(1/5) / lidar_beam_angle) + 1
        # this converts relative angle to corresponding LIDAR index
        index = int(angle / lidar_beam_angle + middle)
        if index + scope > len(self.car.lidar):
            index -= scope
        elif index - scope < 0:
            index += scope
        
        front_dist = self.car.lidar[index]
        for i in range(-scope,scope+1):
            if(self.car.lidar[index+i] < front_dist):
                front_dist = self.car.lidar[index+i]
        return front_dist

    def detectObstacle(self, front_dist):
        #CHECK FOR OBSTACLE within 4x current motor speed or 5x car lengths, whichever is greater
        if self.car.motorSpeed < self.car.carLength*4:
            lookaheadDistance = self.car.carLength*4
            #print("lookahead by car length "+str(lookaheadDistance))
        else:
            lookaheadDistance = self.car.motorSpeed
            #print("lookahead by motor speed "+str(lookaheadDistance))
        if front_dist < lookaheadDistance:
            print("obstacle detected " + str(front_dist)+ "m away")
            self.obsDist = front_dist
            return True
        else:
            return False
            
    def autoProgram(self):
        #CHECK FOR UNAVOIDABLE CRASH
        ''' If the distance reading directly in front of the car is less that the minimum turning radius
            given velocity of the car and friction, car cannot turn to avoid the crash
        '''
        front_dist = self._getFrontDist()
        
        if(self.car.velocity**2/(front_dist/3) > 9.81*self.fricCoeff):
            self.safetyMode = True
            print("safety mode on")
        self.collisionAvoid = self.detectObstacle(front_dist)
        if self.dumb:
            self.collisionAvoid = True
        
        #SET CAR VELOCITY PROPORTIONAL TO FRONT DISTANCE
        motor_speed = front_dist*0.5
        self.car.changeMotorSpeed(motor_speed)

        #DETERMINE ANGLE TO TURN WHEELS TO
        angle = math.pi / (len(self.car.lidar)-1)
        left_slopes = []
        right_slopes = []
        # average of slopes between left and right lidar readings
        for i in range(5):
            left_x1 = self.car.lidar[1] * math.cos(angle)
            left_y1 = self.car.lidar[1] * math.sin(angle)
            left_x2 = self.car.lidar[2] * math.cos(2*angle)
            left_y2 = self.car.lidar[2] * math.sin(2*angle)
            left_slopes.append( math.atan2((left_y2-left_y1) , (left_x2-left_x1)) )
            right_x1 = self.car.lidar[-2] * math.cos(math.pi - angle)
            right_y1 = self.car.lidar[-2] * math.sin(math.pi - angle)
            right_x2 = self.car.lidar[-3] * math.cos(math.pi - 2*angle)
            right_y2 = self.car.lidar[-3] * math.sin(math.pi - 2*angle)
            right_slopes.append( math.atan2((right_y2-right_y1) , (right_x2-right_x1)) )

        # if in a straight hallway type path
        ''' If the angle of left and right wall are kinda the same'''
        if(abs(average(left_slopes) - average(right_slopes)) < math.pi/10):
            new_angle = (average(left_slopes) + average(right_slopes) - math.pi)/2
        else: # if not in a straight hallway type path...
            # intelligent auto driver behavior (the thing to improve)
            #new_angle = self.moveTowardsLongestDist(0, 0, len(self.car.lidar))
            new_angle = 0
            print("not in straight hallway")

        #if car is too close to a wall, modify angle to pull away
        new_angle = self._moveAwayFromWall(self.car.carLength*1.5, new_angle)
                
        # turn the wheels of the car according to the new_angle    
        ''' The intensity of angle change is preportional to the difference in current angle and desired angle'''
        diff = abs(new_angle - self.car.turnAngle)
        if(new_angle > self.car.turnAngle): # right
            # todo, clarify 0.2 constant
            self.car.changeTurnAngle(self.car.turnAngle + 0.2*diff)
        elif(new_angle < self.car.turnAngle): # left
            self.car.changeTurnAngle(self.car.turnAngle - 0.2*diff)

        # update the start angle for decision nodes
        ''' During a turn, the start_angle is not updated, and is used a reference to measure how much the car has turned'''
        self.start_angle = self.car._angle
        self.start_pos = self.car._position

    def slowProgram(self):
        pass

    #-------------------------------------------------------------------------------------
    def clipAngle(self, angle, clipAmount):
        # angle is given in radians,will clip angle between -clipAmount and clipAmount
        ans = angle
        if angle > clipAmount:
            ans = clipAmount
        elif angle < -clipAmount:
            ans = -clipAmount
        return ans
    
    def _chooseAvoidAngle(self, dist, thresh, buffer):
        # make a list of tuples representing start and end indices of lidar segments
        segments = []
        start = 10
        end = 10
        _sum = 0
        for i in range(10,len(self.car.lidar)-10):
            if(self.car.lidar[i] > dist+thresh):
                end = i+1
                _sum += self.car.lidar[i]
            elif(start != end):
                segments.append( (start,end, _sum) )
                start = end = i+1
                _sum = 0
            else:
                start = end = i+1
        segments.append( (start, end, _sum) )
        # select segment of greatest area
        _max = 0
        index = 0
        for i in range(len(segments)):
            if(segments[i][2] > _max):
                _max = segments[i][2]
                index = i
        # get angle from the middle of the best segment
        size = segments[index][1]-segments[index][0]
        best_index = segments[index][0] + size//2
        angle = math.pi / len(self.car.lidar)
        ans = best_index * angle - math.pi/2
        
        return ans

                
    def avoidCollision(self):
        # todo, set to lowest motor speed
        motor_speed = 1
        self.car.changeMotorSpeed(motor_speed)
        buffer = math.pi/15
        new_angle = self._chooseAvoidAngle(self.obsDist, 15, buffer)
        #print("avoid angle: "+str(new_angle))
        #new_angle = self._moveAwayFromWall(10, new_angle)

        if(new_angle > self.car.turnAngle): # right
            # todo
            self.car.changeTurnAngle(self.car.turnAngle + 0.2)#weight*diff)
            #self.turningProgram()
        elif(new_angle < self.car.turnAngle): # left
            self.car.changeTurnAngle(self.car.turnAngle - 0.2)#weight*diff)
        # todo, clarify positions
        # dist = dist_between(self.start_pos, self.car._position)
        # print(dist)
        # print(self.start_pos)
        # if(dist > self.obsDist):
            # self.collisionAvoid = False
        self.collisionAvoid = self.detectObstacle(self._getFrontDist())

    #-------------------------------------------------------------------------------------

    def turningProgram(self):
        #set car velocity preportional to front dist
        #front_dist = self.car.lidar[len(self.car.lidar)//2]
        motor_speed = 1
        self.car.changeMotorSpeed(motor_speed)

        self.detectObstacle(self._getFrontDist())
        
        #decide turning angle
        ''' This makes sure Driver does not turn too much at a node. Planned to make the turning cap 90 degress, but found
        that an underestimate like 30 degrees work a lot better. Turing program only has to nudge the drive toward
        the right direction, after that, the autoProgram can stabalize the car on its path much better.'''
        if(abs(self.start_angle - self.car._angle) <= math.pi/6): # if car hasnt turned 30 degrees yet
            if(self.state == "left"):
                #print("left")
                right = 0
                left = len(self.car.lidar)//2-1
                new_angle = self.moveTowardsLongestDist(0, right, left)
            elif(self.state == "right"):
                #print("right")
                right = len(self.car.lidar)//2+1
                left = len(self.car.lidar)
                new_angle = self.moveTowardsLongestDist(0, right, left)
        else:
            #print("TURNED ENOUGH")
            new_angle = self.moveTowardsLongestDist(15, 0, len(self.car.lidar))
            
        diff = abs(new_angle - self.car.turnAngle)
        if(new_angle > self.car.turnAngle): # right
            # todo, clarify 0.1 constant
            self.car.changeTurnAngle(self.car.turnAngle + 0.1)#*abs(max_index - self.car.reading_number//2))
        elif(new_angle < self.car.turnAngle): # left
            self.car.changeTurnAngle(self.car.turnAngle - 0.1)#*abs(max_index - self.car.reading_number//2))

    #-------------------------------------------------------------------------------------

    def safetyProgram(self):
        if(self.car.velocity > 0.1): #not stopped
            self.car.changeMotorSpeed(-30)
        self.car.changeMotorSpeed(0)

    #-------------------------------------------------------------------------------------

    def main_funct(self):
        # check for a changed state from Codriver
        if self.codriver is not None:
            self.state = self.codriver.chooseState()
        
        if(not self.safetyMode):
            if(self.collisionAvoid):
                #print("COLLISION AVOID")
                self.avoidCollision()
            elif(self.state == "auto"):
                #print("auto")
                self.autoProgram()
            elif(self.state == "left" or self.state == "right"):
                #print(self.state)
                self.turningProgram()
            elif(self.state =="slow"):
                self.slowProgram()
        else:
            self.safetyProgram()
        print('motorspeed = ' + str(self.car.motorSpeed))
        self.publisher()

    #------------------------------------------------------------------------------------

    def update_lidar(self, data):
        #print(data)
        # LIDAR data: (index, distance), where index goes from 1080 to 0
        # from the right going CCW, with 0 as center, 270deg = 0, -270deg = 1080
        # updates car's lidar array with the new tuple, converting to 0 to 180*n
        for i in range(180,len(data.ranges)-180):
            # these are values behind the LIDAR, we will discard them
            mapped_index = int(-(180.0*self.car.reading_number/720)*(i-900))
            self.car.lidar[mapped_index] = data.ranges[i]
        self.main_funct()   # lidar data updates very quickly, maybe trigger main_funct some other way

    def publisher(self):
        #todo, map vel and angle to [-100, 100]
        msg = drive_param()
        msg.velocity = 0 # self.car.velocity
        msg.angle = self.car.turnAngle
        print("angle = " + str(self.car.turnAngle))
        self.pub.publish(msg)
    
    def listener(self):
        rospy.Subscriber('scan', LaserScan, self.update_lidar) # calls driver main function when lidar is updated

############################################################################

if __name__ == '__main__':
    rospy.init_node('driver', anonymous=True) # what is anonymous??
    car = Car()
    RacecarAI(car, False, False)
    rospy.spin()
