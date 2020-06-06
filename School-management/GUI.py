from tkinter import * 
import tkinter as tk
import tkinter.font
import datetime
import tkinter.messagebox
from datetime import timedelta
import os
import hashlib
import binascii
from PIL import Image, ImageTk

def login_in():
	global id_input_login
	global password_input_login
	global login_menu

	login_menu=Tk()
	login_menu.wm_title("Login")
	login_menu.geometry('700x550')
	login_menu.resizable(True,True)
	k_font = tkinter.font.Font(family='Times new roman', size=16, weight=tkinter.font.BOLD)
	orionLabel=Label(login_menu, text="GYAAN MANDIR",bg='dark orange',font=("Castellar", "25","bold","italic","underline"),fg="black")
	subLabel=Label(login_menu, text="A SCHOOL FOR LEARNING",font=("Castellar", "16","bold","italic"))
	id_label=Label(login_menu,text="Enter Your ID:",height=3, font=k_font)
	password_label=Label(login_menu,text="Enter Password:",height=3,font=k_font)
	id_input_login=Entry(login_menu, width=30)
	password_input_login=Entry(login_menu, width=30)
	loginbutton1=Button(login_menu,command=login_check,text=" Login ",bg='light blue',height='1',width='8', font=k_font,  bd = '5')
	registerbutton=Button(login_menu,command=register_in,text=" Register ",bg='green',fg='white',height='2',width='11',font=k_font, bd = '5',)
	feedbackbutton=Button(login_menu,command=feedback_read,text=" Feedback ",bg='yellow',height='2',width='11',font=k_font, bd = '5')
	adminbutton=Button(login_menu,command=admin_in,text=" Admin Login ",bg='red', fg='white',height='2',width='11',font=k_font, bd = '5')
	password_input_login.config(show="*")

	orionLabel.place(x=160, y=20)
	subLabel.place(x=190, y=80)
	id_label.place(x=10,y=120)
	id_input_login.place(x=160,y=150)
	password_label.place(x=10,y=170)
	password_input_login.place(x=160,y=200)
	loginbutton1.place(x=30,y=240)
	registerbutton.place(x=500,y=150)
	adminbutton.place(x=500,y=230)
	feedbackbutton.place(x=500,y=310)

	login_menu.mainloop()

def login_check():
	global id
	id=id_input_login.get()
	password=password_input_login.get()

	pos = binary_search('index.txt', id)
	if pos == -1:
		tkinter.messagebox.showinfo("Login"," Username is incorrect.Please reenter")
		return(login_in)
	else:
		f2 = open ('Userprofile.txt', 'r')
		f2.seek(int(pos))
		l = f2.readline()
		l = l.rstrip()
		word = l.split('|')
		if(verify_password(word[1], password)):
			tkinter.messagebox.showinfo("Login","Login Successful!")
			login_menu.destroy()
			Main_Menu()
		else:
			tkinter.messagebox.showinfo("Login"," Password that you have entered is incorrect.Please reenter")
			return(login_in)
		f2.close()


def register_in():
	global id_input
	global name_input
	global email_input
	global password_input
	global register_menu

	register_menu=Tk()
	register_menu.wm_title("Register")
	register_menu.geometry('400x400')
	register_menu.resizable(0,0)
	k_font = tkinter.font.Font(family='Lucida Calligraphy', size=10, weight=tkinter.font.BOLD)

	id_label=Label(register_menu,text="Your ID")
	name_label=Label(register_menu,text="Full Name")
	email_label=Label(register_menu,text="Email")
	password_label=Label(register_menu,text="Password")
	login_label=Label(register_menu,text="Already have an account?")
	id_input=Entry(register_menu,width=30)
	name_input=Entry(register_menu,width=30)
	email_input=Entry(register_menu,width=30)
	password_input=Entry(register_menu,width=30)
	loginbutton1=Button(register_menu,command=login_in,text=" Login ",bg='light blue',height=1,width=9,font=k_font)
	registerbutton=Button(register_menu,command=register_check,text=" Register ",bg='dark blue', fg='white',height=1,width=7,font=k_font, bd='5')
	password_input.config(show="*")

	id_label.grid(row=3, column = 4, pady = (10,10),padx=(10, 10))
	id_input.grid(row=3,column=5, sticky=E)
	name_label.grid(row=4, column = 4, pady = (10,10),padx=(10, 10))
	name_input.grid(row=4, column = 5, sticky=E)
	email_label.grid(row=5, column = 4, pady = (10,10),padx=(10, 10))
	email_input.grid(row=5,column=5, sticky=E)
	password_label.grid(row=6, column = 4, pady = (10,10),padx=(10, 10))
	password_input.grid(row=6,column=5, sticky=E)
	login_label.grid(row=8, column = 4, pady = (10,10),padx=(10, 10))
	registerbutton.grid(row =7, column = 5, pady = (10,10),padx=(10, 10))
	loginbutton1.grid(row =8, column = 5, pady = (10,10),padx=(10, 10))

	register_menu.mainloop()

def register_check():
	global id

	id=id_input.get()
	name=name_input.get()
	email=email_input.get()
	password=password_input.get()

	if len(id)==0 or len(name) == 0 or len(email) == 0 or len(password) == 0:
		tkinter.messagebox.showinfo("Register","You left one or more fields blank, please fill it up.")
		register_menu.lift()
		return(register_in)

	pos = binary_search('index.txt', id)
	if pos != -1:
		tkinter.messagebox.showinfo("Register","Already registered. Choose a different ID")
		register_menu.destroy()

	f2 = open ('Userprofile.txt', 'a')
	pos = f2.tell()
	f3 = open ('index.txt', 'a')
	buf = id + '|' + hash_password(password) + '|' + name + '|' + email + '|' + '#'
	f2.write(buf)
	f2.write('\n')
	buf = id + '|' + str(pos) + '|' + '#'
	f3.write(buf)
	f3.write('\n')
	f3.close()
	f2.close()
	key_sort('index.txt')
	tkinter.messagebox.showinfo("Register","Registration Successful!Please Login again")
	register_menu.destroy()


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def admin_in():
		global id_admin
		global password_admin
		global admin_menu

		admin_menu=Tk()
		admin_menu.wm_title("Admin")
		admin_menu.geometry('250x250')
		admin_menu.resizable(0,0)
		k_font = tkinter.font.Font(family='Times new roman', size=10, weight=tkinter.font.BOLD)

		admin_label=Label(admin_menu,text="Admin ID")
		admin_password_label=Label(admin_menu,text="Password")
		id_admin=Entry(admin_menu)
		password_admin=Entry(admin_menu)
		loginbutton2=Button(admin_menu,command=admin_check,text=" Login ",bg='light blue',height=1,width=7,font=k_font, bd='5')
		password_admin.config(show="*")

		admin_label.grid(row=0,sticky=E, pady = (10,10),padx=(10, 10))
		id_admin.grid(row=0,column=1)
		admin_password_label.grid(row=3,sticky=E, pady = (10,10),padx=(10, 10))
		password_admin.grid(row=3,column=1)
		loginbutton2.grid(row =5, column = 1, pady = (10,10),padx=(10, 10))

		admin_menu.mainloop()

def admin_check():
	global admin_id

	admin_id=id_admin.get()
	admin_password=password_admin.get()

	if admin_id=="admin" and admin_password=="admin":
		tkinter.messagebox.showinfo("Login","Admin Login Successful!")
		admin_menu.destroy()
		login_menu.destroy()
		Admin_Opt()
	else:
		tkinter.messagebox.showinfo("Login","Admin id or password INCORRECT. Please re-enter")

def Admin_Opt():
		global opt_menu

		opt_menu=Tk()
		opt_menu.wm_title("Admin_menu")
		opt_menu.geometry('450x450')
		opt_menu.resizable(0,0)
		k_font = tkinter.font.Font(family='Times new roman', size=13, weight=tkinter.font.BOLD)

		addTeacherbutton=Button(opt_menu,command=add_teacher,text=" Add Teacher ",bg='pink',height=2,width=12,font=k_font)
		delTeacherbutton=Button(opt_menu,command=del_teacher,text=" Remove Teacher ",bg='light blue',height=2,width=12,font=k_font)
		addStudentbutton=Button(opt_menu,command=add_student,text=" Add Student ",bg='light blue',height=2,width=12,font=k_font)
		delStudentbutton=Button(opt_menu,command=del_student,text=" Remove Student ",bg='pink',height=2,width=12,font=k_font)
		backbutton=Button(opt_menu,command=reopen_login,text=" Log out ",bg='red',fg='white',height=2,width=10,font=k_font)

		addTeacherbutton.place(height=50, x=50, y=100)
		delTeacherbutton.place(height=50, x=300, y=100)
		addStudentbutton.place(height=50, x=50, y=160)
		delStudentbutton.place(height=50, x=300, y=160)
		backbutton.place(height=50, x=170, y=220)
		opt_menu.mainloop()

def reopen_login():
	tkinter.messagebox.showinfo("Login","Admin Logout Successful!")
	opt_menu.destroy()

	f7=open('TeacherIndex.txt','r')
	lines1=f7.readlines()
	f7.close()
	f8=open('TeacherIndex.txt','w')
	for line1 in lines1:
		if line1.startswith('*'):
			continue
		else:
			f8.write(line1)
	f8.close()

	login_in()


def key_sort(fname):
	t=list()
	fin=open(fname,'r')
	for line in fin:
		line=line.rstrip('\n')
		words=line.split('|')
		t.append((words[0],words[1]))
	fin.close()
	t.sort()
	with open("temp.txt",'w') as fout:
		for pkey,addr in t:
			pack=pkey+"|"+addr+"|#"
			fout.write(pack+'\n')
	os.remove(fname)
	os.rename("temp.txt",fname)


def binary_search(fname, search_key):
	t = []
	fin = open(fname,'r')
	for lx in fin:
		lx = lx.rstrip()
		wx = lx.split('|')
		t.append((wx[0], wx[1]))
	fin.close()
	l = 0
	r = len(t) - 1
	while l <= r:
		mid = (l + r)//2
		if t[mid][0] == search_key:
			return int(t[mid][1])
		elif t[mid][0] <= search_key:
			l = mid + 1
		else:
			r = mid - 1
	return -1

# add teacher

def add_teacher():
	global teacher_id
	global teacher_name
	global class_name_section
	global add_menu

	add_menu=Tk()
	add_menu.wm_title("Add Teacher")
	add_menu.geometry('450x400')
	add_menu.resizable(0,0)
	k_font = tkinter.font.Font(family='Times new roman', size=15, weight=tkinter.font.BOLD)

	teacher_id_label=Label(add_menu,font=k_font,text="Teacher ID (Should have 5 digits)")
	teacher_name_label=Label(add_menu,font=k_font,text="Teacher Name")
	class_info=Label(add_menu,font=k_font,text="Class")
	teacher_id=Entry(add_menu,width=30)
	teacher_name=Entry(add_menu,width=30)
	class_name_section=Entry(add_menu,width=30)
	addbutton=Button(add_menu,command=add_teacher_check,text=" Add Teacher ",bg='dark orange',height=1,width=12,font=k_font)

	teacher_id_label.grid(row=1,sticky=E)
	teacher_id.grid(row=1,column=1)
	teacher_name_label.grid(row=2,sticky=E)
	teacher_name.grid(row=2,column=1)
	class_info.grid(row=3,sticky=E)
	class_name_section.grid(row=3,column=1)
	addbutton.place(x=140, y=100)

	add_menu.mainloop()

def add_teacher_check():
	global t_id
	t_id=teacher_id.get()
	t_name=teacher_name.get().upper()
	c_id=class_name_section.get()

	if len(t_name)==0:
		tkinter.messagebox.showinfo("Add teacher","You did not type a teacher's name.")
		add_menu.lift()
		return(add_teacher)

	if len(t_id)!=5 or t_id.isdigit()==False:
		tkinter.messagebox.showinfo("Add teacher","Please renter the details(ID should be 5 positive integers)")
		add_menu.lift()
		return(add_teacher)

	if len(c_id) == 0:
		c_id = "No class alloted"

	pos = binary_search('TeacherIndex.txt', t_id)
	if pos != -1:
		tkinter.messagebox.showinfo("Teacher","This teacher exists.Please try again")
		add_menu.lift()
		return(add_teacher)

	f11 = open ('TeacherData.txt', 'a')
	pos = f11.tell()
	f00 = open ('TeacherIndex.txt', 'a')
	buf = t_id + '|' + t_name + '|' + c_id + '|' + '#'
	f11.write(buf)
	f11.write('\n')
	buf = t_id + '|' + str(pos) + '|' + '#'
	f00.write(buf)
	f00.write('\n')
	f00.close()
	f11.close()
	key_sort('TeacherIndex.txt')
	tkinter.messagebox.showinfo("Add Teacher","Teacher added Successfully!")
	add_menu.destroy()

# add student

def add_student():
	global student_id
	global student_name
	global class_name
	global add_details

	add_details=Tk()
	add_details.wm_title("Add Student")
	add_details.geometry('450x400')
	add_details.resizable(0,0)
	k_font = tkinter.font.Font(family='Helvetica', size=15, weight=tkinter.font.BOLD)

	student_id_label=Label(add_details,font=k_font,text="Student ID (Should be 5 digits)")
	student_label=Label(add_details,font=k_font,text="Student Name")
	class_label=Label(add_details,font=k_font,text="Class")
	student_id=Entry(add_details, width=30)
	student_name=Entry(add_details, width=30)
	class_name=Entry(add_details, width=30)
	addbutton1=Button(add_details,command=add_student_check,text=" Add Student ",bg='#0059b3', fg='white', height=1,width=10,font=k_font)

	student_id_label.grid(row=1,sticky=E)
	student_id.grid(row=1,column=1)
	student_label.grid(row=2,sticky=E)
	student_name.grid(row=2,column=1)
	class_label.grid(row=3,sticky=E)
	class_name.grid(row=3,column=1)
	addbutton1.place(x=140, y=100)


	add_details.mainloop()

def add_student_check():
	global s_id
	s_id=student_id.get()
	s_name=student_name.get().upper()
	c_id=class_name.get()

	if len(s_name)==0:
		tkinter.messagebox.showinfo("Add Student","You did not type any student's name ")
		add_details.lift()
		return(add_student)

	if len(s_id)!=5 or s_id.isdigit()==False:
		tkinter.messagebox.showinfo("Add student","Please renter the details(ID should be 5 positive integers)")
		add_details.lift()
		return(add_student)

	if len(c_id) == 0:
		c_id = "No class alloted"

	pos = binary_search('StudentIndex.txt', s_id)
	if pos != -1:
		tkinter.messagebox.showinfo("Add Student","This Student already exists.Please try again")
		add_details.lift()
		return(add_student)

	f11 = open ('StudentData.txt', 'a')
	pos = f11.tell()
	f00 = open ('StudentIndex.txt', 'a')
	buf = s_id + '|' + s_name + '|' + c_id + '|' + '#'
	f11.write(buf)
	f11.write('\n')
	buf = s_id + '|' + str(pos) + '|' + '#'
	f00.write(buf)
	f00.write('\n')
	f00.close()
	f11.close()
	key_sort('StudentIndex.txt')
	tkinter.messagebox.showinfo("Add Student","Student added Successfully!")
	add_details.destroy()

#del teacher
def del_teacher():
	global dt_id
	global del_menu

	del_menu=Tk()
	del_menu.wm_title("Delete")
	del_menu.geometry('800x600')
	del_menu.resizable(0,0)
	k_font = tkinter.font.Font(family='Helvetica', size=12, weight=tkinter.font.BOLD)

	TeacherId=[]
	TeacherName = []
	TeacherClassAndSection = []

	f1 = open('TeacherIndex.txt', 'r')
	f = open ("TeacherData.txt", 'r')
	norecord = 0

	for line in f1:
		if not line.startswith('*'):
			norecord += 1
			line = line.rstrip('\n')
			word = line.split('|')
			f.seek(int(word[1]))
			line1 = f.readline().rstrip()
			word1 = line1.split('|')
			TeacherId.append(word1[0])
			TeacherName.append(word1[1])
			TeacherClassAndSection.append(word1[2])
	f.close()


	teacher_list=Listbox(del_menu,height=50,width=20)
	teacher_list2=Listbox(del_menu,height=50,width=50)
	teacher_list3=Listbox(del_menu,height=50,width=50)

	for num in range(0,norecord):
		teacher_list.insert(0,TeacherId[num])
		teacher_list2.insert(0,TeacherName[num])
		teacher_list3.insert(0,TeacherClassAndSection[num])


	b_label=Label(del_menu,text="Teacher ID",font=k_font)
	dt_id=Entry(del_menu)
	delbutton1=Button(del_menu,command=del_teacher_check,text=" Remove Teacher ",bg='red',height=1,width=13,font=k_font)
	teacher_list2.configure(background="pink")
	teacher_list3.configure(background="pink")
	teacher_list.configure(background="light grey")

	teacher_label=Label(del_menu,font=k_font,text="Id")
	teacher_label2=Label(del_menu,font=k_font,text="Name")
	teacher_label3=Label(del_menu,font=k_font,text="Class and Section")

	teacher_label.grid(row=7,column=0,pady=20)
	teacher_label2.grid(row=7,column=1,pady=20)
	teacher_label3.grid(row=7,column=3,pady=20)

	teacher_list.grid(row=8,column=0)
	teacher_list2.grid(row=8,column=1)
	teacher_list3.grid(row=8,column=3)

	b_label.grid(row=0,sticky=E)
	dt_id.grid(row=0,column=1)
	delbutton1.place(x=360)

	del_menu.mainloop()

def del_teacher_check():

	global del_id
	del_id=dt_id.get()

	if len(del_id)==0:
		tkinter.messagebox.showinfo("Delete Teacher","You did not type anything O_O")
		del_menu.lift()
		return(del_teacher)

	pos = binary_search('TeacherIndex.txt', del_id)
	if(pos == -1):
		tkinter.messagebox.showinfo("Delete","Teacher not found.Please re-enter")
		del_menu.destroy()
		return(del_teacher)

	index = -1

	with open('TeacherIndex.txt','r') as file:
		for line in file:
			words=line.split("|")
			if(words[0]==del_id):
				index=int(words[1])

	index=0
	with open("TeacherIndex.txt",'r+') as file:
		line=file.readline()
		while line:
			words=line.split("|")
			if words[0]==del_id:
				file.seek(index,0)
				file.write("*")
				break
			else:
				index=file.tell()
				line=file.readline()
	tkinter.messagebox.showinfo("Delete","Teacher is removed from the list successfully ")
	del_menu.destroy()

#del student
def del_student():
	global ds_id
	global del_item

	del_item=Tk()
	del_item.wm_title("Delete Student")
	del_item.geometry('800x600')
	del_item.resizable(0,0)
	k_font = tkinter.font.Font(family='Helvetica', size=12, weight=tkinter.font.BOLD)

	StId=[]
	StName = []
	StClass = []

	# f3 = open('StudentIndex.txt', 'r')
	# f2 = open ("StudentData.txt", 'r')
	# norecord = 0
	# for line0 in f3:
	# 	if not line0.startswith('*'):
	# 		norecord += 1
	# 		line0 = line0.rstrip('\n')
	# 		word0 = line0.split('|')
	# 		f2.seek(int(word0[1]))
	# 		line2 = f2.readline().rstrip()
	# 		word2 = line2.split('|')
	# 		Id.append(word2[0])
	# 		Name.append(word2[1])
	# 		Class_Section.append(word2[2])

	# f2.close()

	f2 = open('StudentIndex.txt', 'r')
	f3 = open ("StudentData.txt", 'r')
	norecords = 0
	for lin in f2:
		norecords += 1
		lin = lin.rstrip('\n')
		words = lin.split('|')
		f3.seek(int(words[1]))
		line0 = f3.readline().rstrip()
		word0 = line0.split('|')
		StId.append(word0[0])
		StName.append(word0[1])
		StClass.append(word0[2])

	f3.close()

	student_list=Listbox(del_item,height=50,width=20)
	student_list2=Listbox(del_item,height=50,width=50)
	student_list3=Listbox(del_item,height=50,width=50)

	for num in range(0,norecords):
		student_list.insert(0,StId[num])
		student_list2.insert(0,StName[num])
		student_list3.insert(0,StClass[num])


	s_label=Label(del_item,text="Student ID",font=k_font)
	ds_id=Entry(del_item)
	delbutton2=Button(del_item,command=del_check,text=" Remove Student ",bg='black', fg='white', height=1,width=13,font=k_font)
	student_list2.configure(background="bisque")
	student_list3.configure(background="bisque")
	student_list.configure(background="light grey")

	student_label=Label(del_item,font=k_font,text="Id")
	student_label2=Label(del_item,font=k_font,text="Student Name")
	student_label3=Label(del_item,font=k_font,text="Class and Section")


	student_label.grid(row=7,column=0,pady=(20,10))
	student_label2.grid(row=7,column=1,pady=(20,10))
	student_label3.grid(row=7,column=3,pady=(20,10))

	student_list.grid(row=8,column=0)
	student_list2.grid(row=8,column=1)
	student_list3.grid(row=8,column=3)

	s_label.grid(row=0,sticky=E)
	ds_id.grid(row=0,column=1)
	delbutton2.place(x=360)

	del_item.mainloop()

def del_check():

	global del_id
	del_id=ds_id.get()

	if len(del_id)==0:
		tkinter.messagebox.showinfo("Delete Student","You did not type anything ;)")
		del_item.lift()
		return(del_student)

	pos = binary_search('StudentIndex.txt', del_id)
	if(pos == -1):
		tkinter.messagebox.showinfo("Delete","Student not present.Please reenter:-)")
		del_item.destroy()
		return(del_student)

	index = -1

	with open('StudentIndex.txt','r') as file:
		for line in file:
			words=line.split("|")
			if(words[0]==del_id):
					index=int(words[1])

	index=0
	with open("StudentIndex.txt",'r+') as file:
		line=file.readline()
		while line:
			words=line.split("|")
			if words[0]==del_id:
				file.seek(index,0)
				file.write("*")
				break
			else:
				index=file.tell()
				line=file.readline()
	tkinter.messagebox.showinfo("Delete","Student Successfully removed from the list")
	del_item.destroy()

#------------------------------------------------------

def Main_Menu():
	global base
	base = Tk()
	#Window title and size optimization
	base.wm_title("SCHOOL FOR LEARNING")
	base.geometry('1000x650')

	in_font = tkinter.font.Font(family='Lucida Calligraphy', size=15, weight=tkinter.font.BOLD)
	current_time1=datetime.datetime.now()
	current_time=str(current_time1)

	#Bunch of labels
	status = Label(base,text=("Date and time logged in: " + current_time),bd=1,relief=SUNKEN,anchor=W,bg='light pink')
	orionLabel=Label(base, text="GYAAN MANDIR",bg='dark orange',font=("Castellar", "50","bold","italic","underline"),fg="black")
	backbutton=Button(base,command=student_logout,text=" Log out ",bg='black',fg='white',height=2,width=10,font=in_font)
	welcomeLabel=Label(base,text=("Welcome "+id+"!"),font=("Freestyle Script","50","bold"))
	img = ImageTk.PhotoImage(Image.open('myschool.jpg').resize((550,290)))
	topFrame=Frame(base)
	bottomFrame=Frame(base)

	#Positioning of labels
	status.pack(side=BOTTOM,fill=X)
	orionLabel.pack(fill=X)
	backbutton.place(height=35,width=100,x=880, y=20)
	welcomeLabel.pack()
	Label(base, image=img).pack()
	topFrame.pack()
	bottomFrame.pack(side=BOTTOM)

	#Buttons
	view1=Button(bottomFrame,bg="black",fg="white",text="View Teachers",font=in_font,height=5,width=15,command=view_teacher)
	view2=Button(bottomFrame,bg="dark orange",text="View Students",font=in_font,height=5,width=15,command=view_student)
	search_butn1=Button(bottomFrame,bg="grey",fg="white",text="Search for a teacher",font=in_font,height=2,width=16,command=search_teacher)
	search_butn2=Button(bottomFrame,bg="dark orange",fg="white",text="Search for a student",font=in_font,height=2,width=16,command=search_student)	
	feedback_butn=Button(bottomFrame,bg="black",fg="white",text="Feedback",font=in_font,height=5,width=15,command=feedback_in)

	#Positioning of buttons
	view1.pack(side=LEFT)
	view2.pack(side=LEFT)
	feedback_butn.pack(side=LEFT)
	search_butn1.pack(side=TOP)
	search_butn2.pack(side=BOTTOM)
	base.mainloop()

def student_logout():
	tkinter.messagebox.showinfo("Login","User Logout Successful!")
	base.destroy()

	f7=open('TeacherIndex.txt','r')
	lines1=f7.readlines()
	f7.close()
	f8=open('TeacherIndex.txt','w')
	for line1 in lines1:
		if line1.startswith('*'):
			continue
		else:
			f8.write(line1)
	f8.close()

	login_in()

def view_teacher():
	# global borrow_entry1
	global teacher_menu

	teacher_menu=Tk()

	teacher_menu.wm_title("View Teachers")
	teacher_menu.minsize(900,550)
	teacher_menu.maxsize(1200,550)
	teacher_menu.resizable(0,0)

	Id=[]
	Tname = []
	TClass = []

	f1 = open('TeacherIndex.txt', 'r')
	f = open ("TeacherData.txt", 'r')
	norecord = 0
	for line in f1:
		norecord += 1
		line = line.rstrip('\n')
		word = line.split('|')
		f.seek(int(word[1]))
		line1 = f.readline().rstrip()
		word1 = line1.split('|')
		Id.append(word1[0])
		Tname.append(word1[1])
		TClass.append(word1[2])

	f.close()
	t_list=Listbox(teacher_menu,height=50,width=20)
	t_list1=Listbox(teacher_menu,height=50,width=50)
	t_list2=Listbox(teacher_menu,height=50,width=50)

	for num in range(0,norecord):
		t_list.insert(0,Id[num])
		t_list1.insert(0,Tname[num])
		t_list2.insert(0,TClass[num])

	t_list.configure(background="light grey")
	t_list1.configure(background="pink")
	t_list2.configure(background="pink")
	t_label=Label(teacher_menu,text="Id")
	t_label2=Label(teacher_menu,text="Teacher Name")
	t_label3=Label(teacher_menu,text="Class")

	t_label.grid(row=3,column=0)
	t_label2.grid(row=3,column=1)
	t_label3.grid(row=3,column=4)

	t_list.grid(row=4,column=0)
	t_list1.grid(row=4,column=1)
	t_list2.grid(row=4,column=4)

	teacher_menu.mainloop()

def view_student():
	# global borrow_entry1
	global student_menu

	student_menu=Tk()

	student_menu.wm_title("View students")
	student_menu.minsize(900,550)
	student_menu.maxsize(1200,550)
	student_menu.resizable(0,0)

	StId=[]
	Stname = []
	StClass = []

	f2 = open('StudentIndex.txt', 'r')
	f3 = open ("StudentData.txt", 'r')
	norecords = 0
	for lin in f2:
		norecords += 1
		lin = lin.rstrip('\n')
		words = lin.split('|')
		f3.seek(int(words[1]))
		line0 = f3.readline().rstrip()
		word0 = line0.split('|')
		StId.append(word0[0])
		Stname.append(word0[1])
		StClass.append(word0[2])

	f3.close()
	s_list=Listbox(student_menu,height=50,width=20)
	s_list1=Listbox(student_menu,height=50,width=50)
	s_list2=Listbox(student_menu,height=50,width=50)

	for num in range(0,norecords):
		s_list.insert(0,StId[num])
		s_list1.insert(0,Stname[num])
		s_list2.insert(0,StClass[num])

	s_list.configure(background="light grey")
	s_list1.configure(background="pink")
	s_list2.configure(background="pink")
	s_label=Label(student_menu,text="Id")
	s_label2=Label(student_menu,text="Student's Name")
	s_label3=Label(student_menu,text="Class")

	s_label.grid(row=3,column=0)
	s_label2.grid(row=3,column=1)
	s_label3.grid(row=3,column=4)

	s_list.grid(row=4,column=0)
	s_list1.grid(row=4,column=1)
	s_list2.grid(row=4,column=4)

	student_menu.mainloop()


#teacher search
def search_teacher():
	global search_teacher_entry
	global search_menu
	search_menu=Tk()
	search_menu.geometry('400x400')
	search_menu.wm_title("Search Teacher")
	search_menu.resizable(0,0)

	#search teacher
	search_label1=Label(search_menu,text="To search a teacher, please enter his or her ID",font=("Times", "12","bold","italic"),bg="light blue")
	search_label1.pack(side=TOP)

	search_teacher_entry = Entry(search_menu,width=20)
	search_teacher_entry.pack(side=TOP)

	search_button1=Button(search_menu,text="Search",command=teacher_check,font=("Times new roman","12","bold"),bg="magenta")
	search_button1.pack(side=TOP)

	search_menu.mainloop()

#student search
def search_student():
	global search_student_entry
	global search_list
	search_list=Tk()
	search_list.geometry('400x400')
	search_list.wm_title("Search Student")
	search_list.resizable(0,0)

	#search student
	search_label1=Label(search_list,text="To search a student, please enter his or her ID ",font=("Times", "12","bold","italic"),bg="light blue")
	search_label1.pack(side=TOP, fill=Y)

	search_student_entry = Entry(search_list,width=20)
	search_student_entry.pack(side=TOP, fill=Y)

	search_button2=Button(search_list,text="Search",command=student_check,font=("Times new roman","12","bold"),bg="blue", fg="white")
	search_button2.pack(side=TOP, fill=Y)

	search_list.mainloop()

#teacher check
def teacher_check():
	search_word=search_teacher_entry.get().upper()
	search_menu.destroy()

	if len(search_word) == 0:
		tkinter.messagebox.showinfo("Search","You did not search anything O_O")
		return(search_teacher)

	pos = binary_search('TeacherIndex.txt', search_word)

	if (pos == -1):
		tkinter.messagebox.showinfo("Search","Sorry,this person does not exist in our school")
	else:
		search_menu1=Tk()
		search_menu1.wm_title("Search")
		search_menu1.attributes("-topmost",True)
		tkinter.messagebox.showinfo("Search","Person Found!")

		search_result1=Listbox(search_menu1,height=10,width=50)
		f2 = open('TeacherData.txt', 'r')
		f2.seek(pos)
		l1 = f2.readline()
		l1 = l1.rstrip()
		w1 = l1.split('|')
		t_id = w1[0]
		t_name = w1[1]
		class_name= w1[2]
		f2.close()

		search_result1.insert(1,"ID:" + t_id)
		search_result1.insert(2,"Teacher's Name:" + t_name)
		search_result1.insert(3,"Class:" + class_name)

		search_result1.pack()
		search_menu1.mainloop()

#student check
def student_check():
	search_keyword=search_student_entry.get().upper()
	search_list.destroy()

	if len(search_keyword) == 0:
		tkinter.messagebox.showinfo("Search","You did not search anything O_O")
		return(search_student)

	pos = binary_search('StudentIndex.txt', search_keyword)

	if (pos == -1):
		tkinter.messagebox.showinfo("Search","Sorry,this person does not exist in our school")
	else:
		search_list2=Tk()
		search_list2.wm_title("Search")
		search_list2.attributes("-topmost",True)
		tkinter.messagebox.showinfo("Search","Person found!")

		search_result=Listbox(search_list2,height=10,width=50)
		f2 = open('StudentData.txt', 'r')
		f2.seek(pos)
		l1 = f2.readline()
		l1 = l1.rstrip()
		w1 = l1.split('|')
		s_id = w1[0]
		s_name = w1[1]
		class_details = w1[2]
		f2.close()

		search_result.insert(1,"ID:" + s_id)
		search_result.insert(2,"Student's Name:" + s_name)
		search_result.insert(3,"Class:" + class_details)

		search_result.pack()
		search_list2.mainloop()


def feedback_in():
	global feedback_bar
	global feedback_menu
	global feedback_input

	feedback_menu=Tk()
	feedback_menu.wm_title("Feedback")
	feedback_menu.geometry('450x400')
	feedback_menu.resizable(0,0)

	feedback_bar=Entry(feedback_menu,width=40)
	feedback_label=Label(feedback_menu,text= "We improve from your valuable feedback.Thank you!",font=("Roboto","13","italic"),bg="light blue", width=40)
	button1=Button(feedback_menu, text="Submit feedback",command=feedback_check,font=("Times new roman","10","bold"),bg="dark orange")

	feedback_bar.place(x=100,y=30)
	feedback_label.place(x=20,y=60 )
	button1.place(x=170, y=100)
	feedback_menu.mainloop()

def feedback_check():
	user_feedback=feedback_bar.get()
	if len(feedback_bar.get())==0:
		tkinter.messagebox.showinfo("Feedback","You did not type anything O_O")
		feedback_menu.lift()
		return(feedback_in)
	else:
		tkinter.messagebox.showinfo("Feedback","Thank you for your valuable feedback! >_<")
		file = open('Feedback.txt', 'a')
		file.write(user_feedback + "\n")
		file.close()
		feedback_menu.destroy()


def feedback_read():
	read_feedback_menu=Tk()
	read_feedback_menu.geometry('400x400')
	read_feedback_menu.resizable(0,0)
	read_feedback_menu.wm_title("Users' feedback")

	list=Listbox(read_feedback_menu)
	file = open('Feedback.txt' , 'r')
	num_feedback = len(file.readlines())
	file.close()
	file = open('Feedback.txt' , 'r')
	count = 1
	feedback = file.readlines()
	for i in range(0, num_feedback):
		list_feedback =str(count) + ('.') + (feedback[count - 1])
		list.insert(count,list_feedback)
		count += 1
	file.close()

	list.pack(side=TOP,fill=X,expand=1)
	read_feedback_menu.mainloop()

login_in()
