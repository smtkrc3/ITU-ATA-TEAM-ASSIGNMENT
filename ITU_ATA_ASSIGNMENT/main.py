from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
import pymavlink
import datetime
import dairetespit

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

    def getdistancemetres(self,aLocation1, aLocation2):
        dlat = aLocation2.lat - aLocation1.lat
        dlong = aLocation2.lon - aLocation1.lon
        return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
    
    
    def flightlogs(self):
        self.file=open('flightlogs.txt','a')
        now=datetime.datetime.now()
        self.file.write(f"Time: {now}\nAirspeed: {self.tb2.airspeed} m/s\nEuler Angles: {self.tb2.attitude}\n")
        self.file.write("Relative Altitude: %s\n" % self.tb2.location.global_relative_frame.alt)
        self.file.write(f"Longitute:{self.tb2.location.global_relative_frame.lon} Latitude:{self.tb2.location.global_relative_frame.lat}\n")
        self.file.close()


iha=UAV('tcp:127.0.0.1:5762')
iha.takeCommands()
iha.arm_and_takeoff()
kameraac=1
while 1:
    if iha.tb2.commands.next==1:
        print(f"Distance to Waypoint {iha.tb2.commands.next} :{iha.distance_to_current_waypoint()}")
        iha.flightlogs()
        time.sleep(0.3)
    if iha.tb2.commands.next==2:
        print(f"Distance to Waypoint {iha.tb2.commands.next} :{iha.distance_to_current_waypoint()}")
        time.sleep(0.3)
        if kameraac ==True:
            dairetespit.find_blue_circle()
            kameraac=0

    if iha.tb2.commands.next==3:
        print(f"Distance to Waypoint {iha.tb2.commands.next} :{iha.distance_to_current_waypoint()}")
        iha.flightlogs()
        time.sleep(0.3)
    if iha.tb2.commands.next==4:
        print(f"Distance to Waypoint {iha.tb2.commands.next} :{iha.distance_to_current_waypoint()}")
        iha.flightlogs()
        time.sleep(0.3)
    if iha.tb2.commands.next==5:
        print(f"Distance to Waypoint {iha.tb2.commands.next} :{iha.distance_to_current_waypoint()}")
        iha.flightlogs()
        time.sleep(0.3)


    
    
    


