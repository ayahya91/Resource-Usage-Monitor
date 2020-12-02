#!/usr/bin/env python

'''
	Resource Usage Monitor GUI
	Written By Ahmed Yahya
'''
import time, sys, subprocess
from Tkinter import *

CPU_THRESHOLD = 50.0
MEM_THRESHOLD = 75.0
DISK_USAGE_THRESHOLD = 75
DROPPED_PACKAGE_THRESHOLD = 16

def cpu_usage():
	threshold_reached = 0
	bash_command = "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
	process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, shell=True)
	total_cpu_usage = process.communicate()[0]
	total_cpu_usage = float(total_cpu_usage[:-1])
	if total_cpu_usage >= CPU_THRESHOLD:
		threshold_reached = 1
	output = ["Total CPU Usage: %6.2f%%" % total_cpu_usage, threshold_reached]
	return output

def mem_usage():
	threshold_reached = 0
	memCommand_Avail = "grep 'MemAvailable:' /proc/meminfo | awk '{available=$2} END {print available}'"
	memCommand_Free = "grep 'MemFree:' /proc/meminfo | awk '{free=$2} END {print free}'"
	process_mem_avail = subprocess.Popen(memCommand_Avail, stdout=subprocess.PIPE, shell=True)
	process_mem_free = subprocess.Popen(memCommand_Free, stdout=subprocess.PIPE, shell=True)
	output_mem_avail = process_mem_avail.communicate()[0]
	output_mem_free = process_mem_free.communicate()[0]
	total_mem_usage = (float(output_mem_free[:-1])/float(output_mem_avail[:-1]))*100
	if total_mem_usage >= MEM_THRESHOLD:
		threshold_reached = 1
	output =  ["Total MEM Usage: %6.2f%%" % total_mem_usage, threshold_reached]
	return output

def disk_usage():
	threshold_reached = 0
	disk_usage_command = "df -Tha --total | grep 'total' | awk '{disk_usage=$6} END {print disk_usage}'"
	process_disk_usage = subprocess.Popen(disk_usage_command, stdout=subprocess.PIPE, shell=True)
	output = process_disk_usage.communicate()[0]
	disk_usage = int(output.replace("%", ""))
	if disk_usage >= DISK_USAGE_THRESHOLD:
		threshold_reached = 1
	output = ["Total Disk Usage: %d%%" % disk_usage, threshold_reached]
	return output

def network_usage():
	Incoming_Packets_Threshold = 0
	Outgoing_Packets_Threshold = 0
	networkCommand_total_received = "netstat -s | grep 'total packets received' | awk '{total_received=$1} END {print total_received}'"
	networkCommand_requests_sent = "netstat -s | grep 'requests sent out' | awk '{requests_sent=$1} END {print requests_sent}'"
	networkCommand_incoming_delivered = "netstat -s | grep 'incoming packets delivered' | awk '{incoming_delivered=$1} END {print incoming_delivered}'"
	networkCommand_packets_dropped_1 = "netstat -s | grep 'outgoing packets dropped' | awk '{packets_dropped_1=$1} END {print packets_dropped_1}'"
	networkCommand_packets_dropped_2 = "netstat -s | grep 'incoming packets discarded' | awk '{packets_dropped_2=$1} END {print packets_dropped_2}'"

	process_network_total_received = subprocess.Popen(networkCommand_total_received, stdout=subprocess.PIPE, shell=True)
	process_network_requests_sent = subprocess.Popen(networkCommand_requests_sent, stdout=subprocess.PIPE, shell=True)
	process_network_incoming_delivered = subprocess.Popen(networkCommand_incoming_delivered, stdout=subprocess.PIPE, shell=True)
	process_network_packets_dropped_1 = subprocess.Popen(networkCommand_packets_dropped_1, stdout=subprocess.PIPE, shell=True)
	process_network_packets_dropped_2 = subprocess.Popen(networkCommand_packets_dropped_2, stdout=subprocess.PIPE, shell=True)

	total_received = process_network_total_received.communicate()[0]
	requests_sent = process_network_requests_sent.communicate()[0]
	incoming_delivered = process_network_incoming_delivered.communicate()[0]
	packets_dropped_1 = process_network_packets_dropped_1.communicate()[0]
	packets_dropped_2 = process_network_packets_dropped_2.communicate()[0]
	if int(packets_dropped_1) >= DROPPED_PACKAGE_THRESHOLD:
		Outgoing_Packets_Threshold = 1
	if int(packets_dropped_2) >= DROPPED_PACKAGE_THRESHOLD:
		Incoming_Packets_Threshold = 1
	output = ["Total Packets Received: %d" % int(total_received), "Total Packets Sent: %d" % int(requests_sent), "Total Packets Delivered: %d" % int(incoming_delivered), "Total Out-Packets Dropped: %d" % int(packets_dropped_1), "Total In-Packets Dropped: %d" % int(packets_dropped_2), Outgoing_Packets_Threshold, Incoming_Packets_Threshold]
	return output

def guage_meter(usage_value):
	usage_value = int(usage_value)
	if usage_value < 20:
		guage = 0
	elif usage_value >= 20 and usage_value < 40:
		guage = 1
	elif usage_value >= 40 and usage_value < 60:
		guage = 2
	elif usage_value >= 60 and usage_value < 80:
		guage = 3
	elif usage_value >= 80 and usage_value < 100:
		guage = 4
	elif usage_value >= 100:
		guage = 5
	return " [" + "|"*guage + "."*(5-guage) + "]"


root = Tk()
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(400, 75))
root.wm_title("Resource Usage Monitor v3")
img = PhotoImage(file='/Users/ahmed_yahya/Desktop/Lenovo Desktop Image/System Monitor/resource_monitor_icon.png')
root.tk.call('wm', 'iconphoto', root._w, img)

frame = Frame(root)

cpu_usage_str = StringVar()
cpu_usage_label = Label(frame, textvariable=cpu_usage_str, relief=RAISED, bg='lavender', anchor=W)

mem_usage_str = StringVar()
mem_usage_label = Label(frame, textvariable=mem_usage_str, relief=RAISED, bg='lavender', anchor=W)

disk_usage_str = StringVar()
disk_usage_label = Label(frame, textvariable=disk_usage_str, relief=RAISED, bg='lavender', anchor=W)

network_packet_str1 = StringVar()
network_packet_label1 = Label(frame, textvariable=network_packet_str1, relief=RAISED, bg='lavender', anchor=W)

network_packet_str2 = StringVar()
network_packet_label2 = Label(frame, textvariable=network_packet_str2, relief=RAISED, bg='lavender', anchor=W)

network_packet_str3 = StringVar()
network_packet_label3 = Label(frame, textvariable=network_packet_str3, relief=RAISED, bg='lavender', anchor=W)

network_packet_str4 = StringVar()
network_packet_label4 = Label(frame, textvariable=network_packet_str4, relief=RAISED, bg='lavender', anchor=W)

network_packet_str5 = StringVar()
network_packet_label5 = Label(frame, textvariable=network_packet_str5, relief=RAISED, bg='lavender', anchor=W)

network_stats = network_usage()

cpu_usage_str.set(cpu_usage()[0])
mem_usage_str.set(mem_usage()[0])
disk_usage_str.set(disk_usage()[0])

network_packet_str1.set(network_stats[0])
network_packet_str2.set(network_stats[1])
network_packet_str3.set(network_stats[2])
network_packet_str4.set(network_stats[3])
network_packet_str5.set(network_stats[4])

cpu_usage_label.grid(row=0,column=0, sticky=N+S+E+W)
mem_usage_label.grid(row=1,column=0, sticky=N+S+E+W)
network_packet_label4.grid(row=3,column=1, sticky=N+S+E+W)
network_packet_label1.grid(row=2,column=1, sticky=N+S+E+W)
network_packet_label2.grid(row=0,column=1, sticky=N+S+E+W)
network_packet_label3.grid(row=1,column=1, sticky=N+S+E+W)
network_packet_label5.grid(row=3,column=0, sticky=N+S+E+W)
disk_usage_label.grid(row=2,column=0, sticky=N+S+E+W)

frame.pack()

def update():
	cpu_stats = cpu_usage()
	cpu_usage_str.set(cpu_stats[0])
	if cpu_stats[1] == 1:
		cpu_usage_label.config(bg='red')
	else:
		cpu_usage_label.config(bg='lavender')
	mem_stats = mem_usage()
	mem_usage_str.set(mem_stats[0])
	if mem_stats[1] == 1:
		mem_usage_label.config(bg='red')
	else:
		mem_usage_label.config(bg='lavender')

	disk_stats = disk_usage()
	disk_usage_str.set(disk_stats[0])
	if disk_stats[1] == 1:
		disk_usage_label.config(bg='red')
	else:
		disk_usage_label.config(bg='lavender')
	network_stats = network_usage()
	network_packet_str1.set(network_stats[0])
	network_packet_str2.set(network_stats[1])
	network_packet_str3.set(network_stats[2])
	network_packet_str4.set(network_stats[3])
	if network_stats[5] == 1:
		network_packet_label4.config(bg='red')
	else:
		network_packet_label4.config(bg='lavender')
	network_packet_str5.set(network_stats[4])
	if network_stats[6] == 1:
		network_packet_label5.config(bg='red')
	else:
		network_packet_label5.config(bg='lavender')
	root.after(3000, update)

update()
root.mainloop()





