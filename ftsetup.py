from datahandler import *

ftp_host = ""
host_port = ""
ftp_user = ""
ftp_pass = ""
path = ""
ftp_host2 = ""
host_port2 = ""
ftp_user2 = ""
ftp_pass2 = ""
path2 = ""
config = ""

#initial setup wizard
def setupWizard():
    print("Welcome to the setup wizard.\n Please take a minute to configure your porting.co.za ftp settings")
    ftp_host = input("FTP Server address: ")
    ftp_port = int(input("FTP port: "))
    ftp_user = input("FTP Username: ")
    ftp_pass = input("FTP Password: ")
    path = input("path('/DWNLDS'):")
    ftp1 = f"host:{ftp_host}\nport:{ftp_port}\nuser:{ftp_user}\npass:{ftp_pass}\npath:{path}"
    input("Ready to configure ftp server 2? press return to continue.")
    ftp_host = input("FTP Server address: ")
    ftp_port = int(input("FTP port: "))
    ftp_user = input("FTP Username: ")
    ftp_pass = input("FTP Password: ")
    path = input("path('/DWNLDS'):")
    ftp1+=f"\nhost:{ftp_host}\nport:{ftp_port}\nuser:{ftp_user}\npass:{ftp_pass}\npath:{path}\nconfig_mode:1"
    with open(".config", "w") as file:
        file.write(ftp1)
        file.close()
    with open(".log","w") as file:
        file.write("")
        file.close()

def OneTimeFTP_EXEC():
    print("Configure One Time FTP server\n Please take a minute to configure your porting.co.za ftp settings")
    otftp_host = input("FTP Server address: ")
    otftp_port = int(input("FTP port: "))
    otftp_user = input("FTP Username: ")
    otftp_pass = input("FTP Password: ")
    otpath = input("path('/DWNLDS'):")
    data = OneTimeFTP(otftp_host,otftp_port,otftp_user,otftp_pass,otpath)
    DataPopulator(data)

#writes config to be 0 so the script can run in routine mode.
def disableConfig():
    global ftp_host, host_port, ftp_user, ftp_pass, path, ftp_host2, host_port2, ftp_user2, ftp_pass2, path2, config
    ftp1 = f"host:{ftp_host}\nport:{host_port}\nuser:{ftp_user}\npass:{ftp_pass}\npath:{path}\nftp_num:2\nconfig_mode:0"
    ftp1 += f"\nhost:{ftp_host2}\nport:{host_port2}\nuser:{ftp_user2}\npass:{ftp_pass2}\npath:{path2}"
    with open(".config", "w") as file:
        file.write(ftp1)
        file.close()
    print("Config has been reset to 0 routing starts will resume.")

#allows user to configure smtp details and save to file.
def configSmtp():
    print("Please enter your SMTP details below.")
    smtp_server = input("SMTP server: ")
    from_address = input("From address: ")
    username = input("Username: ")
    password = input("Password: ")
    to_address = input("To address:")
    smtpstring = f"smtp_server:{smtp_server} \nfrom_address:{from_address} \nusername:{ username} \npassword:{password} \nto_address:{to_address}"
    with open(".smtpconfig", "a") as file:
        file.write(smtpstring)
        file.close()

#reads config file and writes to an array of options to return. To be used with config loader.
def Loader(file):
    options=[]
    doc= file.read()
    lines= doc.split("\n")
    for option in lines:
        setting= option.split(":")[1]
        options.append(setting)
    return options

#Writes current config from config file to global variables.
def configLoader():
    global ftp_host, host_port, ftp_user, ftp_pass, path, ftp_host2, host_port2, ftp_user2, ftp_pass2, path2, config
    with open(".config", "r") as file:
        options = Loader(file)
        print(options)
    ftp_host = options[0]
    host_port = int(options[1])
    ftp_user = options[2]
    ftp_pass = options[3]
    path = options[4]
    ftp_host2 = options[5]
    host_port2 = int(options[6])
    ftp_user2 = options[7]
    ftp_pass2 = options[8]
    path2 = options[9]
    config = options[10]
    return config

#Initiates setup wizard so user can configure ftp details also downloads
#all current updates and writes them to database
def firstStart():
    setupWizard()


#redownloads and updates database with all update files. Can be used with Purge function
#to repopulate data.
def redownload():
    Download_all_updates(ftp_host, host_port, ftp_user, ftp_pass, path)
    Download_all_updates(ftp_host2, host_port2, ftp_user2, ftp_pass2, path2)

#daily script to download latest updates file.
def routineStart():
    Download_latest_update(ftp_host, host_port, ftp_user, ftp_pass, path)
    Download_latest_update(ftp_host2, host_port2, ftp_user2, ftp_pass2, path2)

#does a test login to configured ftp servers and returns file list.
def ftpTestExec():
    print("testing ftp server 1")
    ftp_tester(ftp_host, host_port, ftp_user, ftp_pass, path)
    print("testing ftp server 2")
    ftp_tester(ftp_host2, host_port2, ftp_user2, ftp_pass2, path2)

#tests connection to MongoDB database.
def DbTesterExec():
    DBTester()

#Purges all info stored in the database. Recommended to run redownload afterwards.
def DbPurgeExec():
    DataPurge()

#This code was written by Willie Pretorius
#Fork me at https://github.com/Willie-Pretorius

