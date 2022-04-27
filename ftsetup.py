from datahandler import DataPurge,DBTester,Download_all_updates,Download_latest_update,DataWriter,ftp_tester
from logginghandler import sendEmail

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
def Setup_wizard():
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

#writes config to be 0 so the script can run in routine mode.
def disable_config():
    global ftp_host, host_port, ftp_user, ftp_pass, path, ftp_host2, host_port2, ftp_user2, ftp_pass2, path2, config
    ftp1 = f"host:{ftp_host}\nport:{host_port}\nuser:{ftp_user}\npass:{ftp_pass}\npath:{path}\nftp_num:2\nconfig_mode:0"
    ftp1 += f"\nhost:{ftp_host2}\nport:{host_port2}\nuser:{ftp_user2}\npass:{ftp_pass2}\npath:{path2}"
    with open(".config", "w") as file:
        file.write(ftp1)
        file.close()
    print("Config has been reset to 0 routing starts will resume.")

#allows user to configure smtp details and save to file.
def config_smtp():
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
def config_loader():
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
def first_start():
    Setup_wizard()
    config_loader()
    data = Download_all_updates(ftp_host, host_port, ftp_user, ftp_pass, path)
    DataWriter(data)
    data2 = Download_all_updates(ftp_host2, host_port2, ftp_user2, ftp_pass2, path2)
    DataWriter(data2)

#redownloads and updates database with all update files. Can be used with Purge function
#to repopulate data.
def redownload():
    data = Download_all_updates(ftp_host, host_port, ftp_user, ftp_pass, path)
    DataWriter(data)
    data2 = Download_all_updates(ftp_host2, host_port2, ftp_user2, ftp_pass2, path2)
    DataWriter(data2)

#daily script to download latest updates file.
def routine_start():
    data = Download_latest_update(ftp_host, host_port, ftp_user, ftp_pass, path)
    DataWriter(data)
    data2 = Download_latest_update(ftp_host2, host_port2, ftp_user2, ftp_pass2, path2)
    DataWriter(data2)

#does a test login to configured ftp servers and returns file list.
def ftp_test_exec():
    print("testing ftp server 1")
    ftp_tester(ftp_host, host_port, ftp_user, ftp_pass, path)
    print("testing ftp server 2")
    ftp_tester(ftp_host2, host_port2, ftp_user2, ftp_pass2, path2)

#tests connection to MongoDB database.
def DB_Tester_exec():
    DBTester()

#Purges all info stored in the database. Recommended to run redownload afterwards.
def DB_Purge_exec():
    DataPurge()

#This code was written by Willie Pretorius
#Fork me at https://github.com/Willie-Pretorius

