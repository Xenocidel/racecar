# Static class for storing all constants
#PID constants

# TODO 
# Measure stopping distance for speed 12
PID_CONST = {12:{"KD":0.09,"SPEED_FACTOR":1, "STOPPING_DISTANCE":0.9},\
              20:{"KD":10,"SPEED_FACTOR":1.3, "STOPPING_DISTANCE":2.5},\
              23: { "KD":11, "SPEED_FACTOR":1.2, "STOPPING_DISTANCE":3.5 },\
              30: { "KD":12.5, "SPEED_FACTOR":1.5, "STOPPING_DISTANCE":5.4 }, \
              45: {"KD":15,"SPEED_FACTOR":1.5, "STOPPING_DISTANCE":8.5}}

        

PID_CONST_FAST = {12:{"KD":0.09,"SPEED_FACTOR":1, "STOPPING_DISTANCE":2.0},\
              20:{"KD":10,"SPEED_FACTOR":1.3, "STOPPING_DISTANCE":2.5},\
              23: { "KD":11, "SPEED_FACTOR":1.2, "STOPPING_DISTANCE":2.8 },\
              30: { "KD":12.5, "SPEED_FACTOR":1.5, "STOPPING_DISTANCE":8.0 }, \
              45: {"KD":15,"SPEED_FACTOR":1.5, "STOPPING_DISTANCE":10}}
