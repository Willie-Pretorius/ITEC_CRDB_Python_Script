from logginghandler import addLog,sendEmail
import ftplib
import os
import gzip
import shutil
import lxml
import xml.etree.ElementTree as et
from pymongo import MongoClient
dir_names=[]
import time

def see_info(string):
    global dir_names
    dir_names.append(string)
    print(string)

def Download_all_updates(ftp_host,host_port,ftp_user,ftp_pass,path):
    print("Downloading all updates")
    global dir_names
    dir_names = []
    data=[]
    ftp = ftplib.FTP_TLS()
    ftp.set_debuglevel(1)
    try:
        ftp.connect(host=ftp_host,port=host_port)
    except:
        print(f'cannot connect to {ftp_host} ')
        addLog(f'cannot connect to {ftp_host} \n')
    ftp.auth()
    try:
        ftp.login(user=ftp_user,passwd=ftp_pass)
        print(f"Successfully logged into FTP server {ftp_host}")
    except ftplib.error_perm:
        print(f"error login into FTP server {ftp_host} using {ftp_user}")
        addLog(f"error login into FTP server {ftp_host} using {ftp_user}\n")
    try:
        ftp.cwd(path)
        print ("Directory has been set")
    except:
        print(f"{path} not available")
        addLog(f"{path} not available\n")
    ftp.prot_p()
    ftp.retrlines('NLST',see_info)
    for file in dir_names:
        try:
            with open(file,'wb') as fp:
                ftp.retrbinary('RETR ' + file,fp.write)
            with gzip.open(file,'rb') as zipped_file:
                with open(file[slice(0,31)],'wb') as unzipped_file:
                    shutil.copyfileobj(zipped_file,unzipped_file)
            tree = et.parse(file[slice(0,31)])
            root = tree.getroot()
            ans = root.find("ActivatedNumbers")
            try:
                numbers= ans.findall("ActivatedNumber")
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
                        "id":id,
                        "number":msisdn,
                    }
                    data.append(object)
            except:
                print(f"{file} is empty.")
        except:
            print(f"{file} won't open")
    ftp.quit()
    for file in dir_names:
        try:
            os.remove(file)
            os.remove(file[slice(0,len(file)-3)])
        except:
            pass
    print("Download all data function complete.")
    addLog("Download all data function complete.\n")
    return data

def DataWriter(data):
    client = MongoClient('mongodb://localhost:27017/')
    mydb = client['numbers_db']
    mycol = mydb['numbers_col']
    print("dbNumbers successfully opened")
    for item in data:
        mycol.replace_one({"number":item['number']}, item)
    print("Data successfully uploaded to Database.")
    client.close()
    addLog(f"{len(data)} numbers successfully uploaded to Database\n")
    # time.sleep(60)

def DBTester():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        mydb = client['numbers_db']
        mycol = mydb['numbers_col']
        print("dbNumbers successfully opened")
        count = mycol.count_documents({})
        print(f"{count} number of entries found.")
        addLog("DB Connection successfully tested\n")
    except:
        addLog("DB Connection failed\n")


def DataPurge():
    client = MongoClient('mongodb://localhost:27017/')
    mydb = client['numbers_db']
    mycol = mydb['numbers_col']
    print("dbNumbers successfully opened")
    mycol.delete_many({})
    print("Database Successfully emptied.")
    addLog("Database Purged\n")

def ftp_tester(ftp_host,host_port,ftp_user,ftp_pass,path):
    global dir_names
    dir_names = []
    data=[]
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
    ftp.retrlines('NLST',see_info)
    ftp.quit()
    print(dir_names)

def Download_latest_update(ftp_host,host_port,ftp_user,ftp_pass,path):
    # print("downloading last update")
    global dir_names
    dir_names = []
    data=[]
    ftp = ftplib.FTP_TLS()
    ftp.set_debuglevel(1)
    try:
        ftp.connect(host=ftp_host,port=host_port)
    except:
        print(f'cannot connect to {ftp_host} ')
        addLog(f'Cannot connect to {ftp_host} \n')
    ftp.auth()
    try:
        ftp.login(user=ftp_user,passwd=ftp_pass)
        print(f"Successfully logged into FTP server {ftp_host}")
    except ftplib.error_perm:
        print(f"error login into FTP server {ftp_host} using {ftp_user}")
        addLog(f"error login into FTP server {ftp_host} using {ftp_user}\n")
    try:
        ftp.cwd(path)
        print ("Directory has been set")
    except:
        print(f"{path} not available")
        addLog(f"{path} not available\n")
    ftp.prot_p()
    ftp.retrlines('NLST',see_info)
    file = dir_names[len(dir_names)-1]
    try:
        with open(file,'wb') as fp:
            ftp.retrbinary('RETR ' + file,fp.write)
        with gzip.open(file,'rb') as zipped_file:
            with open(file[slice(0,31)],'wb') as unzipped_file:
                shutil.copyfileobj(zipped_file,unzipped_file)
        tree = et.parse(file[slice(0,31)])
        root = tree.getroot()
        ans = root.find("ActivatedNumbers")
        try:
            numbers= ans.findall("ActivatedNumber")
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
                    "id":id,
                    "number":msisdn,
                }
                data.append(object)
            print(f"{file} added to array.")
            addLog(f"{file} added to array\n")
            sendEmail("CRDB Daily Update",f"{file} from {ftp_user} has been processed and uploaded.\n")
        except:
            print(f"{file} from {ftp_user} is empty.")
            addLog(f"{file} from {ftp_user} is empty.\n")
            sendEmail("CRDB Daily Update", f"{file} from {ftp_user} had no new data\n")

    except:
        print(f"{file} won't open")
        addLog(f"{file} won't open\n")
    ftp.quit()
    try:
        os.remove(file)
        os.remove(file[slice(0,len(file)-3)])
    except:
        pass
    print("Routine download complete.")
    addLog("Routine download complete.\n")
    return data

#This code was written by Willie Pretorius
#Fork me at https://github.com/Willie-Pretorius
