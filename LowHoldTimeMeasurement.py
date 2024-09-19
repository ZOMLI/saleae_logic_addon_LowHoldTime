from saleae.range_measurements import DigitalMeasurer
from saleae.data import SaleaeTimeDelta

LOW_HOLD_SUM = "lowholdsum"
LOW_HOLD_MEAN = "lowholdmean"
LOW_HOLD_MAX = "lowholdmax"
LOW_HOLD_MIN = "lowholdmin"

class LowHoldTimeMeasurement(DigitalMeasurer):
	# Add supported_measurements here. This includes the metric
	supported_measurements = [LOW_HOLD_SUM, LOW_HOLD_MEAN, LOW_HOLD_MAX, LOW_HOLD_MIN]
	# strings that were defined in the extension.json file.

	def __init__(self, requested_measurements):
		super().__init__(requested_measurements)
		# Initialize your variables here
		self.time_max = None
		self.time_min = None
		self.last_time = None
		self.state = None
		self.is_begin = True
		self.Begin_time = None
		self.Final_time = None
		self.time_sum = None
		self.time_num = 0

	def process_data(self, data):
		for t, bitstate in data:
			# Process data here
			# First Time
			if self.is_begin is True:
				self.is_begin = False
				if bitstate is False:
					self.state = True
					self.last_time = t
				else:
					self.state = False
					# time_sum += t - self.Begin_time
			# Other Time
			else:
				if bitstate is False:
					self.last_time = t
				else:
					del_time = t - self.last_time
					if self.time_max is None:
						self.time_max = del_time
						self.time_min = del_time
						self.time_sum = del_time
						self.time_num = 1
					else:
						self.time_sum += del_time
						self.time_num += 1
						if self.time_max < del_time:
							self.time_max = del_time
						if self.time_min > del_time:
							self.time_min = del_time

	def measure(self):
		values = {}
		if self.time_sum is None:
			values[LOW_HOLD_SUM] = 0.0
			values[LOW_HOLD_MEAN] = 0.0
		else:
			values[LOW_HOLD_SUM] = self.time_sum
			if self.time_num == 0:
				values[LOW_HOLD_MEAN] = 0.0
			else:	
				values[LOW_HOLD_MEAN] = float(self.time_sum)/self.time_num
		if self.time_max is None:
			values[LOW_HOLD_MAX] = 0.0
		else:
			values[LOW_HOLD_MAX] = self.time_max
		if self.time_min is None:
			values[LOW_HOLD_MIN] = 0.0
		else:
			values[LOW_HOLD_MIN] = self.time_min
		# Assign the final metric results here to the values object
		return values

	