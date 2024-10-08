import sys, subprocess
import paramiko
import socket
import time
import xml.etree.ElementTree as et


def show(remote, command, EPA):
    """
        Executes a command on a remote system and prints the result.

        Parameters:
        remote (paramiko.SSHClient): The SSH client connected to the remote system.
        command (str): The command to be executed on the remote system.
        EPA (bool): A flag indicating whether the system is with EPA.

        Returns:
        None
        """
    stdin, stdout, stderr = remote.exec_command(command)
    result = stdout.read()
    i = 250
    if not EPA:
        try:
            while result[i] != "U" and result[i] != "N" and result[i] != "P" and result[i] != "p" and result[i] != "S":
                i += 1
        except IndexError:
            pass
        print(result[i:] + "\n")  # print the output sans banner
    else:
        print(result)

def main(router):
    """
        Main function to check the router.

        Parameters:
        router (list): The router to be checked.

        Returns:
        None
        """
    if router[0]=="/home/campagnollo/Documents/Python/router_check_xml-master/rtrcheck.py":
        router[0]=0
        router.append("192.168.1.2")
    authtree = et.parse("/home/campagnollo/Documents/Python/router_check_xml-master/auth.xml")
    authroot = authtree.getroot()
    commands = ("sh bgp ipv4 uni sum | b Neighbor", "sh bgp ipv6 uni sum | b Neighbor", "sh ppp multi | i Se")
    print("\n" + time.ctime())
    try:
        ip = socket.gethostbyname(router[1])
        tree = et.parse("sites.xml")
        root = tree.getroot()
        siterouter = {}
        for child in root.findall('site'):
            if child.get('IP') == ip:
                for i in range(0, len(child)):
                    siterouter[child[i].tag] = child[i].text
                break
        if siterouter['routerID']: #check if dict is loaded. If not, exception thrown.
            pass
    except socket.gaierror:  # Exception if IP isn't found
        print("Device not identified on DNS")
        exit()
    except KeyError:  # Exception if IP not found in dictionary "siterouter"
        print("Device not found on critical db")
        exit()
    except UnboundLocalError:  # Exception if IP not found in database
        print("Device not found in database")
        exit()

    if siterouter["critical"] == "yes": #create visual flag if critical site
        for i in range(0, 5):
            print("*****critical******")

    if siterouter["ownership"] == "EPA":  # Use these credentials if with EPA
        EPA = True
        own = 1
    else:
        EPA = False
        own = 0

    user = authroot[own][0].text
    password = authroot[own][1].text

    print("\r")
    try:
        remote = paramiko.SSHClient()
        remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote.connect(hostname=ip, port=22, username=user, password=password, timeout=10)

    except paramiko.AuthenticationException:
        print("Authentication failed")
        exit()

    except socket.error:
        print(siterouter['routerID'])
        print(siterouter['location'])
        print("Unable to connect to device")
        print("Call OOBM:{}".format(siterouter["OOBM"]))
        exit()

    else:
        stdin, stdout, stderr = remote.exec_command("sh ver | i uptime")
        print(stdout.read())

    finally:
        remote.close()

    for i in range(0, len(commands)):
        try:
            remote.connect(hostname=ip, port=22, username=user, password=password, timeout=10)
        except paramiko.AuthenticationException:
            print("Authentication failed")
            exit()
        else:
            show(remote, commands[i], EPA)
        remote.close()


if __name__ == '__main__':
    """
        Entry point of the script. Checks the Python interpreter version and calls the main function.
    """
    try:
        assert sys.version_info[0] < 3
    except AssertionError:
        print("Incorrect interpreter being run. Please use Python 2.x")
        exit()
    main(sys.argv)
    
