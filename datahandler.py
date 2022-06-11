from logginghandler import addLog,sendEmail
import ftplib
import os
import gzip
import shutil
import xml.etree.ElementTree as et
from tqdm import tqdm
from pymongo import MongoClient
dir_names=[]
data = []


def ftp_tester(ftp_host,host_port,ftp_user,ftp_pass,path):
    global dir_names
    ftp = ftplib.FTP_TLS()
    ftp.set_debuglevel(1)
    try:
        ftp.connect(host=ftp_host, port=host_port)
    except:
        print(f'cannot connect to {ftp_host} ')
        addLog(f"FTP Test failed, cannot connect to {ftp_host}\n")
    ftp.auth()
    try:
        ftp.login(user=ftp_user, passwd=ftp_pass)
        print(f"Successfully logged into FTP server {ftp_host}")
    except ftplib.error_perm:
        print(f"error login into FTP server {ftp_host} using {ftp_user}")
        addLog(f"error login into FTP server {ftp_host} using {ftp_user}\n")
    try:
        ftp.cwd(path)
        print("Directory has been set")

    except:
        print(f"{path} not available")
        addLog(f"{path} not available\n")
    ftp.prot_p()
    ftp.retrlines('NLST',appendFileName)
    ftp.quit()
    print(dir_names)

def Download_latest_update(ftp_host,host_port,ftp_user,ftp_pass,path):
    # print("downloading last update")
    global dir_names,data
    getFiles(ftp_host,host_port,ftp_user,ftp_pass,path,"",[])
    download_list = [dir_names[len(dir_names)-1]]
    getFiles(ftp_host, host_port, ftp_user, ftp_pass, path, "download", download_list)
    for file in download_list:
        translator(file, ftp_user)
    try:
        os.remove(file)
    except:
        print(f"Couldn't delete {file}")
        addLog(f"Couldn't delete {file}")
    try:
        os.remove(file[slice(0, len(file) - 3)])
    except:
        try:
            os.remove(file[slice(0, len(file) - 2)])
        except:
            print(f"Couldn't delete {file[slice(0, len(file) - 3)]}")
            addLog(f"Couldn't delete {file[slice(0, len(file) - 3)]}\n")
    print(f"Routine download complete, {len(data)} processed")
    addLog(f"Routine download complete, {len(data)} processed\n")
    DataWriter(data,ftp_user)

def Download_all_updates(ftp_host,host_port,ftp_user,ftp_pass,path):
    print("Downloading all updates")
    global dir_names, data
    data = []
    getFiles(ftp_host, host_port, ftp_user, ftp_pass, path,"",[])
    getFiles(ftp_host, host_port, ftp_user, ftp_pass, path,"download",dir_names)
    for file in dir_names:
        translator(file,ftp_user)
    for file in dir_names:
        try:
            os.remove(file)
        except:
            print(f"Couldn't delete {file}")
            addLog(f"Couldn't delete {file}")
        try:
            os.remove(file[slice(0, len(file) - 3)])
        except:
            try:
                os.remove(file[slice(0, len(file) - 2)])
            except:
                print(f"Couldn't delete {file[slice(0, len(file) - 3)]}")
                addLog(f"Couldn't delete {file[slice(0, len(file) - 3)]}\n")

    if data == []:
        print("Failed: Download all data function.")
    else:
        print(f"Download all data function complete, {len(data)} processed.")
        addLog(f"Download all data function complete, {len(data)} processed\n")
    DataWriter(data,ftp_user)

def OneTimeFTP(ftp_host,host_port,ftp_user,ftp_pass,path):
    print("Downloading all updates")
    global dir_names, data
    getFiles(ftp_host, host_port, ftp_user, ftp_pass, path, "", [])
    download_list = [dir_names[len(dir_names) - 1]]
    getFiles(ftp_host, host_port, ftp_user, ftp_pass, path, "download", download_list)
    for file in download_list:
        translator(file, ftp_user)
    try:
        os.remove(file)
    except:
        print(f"Couldn't delete {file}")
        addLog(f"Couldn't delete {file}")
    try:
        os.remove(file[slice(0, len(file) - 3)])
    except:
        try:
            os.remove(file[slice(0, len(file) - 2)])
        except:
            print(f"Couldn't delete {file[slice(0, len(file) - 3)]}")
            addLog(f"Couldn't delete {file[slice(0, len(file) - 3)]}\n")
    print(f"Routine download complete, {len(data)} processed")
    addLog(f"Routine download complete, {len(data)} processed\n")
    DataPopulator(data,ftp_user)


def appendFileName(string):
    global dir_names
    dir_names.append(string)
    print(string)

def getFiles(ftp_host,host_port,ftp_user,ftp_pass,path,task,download_list):
    global dir_names
    ftp = ftplib.FTP_TLS()
    ftp.set_debuglevel(1)
    try:
        ftp.connect(host=ftp_host, port=host_port)
    except:
        print(f'cannot connect to {ftp_host} check port or server address')
        addLog(f'Cannot connect to {ftp_host} check port or server address\n')
    ftp.auth()
    try:
        ftp.login(user=ftp_user, passwd=ftp_pass)
        print(f"Successfully logged into FTP server {ftp_host}")
    except ftplib.error_perm:
        print(f"error login into FTP server {ftp_host} using {ftp_user}")
        addLog(f"error login into FTP server {ftp_host} using {ftp_user}\n")
    try:
        ftp.cwd(path)
        print("Directory has been set")
    except:
        print(f"{path} not available")
        addLog(f"{path} not available\n")
    ftp.prot_p()
    dir_names = []
    ftp.retrlines('NLST', appendFileName)
    if task == "download":
        for i in tqdm(range(len(download_list))):
            file = download_list[i]
            try:
                with open(file, 'wb') as fp:
                    ftp.retrbinary('RETR ' + file, fp.write)
                with gzip.open(file, 'rb') as zipped_file:
                    with open(file[slice(0, 31)], 'wb') as unzipped_file:
                        shutil.copyfileobj(zipped_file, unzipped_file)
            except:
                print(f" Can't open {file}")
    ftp.quit()


def translator(file,ftp_user):
    global data
    data =[]
    tree = et.parse(file[slice(0, 31)])
    root = tree.getroot()
    ans = root.find("ActivatedNumbers")
    try:
        numbers = ans.findall("ActivatedNumber")
        for number in numbers:
            id = number.find("IDNumber").text
            try:
                msisdnElement = number.find("MSISDN")
                msisdn = msisdnElement.text
            except:
                dnr = number.find("DNRanges")
                msisdnElement = dnr.find("DNFrom")
                msisdn = msisdnElement.text
            object = {
                "id": id,
                "number": msisdn,
            }
            data.append(object)
        print(f"{file} added to array.")
        addLog(f"{file} added to array\n")
    except:
        print(f"{file} from {ftp_user} is empty.")
        addLog(f"{file} from {ftp_user} is empty.\n")



#Pymongo functions.

def DataWriter(data,ftp_user):
    client = MongoClient('mongodb://127.0.0.1:27017/numbers_db')
    mydb = client['numbers_db']
    mycol = mydb['numbers_col']
    print("dbNumbers successfully opened")
    for i in tqdm(range(len(data))):
        item = data[i]
        number = item["number"]
        test=mycol.find_one({"number": number})
        if test == None:
            mycol.insert_one({"number": number},item)
        elif item == test:
            pass
        else:
            mycol.replace_one({"number": number},item)
    print("Data successfully uploaded to Database.")
    client.close()
    addLog(f"{len(data)} numbers successfully uploaded to Database\n")
    sendEmail("CRDB Daily Update", f"{len(data)} from {ftp_user} has been processed and uploaded.\n")

def DataPopulator(data,ftp_user):
    client = MongoClient('mongodb://127.0.0.1:27017/numbers_db')
    mydb = client['numbers_db']
    mycol = mydb['numbers_col']
    print("dbNumbers successfully opened")
    for i in tqdm(range(len(data))):
        item = data[i]
        number = item["number"]
        mycol.insert_one({"number": number},item)
    print("Data successfully uploaded to Database.")
    client.close()
    addLog(f"{len(data)} numbers successfully uploaded to Database\n")
    sendEmail("CRDB Daily Update", f"{len(data)} from {ftp_user} has been processed and uploaded.\n")

def DBTester():
    try:
        client = MongoClient('mongodb://127.0.0.1:27017/numbers_db')
        mydb = client['numbers_db']
        mycol = mydb['numbers_col']
        print("dbNumbers successfully opened")
        count = mycol.count_documents({})
        print(f"{count} number of entries found.")
        addLog("DB Connection successfully tested\n")
    except:
        addLog("DB Connection failed\n")


def DataPurge():
    client = MongoClient('mongodb://localhost:27017/numbers_db')
    mydb = client['numbers_db']
    mycol = mydb['numbers_col']
    print("dbNumbers successfully opened")
    mycol.delete_many({})
    print("Database Successfully emptied.")
    addLog("Database Purged\n")


#This code was written by Willie Pretorius
#Fork me at https://github.com/Willie-Pretorius
