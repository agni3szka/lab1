#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os, time, atexit
from signal import SIGTERM

pid_path = '/tmp/daemon.pid'
log_path = '/tmp/daemon.log'

class Daemon:
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile

        def daemonize(self):
                try:
                        pid = os.fork()
                        if pid > 0:
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("Fork #1 error: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)

                os.chdir("/")
                os.setsid()
                os.umask(0)

                try:
                        pid = os.fork()
                        if pid > 0:
                                print "Daemon PID %d" % pid
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("Fork #2 error: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)

                sys.stdout.flush()
                sys.stderr.flush()
                si = file(self.stdin, 'r')
                so = file(self.stdout, 'a+')
                se = file(self.stderr, 'a+', 0)
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())

                atexit.register(self.delpid)
                pid = str(os.getpid())
                file(self.pidfile,'w+').write("%s\n" % pid)


        def delpid(self):
                os.remove(self.pidfile)


        def status(self):
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                        print "Daemon is working. PID = %d" % pid
                        return True
                except IOError:
                        pid = None
                        print "Daemon is not working."
                        return False


        def start(self):
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
						
                if pid:
                        message = 'Daemon is already working.\n'
                        sys.stderr.write(message)
                        sys.exit(1)

                self.daemonize()
                self.run()


        def stop(self):
                try:
                        pf = file(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None

                if not pid:
                        message = 'Deamon is not working. Nothing to stop.\n'
                        sys.stderr.write(message)
                        return

                try:
                        while 1:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError, err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                        else:
                                print str(err)
                                sys.exit(1)

        def restart(self):
                self.stop()
                self.start()

        def run(self):
		  f = open(log_path, "w")
		  while True:
			   p = os.popen('date',"r")
			   date = p.readline()
			   f.write('%s \n' % date)
		 	   p = os.popen('top -bn1 | grep "Cpu(s)"',"r")
			   cpu = p.readline()
			   f.write('%s \n' % cpu)
		 	   p = os.popen('free -m',"r")
			   mem = p.read()
			   f.write('%s \n' % mem)
			   p = os.popen('/sbin/ifconfig',"r")
			   network = p.read()
			   f.write('%s' % network)
			   f.write('----------------------------------\n\n')
			   f.flush()
                	   time.sleep(30)
						
if __name__ == "__main__":
        daemon = Daemon(pid_path)
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                elif 'status' == sys.argv[1]:
                        daemon.status()
                else:
                        print "Nieznany parametr"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "Usage: %s start|stop|restart|status" % sys.argv[0]
                sys.exit(2)
