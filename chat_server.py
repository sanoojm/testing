#! python                                                                                 
import socket, time                                                                       
import select, sys, re, subprocess                                                        
import shlex, os, getopt                                                                  

class Chat:

        def __init__(self,run_as, server_ip):

                self.fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                if run_as == "server":                                    
                        self.LOCAL_ADDR = (server_ip, 8010)               
                        self.fd.bind(self.LOCAL_ADDR)                     
                else:                                                     
                        self.TO_ADDR = (server_ip, 8010)                  

                self.MSG_LEN = 10000
                self.length,self.width=self.screen_size()
                self.screen_size_array()                 

        def whattodo(self):

                self.screen_output()
                caught = select.select([sys.stdin,self.fd],[],[])
                stdin = self.which_handler(caught)               
                if stdin:                                        
                        self.user_input(caught)                  
                        try:                                     
                                self.send_input(self.msg)                
                        except AttributeError:                           
                                self.array.append("Error: Client should initiate the chat first")
                else:                                                                            
                        self.recv_input(caught[0][0])                                            

        def which_handler(self,f):
                pattern=r'stdin'  
                return re.search(pattern,str(f[0][0]))

        def send_input(self,msg):
                self.fd.sendto(msg,self.TO_ADDR)

        def user_input(self,f):
                self.msg= f[0][0].readline()
                self.array.append(self.time_now()+" me: "+str(self.msg))
                self.is_a_command(self.msg)                             

        def is_a_command(self,msg):
                pattern=r'`(.*)`'  
                match=re.search(pattern,msg)
                if match:                   
                        try:                
                                out=subprocess.Popen(shlex.split(match.group(1)),stdout=subprocess.PIPE)
                        except:                                                                         
                                self.array.append("Wrong command $!")                                   
                                return 0                                                                

                        output=out.communicate()
                        self.msg+=output[0]     
                        self.array.append("\nOutput: "+str(self.msg))


        def screen_output(self):
                subprocess.call("clear")
                for element in self.array:
                        print element     
                print "="*int(self.width) 

        def screen_size(self):
                run= subprocess.Popen(["/bin/stty","-a"], stdout=subprocess.PIPE)
                output=run.communicate()                                         
                match = re.search(r'rows\s+(\d+);\s+columns\s+(\d+)', output[0]) 
                return [match.group(1),match.group(2)]                           

        def screen_size_array(self):
                self.array=['']*(int(self.length)-2)

        def recv_input(self,f):
                s=f.recvfrom(self.MSG_LEN)
                self.string, self.TO_ADDR=s[0], s[1]
                if self.is_an_invisible_msg(self.string):
                        self.invisible=self.is_an_invisible_msg(self.string)
                        return 0
                else: self.array.append(self.time_now()+" User: "+str(self.string))
#               if self.log_length <= self.array.__len__(): self.array=self.array[1:]

        def is_an_invisible_msg(self,msg):
                pattern=r'`INVISIBLE-PYTHON-CHAT-WORD-\s+(.*)\s+(.*)`'
                match=re.search(pattern,msg)
                if match:  return {match.group(1):match.group(2)}
                else: return 0


        def time_now(self):
                return str(time.asctime()[-13:-5])

        def __str__(self):
                return 'User: %s' % (self.string)


def main():
	run_as, server_ip = command_line_args()
	login=1
	me=Chat(run_as,server_ip)
	if run_as == "client": me.send_input('`INVISIBLE-PYTHON-CHAT-WORD-  `')
	loop(login,me)

def command_line_args():
	args=sys.argv[1:]
	try:
		optlist,args=getopt.getopt(args,'-r:-i:')
	except getopt.GetoptError:          
	        usage()                         
	        sys.exit(2)  
	return (optlist[0][1], optlist[1][1])

def loop(login,me):
	while login:

	   try:
	        me.whattodo()

	   except KeyboardInterrupt:
	        login=0
	        print "You are logged out."
        	me.send_input("User has logged out")

	   else:
	        print "The program has crashed"
	
def usage():

         print '''Usage:\npython''',sys.argv[0],''' -r (server|client) -i (server ip address)

         -r  run_as, it can be server/ client.
             One instance of the script should be server and the other should be client
         -i  IP address of the machine where the script is running as server

         Ex: python ''',sys.argv[0],''' -r server -i 127.0.0.1
             python ''',sys.argv[0],''' -r client -i 127.0.0.1 \n'''


if __name__ == '__main__':
	main()


