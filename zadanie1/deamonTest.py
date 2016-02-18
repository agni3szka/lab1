#!/usr/bin/env python
# -*- coding: utf-8 -*-

from StringIO import StringIO
import sys
import unittest
from deamon import Daemon

pid_path = '/tmp/daemon.pid'

class daemonTest(unittest.TestCase):			
    def test_init(self):
        daemon = Daemon(pid_path)
        self.assertEqual(pid_path, daemon.pidfile)
        self.assertEqual('/dev/null', daemon.stdin)
        self.assertEqual('/dev/null', daemon.stdout)
        self.assertEqual('/dev/null', daemon.stderr)

    def test_start(self):
		with self.assertRaises(SystemExit):
			daemon = Daemon(pid_path)
			daemon.start()
			sys.exit(0)	


if __name__ == '__main__':
    unittest.main()
	
	