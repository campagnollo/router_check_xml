import sys, subprocess
import paramiko
import socket
import time
import xml.etree.ElementTree as et

def show(remote, command, EPA):

    stdin, stdout, stderr=remote.exec_command(command)
    result = stdout.read()
    i=250
    if not(EPA):
        try:
            while result[i]!="U" and result[i]!="N" and result[i]!="P" and result [i]!="p" and result[i]!="S":
               i+=1
        except IndexError:
            pass
        print(result[i:]+"\n") #print the output sans banner
    else:
        print(result)


def main(router):
    ATTuser="***redacted***"
    ATTpassword="***redacted***"
    TACACSuser="***redacted***"
    TACACSpassword="***redacted***"
    commands=("sh bgp ipv4 uni sum | b Neighbor","sh bgp ipv6 uni sum | b Neighbor","sh ppp multi | i Se")
    print("\n"+time.ctime())
    try:
        ip = socket.gethostbyname(router[1])  # ID device name or pass IP address
        tree = et.parse("sites.xml")
        root = tree.getroot()
        siterouter={}
        for child in root.findall('site'):
            if child.get('IP') == ip:
                for i in range (0,len(child)):
                    siterouter[child[i].tag] = child[i].text
                break
        if siterouter['routerID']:
            pass
    except socket.gaierror: #Exception if IP isn't found
        print("Device not identified on DNS")
        exit()
    except KeyError: #Exception if IP not found in sites.xml
        print("Device not found on critical db")
        exit()
    except UnboundLocalError: #Exception if IP not found in database
        print("Device not found in database")
        exit()

    if siterouter["critical"] == "yes":
        for i in range (0,5):
            print("*****critical******")

    if siterouter["ownership"]=="EPA": #Use these credentials if with EPA
        user=TACACSuser
        password=TACACSpassword
        EPA=True

 else:  #Use credentials if with AT&T
        user=ATTuser
        password=ATTpassword
        EPA=False

    print("\r") #White space
    try:
        remote=paramiko.SSHClient()
        remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote.connect(hostname=ip, port=22,username=user,password=password, timeout=10)
        remote_transport=remote.get_transport()

    except paramiko.AuthenticationException:
        print("Authentication failed")
        exit()

    except socket.error:
        print(siterouter[routerID])
        print(siterouter[location])
        print("Unable to connect to device")
        print("Call OOBM:{}".format(siterouter["OOBM"]))
        exit()

    else:
        stdin, stdout, stderr=remote.exec_command("sh ver | i uptime")
        print(stdout.read())

    finally:
        remote.close()


    for i in range (0,len(commands)):
       try:
          remote.connect(hostname=ip, port=22,username=user,password=password, timeout=10)
          remote_transport=remote.get_transport()
       except paramiko.AuthenticationException:
          print("Authentication failed")
          exit()
       else:
          show(remote,commands[i],EPA) #If connected, run through 'show' commands
       remote.close()

if __name__ == '__main__':
#"""Python interpreter check"""
    try:
        assert sys.version_info[0]<3
    except AssertionError:
        print("Incorrect interpreter being run. Please use Python 2.x")
        exit()
    main(sys.argv)

