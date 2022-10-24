import pandas as pd
from datetime import datetime

def convertLog2Asc(fileName):
    logFile = pd.read_csv(fileName+".log",header=None)
    time = str(logFile.iloc[4])
    time = time[5:54]
    heasder = "base hex  no internal events logged \n  // version 7.1.0"

    logFile = pd.read_csv("2022_10_14_overVoltage.log",skiprows=15,index_col = False ,delimiter=" ",names=["Time","Tx/Rx","Channel","CAN_ID","Type","DLC","DataByte1","DataByte2","DataByte3","DataByte4","DataByte5","DataByte6","DataByte7","DataByte8"])
    LenRow = len(logFile.index) 
    dColumn = ["d"]*LenRow
    logFile["data"] = dColumn
    logFile.drop(logFile.tail(2).index,inplace=True)
    # print(logFile)
    logFile["CAN_ID"] =logFile["CAN_ID"].str.replace(r'0x', '')

    faultX = logFile.index[logFile["Type"] == "x"]
    for i in faultX:
        logFile["CAN_ID"][i] =logFile["CAN_ID"][i] + "x"

    timeData = pd.to_datetime(logFile["Time"],format= '%H:%M:%S:%f')
    logFile["Time"] = timeData.dt.hour*3600 + timeData.dt.minute*60 + timeData.dt.second + timeData.dt.microsecond*1e-6 
    logFile["Time"] = logFile["Time"].map('{:.6f}'.format)

    indexEmpty = logFile.index[logFile["DLC"] == "0"]
    for i in indexEmpty:
        logFile["DataByte1"][i] = "00"
        logFile["DataByte2"][i] = "00"
        logFile["DataByte3"][i] = "00"
        logFile["DataByte4"][i] = "00"
        logFile["DataByte5"][i] = "00"
        logFile["DataByte6"][i] = "00"
        logFile["DataByte7"][i] = "00"
        logFile["DataByte8"][i] = "00" 



    cols = ["Time","Channel","CAN_ID","Tx/Rx","data","DLC","DataByte1","DataByte2","DataByte3","DataByte4","DataByte5","DataByte6","DataByte7","DataByte8"] 
    # print(cols)
    ascFile = logFile[cols]
    ascFile.to_csv(fileName+'.asc',index=False,header=False,sep= " ")

    with open(fileName+'.asc', 'r+') as file:
        ascFile = file.read()

    date = time[23:33]
    time = time[34:42]
    time = datetime.strptime(time,'%H:%M:%S')
    date = datetime.strptime(date,'%d:%m:%Y')
    year = date.strftime("%Y")
    month = date.strftime("%b")
    dayName = date.strftime("%a")
    dayNumber = date.strftime("%d")
    amPm = time.strftime("%H:%M:%S %p")
    amPm = amPm.lower()
    ascFile = "date "+ dayName +" "+ month+ " "+ dayNumber+ " " + amPm +" "+ year + "\nbase hex  no internal events logged \n// version 7.1.0 \n" + ascFile + "End TriggerBlock\n\n"
    with open(fileName+'.asc', 'w') as file:
        file.write(ascFile)

import os


# input("failed")
# folder path
dir_path = "./"

# list to store files
res = []
# Iterate directory
for file in os.listdir(dir_path):
    # check only text files
    if file.endswith('.log'):
        res.append(file)
        # print(file[:-3])
        convertLog2Asc(file[:-4])


print("done ")
# input("failed")

