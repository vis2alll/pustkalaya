# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 11:33:05 2017

@author: DELL
"""


#=========================        req module install & import          =========================#


#req_modules=["Tkinter",'datetime','time','tkMessageBox','pyserial',
#                         'thread','ttk','platform',"PIL",'Image',"sys","os"]
#plt_modules=["numpy","matplotlib","scipy"]


req_modules=["requests"]
#req_modules.extend(plt_modules)



def install_and_import(package):
    
    import importlib
    global manually,proxy
    _import=True
    
    
    
    try:
        if package=='pyserial':
            importlib.import_module("serial")
        else:
            importlib.import_module(package)
#        print 'import ',package
    except ImportError: 
        print 'import ERROR:  ',package
 
        manually.append(package)
        print "       installing "+str(package)+"..."
    
      
        import pip
        try:
            pip.main(['install', package])
#            pip.main(['install', "--retries=1",package])
#            pip.main(['uninstall', 'leancloud'])
            if package=='pyserial':
                importlib.import_module("serial")
            else:
                importlib.import_module(package)

            
        except ImportError:
            response=["y","n"]
                
            if proxy==None:
                is_proxy=str(raw_input("Are you running Internet behind a proxy (y/n)? : "))
                
                while 1:
                    if not is_proxy in response:
                        print "Your response "+str((is_proxy))+" was not one of the expected responses: (y , n) "
                        is_proxy=str(raw_input("Are you running Internet behind a proxy (y/n)? : "))
                    else:
                        break
                        
                    
                if  is_proxy=="y" :
                    proxy=str(raw_input("Enter proxy_IP & proxy_Port  ex: 10.10.78.21:3128 : "))
                    pip.main(['install','--proxy='+proxy, package])
 
            #=====================================#    
import sys,os,importlib

manually=[]
proxy=None

print "      ----installing Packages...   "

for package in req_modules:
#    try:
    if package=="Image":
        try:
            from PIL import Image,ImageTk
        except ImportError:
            install_and_import(package) 
            
    else:    
        install_and_import(package)
#    except Exception as e:
#         exc_type, exc_obj, exc_tb = sys.exc_info()
#         fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#         print(exc_type, fname, exc_tb.tb_lineno)




        try:
            if package=="pyserial":
                package=="serial"
                
            globals()[package] = importlib.import_module(package)
            print 'import ',package
        except ImportError:
            pass
#        manually.append(package)





if not manually==[]: 
    
    if 'pyserial' in manually:
        try:
            import serial
            manually.remove("pyserial")
        except ImportError:   
            pass
        
    if 'PIL' in manually:
        try:
            from PIL import Image,ImageTk
            
            manually.remove("PIL")
            manually.remove("Image")
        except ImportError:   
            pass

    if manually==[]:    
        print "_______________________________"
        print "Packages not installed yet:"+str(manually)
        print  "Try to install them manually. "
    else:
        print "All Packages imported successfully. "
else:
    print "All Packages imported successfully. "
#================================   installation finished   =========================================#


#================================   GUI Part   ==========================================#


import Tkinter as t
import Tkinter as tk
from Tkinter import *
import time
import datetime
import tkMessageBox
import serial
import serial.tools.list_ports
import Cell_Pin
#from Cell_Pin import Port,ser
import ttk
import thread
from time import gmtime, strftime
import os,csv,sys
from PIL import Image
from PIL import ImageTk
import platform

#===============  plot  ================#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches
import scipy.interpolate as interpolate
from tool_tip import CreateToolTip
#========================================


total_cell=10
no_pin=8
host_addr=0
cell_no=0
Data=0
packet=[]
cycle=None
test_flag=None
HOST_Version = 21

root=t.Tk()

root_color='slategray'
w = root.winfo_screenwidth()#int(round(h*.90)
h = root.winfo_screenheight()
root.geometry(("%dx%d+%d+%d" %( w ,int(round(h*.90)) ,0,0)))  ## set location dyanamic
root.minsize(width=200,height=100)
root.configure(background = root_color)
root.title("RBD Debugging Tool - v" + str(HOST_Version-15))
#root.state('zoomed')
#=============================== for scrollbars=======================================#

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

#============

f0=t.Frame(root, bg="lightskyblue4",relief=t.RIDGE,bd=1 ,highlightthickness=2,pady=2)
f0.pack(side=TOP, expand = 1,fill=BOTH)

f1=t.Frame(root, bg="grey92",relief=t.RIDGE ,padx=1,pady=8)
f1.pack(side=TOP, expand = 1,fill=X)

canvas1=f1
#canvas2= tk.Canvas(f1 , background="grey92" )
#canvas2.pack(side="top", fill="both", expand=True )


f4=t.Frame(root, bg="grey23",relief=t.RIDGE,bd=1,  height=200 ,highlightthickness=1,pady=1, borderwidth=1)
f4.pack(side=BOTTOM, expand = 1,fill=X) #bg="grey23"
f4.propagate(1)

#====================main central frame=====================#


f2=t.Frame(root, bg="grey23",relief=t.RIDGE,bd=1,  height=400 ,highlightthickness=0,pady=1, borderwidth=2)
f2.pack(side=BOTTOM, expand = 1,fill=BOTH)
f2.propagate(0)

#notebook = ttk.Notebook(f2)
#nf1 = ttk.Frame(notebook)
#nf2 = ttk.Frame(notebook)
#notebook.add(nf1, text='Mode One')
#notebook.add(nf2, text='Mode Two')
#notebook.pack(side=TOP,expand = 1,fill=BOTH)

canvas3= tk.Canvas(f2, borderwidth=1, background="grey90" ,bd=2)
canvas3.pack(side="top", fill="both", expand=True)
 
f3=t.Frame(canvas3, bg="#e0ebeb",relief=t.RIDGE,bd=1,   height=400 ,highlightthickness=0,pady=1)
f3.pack(side=BOTTOM, expand = 1,fill=BOTH)      #checkbutton winow
f3.propagate(0)
#============================ ttk_notebook ==================#



##=================   background Image   =====================##
background_image=ImageTk.PhotoImage(file= "b8.png") #a1,b8,b10,b12,b15,b16,b17
background_label = tk.Label(f3, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1) 

f3.pack_propagate(0)  

     
#======================== frame to hold function buttons =======================#

fn_btns_frame=tk.Frame(f3, bg="grey45",relief=t.RIDGE,bd=1 ,highlightthickness=1,padx=2,pady=1,borderwidth=1)       
fn_btns_frame.pack(side=BOTTOM , anchor="s", expand = 1,fill=None,pady=40)

#ttk.Separator(f3,orient=HORIZONTAL).pack(side="top",fill=X,pady=25)

##====================   func_button_image  ========###
def button_image(b,img):
    image = ImageTk.PhotoImage(file=img)
    b.config(image=image)
    b.image = image
 
##===================================Toolbar(Menubar)=================#
#def donothing():
#   filewin = Toplevel(root)
#   button = Button(filewin, text="Do nothing button")
#   button.pack()
#   
#def openfile():
#   path=os.getcwd()
#   os.startfile(str(path))
#menubar = Menu(root,fg='red')
#
#filemenu = Menu(menubar, tearoff=0)
#filemenu.add_command(label="New", command=donothing)
#filemenu.add_command(label="Open", command=openfile)
#filemenu.add_command(label="Save", command=donothing)
#filemenu.add_command(label="Save as...", command=donothing)
#filemenu.add_command(label="Close", command=donothing)
#
#filemenu.add_separator()
#
#filemenu.add_command(label="Exit", command=root.quit)
#menubar.add_cascade(label="File", menu=filemenu)
#
#csvmenu = Menu(menubar, tearoff=0)
#csvmenu.add_command(label="Slave_wise", command=donothing)
#
#csvmenu.add_separator()
#
#csvmenu.add_command(label="Row_wise", command=donothing)
# 
#
#menubar.add_cascade(label="csv", menu=csvmenu)
#
#helpmenu = Menu(menubar, tearoff=0)
#helpmenu.add_command(label="Help Index", command=donothing)
#helpmenu.add_command(label="About...", command=donothing)
#menubar.add_cascade(label="Help", menu=helpmenu)
#
#root.config(menu=menubar)
#=============================================func to Get  =====================================================#

def GetHostAdress(event=None):
    
    try:
        host_addr=Host.get()
    except ValueError:
         tkMessageBox.showwarning("WARNING", "    Enter Proper Host Address !    ")
         return
    
       #tkMessageBox.font=('arial',28,'bold')
    tkMessageBox.showinfo("OK", " Entered "+'Host Address is '+str(host_addr))
    return



def GetData(event=None):
    
    try:
        Data=datac.get()
    except ValueError:
         tkMessageBox.showwarning("WARNING", "    Enter Proper Data  ! . Data must be in range (0,255)   ")
         return
    
       #tkMessageBox.font=('arial',28,'bold')
    if not Data in range(0,256):
        tkMessageBox.showwarning("Err", " Data must be in range (0,255)")
        return
    #tkMessageBox.showinfo("OK", " Entered "+'Data  is '+str(Data))
    return Data
 
    
    
def GetCellNo(event=None):
    
    try:
        cell_no=cell.get()
    except ValueError:
         tkMessageBox.showwarning("WARNING", "    Enter Proper Cell no  !. must be integer in range (1,10)    ")
         return
    if not cell_no in range(1,11):
        tkMessageBox.showwarning("Err", " Cell_no must be in range (1,10)")
        return
       #tkMessageBox.font=('arial',28,'bold')
    #tkMessageBox.showinfo("OK", " Entered "+'Cell no  is '+str(cell_no))
    Data=GetData()
    main_func(Data,cell_no)
    

    #for widget in f2.winfo_children():
       # widget.destroy()
     


#=============================================func to Main=====================================================#
def main_func(Data,cell_no):
    global ser,Port
    try: ##change\remove 
      ser=serial.Serial(Port.get(), 115200)
      #print('Seial_Port_was_already_closed')
      #ser.close()  
    except serial.SerialException: 
     
       tkMessageBox.showwarning("WARNING", "   Port "+Port.get()+"  not Available!  or Busy!           ")
       if ser.isOpen():
           ser.close()
       return    
    try:
       host_addr=Host.get()
       if  abs(host_addr) not in range(0,256):
           tkMessageBox.showinfo("WARNING", "Please Enter Proper Host address. Host address must be in range(0, 256) ")
           ser.close()
           return
       else:
           if ser.isOpen():
               Cell_Pin.send_data (ser,host_addr,Cell_Pin.ACC_CMD,cell_no,Data)
               ser.close()

    except ValueError:
       tkMessageBox.showwarning("WARNING", "     Enter Host Address First !     ")
       ser.close()
       return
    
    




#=================================Label and Entry Widgets on f0============================================#

#==========Module_ID========##
M_id=t.StringVar()


lblM_id= t.Label(f0,font=('arial',10,'bold'),text="Module_ID",bd=2,anchor="w" ,relief=t.RIDGE,highlightthickness=1)
lblM_id.pack(side=LEFT, expand = 1,fill=None,ipadx=2)

txtM_id= t.Entry(f0,font=('arial',9,'bold'),textvariable=M_id,bd=4,insertwidth=3,bg="gray99",justify='left')
txtM_id.pack(side=LEFT, expand = 1,fill=None)


#==========version===========#

#ttk.Separator(f0,orient=HORIZONTAL).pack(side=LEFT, expand = 1,fill=Y,ipadx=11)

lbl_Vstatus= t.Label(f0,font=('arial',8,'bold'),text="         ",bd=3 ,width=7,anchor="w",pady=2,relief=t.SUNKEN,justify='center')
lbl_Vstatus.pack(side=RIGHT, expand = 1,fill=None,ipadx=1)

lbl_version= t.Label(f0,font=('arial',9,'bold'),text="Version",highlightthickness=1,bd=3,anchor="w" ,relief=t.RIDGE)
lbl_version.pack(side=RIGHT, expand = 1,fill=None,ipadx=1)





#==================================HOST_ADDR=================================##

Host=t.IntVar()
txtHost= t.Entry(f0,font=('arial',9,'bold'),textvariable=Host,bd=3,width=3,insertwidth=3,bg="gray99",justify='center')
txtHost.pack(side=RIGHT, expand = 1,fill=X,padx=1)

lblHost= t.Label(f0,font=('arial',9,'bold'),text="Host",bd=2,anchor="w" ,highlightthickness=1,relief=t.RIDGE)
lblHost.pack(side=RIGHT, expand = 1,fill=None)
lblHost_ttp = CreateToolTip(lblHost, " Host Addres ")

#txtHost.focus_set()

#btnHost=t.Button(f0,font=('arial',8,'bold'),text="ENTER",fg="Black",bd=8,width=8,command=GetHostAdress,pady=2).pack(side=LEFT, expand = 1,fill=X)
#txtHost.bind('<Return>', GetHostAdress)

##------------------------------------Test Status ----------------------------#

lbl_status= t.Label(f3,font=('arial',8,'bold'),text="         ",bd=3 ,width=7,anchor="nw",pady=3,relief=t.SUNKEN,justify='center')
lbl_status.pack(side="right")

lbl_Test= t.Label(f3,font=('arial',8,'bold'),text="Status", width=7,anchor="center",pady=4,
                  highlightthickness=1,relief=t.RIDGE,justify='center')
lbl_Test.pack(side="right")

lbl_Test_ttp = CreateToolTip(lbl_Test, "Test Result status")


ttk.Separator(f3,orient=HORIZONTAL).place(x=0,y=30, relwidth=1)

#=================================cycles_widgets============================================#

cycle_var=t.IntVar(value=1)

txtcycles= t.Entry(f3,font=('arial',8,'bold'),exportselection=0,textvariable=cycle_var,bd=4,width=15,insertwidth=3 ,bg="lightskyblue2",justify='center')
txtcycles.pack(side="right")

lbl_cycles= t.Label(f3,font=('arial',8,'bold'),text="Cycles", width=7,anchor="center",pady=3,
                    highlightthickness=1,relief=t.RIDGE,justify='center')
lbl_cycles.pack(side="right") 



#=============================================combobox to save_as option  =====================================================#

save_as_list=['Slaves matrix','Single Row']

save_var=StringVar()
cbo_save= ttk.Combobox( f3)

cbo_save.config(values=save_as_list,textvariable=save_var,font=('flat',9,),width=16)#,background="lightskyblue"
try:
   cbo_save.set(save_as_list[0])
except:
    pass
#cbo.place( x=100,y=1 ) 
cbo_save.pack(side="right")
#cbo.pack( expand=1,fill=X ) 
cbo_save.config(state='readonly')

lbl_save_as= t.Label(f3,font=('arial',8,'bold'),text="Save as..",bd=2,bg='grey96',
                     highlightthickness=1,anchor="nw",relief=t.RIDGE)
lbl_save_as.pack(side="right",ipady=1)


#=============================================combobox to pattern option  =====================================================#

pat_list=['Pattern','Custom']

pat_var=StringVar()
cbo_pat= ttk.Combobox( f3)

cbo_pat.config(values=pat_list,textvariable=pat_var,font=('flat',9,),width=16, )
try:
   cbo_pat.set(pat_list[1])
except:
    pass
cbo_pat.pack(side="right")
cbo_pat.config(state='readonly')

#======================label_TEST=====================#
lbl_test_pat= t.Label(f3,font=('arial',8,'bold'),text=" Pattern ",bd=2,bg='grey96',
                     highlightthickness=1,anchor="nw",relief=t.RIDGE)
lbl_test_pat.pack(side="right",ipady=1)
lbl_test_pat_ttp = CreateToolTip(lbl_test_pat, " Test Patterns ")




#=============================================scanning combobox as a function to Get port and ser=====================================================#
ser=None

com_ports=list(serial.tools.list_ports.comports())
#print com_ports
cbo = ttk.Combobox( f0)

def scan_ports():
    global ser,Port,cbo
    port_list=[]
    com_ports=list(serial.tools.list_ports.comports())
    #____For windows8____#
#    print com_ports
    for e in com_ports:
#        print e, "   :    " ,e.device
        port_list.append(e[0])
        
    ##____new-method_____#
    #
    #
    #try:
    #    #______NEW-METHOD_______#
    #    for item in com_ports:
    #        port_list.append(item.device)
    #except:
    ##____old-method_____#
    #    
    #    port_list=list(serial.tools.list_ports.comports())
    #    for i in range(0,len(port_list)):
    #        for j in range(0,len(str(port_list[i]))):
    #            if (str(port_list[i]))[j]=='-':
    #                port_list[i]=str(port_list[i])[0:j-1]
    #                print port_list[i]
    #                break
    
       
    
    Port =StringVar()
#    cbo = ttk.Combobox( f0)
    
    cbo.config(values=port_list,textvariable=Port,font=('flat',9,),width=20, )
    try:
       cbo.set(port_list[-1])
    except:
#        print "exception : no port detected"
        pass
    #cbo.place( x=100,y=1 ) 
    cbo.pack(side='right',expand=True,fill=None)
    #cbo.pack( expand=1,fill=X ) 

scan_ports()


##=============================================combobox to Get port and ser=====================================================#
#ser=None
#port_list=[]
#com_ports=list(serial.tools.list_ports.comports())
##____For windows8____#
##print com_ports
#for e in com_ports:
##    print e,e.device
#    port_list.append(e[0])
#    
###____new-method_____#
##
##
##try:
##    #______NEW-METHOD_______#
##    for item in com_ports:
##        port_list.append(item.device)
##except:
###____old-method_____#
##    
##    port_list=list(serial.tools.list_ports.comports())
##    for i in range(0,len(port_list)):
##        for j in range(0,len(str(port_list[i]))):
##            if (str(port_list[i]))[j]=='-':
##                port_list[i]=str(port_list[i])[0:j-1]
##                print port_list[i]
##                break
#
#   
#
#Port =StringVar()
#cbo = ttk.Combobox( f0)
#
#cbo.config(values=port_list,textvariable=Port,font=('flat',9,),width=20, )
#try:
#   cbo.set(port_list[-1])
#except:
#    pass
##cbo.place( x=100,y=1 ) 
#cbo.pack(side='right',expand=True,fill=None)
##cbo.pack( expand=1,fill=X ) 
#################################


fill='                      '
lbl_fill= t.Label(f0 ,text=fill*4, bg='lightskyblue4',anchor="nw",pady=6,relief=t.FLAT)
lbl_fill.pack(side='left',expand=True ,fill=None)
 

lbl_channel= t.Label(f0,font=('arial',10,'bold'),text="Channel",bd=2,bg='grey99',anchor="nw",
                     highlightthickness=1,relief=t.RIDGE)
lbl_channel.pack(side='right', expand=True )

##############################
#ser=None
#
#port_list=None
# 
#
#Port =StringVar()
#
#def scan_port():
#    global Port,port_list,cbo
#    time.sleep(.4)
#    port_list=list(serial.tools.list_ports.comports())
#    for i in range(0,len(port_list)):
#      for j in range(0,len(str(port_list[i]))):
#        if (str(port_list[i]))[j]=='-':
#            port_list[i]=str(port_list[i])[0:j-1]
##            print port_list[i]
#            break
#    cbo.config(values=port_list,textvariable=Port,font=('flat',9,),width=25  )     
#
#    time.sleep(.4)
#    scan_port()
#    
#cbo = ttk.Combobox( f0)
#cbo.config(values=port_list,textvariable=Port,font=('flat',10,),width=25 )    
#cbo.pack(side='right',expand=True,fill=None)
#
#thread.start_new_thread(scan_port, ())

#=========================================Time_Stamp========================================#


showDate = strftime("%Y-%m-%d %H:%M:%S", time.localtime() )
lblDate_show= t.Label(f0,font=('arial',10,'bold'),text='Date&time:   '+showDate[0:10]+'  '+showDate[10:16],fg="white" ,bg='lightskyblue4')#bg=root color
lblDate_show.pack(side="bottom",anchor='w',padx=2,fill=X)

def show_time():
    global showDate
    showDate = strftime("%Y-%m-%d %H:%M:%S", time.localtime() )
    lblDate_show.config(text='   '+showDate[0:10]+'  '+showDate[10:])
    root.after(1000,show_time)
thread.start_new_thread(show_time, ())
##=============================fill_space================##

fill='                            '
lbl_fill= t.Label(f0 ,text=fill*4, bg='lightskyblue4',anchor="nw",pady=6,relief=t.FLAT)
lbl_fill.pack(side='left',expand=True ,fill=X)
 

#lbl_ch= t.Label(f0,font=('arial',10,'bold'),text="Channel",bd=3,bg='grey99',anchor="nw",relief=t.FLAT)
#lbl_ch.pack(side='right',expand=True )


#=================================Label and Entry Widgets on f1============================================#   

cell=t.IntVar(value=1)

 

lblCell= t.Label(canvas1,font=('arial',10,'bold'),text="Cell No:",relief=t.FLAT,justify='right')
lblCell.pack(side='left', expand = 1)

txtCell= t.Entry(canvas1,font=('arial',10,'bold'),textvariable=cell,insertwidth=1,bg="gray99",justify='center')
txtCell.pack(side='left', expand = 1,anchor='w')

#txtCell.bind('<Return>', GetCellNo)

 

#lbl= t.Label(canvas1,bg='grey50',width=22)
#lbl.pack(side='left', expand = 1,fill=X)
#lbl= t.Label(canvas1,bg='grey50',width=22)
#lbl.pack(side='left', expand = 1,fill=X)
#lbl= t.Label(canvas1,bg='grey50',width=22)
#lbl.pack(side='left', expand = 1,fill=X)

#txtHost.focus_set()
  

datac=t.IntVar(value=0)

#lbl= t.Label(canvas2,bg='grey50',width=22)
#lbl.pack(side='left', expand = 1,fill=X)

 

lblData= t.Label(canvas1,font=('arial',10,'bold'),text="Data:",anchor="w",relief=t.FLAT,justify='left')
lblData.pack(side='left', expand = 1 ,anchor=CENTER)

txtData= t.Entry(canvas1,font=('arial',10,'bold'),textvariable=datac,insertwidth=1,bg="gray99",justify='center')
txtData.pack(side='left', expand = 1 ,anchor='w')
#txtData.bind('<Return>', GetCellNo)

 
#txtHost.focus_set()

#lbl= t.Label(canvas2,bg='grey50',width=14)
#lbl.pack(side='left', expand = 1,fill=X)
 
#btnData=t.Button(canvas1,font=('arial',8,'bold'),text="SEND",bg='#e6f7ff',fg="Black",bd=2,width=8,command=GetCellNo ,relief=t.RAISED,activebackground='#b3e6ff')
btnData=t.Button(canvas1   ,command=GetCellNo,bd=1  ,highlightthickness=1)
button_image(btnData,"i1.ico")
btnData.pack(side=LEFT, expand = 1 ,anchor='w')
btnData_ttp = CreateToolTip(btnData, "  SEND  ")
 

#lbl= t.Label(canvas2,bg='grey50',width=22)
#lbl.pack(side='left', expand = 1,fill=X)
#lbl= t.Label(canvas2,bg='grey50',width=22)
#lbl.pack(side='left', expand = 1,fill=X)



#=================================Label and  Widgets on f2============================================#  
def go(x):
    j=x[0]
    i=x[1]
    print Var[j][i].get()
    
   


Var=['VarC']*total_cell
Tag=['TagC']*total_cell


sp=100  
#===========================80 pins====================#
 
for j in range(0,total_cell):
    Var[j]=['VarP']*no_pin
    Tag[j]=['TagP']*no_pin
    for i in range (0,no_pin):
        Var[j][i] = IntVar()
        #print Var[j][i]
        if i<4:
          Tag[j][i]= Checkbutton(f3 , variable = Var[j][i],command=lambda x=(j,i): go(x), \
                     onvalue =pow(2,i), offvalue = 0, height=1, \
                     width = 2,bg='grey74')
          Tag[j][i].place(x=sp+100+85*j,y=30*i+100)
      
        if i>=4:
          Tag[j][i]= Checkbutton(f3 , variable = Var[j][i],command=lambda x=(j,i): go(x), \
                     onvalue =pow(2,(i-1)), offvalue = 0, height=1, \
                     width = 2,bg='grey74')
          Tag[j][i].place(x=sp+125+85*j,y=30*(i-4)+100)
            
     
for j in range(0,total_cell):
    Tag[j][3].config(onvalue =pow(2,6))
    Tag[j][7].config(onvalue =pow(2,7))

 
#================================cell no labels=========================#
lblcn=[0]*total_cell
for i in range(0,total_cell):
    lblcn[i]= t.Label(f3,bg='white',text=str(i+1) ,bd=2,padx=3)
    lblcn[i].place(x=sp+125+85*(i),y=0+73)
 
#================================ func for vertical and hrizontal extra checkbuttons=========================#
def go_all():
    if Var_all.get()==1:
        value=1
    else:
        value=0
    for i in range(0,4):
       Var_V[i].set(value)   
    go_V()
      
      
def go_V():
    
#  for i in range(0,20):
#         Var_H[i].set(0)
#         go_H()
    
  for i in range(0,3):
     if  not Var_V[i].get()==0: #(select)
         for j in range(0,total_cell):
              Var[j][i].set(pow(2,i))
              Var[j][i+4].set(pow(2,i+3))
 
              
     if  Var_V[i].get()==0:#(deselect)
         for j in range(0,total_cell):
              Var[j][i].set(0)
              Var[j][i+4].set(0)
 

  i=3 
  if  not Var_V[i].get()==0:
      for j in range(0,total_cell):
          Var[j][i].set(pow(2,i*2))
          Var[j][i+4].set(pow(2,i+4))
 
          
  if  Var_V[i].get()==0:
      for j in range(0,total_cell):
          Var[j][i].set(0)
          Var[j][i+4].set(0)
   
              

def go_H(): 
    
    
     k=0
     for j in range(0,20):
        if j%2==0 :   #(even)
          if  not Var_H[j].get()==0:  #(select)
                 for i in range(0,3):
                      Var[k][i].set(pow(2,i))
                 Var[k][3].set(pow(2,6))
                 
          elif  Var_H[j].get()==0:  #(deselect)
                 for i in range(0,4):
                      Var[k][i].set(0)
                 
        if not j%2==0 :
            if  not Var_H[j].get()==0:
                 for i in range(4,7):
                      Var[k][i].set(pow(2,(i-1)))
                 Var[k][7].set(pow(2,7))
            elif   Var_H[j].get()==0:  #(tic)
                 for i in range(4,8):
                      Var[k][i].set(0)                 
            k+=1


#================================Vertical checkbuttons for row select=========================#
             
Var_V=['V1']*4
Tag_V=['Tag_V']*4

for i in range(0,len(Var_V)):
   Var_V[i] = IntVar()
 

   Tag_V[i] = Checkbutton(f3 , variable = Var_V[i],command=go_V, \
                 onvalue =1, offvalue = 0, height=1, \
                 width = 1,bg='lightskyblue4',fg='red')
   Tag_V[i].place(x=sp+30,y=30*i+100)

#================================checkbutton for ALL_PIN select=========================#
vm=15 #vertical margin

Var_all=IntVar()
Tag_all =Checkbutton(f3 , variable = Var_all,command=go_all, \
                 onvalue =1, offvalue = 0, height=1, \
                 width = 1,bg='lightskyblue3',fg='red')
Tag_all.place(x=sp+30,y=225+vm) 
Tag_all_ttp = CreateToolTip(Tag_all , "Select All Pins")
#================================Horizontal checkbuttons for column select=========================#


Var_H=['H']*20
Tag_H=['Tag_H']*20
X=[]
for i in range(0,len(Var_H)):
   X.append(100+85*i)
   X.append(107+25+85*i)
#print X    
for i in range(0,len(Var_H)):
   Var_H[i] = IntVar()
 

   Tag_H[i] = Checkbutton(f3 , variable = Var_H[i],command=go_H, \
                 onvalue =1, offvalue = 0, height=1, \
                 width = 1,bg='lightskyblue4',fg='red')
   Tag_H[i].place(x=sp+X[i],y=225+vm)
 
#
#def pat():
#    a = 0
#    print pat_chk.get()
#    
#pat_chk =IntVar() 
#chk_pat=Checkbutton(f3 , variable = pat_chk,command=pat, \
#                 onvalue =1, offvalue = 0, height=1, \
#                 width = 1,bg='lightskyblue4',fg='red')
#chk_pat.place(x=900,y=283)
#
#lblpat= t.Label(f3,font=('arial',10,'bold'),text="Pattern :",relief=t.FLAT,justify='right')
##lblpat.pack(side='left', expand = 1)

 


def GetDatap():
   global Var
   datap=[0]*10
   for j in range(0,total_cell):
      for i in range(0,no_pin):
        datap[j]+=Var[j][i].get()

   return datap

def GetDatap_cust(data):
    data = data%64
    if(data % 2 == 0):
        datap=[(data/2)+192]*10
    else:
        datap=[(data/2)]*10
    return datap

def GetDatap_cust1(data):
    data = data%64
    dat = 126
    if(data % 2 == 0):
        datap=[255]*10
        datap[0] = 0
    else:
        datap=[255]*10
        datap[1] = 0
    return datap


def reFormat(fb):
    
     global w, h,btn_color,Tag_all,vm
     w = root.winfo_screenwidth()
     sp=0  #starting_point
     if fb==False:    ## in clear(deselect func) to clear screen and resize frame widgets
        sp=100
#====================================Each cell reposition===============================#         
        for j in range(0,total_cell):
            for i in range (0,no_pin):
                Tag[j][i].config(text='',width=1,height=1 )                
                if i<4:
                  Tag[j][i].place(x=sp+100+85*j,y=30*i+100)
              
                if i>=4:
                  Tag[j][i].place(x=sp+125+85*j,y=30*(i-4)+100)  
#====================================cell_no label===============================#             
        for i in range(0,total_cell):
                lblcn[i].destroy()
                lblcn[i]= t.Label(f2,bg='white',text=str(i+1) ,bd=2,padx=3)
                lblcn[i].place(x=sp+125+85*(i),y=0+73)   
#====================================Var_H===============================#             
        X=[]
        for i in range(0,len(Var_H)):
           X.append(sp+102+85*i)
           X.append(sp+102+25+85*i)
        #print X    
        for i in range(0,len(Var_H)):
            
           Tag_H[i].destroy()
        
           Tag_H[i] = Checkbutton(f2 , variable = Var_H[i],command=go_H, \
                         onvalue =1, offvalue = 0, height=1, \
                         width = 1,bg='lightskyblue4',fg='red')
           Tag_H[i].place(x=X[i],y=225+vm)            
            
#====================================Var_V===============================#             
        for i in range(0,len(Var_V)):
           Tag_V[i].destroy() 
           Tag_V[i] = Checkbutton(f3 , variable = Var_V[i],command=go_V, \
                         onvalue =1, offvalue = 0, height=1, \
                         width = 1,bg='lightskyblue4',fg='red')
           Tag_V[i].place(x=sp+30,y=30*i+100)            
#====================================Var_all===============================#   
        Tag_all.destroy()
        Tag_all =Checkbutton(f3 , variable = Var_all,command=go_all, \
                 onvalue =1, offvalue = 0, height=1, \
                 width = 1,bg='lightskyblue3',fg='red')
        Tag_all.place(x=sp+30,y=225+vm)
        Tag_all_ttp = CreateToolTip(Tag_all , "Select All Pins")
#====================================Root===============================#             
       # root.geometry(("%dx%d+%d+%d" % (1100, 950,120,0)))   
 

         
     else:
         #starting_point
         if w<1500:
            sp=30
    #====================================Each cell reposition===============================#         
            for j in range(0,total_cell):
                for i in range (0,no_pin):
                    Tag[j][i].config(text=fb[j][i],width=2,height=1,fg=btn_color[j][i])
                    if i<4:
                      Tag[j][i].place(x=sp+40+90*j,y=25*i+100)
                  
                    if i>=4:
                      Tag[j][i].place(x=sp+80+90*j,y=25*(i-4)+100)
    #====================================cell_no label===============================#      
            for i in range(0,total_cell):
                lblcn[i].destroy()
                lblcn[i]= t.Label(f3,bg='white',text=str(i+1),bd=2,padx=3 )
                lblcn[i].place(x=sp+80+90*(i),y=0+73)
    #====================================Var_H===============================#             
            X=[]
            for i in range(0,len(Var_H)):
               X.append(40+ 90*i)
               X.append(40+40+90*i)
            #print X    
            for i in range(0,len(Var_H)):
               Tag_H[i].destroy()
            
               Tag_H[i] = Checkbutton(f3 , variable = Var_H[i],command=go_H, \
                             onvalue =1, offvalue = 0, height=1, \
                             width = 2,bg='lightskyblue4',fg='red')
               Tag_H[i].place(x=sp+X[i],y=210)
               
    
    #====================================Var_V===============================#             
            for i in range(0,len(Var_V)):
               Tag_V[i].destroy() 
               Tag_V[i] = Checkbutton(f3 , variable = Var_V[i],command=go_V, \
                             onvalue =1, offvalue = 0, height=1, \
                             width = 1,bg='lightskyblue4',fg='red')
               Tag_V[i].place(x=sp+0,y=25*i+100)  
#====================================Var_all===============================#   
            Tag_all.destroy()
            Tag_all =Checkbutton(f3 , variable = Var_all,command=go_all, \
                     onvalue =1, offvalue = 0, height=1, \
                     width = 1,bg='lightskyblue3',fg='red')
            Tag_all.place(x=sp+0,y=210)               
    #====================================Root===============================#             
#            root.geometry(("%dx%d+%d+%d" % (w,int(round(h*.90)),0,0)))    
            
         else:
            sp=50 #staring point
    #====================================Each cell reposition===============================#         
            for j in range(0,total_cell):
                for i in range (0,no_pin):
                    Tag[j][i].config(text=fb[j][i],width=3,height=2,fg=btn_color[j][i])
                    if i<4:
                      Tag[j][i].place(x=sp+100+130*j,y=35*i+100)
                  
                    if i>=4:
                      Tag[j][i].place(x=sp+150+130*j,y=35*(i-4)+100)
    #====================================cell_no label===============================#      
            for i in range(0,total_cell):
                lblcn[i].destroy()
                lblcn[i]= t.Label(f2,bg='white',text=str(i+1) ,bd=2,padx=3)
                lblcn[i].place(x=sp+150+130*(i),y=0+73)
    #====================================Var_H===============================#             
            X=[]
            for i in range(0,len(Var_H)):
               X.append(100+130*i)
               X.append(100+50+130*i)
            #print X    
            for i in range(0,len(Var_H)):
               Tag_H[i].destroy()
            
               Tag_H[i] = Checkbutton(f2 , variable = Var_H[i],command=go_H, \
                             onvalue =1, offvalue = 0, height=1, \
                             width = 3,bg='lightskyblue4',fg='red')
               Tag_H[i].place(x=sp+X[i],y=280)
               
    
    #====================================Var_V===============================#             
            for i in range(0,len(Var_V)):
               Tag_V[i].destroy() 
               Tag_V[i] = Checkbutton(f2 , variable = Var_V[i],command=go_V, \
                             onvalue =1, offvalue = 0, height=2, \
                             width = 1,bg='lightskyblue4',fg='red')
               Tag_V[i].place(x=sp+30,y=35*i+100)  
#====================================Var_all===============================#   
            Tag_all.destroy()
            Tag_all =Checkbutton(f3, variable = Var_all,command=go_all, \
                     onvalue =1, offvalue = 0, height=1, \
                     width = 1,bg='lightskyblue3',fg='red')
            Tag_all.place(x=sp+30,y=278)                 
      #====================================Buttons===============================# 
 
#            btnAct.place(x=730,y=350)
#            btnClr.place(x=800,y=350)
#            btnPlt.place(x=870,y=350)
#            chk_pat.place(x=870,y=353)
            
      #====================================Counter===============================# 
 
#            lbl_Counter.place(x=int(round(w*.1)),y=360)
#            lbl_Counter_show.place(x=int(round(w*.152)),y=360)
      #====================================Counter===============================#
            
#            plot_chk.place(x=int(round(w*.4)),y=357)   
            
    #====================================Root===============================#             
#            root.geometry(("%dx%d+%d+%d" % (w, int(round(h*.90)),0,0)))   
     btn_color=[]     
     
 
btn_color=[]
def classify(fb):
    global btn_color
    btn_color=[]
    for i in range(0,total_cell*no_pin)  :
        if  100<fb[i]<200:                                            ##   change 100<-<200
            btn_color.append('#006633')#green
        elif fb[i]==0:
            btn_color.append('grey10')
        else:    
            btn_color.append('#cc0000')#red
#    print (btn_color),'len btn_co'        
    btn_color=fb_Format(btn_color) #3 FOR INDEXING 


def fb_Format(fb):
    s1=fb[0:20]     #7th in start and 3rd from the last 
    s2=fb[20:40]
    s3=fb[40:60]
    s4=fb[60:80]
    fbb=[0]*total_cell
    k=0
    for j in range(0,total_cell):
            fbb[j]=[s1[k],s2[k],s3[k],s4[k],s1[k+1],s2[k+1],s3[k+1],s4[k+1]]
            k+=2
    fb=fbb
#    print fb,'  :fb in fb_format'
    return fb        
    
def test_status(packet):
#    print packet,'print_packet'
    x=0
    global btn_color
#    print btn_color,'btn_color'
    for j in range(0,total_cell):
       for i in range(0,no_pin):
           x=Var[j][i].get()+x
           if not Var[j][i]==0:
               if btn_color[j][i]=='#cc0000': #red
                  lbl_status.config(text='Fail',bg='#ff0000',anchor='center',pady=3)#red
                  return
    if not lbl_status=='Fail':         
        lbl_status.config(text='Pass',bg='green',anchor='center',pady=3)
    if x==0:         
        lbl_status.config(text='      ',bg='grey93',anchor='center',pady=2)
    
    if not Cell_Pin.err_msg==[]:
        lbl_status.config(text='Fail',bg='#ff0000',anchor='center',pady=3)
#lbl_status.config(text='Fail',bg='#ff0000',anchor='center',pady=3)
              
        
#    for j in range(0,total_cell):
#       for i in range(0,no_pin):
##           Var[j][i].set(0)
#           Tag[j][i].config(text='0')


def write_csv(fb):
      global lbl_status 
#      showDate = strftime("%Y-%m-%d %H:%M:%S", time.localtime() )
      try:
        m_id=M_id.get()
        if len(m_id)==0 or m_id==''or m_id==' ':
            tkMessageBox.showinfo("WARNING", "Enter Module ID first. ")
            return
      except:
        tkMessageBox.showinfo("WARNING", "Enter Module ID first. ")
        return
      filename_csv=str(M_id.get())+".csv" 
      path = str( os.getcwd() ) + "\\Test_Results\\"
      if not os.path.exists(path):
            os.makedirs(path)
      s1=fb[0:20]      
      s2=fb[20:40]
      s3=fb[40:60]
      s4=fb[60:80]
      sfb=[s1,s2,s3,s4]
      try:
          with open(os.path.join(path, filename_csv), 'ab') as file:
               a = csv.writer(file)
               status=[str(lbl_status["text"])]
               if save_var.get()=='Single Row':      
#                   lbl=[str(lbl_status["text"]),' ']
                   lbl=status
                   for j in range(0,4):
                       for i in range(0,20):
                           lbl.append(sfb[j][i])
                       lbl.append(' ')    
                   a.writerow(lbl)
                   
               if save_var.get()=='Slaves matrix':
                   a.writerow(status)
                   for j in range(0,4):
                       lbl=['S'+str(j+1)]
                       for i in range(0,20):
                           lbl.append(sfb[j][i])
                       a.writerow(lbl)
      except IOError:
           tkMessageBox.showinfo("WARNING", "CSV file is open/close it. ")
           
def write_err(err):
      showDate = strftime("%Y-%m-%d %H:%M:%S", time.localtime() ) 
      try:
        m_id=M_id.get()
        if len(m_id)==0 or m_id==''or m_id==' ':
            tkMessageBox.showinfo("WARNING", "Enter Module ID first. ")
            return
      except:
        tkMessageBox.showinfo("WARNING", "Enter Module ID first. ")
        return
      filename_csv=str(M_id.get())+".log" 
      #path = str( os.getcwd() )
      path = str( os.getcwd() ) + "\\Test_Results\\"
   
      if not os.path.exists(path):
            os.makedirs(path)
      try:
          with open(os.path.join(path, filename_csv), 'ab') as file:
               a = csv.writer(file)
               lbl=[showDate,lbl_status["text"],str(err)]
               a.writerow(lbl)
               
      except IOError:
           tkMessageBox.showinfo("WARNING", "CSV file is open/close it. ")

def layout_csv(str_type):#1.(*) #2.(-)
      global cycle_var
      showDate = strftime("%Y-%m-%d %H:%M:%S", time.localtime() ) 
      filename_csv=str(M_id.get())+".csv" 
      path = str( os.getcwd() ) + "\\Test_Results\\"
      if not os.path.exists(path):
            os.makedirs(path)
            
      if type(str_type)==int:  #is cycle
        try:
          with open(os.path.join(path, filename_csv), 'ab') as file:
               a = csv.writer(file)
               lbl=[showDate[0:10],showDate[10:-1],'Cycles:'+str(str_type)]
               a.writerow(lbl)
               return
        except IOError:
               tkMessageBox.showinfo("WARNING", "CSV file is open/close it. ")
               return
           
      if type(str_type)==list:  #is cycle
        try:
          with open(os.path.join(path, filename_csv), 'ab') as file:
               a = csv.writer(file)
               lbl=[showDate[0:10],showDate[10:-1],'  Cycle:'+str(str_type[0])]
               a.writerow(lbl)
               return
        except IOError:
               tkMessageBox.showinfo("WARNING", "CSV file is open/close it. ")
               return
            
      try:
          with open(os.path.join(path, filename_csv), 'ab') as file:
               a = csv.writer(file)
               fill=[str(str_type)*20]*90
               a.writerow(fill)
      except IOError:
           tkMessageBox.showinfo("WARNING", "CSV file is open/close it. ")            


   #=============================== for console scrollbars on f4=======================================# 
   
canvas = tk.Canvas(f4, borderwidth=1, background="grey99", width=int(round(w*.96)), height=150 )
frame = tk.Frame(canvas, background="grey60",padx=6)#background="grey33"
vsb = tk.Scrollbar(f4, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y",expand=True)
#vsb.propagate(0)
canvas.pack(side="left", fill="both", expand=True,ipadx=10,ipady=10)
#canvas.propagate(0)

canvas.create_window((0,0), width=w-30,window=frame  )
#canvas.create_rectangle(00, 100, w, h, fill="grey88" )

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))



#=========TEXT widget on console ==========#
#rd=[123]*8

text = Text(frame,font=('arial',11))

def console_entry(packet):
    global text
    try:
        text.destroy()
        root.update()
    except:
        pass
    text = Text(frame,font=('arial',11))
    err_flag=False
#    print '#### packet :  ', packet,'####packet'
    for i in range(0,len(packet)):
        if packet[i]==None:
           packet[i]='_'
         
            
 
    try:
        for i in range(0,len(packet)):
            text.insert(INSERT, '>>'+str(packet[i]))
            text.tag_add("rd", "1.0", "155.27")
            text.tag_config("rd",  foreground="black")
            text.insert(INSERT, "\n")
        text.pack(side='right', expand = 1,fill=BOTH)
        text.config(state=DISABLED)
    except:
 
        print 'err_in (try: console entry check --Text height'
        return
    


#def detect_stop():
#      global cycle_var
#      x=cycle_var.get()
#      return x
#thread.start_new_thread(detect_stop, ())

#======================================plot=============================#

def update_plot(fb_time,cycle,cycle_num):
    
    global xdata,ydata,ln,fig,plt_color,pins#,root
    
#    root.lift()
    cmap_patch=[0]*len(pins)
    for i in range(len(ln)):
        ln[i].set_color(plt_color[i])
    plt_tag=[0]*len(pins)   
    cycle_num+=1
    if cycle==1 :
        for i in range(len(pins)):
            plt.plot(1,fb_time[pins[i]-1],"b.",ms=3)
    else:
        for i in range(len(pins)):
 
 
            if len(pins)<11:
                ax.legend(labels=str(pins[i]))
                plt.legend(loc = 'best')
            
            xdata[i].append(cycle_num)
            ydata[i].append(fb_time[pins[i]-1])
            ln[i].set_data(xdata[i],ydata[i])
            ln[i].set_label(str(pins[i]))

            if cycle<=40 and len(pins)<=4:
                plt.plot(xdata[i],ydata[i], 'k.', ms = 3)
        
    
#=========================================
#pins=range(1,81)#,1,5,9]
pins=[]


fig=None
xdata, ydata = [],[]
ln=None
plotter=False
plt_color=None



def plot_setup(cycle):
    
    global ln, xdata, ydata ,ax,fig,pins,plt_color,M_id
    
    get_pins()
    xdata, ydata =[0]*len(pins), [0]*len(pins)
    
    fig, ax = plt.subplots()
    fig.canvas.set_window_title("Module: "+str(M_id.get()))
    
    plt.axis([0,cycle+1,0,260])
    if cycle<=30:
        plt.xticks(np.arange(0, cycle+1, 1))
        plt.yticks(np.arange(0,260, 25))
    ax.set_title("Realtime")
    ax.set_xlabel("cycles -->")
    ax.set_ylabel("Feedback Time -->")
    cmap = plt.get_cmap('jet')    
#    print cmap
    #hsv(float(i)/(len(data)-1))
    plt_color = cmap(np.linspace(0, 1.0, len(pins)))


    
    plt.show()
    ln=[0]*len(pins)
    
    for i in range(len(pins)):
        ln[i], = ax.plot([], [])
        xdata[i]=[]
        ydata[i]=[]
    print xdata,"\n",ydata
#    fig.canvas.flush_events()


def get_pins():
    
    global pins,total_cell,no_pin,Var
    pins=[]
#    pins=range(1,81)
    for j in range(0,total_cell):
      for i in range(0,no_pin):
          
        if not Var[j][i].get()==0:
            if Var[j][i].get() in [1,2,4,64]:
                pins.append( (2*j+i*20)+1 )
            if Var[j][i].get() in [8,16,32,128]:
                pins.append( ( 2*j+1+(i-4)*20 )+1)            
    
    pins.sort()
#    print pins,"\n",len(pins)
    
    
def post_plot():
    global  pins, acc_over, plt_data,ax
#    acc_over=True##correction 
    
    if acc_over==True:
#        print plt_data
        fb_time=plt_data["fb_time"]
#        print plt_data["cycle"],"\n",plt_data["fb_time"],"\n",plt_data["pins"]
        
        plot_setup(plt_data["cycle"])
        ax.set_title("Last Acctuation Time ")
        get_pins()
        print "pins:______",pins
        for i in range(plt_data["cycle"]) :
            update_plot(plt_data["fb_time"][i],plt_data["cycle"],i)
            plt.show()
    else:
        tkMessageBox.showinfo("WARNING", "No Acctuation Record found !")

#=========================================
plt_data={}

reset=False
acc_over=False

def Acctuate():
    
    global HOST_Version,reset,Var_plot,pins,acc_over,plt_data,hold,lblHCC

    plt_fb_time=[]
    plt_data["pins"]=[]
    plt_data["cycle"]=0
    v_count=0
    #============================= Module_id ENTRY ============================#     
    try:
        m_id=M_id.get()
        if len(m_id)==0 or m_id==''or m_id==' ':
            tkMessageBox.showinfo("WARNING", "Enter Module ID first. ")
            return
    except:
        tkMessageBox.showinfo("WARNING", "Enter Module ID first. ")
        return


    #============================= Pins Selection Check ============================#     
    get_pins()
    if pins==[] :
        tkMessageBox.showinfo("WARNING", " No Pin Selected !" )
        return

    
    
    global ser,Port,packet,cycle_var,cycle
    lbl_Counter_show.config(text=' ',fg='red4')
    #=============================Cycle check============================# 
    try:
       if pat_var.get() == 'Custom':
           cycle=cycle_var.get()
       else:
           cycle=64*cycle_var.get()
       
    except :
         tkMessageBox.showinfo("WARNING", "Cycle must be an Integer !")
         cycle=None
         return  
         
    if cycle==None:
        tkMessageBox.showinfo("WARNING", "Enter Cycles First !-     ")
        return 
    if cycle==0:
        tkMessageBox.showinfo("WARNING", "Enter cycles First !")   
    #=================    
    
    #============================= host_addr  ENTRY============================#
    try:
       host_addr=Host.get()
       if  abs(host_addr) not in range(0,256):
           tkMessageBox.showinfo("WARNING", "Please Enter Proper Host address. Host address must be in range(0, 256) ")
           ser.close()
           return

    except ValueError:
       tkMessageBox.showwarning("WARNING", "     Enter Host Address First !     ")
       return
   
    
    layout_csv('*')
    layout_csv(cycle)
    layout_csv('--')   
    ##cycle starts
    btnAct.config(state='disabled')
    root.update()
    
#============= Serial port initialization =============#  

    try:
        ser.close()
    except:
        pass
  
    try: ##change\remove 
      ser=serial.Serial(Port.get(), 115200)
      #print('Seial_Port_was_already_closed')
      #ser.close()  
    except serial.SerialException: 
       tkMessageBox.showwarning("WARNING", "   Port "+Port.get()+"  not Available!  or Busy!           ")
       return  

#========================== plotting =====================#
    
    get_pins()
    plt_data["pins"].append(pins)
            
    if Var_plot.get()==True:
        pins=[]
        acc_over=True
        plot_setup(cycle)

    hold=False
#-----------___loop___================#    
    for j in range(0,cycle):
 
        
        
#===================condition check for hold ======================
        hold_btn_color = btnHold.cget("background")
        if hold==True:
            btnHold.config(relief=t.SUNKEN)
            
            btnHold.config(bg="grey60")
            root.update()
            while hold != False:
                root.update()
            btnHold.config(relief=t.RAISED)
            btnHold.config(bg=hold_btn_color)
            root.update()
#==============================================           
            
        
        if j==0:
            reset=False
        
        if j>=1 and reset==True:
            reset==False
            print 'stoping due to stop_btn(clear)'
            root.update()
            acc_over==True
            break

        if save_var.get()=='Slaves matrix':
            layout_csv([j+1])
        
#        try:
#            ser.close()
#        except:
#            pass
        
#        try: ##change\remove 
#          ser=serial.Serial(Port.get(), 115200)
#          #print('Seial_Port_was_already_closed')
#          #ser.close()  
#        except serial.SerialException: 
#           tkMessageBox.showwarning("WARNING", "   Port "+Port.get()+"  not Available!  or Busy!           ")
#           return
       
        
#============= ACCTUATION PATTERN (by setting datap)=============#         
        if pat_var.get()=='Custom':
            Cell_Pin.pat=False
            datap=GetDatap()
            
        else:
            datap=GetDatap_cust(j)
            Cell_Pin.pat=True 
#===========================================================#        
        packet_A=Cell_Pin.send_data_1(ser,host_addr,Cell_Pin.ACC_CMD,datap)[1]
        time.sleep(.3)
        
        if not Cell_Pin.err_msg==[]:
            write_err(Cell_Pin.err_msg[0])
            layout_csv('*')
            tkMessageBox.showwarning("WARNING", Cell_Pin.err_msg[0])
            Cell_Pin.err_msg=[]
            btnAct.config(state='normal')
            root.update()
            lbl_status.config(text='Fail',bg='#ff0000',anchor='center',pady=3)

            return
        
        [fb,packet_B]=Cell_Pin.GetFB_time(ser,host_addr)
       # print 'FB:', fb
        if 0 in fb:
            print 'zero detected'
           # tkMessageBox.showwarning("WARNING", " ZERO")
            btnAct.config(state='normal')

        if not Cell_Pin.err_msg==[]:
            write_err(Cell_Pin.err_msg[0])
            layout_csv('*')
            tkMessageBox.showwarning("WARNING", Cell_Pin.err_msg[0])
            Cell_Pin.err_msg=[]
            btnAct.config(state='normal')
            lbl_status.config(text='Fail',bg='#ff0000',anchor='center',pady=3)

            return
        
        #______get version__________#       
        if v_count==0:
            Cell_Pin.get_version(ser,host_addr)
#            print Cell_Pin.HST_Version,")))))))))))))))(*****&&&&&&&&&&&&&&^^^^"
            lbl_Vstatus.config(text=str(Cell_Pin.HST_Version),font=("aerial", 9),bg='grey99',anchor='center',pady=1)#'#ff0000'
            if(Cell_Pin.HST_Version != HOST_Version): 
                lbl_Vstatus.config(fg='#ff0000')
            root.update()
            time.sleep(.01)
            
            v_count+=1
            
#        if(Cell_Pin.HST_Version != HOST_Version):
#            tkMessageBox.showwarning("WARNING", "Version Mismatch - Version: " + str(HOST_Version-16) + " expected" );
#            return
        ###########################
        
        

        
        for i in range(0,len(packet_A)):
            packet.append(packet_A[i])
        for i in range(0,len(packet_B)):
            packet.append(packet_B[i]) 
            
        Cell_Pin.packet_A=[] 
        Cell_Pin.packet_B=[]
        
        
        if not len(fb)==80:
         # print fb,'  :fb in Acctuate',' ,len ',len(fb)
           fb=[0]*80
           #tkMessageBox.showinfo("WARNING", "Feedback_time Packet length is  " +str(len(fb))+" / Check connections or Host_Address") 

           
        

#        print fb,'  :fb in Acctuate',' ,len ',len(fb)
 
        
        classify(fb)
        test_status(packet)
        
        
        write_csv(fb)
        ## ======= to show fb time on checkbuttons=====##
        
        
        #==============for plotting=========
        plt_fb_time.append(fb)
        plt_data["cycle"]+=1
        plt_data["fb_time"]=plt_fb_time
        
        
        if Var_plot.get()==True:
            print pins,"    PINS_____________________"
            update_plot(fb,cycle, j)
        ##=================== 
        
        fb=fb_Format(fb)
        reFormat(fb)

        console_entry(packet)
        packet=[]

        print 'cycle: ',cycle,": ",j+1
        
        if save_var.get()=='Slaves matrix':
            layout_csv('-')   
 
        
        lbl_Counter_show.config(text=str(j+1),fg='red4')
        
        root.update()
        if not Var_plot.get()==True:
            time.sleep(0.1)

       
    acc_over==True    
    btnAct.config(state='normal')
    reset=False
    lblHCC.config(text="              " )
    try: 
      ser.close()
    except:
       pass
    root.update()
        
    

    
def Deselect():
   global lbl_status , lblHCC,reset,Var_all,Var,Var_V,Var_H,btnHold
   scan_ports()
   reset=True
   Var_all.set(0)
   
   try: 
      ser.close()
   except:
       pass

   btnHold.config(relief=t.RAISED)

   
   btnAct.config(state='normal')
   lbl_Counter_show.config(text=' ') 
   reFormat(False)
   lblHCC.config(text="              " )
   lbl_status.config(text="         ",bg='grey98')

   for j in range(0,total_cell):
     for i in range(0,no_pin):
         Var[j][i].set(0)
 
     for i in range(0,len(Var_V)):
         Var_V[i].set(0)
     for i in range(0,len(Var_H)):
         Var_H[i].set(0) 



#def HC_check():
#    global lblHCC
#    host=6
#    datap=[255]*10
#    try:
#        ser.close()
#    except:
#        pass
#       
#    try:
#        x=port.get()
#        if not len(x)==0:
#            pass
#    except:
#        lblHCC.config(font=('arial',8,'bold'),bg='grey99',fg='red2',text='Failed..',width=14,anchor='center')
#        root.after(1000,HC_check) 
#        
#    try: ##change\remove 
#      ser=serial.Serial(Port.get(), 115200)
#      #print('Seial_Port_was_already_closed')
#      #ser.close()  
#    except : 
#       lblHCC.config(font=('arial',8,'bold'),bg='grey99',fg='red2',text='Failed..',width=14,anchor='center')
#       root.after(1000,HC_check)
#       
#    HCC_flag=Cell_Pin.HC_CHECK(ser,host,Cell_Pin.ACC_CMD,datap)
#    if ser.isOpen():
#         ser.close()
#    if HCC_flag==True:
##         lblHCC.config(bg='green4',fg='grey99',text='HOST COMMUNICATION CHECK',width=28)
#         lblHCC.config(font=('arial',8,'bold'),bg='grey99',fg='green4',text='Successful..',width=14,anchor='center')
#    else:
##         lblHCC.config(bg='red3',fg='grey99',text='HOST COMMUNICATION CHECK',width=28) 
#         lblHCC.config(font=('arial',8,'bold'),bg='grey99',fg='red2',text='Failed..',width=14,anchor='center') 
##    time.sleep(2)
##    btnHCC.config(bg='grey93',fg='Black',text='HOST COMMUNICATION CHECK',width=28)
#    time.sleep(.5)
#    root.after(1000,HC_check)

def HC_check():
    global Port,root
#    print Po1rt.get(),'           ---portget'
    host=6
    datap=[255]*10

    try: ##change\remove 
      ser=serial.Serial(Port.get(), 115200)
      #print('Seial_Port_was_already_closed')
      #ser.close()  
    except serial.SerialException: 
       lblHCC.config(font=('arial',8,'bold'),bg='grey99',fg='red2',text='Checking.. ',width=14,anchor='center')
#       tkMessageBox.showwarning("WARNING", "   Port "+Port.get()+"  not Available!  or Busy!           ")
       try:
           ser.close()
       except:
           pass

       root.after(100,HC_check)      
       return
#     sys.stdout=open("automode_console.txt","w")
#     sys.stdout.close()
    HCC_flag=Cell_Pin.HC_CHECK(ser,host,Cell_Pin.ACC_CMD,datap)
#    print HCC_flag,'HCC_flag'
    if ser.isOpen():
         ser.close()
    if HCC_flag==True:
#         lblHCC.config(bg='green4',fg='grey99',text='HOST COMMUNICATION CHECK',width=28)
         lblHCC.config(font=('arial',9,'bold'),bg='grey99',fg='green4',text='Successful',width=14,anchor='center')
    else:
#         lblHCC.config(bg='red3',fg='grey99',text='HOST COMMUNICATION CHECK',width=28) 
         lblHCC.config(font=('arial',9,'bold'),bg='grey99',fg='red2',text='Failed',width=14,anchor='center') 
#    time.sleep(1)
    root.after(1000,HC_check)

##================================ttk style setting================================##

style_HCC= ttk.Style()
style_HCC.configure('TButton', foreground='grey10',bd=10, relief='ridge', padding=1)

btnHCC=ttk.Button(f3 ,text=" CONNECTION STATUS " ,command=HC_check )
btnHCC.pack(side="left")
#btnHCC_ttp = CreateToolTip(btnHCC, "  Connection Status of HOST   ")


lblHCC= t.Label(f3,font=('arial',7,'bold'),text="                ",bd=3,bg='light sky blue' ,width=14,fg='black',anchor="nw",pady=4,relief=t.SUNKEN,justify='center')
lblHCC.pack(side="left")

thread.start_new_thread(HC_check,())

#btnStop=t.Button(f3 ,bd=2, command=Acctuate,pady=4,relief=t.RAISED,highlightthickness=1)
##btnAct=t.Button(f3,font=('arial',8,'bold'),text="ACTUATE",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Acctuate,pady=2,relief=t.RAISED)
#button_image(btnStop,"stop.ico")
#btnStop.place(x=int(round(w*.1)),y=310)


#=============================btn_actuate===========================#    

#btnAct=t.Button(fn_btns_frame ,bd=2, command=Acctuate,pady=4,relief=t.RAISED,highlightthickness=1)
##btnAct=t.Button(f3,font=('arial',8,'bold'),text="ACTUATE",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Acctuate,pady=2,relief=t.RAISED)
#button_image(btnAct,"a1.png") #a1
#btnAct.place(x=790,y=280)

##btnAct=t.Button(f3 ,bd=2, command=Acctuate_pat,pady=4,relief=t.RAISED,highlightthickness=1)
###btnAct=t.Button(f3,font=('arial',8,'bold'),text="ACTUATE",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Acctuate,pady=2,relief=t.RAISED)
##button_image(btnAct,"a2.png") #a1
##btnAct.place(x=900,y=280)
#
##=============================btn_clear===========================#
#
#btnClr=t.Button(fn_btns_frame  ,bd=2, command=Deselect,pady=0,relief=t.RAISED,highlightthickness=2)
##btnClr=t.Button(f3,font=('arial',8,'bold'),text="CLEAR",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Deselect,pady=2,relief=t.RAISED)
#button_image(btnClr,"refresh2.ico") #13
#btnClr.place(x=843,y=280)
#
#
##=============================btn_plot===========================#
#
#btnPlt=t.Button(fn_btns_frame  ,bd=2, command=post_plot,pady=0,relief=t.RAISED,highlightthickness=1)
##btnClr=t.Button(f3,font=('arial',8,'bold'),text="CLEAR",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Deselect,pady=2,relief=t.RAISED)
#button_image(btnPlt,"Data-Scatter-Plot-icon.png")#"icons8-play-graph-report (1).png") #13
#btnPlt.place(x=897,y=280)
#
#
#
##=============================btn_hold===========================#
#
#btnhold=t.Button(fn_btns_frame  ,bd=2, command=post_plot,pady=0,relief=t.RAISED,highlightthickness=1)
##btnClr=t.Button(f3,font=('arial',8,'bold'),text="CLEAR",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Deselect,pady=2,relief=t.RAISED)
#button_image(btnhold,"hold.png")#"icons8-play-graph-report (1).png") #13
#btnhold.place(x=700,y=280)
#



#===========================================Current CYCLE Counter==============================#

lbl_Counter= t.Label(f3,font=('arial',8,'bold'),text="Counter", width=7,anchor="center",pady=3,
                     highlightthickness=1,relief=t.SUNKEN,justify='center')
#lbl_Counter.place(x=int(round(w*.1)),y=300)
lbl_Counter.pack(side="left")

lbl_Counter_show= t.Label(f3,font=('arial',8,'bold'),text="  ", width=4,bd=1,anchor="center",
                          pady=3,relief=t.SUNKEN,justify='center')
#lbl_Counter_show.place(x=int(round(w*.152)),y=300)
lbl_Counter_show.pack(side="left")







#btnfb=t.Button(f2,font=('arial',10,'bold'),text="Get Feedback",bg='grey93',fg="Black",bd=4,width=28,command=get_time,pady=1,relief=t.RAISED)
#btnfb.place(x=200,y=360)

#HC_check()
#f4=t.Frame(f2, bg="grey23",relief=t.RIDGE,bd=1, width=1100, height=400 ,highlightthickness=1,pady=2)
#f4.pack(side=BOTTOM, expand = 1,fill=BOTH)



#=========================================HOST_CHECK_THREAD========================================#

#def HCC():
#    if  not cbo[0]=='':
#      HC_check()
#    root.after(1000,HCC)
# 
#    
#thread.start_new_thread(HC_check, ()) 

#=========================================== btn_panel ==============================#

#============================= btn_actuate ===========================#    

btnAct=t.Button(fn_btns_frame ,bd=3, command=Acctuate,padx=30,pady=30,relief=t.RAISED,highlightthickness=1)
#btnAct=t.Button(f3,font=('arial',8,'bold'),text="ACTUATE",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Acctuate,pady=2,relief=t.RAISED)
button_image(btnAct,"a1.png") #a1
btnAct.pack(side="left",ipadx=3)
btnAct_ttp = CreateToolTip(btnAct, "  Actuate  ")


#btnAct=t.Button(f3 ,bd=2, command=Acctuate_pat,pady=4,relief=t.RAISED,highlightthickness=1)
##btnAct=t.Button(f3,font=('arial',8,'bold'),text="ACTUATE",bg='grey93',activebackground='#b3e6ff',fg="Black",bd=3,width=8,command=Acctuate,pady=2,relief=t.RAISED)
#button_image(btnAct,"a2.png") #a1
#btnAct.place(x=900,y=280)

#============================= btn_clear ===========================#

btnClr=t.Button(fn_btns_frame  ,bd=3, command=Deselect,padx=30,pady=30,relief=t.RAISED,highlightthickness=2)
button_image(btnClr,"refresh2.ico") #13
btnClr.pack(side="left",ipadx=3)
btnClr_ttp = CreateToolTip(btnClr, "  Clear  ")

#============================= btn_plot ===========================#

btnPlt=t.Button(fn_btns_frame  ,bd=3, command=post_plot,padx=30,pady=30,relief=t.RAISED,highlightthickness=1)
button_image(btnPlt,"Data-Scatter-Plot-icon.png")#"icons8-play-graph-report (1).png") #13
btnPlt.pack(side="left",ipadx=3)
btnPlt_ttp = CreateToolTip(btnPlt, "  Plot  ")


#============================= btn_hold ===========================#


hold=False
def hold_act():
    global hold
    
    hold= not hold
    
    
    
btnHold=t.Button(fn_btns_frame , bd=3 , command=hold_act ,padx=30,pady=30,relief=t.RAISED,highlightthickness=1)
button_image(btnHold,"hold.png")#"icons8-play-graph-report (1).png") #13
btnHold.pack(side="left",ipadx=3)
btnHold_ttp = CreateToolTip(btnHold, "  Hold  ")


#============================ plot checkbox ============#

Var_plot= IntVar()
plot_chk= Checkbutton(fn_btns_frame,bd=2 ,text="Plot", variable = Var_plot,\
                                 onvalue =1, offvalue = 0, \
                                 bg='grey52',fg='#300302',padx=5)
plot_chk.pack(side="left",ipadx=2)
plot_chk_ttp = CreateToolTip(plot_chk, " Real Time Plotting  ")

#----------------------------------------------------------------#


root.bind("<Return>",Acctuate)
mainloop()
