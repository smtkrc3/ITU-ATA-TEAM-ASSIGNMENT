from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
import pymavlink
import datetime
import dairetespit
#   https://dronekit-python.readthedocs.io/en/latest/automodule.html#dronekit.connect
#   https://dronekit-python.readthedocs.io/en/latest/examples/vehicle_state.html
#   https://dronekit-python.readthedocs.io/en/latest/examples/simple_goto.html
#   https://dronekit-python.readthedocs.io/en/latest/examples/guided-set-speed-yaw-demo.html
#   https://dronekit-python.readthedocs.io/en/latest/examples/mission_basic.html
class UAV():
    def __init__(self,connection_address):
        self.tb2=connect(connection_address,wait_ready=True)
        if self.tb2:
            print("Connection is successful")
        
    def arm_and_takeoff(self):   # checking engine and being armed
        print("Basic pre-arm checks...")
        while not self.tb2.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)
        self.tb2.arm(wait=True)     # give power to the engine
        self.tb2.mode    = VehicleMode("AUTO")      # put the plane into auto mode
        print ("Taking off!")
        
    def takeCommands(self):     # take commands from mission planner
        cmds=self.tb2.commands
        cmds.download()
        cmds.wait_ready()
        if cmds:
            print("Commands were taken...")
            
    def distance_to_current_waypoint(self):
        nextwaypoint=self.tb2.commands.next
        if nextwaypoint ==0:
            return None
        missionitem=self.tb2.commands[nextwaypoint-1] #commands are zero indexed
        lat=missionitem.x
        lon=missionitem.y
        alt=missionitem.z
        targetWaypointLocation=LocationGlobalRelative(lat,lon,alt)
        distancetopoint = iha.getdistancemetres(self.tb2.location.global_frame, targetWaypointLocation)
        return distancetopoint

    def getdistancemetres(self,aLocation1, aLocation2): # find the distance by using gps data
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
    
    
    def flightlogs(self):  # writing the flight information to a txt file
        self.file=open('flightlogs.txt','a')
        now=datetime.datetime.now() # get time for set apart datas 
        self.file.write(f"Time: {now}\nAirspeed: {self.tb2.airspeed} m/s\nEuler Angles: {self.tb2.attitude}\n")
        self.file.write("Relative Altitude: %s\n" % self.tb2.location.global_relative_frame.alt)
        self.file.write(f"Longitute:{self.tb2.location.global_relative_frame.lon} Latitude:{self.tb2.location.global_relative_frame.lat}\n")
        self.file.close()
    

# Executed Area 
iha=UAV('tcp:127.0.0.1:5762') # starting iha object by sending tcp address
iha.takeCommands()  # download commands from mission planner 
iha.arm_and_takeoff() # go for fly 
kameraac=1  # controlling of camera to execute just once
while 1:
    print(" Battery: %s" % iha.tb2.battery)
    if iha.tb2.commands.next is not None:
        print(f"Distance to Waypoint {iha.tb2.commands.next} :{iha.distance_to_current_waypoint()}")
    iha.flightlogs()
    if iha.tb2.commands.next==2:
        print(f"Distance to Waypoint {iha.tb2.commands.next} :{iha.distance_to_current_waypoint()}")
        if kameraac ==True:  # 10 seconds camera opening
            dairetespit.find_blue_circle()
            kameraac=0
        iha.flightlogs()  # after just once camera execution, log info again if the plane still go for waypoint 2
    time.sleep(0.3)
    if iha.tb2.commands.next==6 and iha.distance_to_current_waypoint()<15: # due to square shaped route, approximately less 15 metres to 6th waypoint, return to launch position
        print("Returning to Launch")        #https://dronekit-python.readthedocs.io/en/latest/examples/simple_goto.html
        iha.tb2.mode = VehicleMode("RTL")
        break


    
    
    


