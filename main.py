from ftsetup import *
from logginghandler import *
def menu():
    addLog("Menu has been accessed\n")
    exit_me = False
    while exit_me == False:
        print("Welcome to CRDB script configurator.\nVersion: Alpha build 0.1 \n Enter ? for help:")
        command = input("enter command:  ")
        if command == "?":
            print("1. View Logs\n"
                  "2. Download last update \n"
                  "3. Re-download all updates\n"
                  "4. FTP config wizard\n"
                  "5. Test FTP logins\n"
                  "6. Config SMTP server\n"
                  "7. Test SMTP server\n"
                  "8. Test Database Connection\n"
                  "9. Purge database\n"
                  "10. Download Data from One time FTP..\n"
                  "11. Exit\n"
                  )
        if command == "1":
            with open("logs.txt","r") as file:
                text = file.read()
                arr = text.split("\n")
                for log in arr:
                    print(log)
        elif command == "2":
            routineStart()
        elif command == "3":
            redownload()
        elif command == "4":
            setupWizard()
        elif command == "5":
            ftpTestExec()
        elif command == "6":
            configSmtp()
        elif command == "7":
            try:
                sendEmail("Test101", "This is a test email")
                print("Test email sent.")
            except:
                print("smtp server test failed.")
                addLog("Menu has been accessed\n")
        elif command == "8":
            try:
                DbTesterExec()
            except:
                print("DBTester got an error")
                addLog("DBTester got an error\n")
        elif command == "9":
            DbPurgeExec()
        elif command == "10":
            OneTimeFTP_EXEC()
        elif command == "11":
            exit_me = True
        #     print("Next start will be a daily download and update cycle. To get back into menu change config to 0")
        #     confirm = input("Proceed to exit?\n press 'enter' to proceed\n type 'n' to go back to menu")
        #     if confirm == "n":
        #         pass
        #     else:
        #         disableConfig()
        #         exit_me = True
        else:
            print("Invalid command type ? for help.")
# menu()
# startup script

#load config file
try:
    config = configLoader()
except:
    firstStart()
menu()



#This code was written by Willie Pretorius
#Fork me at https://github.com/Willie-Pretorius



