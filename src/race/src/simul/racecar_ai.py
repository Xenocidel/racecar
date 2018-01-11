# racecar AI for driver

import math
import python_racecar

def average(array):
    total = 0
    for value in array:
        total += value
    return total / len(array)

def dist_between(pos1, pos2):
    return math.sqrt( (pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 )


class Codriver:

    def __init__(self, car:"Racecar"):
        self.nodes = [(85,85,"right"),(400,85,"right"),(400,515,"left"),
                      (715,515,"left"),(715,85,"left"),(400,85,"left"),
                      (400,515,"right"),(85,515,"right")]
        self.car = car
        self.next_index = 0
        self.at_node = False

    def chooseState(self):
        node = self.nodes[self.next_index]
        #if car is within a certain radius of node...
        if(math.sqrt((self.car._position[0]-node[0])**2 + (self.car._position[1]-node[1])**2) < 90):
            self.at_node = True
            return self.nodes[self.next_index][2]
        else:
            #choose next node and assign Driver a mode
            if(self.at_node): # exiting a node
                self.next_index += 1
                if(self.next_index >= len(self.nodes)):
                    self.next_index = 0
                self.at_node = False
            return "auto"

class RacecarAI:
    '''This is the Driver module that controls the car's basic functions
    It is designed to operate with or without a codriver.
    Without a codriver, the driver will simply drive slowly and safely, avoiding
    obstances and performing turns when necessary. It is designed to be lightweight
    and free of hardcoding.
    '''

    def __init__(self, car:"Racecar", screen, codriver, dumb):
        # codriver - bool that enables codriver
        # dumb - bool that indicates that driver should only avoid collisions
        self.dumb = dumb
        self.state = "auto"
        self.car = car
        if codriver == False:
            self.codriver = None
        else:
            self.codriver = Codriver(car) # in ROS, Codriver will just be a seperate node
        self.fricCoeff = 10 # this will have to be adjusted to a realistic value
        self.safetyMode = False
        
        ''' Variables for collision avoidance'''
        self.collisionAvoid = False
        self.obsDist = 0
        self.obsAngle = 0
        
        self.screen = screen # not necessary, just here to display vector to longest distance
        self.start_angle = self.car._angle # used to keep track of how much the car has turned at nodes, updated in autoProgram
        self.start_pos = self.car._position # used to record distance traveled by car during collision avoidance mode

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

        #draw line just for gui visual
        self.screen.create_line(self.car._position[0], self.car._position[1],
                               self.car._position[0] + math.cos(new_angle + self.car._angle)*50,
                               self.car._position[1] + math.sin(new_angle + self.car._angle)*50, fill="#00FFFF")

        return new_angle

    #-------------------------------------------------------------------------------------

    def _moveAwayFromWall(self, dist, angle):
        #if car is too close to a wall, modify angle to pull away
        right = self.car.lidar[0]
        left = self.car.lidar[len(self.car.lidar)-1]
        if(right < dist):
            #print("too close to right")
            return angle + math.pi/12
        if(left < dist):
            #print("too close to left")
            return angle - math.pi/12
        return angle

    def _getFrontDist(self):
        middle = len(self.car.lidar)//2
        front_dist = self.car.lidar[middle]
        for i in range(-2,3):
            if(self.car.lidar[middle+i] < front_dist):
                front_dist = self.car.lidar[middle+i]
        return front_dist

    def autoProgram(self):
        #CHECK FOR UNAVOIDABLE CRASH
        ''' If the distance reading directly in front of the car is less that the minimum turning radius
            given velocity of the car and friction, car cannot turn to avoid the crash
        '''
        front_dist = self._getFrontDist()
        
        if(self.car.velocity**2/(front_dist/3) > 9.81*self.fricCoeff):
            self.safetyMode = True
            print("safety mode on")

        #CHECK FOR OBSTACLE
        if(front_dist < 100):
            self.collisionAvoid = True
            self.obsDist = front_dist
        
        #SET CAR VELOCITY PREPORTIONAL TO FRONT DISTANCE
        motor_speed = int(15 + 40*(front_dist/500))
        self.car.changeMotorSpeed(motor_speed)

        #DETERMINE ANGLE TO TURN WHEELS TO
        angle = math.pi / len(self.car.lidar)
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
            if self.dumb:
                # if driver is dumb, will just keep going straight until it has
                # to avoid a collision
                new_angle = self.car.turnAngle
            else:
                # intelligent auto driver behavior (the thing to improve)
                new_angle = self.moveTowardsLongestDist(0, 0, len(self.car.lidar))

        #if car is too close to a wall, modify angle to pull away
        new_angle = self._moveAwayFromWall(20, new_angle)
                
        # turn the wheels of the car according to the new_angle    
        ''' The intensity of angle change is preportional to the difference in current angle and desired angle'''
        diff = abs(new_angle - self.car.turnAngle)
        if(new_angle > self.car.turnAngle): # right
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
    
    def _chooseAvoidAngle(self, dist, thresh, buffer):
        angle = math.pi / len(self.car.lidar)
        middle = len(self.car.lidar)//2
        left_count = 0
        right_count = 0
        left_angle = 0
        right_angle = 0
        
        for i in range(len(self.car.lidar)//2-1):
            if(self.car.lidar[middle+i] > dist+thresh):
                right_count += self.car.lidar[middle+i]
                if(right_angle == 0):
                    right_angle = angle*i + buffer
            if(self.car.lidar[middle-i] > dist+thresh):
                left_count += self.car.lidar[middle-i]
                if(left_angle == 0):
                    left_angle = -angle*i - buffer
                    
        if(left_count == 0 and right_count == 0):
            return self.moveTowardsLongestDist(0, 0, len(self.car.lidar))
        elif(right_count > left_count):
            return right_angle
        else:
            return left_angle

    def avoidCollision(self):
        
        motor_speed = 30
        self.car.changeMotorSpeed(motor_speed)

        buffer = math.pi/20
        new_angle = self._chooseAvoidAngle(self.obsDist, 15, buffer)
        #new_angle = self._moveAwayFromWall(10, new_angle)

        if(new_angle > self.car.turnAngle): # right
            self.car.changeTurnAngle(self.car.turnAngle + 0.2)#weight*diff)
            #self.turningProgram()
        elif(new_angle < self.car.turnAngle): # left
            self.car.changeTurnAngle(self.car.turnAngle - 0.2)#weight*diff)

        dist = dist_between(self.start_pos, self.car._position)
        #print(dist)
        #print(self.start_pos)
        if(dist > self.obsDist):
            self.collisionAvoid = False

    #-------------------------------------------------------------------------------------

    def turningProgram(self):
        #set car velocity preportional to front dist
        #front_dist = self.car.lidar[len(self.car.lidar)//2]
        motor_speed = 30
        self.car.changeMotorSpeed(motor_speed)

        # COLLSISION AVOIDANCE
        front_dist = self._getFrontDist()
        if(front_dist < 100):
            self.collisionAvoid = True
            self.obsDist = front_dist
        
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
                print("COLLISION AVOID")
                self.avoidCollision()
            elif(self.state == "auto"):
                print("auto")
                self.autoProgram()
            elif(self.state == "left" or self.state == "right"):
                print(self.state)
                self.turningProgram()
            elif(self.state =="slow"):
                self.slowProgram()
        else:
            self.safetyProgram()
