from threading import Timer
from heartbeat.heatbeatdata import fillHeartbeatStruct


class RepeatingTimer(Timer):
	def run(self):
		while not self.finished.is_set():
			self.function(*self.args, **self.kwargs)
			self.finished.wait(self.interval)
	
t = RepeatingTimer(5.0, fillHeartbeatStruct)
t.start()