import vxi11
import os.path
from sys import version_info

ip = "10.0.4.53"
osc = vxi11.Instrument(ip)
#Since the library doesnt support infinite timeout(-1), put a realy high value (604800 = 1 week in seconds)
osc.timeout = 604800*1000
#Name of the output Files
sensors = ["CH1", "CH2", "CH3", "CH4"]
#Select which measures to get
measures = ["AREA", "TOP"]

measures_header = ""
for i in range(len(measures)):
	measures_header += measures[i]
	measures_header += '\t'
measures_header += 'DATE\n'

files = [None] * len(sensors)

#Check if data file already exists, if true, open it in append mode, if false, create a new one
for i in range(len(sensors)):
	if (os.path.exists(sensors[i]+'.txt')):
		if (version_info[0] > 2):
			response = input("Do you wish to overwrite the existing data files? (Y or N)")
		else:
			response = raw_input("Do you wish to overwrite the existing data files? (Y or N)")
		if (response = "N"):
			files[i] = open(sensors[i]+'.txt',"a")
		elif (response = "Y"):
	else:	
		files[i] = open(sensors[i]+'.txt',"w")
		files[i].write(measures_header)

#Oscilloscope configuration
#Trigger 
#Mode
osc.write("TRMD STOP")
#Type/Source
tr_source = "C2"
osc.write("TRSE EDGE, SR, "+tr_source)
#Level
osc.write(tr_source+":TRLV 100E-3 V")
	
#Start data acquisition
while(1):
	param_value = [None] * len(measures)
	for i in range(len(sensors)):
		for index in range(len(measures)):
			osc.write("ARM")
			osc.write("WAIT")
			query = "C"+str(i+1)+":PAVA? "+measures[index]
			resp = osc.ask(query)
			param_value[index] = resp.split(",")[1]
		date = osc.ask("DATE?")
		format_date = date.split(" ")[1]
		meas_write = ""
		for k in range(len(param_value)):
			meas_write += param_value[k]
			meas_write += '\t'
		meas_write += format_date
		meas_write += '\n'
		files[i].write(meas_write)
	
for i in range(len(sensors)):
	files[i].close()
