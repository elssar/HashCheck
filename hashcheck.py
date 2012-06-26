#!/usr/bin/python

# Will take the md5 & sha1 sums of passwords and search the internet using the Google custom search api to see whether or not there is a result.
# If a result appears then the password is part of a rainbow table and should be considered insecure. Though no results appearing doesn't
# necissarily mean that the password is secure, but it's still reassuring.
# 
# Author : Akshay Bist
# Licence : GPL v3 - http://www.gnu.org/copyleft/gpl.html

from sys import argv, path, exit
from hashlib import md5, sha1
import yaml
from os import remove
from apiclient.discovery import build

DIR= path[0]

def search(d):
	devkey= #your Google API developer key here. If you don't have one, then visit https://code.google.com/apis/console/
	cxnum= '005885665219560850145:li6xrgl1_vy'
	service= build('customsearch', 'v1', developerKey= devkey)
	rs= {}
	for serv in d:
		rs[serv]= []
	for serv in d:
		for h in d[serv]:
			res = service.cse().list(q=h, cx=cxnum).execute()
			rs[serv].append(res)
	return rs

def save_file(d):
	'Save data to the password file'
	pwd_file= open(DIR+'/pwd.yaml', 'w')
	yaml.dump(d, pwd_file)
	pwd_file.close()
		
def load_file():
	'Load the password file'
	try:
		pwd_file= open(DIR+'/pwd.yaml', 'r')
	except IOError:
		return None
	data= yaml.load(pwd_file.read())
	pwd_file.close()
	return data

def display_results(results):
	for serv in results:
		if results[serv][0]['queries']['request'][0]['totalResults']=='0' and results[serv][1]['queries']['request'][0]['totalResults']=='0':
			print serv, ': Probably safe' 
		else:
			print serv, ': Not safe'
	
def mfile(mode):
	'''Password file manipulation.
	   Command line arguments -
	   -m, --makefile : make a new file(will delete previous file)
	   -a, --append   : add new passwords to file
	   -c, --change   : change a password
	   -d, --delete   : delete a password from the file
	   -p, --purge    : delete the password file
	   -v, --view     : view the services whose passwords are stored'''
	if mode=='m' or mode=='makefile':
		pwd_list= []
		print 'Enter passwords. Format : Service-name (one space) password'
		print 'Leave blank to end'
		while True:
			p= raw_input()
			if p=='':
				break
			pwd_list.append(p)
		pwd_dict= {}
		for pwd in pwd_list:
			t= pwd.split()
			pwd_dict[t[0]]= [md5(t[1]).hexdigest(), sha1(t[1]).hexdigest()]
		save_file(pwd_dict)
	
	elif mode=='a' or mode=='append':
		pwd_dict= load_file()
		if not pwd_dict:
			print 'No password file exists. Will create new one instead.'
			pwd_dict= {}
		print 'Enter passwords. Format : Service-name (one space) password'
		print 'Leave blank to end'
		pwd_list= []
		while True:
			p= raw_input()
			if p=='':
				break
			pwd_list.append(p)
		for pwd in pwd_list:
			t= pwd.split()
			pwd_dict[t[0]]= [md5(t[1]).hexdigest(), sha1(t[1]).hexdigest()]
		save_file(pwd_dict)
	
	elif mode=='c' or mode=='change':
		pwd_dict= load_file()
		if not pwd_dict:
			print 'No password file exists. Please make one by running checkpass.py with -m or --makefile as argument'
			exit(1)
		for serv in pwd_dict:
			print serv
		print 'Enter service to change(case sensitive): '
		while True:
			s= raw_input()
			if s not in pwd_dict:
				print 'Error, incorrect input. Try again.'
			else:
				break
		print 'Enter password: '
		p= raw_input()
		pwd_dict[s]= [md5(p).hexdigest(), sha1(p).hexdigest()]
		save_file(pwd_dict)
	elif mode=='d' or mode=='delete':
		pwd_dict= load_file()
		if not pwd_dict:
			print 'No password file exists. Please make one by running checkpass.py with -m or --makefile as argument'
			exit(1)
		for serv in pwd_dict:
			print serv
		print 'Enter service to delete(case sensitive): '
		while True:
			s= raw_input()
			if s not in pwd_dict:
				print 'Error, incorrect input. Try again.'
			else:
				break
		pwd_dict.__delitem__(s)
		save_file(pwd_dict)
		
	elif mode=='p' or mode=='purge':
		remove(DIR+'/pwd.yaml')
	
	elif mode=='v' or mode=='view':
		pwd_dict= load_file()
		if not pwd_dict:
			print 'No password file exists. Please make one by running checkpass.py with -m or --makefile as argument'
			exit(1)
		for serv in pwd_dict:
			print serv

def phelp():
	'''Program help. Command line arguments -
	   -h, --help : will display all help options'''
	loc= DIR+'/help.txt'
	helpfile= open(loc, 'r')
	print helpfile.read(),
	helpfile.close()

def check():
	'''Will search for the passwords in the password file on DuckDuckGo.
	   Default behavior.'''
	pwd_dict= load_file()
	result= search(pwd_dict)
	display_results(result)

def textinput(passwords):
	'''Will check the password(s) input as command line arguments.
	   -t, --textinput : Will take in passwords from the command line & test them'''
	pwd_dict= {}
	for p in passwords:
		pwd_dict[p]= [md5(p).hexdigest(), sha1(p).hexdigest()]
	result= search(pwd_dict)
	display_results(result)

def main():
	'''Main function'''
	args= {'-m':'mfile("m")', '-a':'mfile("a")', '-c':'mfile("c")', '-d':'mfile("d")', '-p':'mfile("p")', '-v':'mfile("v")', '-h':'phelp()',
	       '-t':'textinput(argv[2:])', '--makefile':'mfile("m")', '--append':'mfile("a")', '--change':'mfile("c")',
	       '--delete':'mfile("d")', '--purge':'mfile("p")', '--view':'mfile("view"', '--help':'help()', '--textinput':'textinput(argv[2:])'}
	if len(argv)==1:
		check()
		exit(0)
	elif (argv[1] not in args) or (len(argv)>2 and (argv[1] != '-t' or argv[1] != '--textinput')):
		print '\nIncorrect arguments\n'
		phelp()
	else:
		eval(args[argv[1]])

if __name__ == '__main__':
	main()
