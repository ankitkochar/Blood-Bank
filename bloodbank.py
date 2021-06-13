import sqlite3 as sq3
from os import name,system
# from tabulate import tabulate
from re import search
from prettytable import PrettyTable
def check(email):
	email=email.lower()
	r ="^[a-z0-9._]+@\w+.(in|com|org)$"
	return bool( search(r,email) )
def clear():
	if name=='nt':
		system('cls')
	else:
		system('clear')

def hold():
	input('Press ENTER To Continue :')
con=sq3.connect("database.db")
c=con.cursor()
q='''create table if not exists user(
			id integer not null primary key autoincrement,
			name varchar not null,
			type varchar not null,
			contact integer not null,
			email_id varchar ,
			blood_group varchar not null,
			blood_amount integer not null);'''
c.execute(q)
con.commit()
q=''' create table if not exists bloodbank(
			id integer not null primary key autoincrement,
			bloodtype varchar not null ,
			bloodamount integer not null);'''


c.execute(q)
con.commit()

q=''' select count(bloodtype) from bloodbank;
			'''
c.execute(q)
flag=c.fetchone()
l=['A+','A-','B+','B-','AB+','AB-','O+','O-']
if flag[0]==0:
	for i in l:
		q='insert into bloodbank(bloodtype,bloodamount) values ("{}",{});'.format(i,0)
		c.execute(q)
		con.commit()

def donor():
	while True:
		name=input('ENTER THE DONOR NAME :').upper()
		if name.isalpha():
			break
		else:
			print('INVALID ENTRY')
	typ='DONOR'
	while True:
		contact=input('ENTER THE CONTACT NUMBER :')
		if contact.isnumeric():
			if len(contact)==10:
				if contact[0] in '9876':
					break
		print('INVALID ENTRY')
	while True:
		email_id=input('ENTER THE EMAIL ID :').upper()
		if check(email_id):
			break
		else:
			print('INVALID ENTRY')
	while True:
		blood_group=input('ENTER THE BLOOD GROUP :').upper()
		if blood_group not in l:
			print('INVALID ENTRY')
		else:
			break
	while True:
		blood_amount=input('ENTER THE BLOOD AMOUNT IN UNITS :')
		if blood_amount.isnumeric():
			break
		else:
			print('INVALID ENTRY')
	q1="insert into user(name,type,contact,email_id,blood_group,blood_amount) values('{}','{}','{}','{}','{}','{}');".format(name,typ,contact,email_id,blood_group,blood_amount)
	q2="update bloodbank set bloodamount=bloodamount + '{}' where bloodtype='{}';".format(blood_amount,blood_group)
	c.execute(q2)
	c.execute(q1)
	con.commit()
	print('Successfully Submitted Donor'.upper())
def reciever():
	while True:
		name=input('ENTER THE RECIEVER NAME :').upper()
		if name.isalpha():
			break
		else:
			print('INVALID ENTRY')
	typ='RECIEVER'
	while True:
		contact=input('ENTER THE CONTACT NUMBER :')
		if contact.isnumeric():
			if len(contact)==10:
				if contact[0] in '9876':
					break
		print('INVALID ENTRY')

	while True:
		email_id=input('ENTER THE EMAIL ID :').upper()
		if check(email_id):
			break
		else:
			print('INVALID ENTRY')
	while True:
		blood_group=input('ENTER THE BLOOD GROUP :').upper()
		if blood_group not in l:
			print('INVALID ENTRY')
		else:
			break
	while True:
		blood_amount=input('ENTER THE BLOOD AMOUNT IN UNITS :')
		if blood_amount.isnumeric():
			break
		else:
			print('INVALID ENTRY')
	q=''' select bloodamount 
			from bloodbank
			where bloodtype ="{}";
			'''.format(blood_group)
	c.execute(q)
	bloodinbloodbank=c.fetchone()
	if bloodinbloodbank[0]>=int(blood_amount):
		q1="insert into user(name,type,contact,email_id,blood_group,blood_amount) values('{}','{}','{}','{}','{}','{}');".format(name,typ,contact,email_id,blood_group,blood_amount)
		c.execute(q1)
		q2="update bloodbank set bloodamount=bloodamount - {} where bloodtype='{}';".format(blood_amount,blood_group)
		c.execute(q2)
		con.commit()
		print('Reciever recieved THE blood'.upper())
	else:
		if bloodinbloodbank[0]==0:
			print('Sorry,We are out of Blood for {}'.format(blood_group).upper())
		else:
			print('we are having {} Quantity of blood group {} in our Blood bank!'.format(bloodinbloodbank[0],blood_group).upper())
			print('Still Wants to Recieve all blood of {} blood group?'.format(blood_group).upper())

			while True:
				n=input('for yes enter: 1 and for no type: 2'.upper())
				if n=='1':
					q1="insert into user(name,type,contact,email_id,blood_group,blood_amount) values('{}','{}','{}','{}','{}','{}');".format(name,typ,contact,email_id,blood_group,bloodinbloodbank[0])
					c.execute(q1)
					q2="update bloodbank set bloodamount=bloodamount - {} where bloodtype='{}';".format(bloodinbloodbank[0],blood_group)
					c.execute(q2)
					con.commit()
					print('Reciever Recieved Blood'.upper())
					break
				elif n=='2':
					print('Sorry,We are out of Blood for {}'.format(blood_group).upper())
					break
				else:
					print('WRONG ENTER')
					print('PLEASE ENTER THE VALID NUMBER')
	con.commit()
def detail():
	new=['S.NO.','NAME','TYPE','CONTACT','EMAIL','BLOOD GROUP','BLOOD AMOUNT']
	x=PrettyTable()
	x.field_names=new
	q2='select * from user;'
	c.execute(q2)
	clear()
	d=c.fetchall()
	for i in d:
		x.add_row(i)
	print(x)
	# d.insert(0,new)
	# print(tabulate(d))

def blooddetails():
	x=PrettyTable()
	new1=['B.NO.','BLOOD GROUP','QUANTITY']
	x.field_names=new1
	q3='''select *
			from bloodbank
			'''
	c.execute(q3)
	clear()
	detail=c.fetchall()
	for i in detail:
		x.add_row(i)
	print(x)
	# detail.insert(0,new1)
	# print(tabulate(detail))
while (True) :
	clear()
	print('WELCOME IN BLOOD BANK')
	print(' \n 1: add donor \n 2: add reciever \n 3: check enteries \n 4: check remaining blood amount \n 5: exit'.upper())
	option=input('SELECT AN OPTION :')
	if option=='1':
		clear()
		donor()
		hold()
	elif option=='2':
		clear()
		reciever()
		hold()
	elif option=='3':
		clear()
		detail()
		hold()
	elif option=='4':
		clear()
		blooddetails()
		hold()  
	elif option=='5':
		clear()
		exit()
	else:
		clear()
		print('invalid option'.upper())
		hold()

con.commit()
con.close()

	
