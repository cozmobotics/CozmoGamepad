#!/usr/bin/env python3

help = "                                                                      \n\
 CozmoGamepad                                                                 \n\
 *************                                                                \n\
                                                                              \n\
Steer Cozmo with a gamepad                                                    \n\
(any gamepad should do, tested only with a speedlink strike NX)               \n\
Sticks move robot forward/back, left/right and turn head up/down              \n\
Also try buttons and hat keys                                                 \n\
Feel free to modify this script as you like                                   \n\
                                                                              \n\
End program with Ctrl-C                                                       \n\
"

import cozmo
from cozmo.util import degrees
import inputs




	
# -------------------------------------------------------
	



def robotProgram(robot: cozmo.robot.Robot):
	global OldSpeed
	
	pads = inputs.devices.gamepads
	print ("\n\n *************")
	print ("\nFound " + str(len(pads)) + " gamepad(s)")
	if len(pads) == 0:
		raise Exception("Couldn't find any Gamepads!")
	
	print ("found gamepad" + str(pads[0]))
	print (help)
	
	Lift = 0
	Rc = [0,0,0,0]

	while (True):
	
		AnimIndex = -1
		events = inputs.get_gamepad()

		for event in events:
			# print(event.ev_type, event.code, event.state)
			if (event.ev_type == "Absolute"): 
				# print (event.code)
				stickVal = int(int (event.state) / 327) # / 32767 * 100
				if (event.code == "ABS_X"):
					Rc[3] = stickVal
				elif (event.code == "ABS_Y"):
					Rc[2] = stickVal
					robot.set_head_angle(degrees(-Rc[2]), in_parallel=True)
				elif (event.code == "ABS_RX"):
					Rc[0] = stickVal
				elif (event.code == "ABS_RY"):
					Rc[1] = 2 * stickVal
					
				elif (event.code == "ABS_HAT0Y"): 
					# print ("lift ")
					if (int (event.state) > 0):
						Lift = Lift + .1;
						if (Lift > 1):
							Lift = 1
						# print (Lift)
					if (int (event.state) < 0):
						Lift = Lift - .1;
						if (Lift < 0):
							Lift = 0
						# print (Lift)
					robot.set_lift_height(Lift, in_parallel=True)
					
			elif (event.ev_type == "Key"): 
				if (event.code == "BTN_NORTH"):
					if (str(event.state) == "1"):
						AnimIndex = 23
				elif (event.code == "BTN_SOUTH"):
					if (str(event.state) == "1"):
						AnimIndex = 31
				elif (event.code == "BTN_WEST"):
					if (str(event.state) == "1"):
						AnimIndex = 35
				elif (event.code == "BTN_EAST"):
					if (str(event.state) == "1"):
						AnimIndex = 36
				elif (event.code == "BTN_TL"):
					if (str(event.state) == "1"):
						robot.set_all_backpack_lights(cozmo.lights.red_light)
					else:
						 robot.set_all_backpack_lights(cozmo.lights.off_light) 
				elif (event.code == "BTN_TR"):
					if (str(event.state) == "1"):
						robot.set_all_backpack_lights(cozmo.lights.green_light)
					else:
						 robot.set_all_backpack_lights(cozmo.lights.off_light) 
		
		robot.drive_wheels(Rc[1] + Rc[0] + Rc[3], Rc[1] - Rc[0] - Rc[3])
		
		if (AnimIndex != -1):
			Anim = robot.anim_triggers[AnimIndex]
			print ("animation " + Anim.name)
			robot.play_anim_trigger(Anim)

			#time.sleep (Heartbeat / 1000)



cozmo.run_program(robotProgram)


