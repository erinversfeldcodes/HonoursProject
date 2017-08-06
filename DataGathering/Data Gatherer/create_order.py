import string, itertools, sys, random

for participant_num in range(0, 50):
	order = list(itertools.repeat(list(string.ascii_lowercase), 10))
	flattened_order = [y for x in order for y in x]
	random.shuffle(flattened_order)
	shuffled = ",".join(flattened_order)

	filename = str(participant_num)+"-0.txt"
	arr_0 = shuffled[0:20]
	with open(filename, "w+") as file:
		file.write(arr_0)
	filename = str(participant_num)+"-1.txt"
	arr_1 = shuffled[20:40]
	with open(filename, "w+") as file:
		file.write(arr_1)
	filename = str(participant_num)+"-2.txt"
	arr_2 = shuffled[40:60]
	with open(filename, "w+") as file:
		file.write(arr_2)
	filename = str(participant_num)+"-3.txt"
	arr_3 = shuffled[60:80]
	with open(filename, "w+") as file:
		file.write(arr_3)
	filename = str(participant_num)+"-4.txt"
	arr_4 = shuffled[80:100]
	with open(filename, "w+") as file:
		file.write(arr_4)
	filename = str(participant_num)+"-5.txt"
	arr_5 = shuffled[100:120]
	with open(filename, "w+") as file:
		file.write(arr_5)
	filename = str(participant_num)+"-6.txt"
	arr_6 = shuffled[120:140]
	with open(filename, "w+") as file:
		file.write(arr_6)
	filename = str(participant_num)+"-7.txt"
	arr_7 = shuffled[140:160]
	with open(filename, "w+") as file:
		file.write(arr_7)
	filename = str(participant_num)+"-8.txt"
	arr_8 = shuffled[160:180]
	with open(filename, "w+") as file:
		file.write(arr_8)
	filename = str(participant_num)+"-9.txt"
	arr_9 = shuffled[180:200]
	with open(filename, "w+") as file:
		file.write(arr_9)
	filename = str(participant_num)+"-10.txt"
	arr_10 = shuffled[200:220]
	with open(filename, "w+") as file:
		file.write(arr_10)
	filename = str(participant_num)+"-11.txt"
	arr_11 = shuffled[220:240]
	with open(filename, "w+") as file:
		file.write(arr_11)
	filename = str(participant_num)+"-12.txt"
	arr_12 = shuffled[240:260]
	with open(filename, "w+") as file:
		file.write(arr_12)
	filename = str(participant_num)+"-13.txt"
	arr_13 = shuffled[260:280]
	with open(filename, "w+") as file:
		file.write(arr_13)
	filename = str(participant_num)+"-14.txt"
	arr_14 = shuffled[280:300]
	with open(filename, "w+") as file:
		file.write(arr_14)
	filename = str(participant_num)+"-15.txt"
	arr_15 = shuffled[300:320]
	with open(filename, "w+") as file:
		file.write(arr_15)
	filename = str(participant_num)+"-16.txt"
	arr_16 = shuffled[320:340]
	with open(filename, "w+") as file:
		file.write(arr_16)
	filename = str(participant_num)+"-17.txt"
	arr_17 = shuffled[340:360]
	with open(filename, "w+") as file:
		file.write(arr_17)
	filename = str(participant_num)+"-18.txt"
	arr_18 = shuffled[360:380]
	with open(filename, "w+") as file:
		file.write(arr_18)
	filename = str(participant_num)+"-19.txt"
	arr_19 = shuffled[380:400]
	with open(filename, "w+") as file:
		file.write(arr_19)
	filename = str(participant_num)+"-20.txt"
	arr_20 = shuffled[400:420]
	with open(filename, "w+") as file:
		file.write(arr_20)
	filename = str(participant_num)+"-21.txt"
	arr_21 = shuffled[420:440]
	with open(filename, "w+") as file:
		file.write(arr_21)
	filename = str(participant_num)+"-22.txt"
	arr_22 = shuffled[440:460]
	with open(filename, "w+") as file:
		file.write(arr_22)
	filename = str(participant_num)+"-23.txt"
	arr_23 = shuffled[460:480]
	with open(filename, "w+") as file:
		file.write(arr_23)
	filename = str(participant_num)+"-24.txt"
	arr_24 = shuffled[480:500]
	with open(filename, "w+") as file:
		file.write(arr_24)
	filename = str(participant_num)+"-25.txt"
	arr_25 = shuffled[500:520]
	with open(filename, "w+") as file:
		file.write(arr_25)