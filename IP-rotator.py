import os
import time

def init():
    # Set authentication information
    # Path is normally C:\Users\$USERNAME$\OpenVPN
    root = input("Enter OpenVPN directory path: \n")
    authPath =  root  +"\\config\\auth.txt"
    
    if(not os.path.exists(authPath)):
        name = input("Enter OpenVPN username: ")
        password = input("Enter OpenVPN password: ")
        with open(authPath, 'w') as f:
            f.write(name + "\n" + password) 
        f.close()

    return root

def configModifier(dir):
    unmodified = "auth-user-pass"
    modified = "auth-user-pass auth.txt"

    for file in os.listdir(dir):
        f = os.path.join(dir, file)
        if (os.path.isfile(f) and f.endswith('.ovpn')):
            with open (f, 'r') as t:
                data = t.read()
                if (data.find(modified) == -1):
                    print("Modifying "+ file)
                    data = data.replace(unmodified, modified)
            t.close()

            with open (f, 'w') as t:
                t.write(data)
            t.close()

def connect(configFile):
    # Establish VPN connection
    print("Establishing connection using " + configFile)
    command = """ "C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe" --command connect """ + configFile
    os.system(command)

    # Exceptions and failures are not verbose in command line
    # Must see GUI for error messages
    # So far I don't see a way to handle exceptions in python
    return

def disconnect(configFile):
    # Disconnect from VPN
    command = """ "C:\\Program Files\\OpenVPN\\bin\\openvpn-gui.exe" --command disconnect """ + configFile
    os.system(command)
    print("Disconnected")

    return

def delay():
    # IP switching condition
    # i.e. a certain amount of time, return != 200
    # Replace as needed
    time.sleep(15)

    return

if __name__ == "__main__":
    root = init()
    config = os.path.join(root, "config")
    configModifier(config)

    for file in os.listdir(config):
        f = os.path.join(config, file)
        if (os.path.isfile(f) and f.endswith('.ovpn')):
            connect(file)
            delay()
            disconnect(file) 

    input("\nYou have iterated through all available config files, press <Enter> to exist...")
    