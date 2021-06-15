from scheduler.repeating_timer import RepeatingTimer
from heartbeat.heatbeatdata import fillHeartbeatStruct
	
t = RepeatingTimer(5.0, fillHeartbeatStruct)
t.start()