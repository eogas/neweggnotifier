import sys
import urllib2
import json
import re
import time
from Notifo import *
	
debug = True

listpath = 'products.txt'
pricereg = re.compile(r'\$(\d+)\.(\d+)')
gnotifo = None
user = ''

def main():
	if len(sys.argv) == 3:
		(usr, key) = sys.argv[1:]
		notifo = Notifo(usr, key)
	else:
		print "Usage: neno.py <username> <api key>"
		return

	global user, gnotifo
	user = usr
	gnotifo = notifo
	delay = 1 * 60 # 1 minutes
	
	saveditems = {}

	while True:
		saveditems = UpdateItems(saveditems)

		for itemnum in saveditems:
			Debug('Checking item %s' % itemnum)

			oldinfo = saveditems[itemnum]
			newinfo = GetProductInfo(itemnum)

			if newinfo == None:
				continue

			if oldinfo == None and not newinfo == None and newinfo['isactivated']:
				DoNotify('Product activated!', newinfo)
				saveditems[itemnum] = newinfo

			elif not oldinfo['isactivated'] and newinfo['isactivated']:
				DoNotify('Product activated!', newinfo)
				saveditems[itemnum] = newinfo

			# Note - the afterrebate price is set to the finalprice if there is no
			# rebate, thus the afterrebate price will always drop if the finalprice drops
			elif oldinfo['afterrebate'] > newinfo['afterrebate']:
				DoNotify("Price dropped!", newinfo)
				saveditems[itemnum] = newinfo

		Debug(time.asctime( time.localtime( time.time() ) ))
		Debug('\n')
		time.sleep(delay)

	raw_input()
	
def UpdateItems(saveditems):
	try:
		listfile = open(listpath, 'r')
	except IOError:
		return

	listlines = listfile.readlines()
	listfile.close()

	# add any new items in products.txt
	# remove any items that have been removed from products.txt
	newitems = {}
	for itemnum in listlines:
		itemnum = itemnum.strip('\n')
		if not itemnum == '':
			if not itemnum in saveditems:
				item = GetProductInfo(itemnum)

				newitems[itemnum] = item
			else:
				newitems[itemnum] = saveditems[itemnum]

	return dict(newitems)

def DoNotify(txt, info):
	global user
	msg = '%s\n%s -> $%s' % (info['title'], txt, info['afterrebate'] * 0.01)
	post = {
		 'to':user,
		 'msg':msg,
		 'label':'neweggnotifier',
		 'uri':'http://www.newegg.com/Product/Product.aspx?Item=%s' % info['itemnum']
		 }
	gnotifo.sendNotification(post)
	pass

def Debug(txt):
	if debug:
		print txt

def GetProductInfo(itemnum):
	url = 'http://www.ows.newegg.com/Products.egg/%s/' % itemnum
	response = urllib2.urlopen(url).read()

	# validate reponse
	if response == '':
		return None
	else:
		fullinfo = json.loads(response)

	# grab the "final" price
	m = pricereg.search(fullinfo['FinalPrice'])
	if not m == None:
		finalprice = int(m.group(1) + m.group(2))

	afterrebate = finalprice

	# grap the price after rebate, if there is one
	rebateinfo = fullinfo['MailInRebateInfo']

	if not rebateinfo == None:
		m = pricereg.search(rebateinfo[0])
		if not m == None:
			afterrebate = int(m.group(1) + m.group(2))

	# return dict with prices and some more info
	return {
		 'itemnum':itemnum,
		 'title':fullinfo['Title'],
		 'finalprice':finalprice,
		 'afterrebate':afterrebate,
		 'isactivated':fullinfo['IsActivated'],
		 'freeshipping':fullinfo['FreeShippingFlag']
		 }

if __name__ == '__main__':
	main()