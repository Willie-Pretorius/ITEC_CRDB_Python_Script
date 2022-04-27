from ftsetup import config_smtp,disable_config,DB_Purge_exec,DB_Tester_exec,Setup_wizard,Loader,Setup_wizard,config_loader,first_start,routine_start,redownload, ftp_test_exec
from logginghandler import addLog,sendEmail
def menu():
    addLog("Menu has been accessed\n")
    exit_me = False
    while exit_me == False:
        print("Welcome to CRDB script configurator. Enter ? for help:")
        command = input("enter command:  ")
        if command == "?":
            print("1. View Logs(Not Available Yet)\n"
                  "2. Download last update \n"
                  "3. Re-download all updates\n"
                  "4. FTP config wizard\n"
                  "5. Test FTP logins\n"
                  "6. Config SMTP server\n"
                  "7. Test SMTP server\n"
                  "8. Test Database Connection\n"
                  "9. Purge database\n"
                  "10. Download full datastack(Not available yet)\n"
                  "11. Exit\n")
        if command == "1":
            print("Not Available yet")
        elif command == "2":
            routine_start()
        elif command == "3":
            redownload()
        elif command == "4":
            Setup_wizard()
        elif command == "5":
            ftp_test_exec()
        elif command == "6":
            config_smtp()
        elif command == "7":
            try:
                sendEmail("Test101", "This is a test email")
            except:
                print("smtp server test failed.")
                addLog("Menu has been accessed\n")
        elif command == "8":
            try:
                DB_Tester_exec()
            except:
                print("DBTester got an error")
                addLog("DBTester got an error\n")
        elif command == "9":
            DB_Purge_exec()
        elif command == "10":
            print("This function will be developed further after successful deployment.")
        elif command == "11":
            print("Next start will be a daily download and update cycle. To get back into menu change config to 0")
            confirm = input("Proceed to exit?\n press 'enter' to proceed\n type 'n' to go back to menu")
            if confirm == "n":
                pass
            else:
                disable_config()
                exit_me = True
        else:
            print("Invalid command type ? for help.")
# menu()
# startup script
try:
    #load config file
    config = config_loader()
    if config == "1":
        menu()
    else:
        routine_start()
except:
    try:
        # load config file
        config = config_loader()
    except:
        print("executing first start")
        first_start()
        menu()
    else:
        routine_start()

#This code was written by Willie Pretorius
#Fork me at https://github.com/Willie-Pretorius



