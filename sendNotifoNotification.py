#!/usr/bin/python
# 
#	License
#   =======
#	Creative Commons Attribution-Share Alike 3.0
#	http://creativecommons.org/licenses/by-sa/3.0/us/
#
#	Simply give original credit and a link to http://jrfom.com/
#
from Notifo import *
import optparse
import sys

### Set these values appropriately
user = ''
key = ''



### Begin Main Program ###
def parseOptions(x):
	d = {}
	for k,v in x.items():
		if v is not None:
			d[k] = v
	return d

usage="""
	%prog -t "auser" -m "Hey! How are you?"

	See https://api.notifo.com/ for more information.
"""

parser = optparse.OptionParser(usage=usage)
parser.add_option("-t", "--to", action="store", help="Set the 'to' parameter.", type="string")
parser.add_option("-m", "--msg", action="store", help="Set the message to send.", type="string")
parser.add_option("-l", "--label", action="store", help="Set the label for the application.", type="string")
parser.add_option("-i", "--title", action="store", help="Set the title for the notification message.", type="string")
parser.add_option("-u", "--uri", action="store", help="Set the message callback URI.", type="string")

(options, args) = parser.parse_args()

notifo = Notifo(user, key)
params = parseOptions(vars(options))

if not params.has_key("to"):
	print "You must specify the --to parameter."
	sys.exit(1)

if not params.has_key("msg"):
	print "You must specify the --msg parameter."
	sys.exit(1)

print notifo.sendNotification(params)