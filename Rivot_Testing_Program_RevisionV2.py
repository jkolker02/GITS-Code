#!/usr/bin/env python3
from daqhats import mcc118, mcc152, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string, chan_list_to_mask
import tkinter as tk
from tkinter import *
from tkinter import Canvas
from PIL import ImageTk, Image
import time
import math
import numpy as np
from time import sleep
from datetime import datetime

from daqhats import mcc118, mcc152, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string, chan_list_to_mask

#-----Board Initialization-----
#
address = select_hat_device(HatIDs.MCC_152)
hat = mcc152(address)
options = OptionFlags.DEFAULT
info = mcc152.info().NUM_AO_CHANNELS
channel = 0

address1 = select_hat_device(HatIDs.MCC_118)
hat1 = mcc118(address1)

#-----Window Declaration-----
#
window = tk.Tk()
window.grid()
window.configure(background = '#d9d9d9')
window.title('Rivet Torsional Strength Test')

#-----Variable Declaration-----
#
start_angle = 0
current_angle = 0
end_angle = 10

start_time = 0
cycle_duration = 10

cylinder_feedback = []
torque_feedback = []
angle1_feedback = []
angle2_feedback = []
time_array = []

running = False
manual_running = False
initial = True

counter = 0

latest_cylinder = 0
latest_torque = 0
latest_angle1 = 0
latest_angle2 = 0

var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var4 = StringVar()
var5 = StringVar()

var1.set('Cylinder Position: {}'.format(round(latest_cylinder*18,5)))
var2.set('Torque Feedback: {}'.format(round(latest_torque,5)))
var3.set('Angle 1 Feedback: {}'.format(round(latest_angle1,5)))
var4.set('Angle 2 Feedback: {}'.format(round(latest_angle2,5)))

var5.set('Current Angle Set At: {}'.format(round(current_angle,2)))

#-----Grid configurement-----
#

window.grid_columnconfigure(0, minsize = 50, weight = 1)
window.grid_columnconfigure(1, minsize = 50, weight = 1)
window.grid_columnconfigure(2, minsize = 50, weight = 1)
window.grid_columnconfigure(3, minsize = 80, weight = 1)
window.grid_columnconfigure(4, minsize = 50, weight = 1)
window.grid_columnconfigure(5, minsize = 50, weight = 1) #Divider
window.grid_columnconfigure(6, minsize = 50, weight = 1)
window.grid_columnconfigure(7, minsize = 50, weight = 1)
window.grid_columnconfigure(8, minsize = 50, weight = 1)
window.grid_columnconfigure(9, minsize = 50, weight = 1)
window.grid_columnconfigure(10, minsize = 50, weight = 1)

window.grid_rowconfigure(0, minsize = 40, weight = 1)
window.grid_rowconfigure(1, minsize = 10, weight = 1)#Title Line
window.grid_rowconfigure(2, minsize = 40, weight = 1)
window.grid_rowconfigure(3, minsize = 40, weight = 1)
window.grid_rowconfigure(4, minsize = 40, weight = 1)
window.grid_rowconfigure(5, minsize = 40, weight = 1)
window.grid_rowconfigure(6, minsize = 40, weight = 1)
window.grid_rowconfigure(7, minsize = 40, weight = 1)
window.grid_rowconfigure(8, minsize = 40, weight = 1)
window.grid_rowconfigure(9, minsize = 40, weight = 1)




#-----Functions-----
#

def update_Current_Set_Angle(value):
    global current_angle
    current_angle = slider.get()
    var5.set('Current Angle Set At: {}'.format(round(current_angle,2)))
    display_Set_Angle()

def enable_Manual():
    global manual_running
    global running
    global current_angle
    global latest_cylinder
    
    gather_Initial_Feedback()
    manual_running = True
    running = False
    slider['state'] = ACTIVE
    slider.set(latest_cylinder*18)
    update_User_Status()
    update_Manual_Status()
    manual_Run()
    
def disable_Manual():
    global manual_running
    global running
    
    manual_running = False
    slider['state'] = DISABLED
    update_Manual_Status()
    
def update_User_Status():
    if (running):
        status = Label(window, text = "Current User Status: Active", font = "Arial 8 normal", bg = '#d9d9d9', fg = 'Green', width = 25)
    else:
        status = Label(window, text = "Current User Status: Inactive", font = "Arial 8 normal", bg = '#d9d9d9', fg = 'REd', width = 25)
    status.grid(row = 2, column = 0, sticky = S)
    
def update_Manual_Status():
    if (manual_running):
        status = Label(window, text = "Current Manual Status: Active", font = "Arial 8 normal", bg = '#d9d9d9', fg = "Green", width = 25)
    else:
        status = Label(window, text = "Current Manual Status: Inactive", font = "Arial 8 normal", bg = '#d9d9d9', fg = 'red', width = 30)
    status.grid(row = 2, column = 8, columnspan = 2,sticky = S)

def set_End_Angle():
    global end_angle
    end_angle = float(end_angle_entry.get())
    end_angle_entry.delete(0,'end')
    if (end_angle >90):
        end_angle = 90
    label1 = Label(window, text = "The end angle is {}°".format(end_angle), width = 20,font = "Arial 8 normal")
    label1.grid(row = 7, column = 1,columnspan = 2, sticky = S)

def set_Cycle_Duration():
    global cycle_duration
    cycle_duration = float(execution_Time_Entry.get())
    execution_Time_Entry.delete(0,'end')
    label1 = Label(window, text = "The cycle duration is {} sec".format(cycle_duration), width = 30, font = "Arial 8 normal")
    label1.grid(row = 8, column = 1, sticky = N, columnspan =2)


def exit_Program():
    global channel
    hat.a_out_write(channel=channel,value=0,options=options)

    gather_Initial_Feedback()
    sys.exit()

def user_Start():
    global running, manual
    running = True
    update_User_Status()
    disable_Manual()
    update_Manual_Status()
    run()

def user_Stop():
    global running, cycle_duration, current_time, initial
    current_time=time.time()+cycle_duration
    slider['state'] = ACTIVE
    slider.set(latest_cylinder*18)
    slider['state'] = DISABLED
    running = False
    initial= True
    update_User_Status()
    
    
def display_Set_Angle():
    global current_Angle
    var5.set('Current Angle Set At: {}'.format(round(current_angle,2)))
    
    
def clear_File_Output():
    global cylinder_feedback, torque_feedback, angle1_feedback, angle2_feedback,time_array,initial
    time_array = []
    cylinder_feedback = []
    torque_feedback = []
    angle1_feedback = []
    angle2_feedback = []
    initial = True
    
def gather_Feedback():
    global cylinder_feedback
    global torque_feedback
    global angle1_feedback
    global angle2_feedback
    global start_time
    global latest_cylinder
    global latest_torque
    global latest_angle1
    global latest_angle2
    
    
    time_array.append(time.time() - start_time)
    value1 = round(hat1.a_in_read(channel = 0, options = options), 5)
    value2 = round(hat1.a_in_read(channel = 1, options = options), 5)
    value3 = round(hat1.a_in_read(channel = 2, options = options), 5)
    value4 = round(hat1.a_in_read(channel = 3, options = options), 5)
    #APPEND EACH FEEDBACK LIST WITH APPROPRIATE VALUE
    cylinder_feedback.append(value1)
    torque_feedback.append(value2)
    angle1_feedback.append(value3)
    angle2_feedback.append(value4)
    latest_cylinder = value1
    latest_torque = value2
    latest_angle1 = value3
    latest_angle2 = value4
    
def display_Feedback():
    global latest_cylinder
    global latest_torque
    global latest_angle1
    global latest_angle2
    global var1,var2,var3,var4
    
    value = round(latest_cylinder * 18,5)
    
    var1.set('Cylinder Position: {}'.format(round(latest_cylinder*18,3)))
    var2.set('Torque Feedback: {}'.format(round(latest_torque,3)))
    var3.set('Angle 1 Feedback: {}'.format(round(latest_angle1,3)))
    var4.set('Angle 2 Feedback: {}'.format(round(latest_angle2,3)))

    
def export_Feedback():
    global time_array
    global cylinder_feedback
    global torque_feedback
    global angle1_feedback
    global angle2_feedback
    
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    path = '/home/pi/Desktop/Python Program Scripts/LogFiles/Rivot_Test_Results-{}.txt'.format(date)
    file = open(path,'w')
    for i in range(0, len(time_array)):
        value1 = str(format(time_array[i],'.6f'))
        file.write(value1 +  ' ')
        value2 = str(format(cylinder_feedback[i],'.6f'))
        file.write(value2 + ' ')
        value3 = str(format(torque_feedback[i],'.6f'))
        file.write(value3 + ' ')
        value4 = str(format(angle1_feedback[i],'.6f'))
        file.write(value4 + ' ')
        value5 = str(format(angle2_feedback[i],'.6f'))
        file.write(value5)
        file.write('\n')
   
    file.close()
    clear_File_Output()
    
def gather_Initial_Feedback():
    global cylinder_feedback
    global torque_feedback
    global angle1_feedback
    global angle2_feedback
    global start_time
    global latest_cylinder
    global latest_torque
    global latest_angle1
    global latest_angle2
    
    value1 = round(hat1.a_in_read(channel = 0, options = options), 5)
    value2 = round(hat1.a_in_read(channel = 1, options = options), 5)
    value3 = round(hat1.a_in_read(channel = 2, options = options), 5)
    value4 = round(hat1.a_in_read(channel = 3, options = options), 5)
    latest_cylinder = value1
    latest_torque = value2
    latest_angle1 = value3
    latest_angle2 = value4
    
def run():
    global running
    global manual_running
    global start_time
    global initial
    global current_angle
    global start_angle
    global cycle_duration
    global end_angle
    global counter
    global current_time
    
    
    
    if (running):
        
        if (initial):
            clear_File_Output()
            start_time = time.time()
            initial = False
            start_angle = current_angle
            counter = 0
        current_time = time.time()
        if (current_time - start_time < cycle_duration):
            current_angle = ((current_time - start_time)*((end_angle - start_angle) / cycle_duration) + start_angle)
            voltage = current_angle * .055555555555
            #print(voltage)
            hat.a_out_write(channel = channel, value = voltage, options = options)
            gather_Feedback()
            
            if (counter%3 == 0):
                display_Feedback()
            if (counter%3 ==0):
                display_Set_Angle()
            window.after(5, run)
            counter +=1
            slider['state']=ACTIVE
            slider.set(latest_cylinder*18)
            slider.update_idletasks()
            slider['state'] = DISABLED
    
        if(current_time - start_time > cycle_duration):
            running = False
            slider['state'] = ACTIVE
            current_angle = end_angle
            gather_Initial_Feedback()
            slider.set(latest_cylinder*18)
            slider['state'] = DISABLED
            display_Feedback()
            
            display_Set_Angle()
            initial = True
            user_Stop()
            print(counter/cycle_duration)
          
            

        
def manual_Run():
    global running
    global manual_running
    global counter
    global current_angle
    
    
    if (manual_running):
        update_Current_Set_Angle(0)
        running = False
        current_angle = slider.get()
        voltage = current_angle * .055555555555
        #print(voltage)
        hat.a_out_write(channel = channel, value = voltage, options = options)
        gather_Initial_Feedback()
        if (counter%2==0):
            display_Feedback()
            
        slider.update_idletasks()
        window.after(10, manual_Run)
        counter+=1

    
#-----Display-----
frame1= Label(window, text="User Input",fg = 'black', bg='#d9d9d9', font = 'Arial 19 bold', padx = 15, pady = 7)
frame1.grid(row=0,column=2, sticky = W)

frame2 = Label(window, text="Manual Control", fg = 'black',bg='#d9d9d9', font = 'Arial 19 bold', padx = 15, pady=7)
frame2.grid(row=0, column = 7)

frame3 = Label(window, text="Feedback", fg = 'black', bg = '#d9d9d9', font = 'Arial 19 bold underline', padx = 25)
frame3.grid(row = 5, column = 7,sticky=W)

titleFrame = tk.Frame(window, bg = 'black')
titleFrame.grid(row=1, column = 0, columnspan = 11, sticky = 'ew')

slider = Scale(window, from_= 0, to = 90, orient = HORIZONTAL, length = 300, state = DISABLED, resolution = .01)
slider.grid(row = 2, column = 7)

toggle_Lock_B = Button(window, text = "Enable Manual", command = enable_Manual, fg = 'white', bg = '#11c808', font = "Arial 8 bold", bd = 2, width = 10, height = 1,pady = -2, activebackground = '#08A800', activeforeground = 'white')
toggle_Lock_B.grid(row = 3, column = 7, sticky = W)

toggle_Lock_B2 = Button(window, text = "Disable Manual", command = disable_Manual, fg = 'white', bg = '#ff4848', font = "Arial 8 bold", bd = 2, width = 10, height = 1,pady = -2, activebackground = '#c90000', activeforeground = 'white')
toggle_Lock_B2.grid(row = 3, column = 7, sticky = E)


exit_Button = Button(window, text = 'EXIT', fg = 'white', bg = '#c40909', font = "Arial 18 bold", bd = 4, width = 8, height = 1, activebackground = '#940606', activeforeground = 'white', command = exit_Program)
exit_Button.grid(row = 9, column = 9, sticky = SW)


ending_Angle = Label(window, text="End Angle: ", fg = 'black', bg = '#d9d9d9', font = "Arial 13 normal",padx = 10, pady = 10)
ending_Angle.grid(row = 3, column = 0, sticky = W)

end_angle_entry = tk.Entry(window)
end_angle_entry.grid(row = 3, column = 2, sticky = W)
end_angle_entry.bind('<KP_Enter>', (lambda event: set_End_Angle()))
end_angle_entry.bind('<Return>', (lambda event: set_End_Angle()))

button2 = Button(window, text = 'Enter', command = set_End_Angle, fg = 'black', bg = '#aeaeae', font = "Arial 8 bold", bd = 2, width = 2, height = 1, activebackground = '#11c808', activeforeground = 'white')
button2.grid(row = 3, column = 3, sticky = W)



execution_Time_L = Label(window, text = 'Cycle Duration (sec): ', fg  = 'black', bg = '#d9d9d9', font = "Arial 13 normal", padx = 10, pady =25)
execution_Time_L.grid(row = 4, column = 0, sticky = W)

execution_Time_Entry = tk.Entry(window)
execution_Time_Entry.grid(row = 4, column = 2, sticky = W)
execution_Time_Entry.bind('<KP_Enter>', (lambda event: set_Cycle_Duration()))
execution_Time_Entry.bind('<Return>', (lambda event: set_Cycle_Duration()))

button3 = Button(window, text = 'Enter', command = set_Cycle_Duration, fg = 'black', bg = '#aeaeae', font = "Arial 8 bold", bd = 2, width = 2, height = 1, activebackground = '#11c808', activeforeground = 'white')
button3.grid(row = 4, column = 3, sticky = W)

label1 = Label(window, text = "The cycle duration is {} sec.".format(cycle_duration), width = 30, font = "Arial 8 normal")
label1.grid(row = 8, column = 1, sticky = N, columnspan =2)

label1 = Label(window, text = "The end angle is {}°".format(end_angle), width = 20,font = "Arial 8 normal")
label1.grid(row = 7, column = 1,columnspan = 2, sticky = S)

start_Button = Button(window, text = "Run", command = user_Start, fg = 'white', bg = '#11c808', font = "Arial 12 bold", bd = 3, height = 2, width = 8, activebackground = '#08A800', activeforeground = 'white')
start_Button.grid(row = 9, column = 1, columnspan = 2, sticky = W)

stop_Button = Button(window, text = "Stop", command = user_Stop, fg = 'white', bg = '#ff4848', font = 'Arial 12 bold', bd = 3, height = 2, width = 8, activebackground = '#c90000', activeforeground = 'white')
stop_Button.grid(row = 9, column = 1, columnspan = 2, sticky = E)

export_Results = Button(window, text = "Export Results", command = export_Feedback, fg = 'black', bg = '#ffae36', font = "Arial 10 bold", activeforeground = 'black', activebackground = '#f09205', bd = 4)
export_Results.grid(row = 7, column = 9)

clear_Results = Button(window, text = "Clear Results", command = clear_File_Output, fg = 'black', bg = 'white', font = "Arial 10 bold", activeforeground = 'black', activebackground = '#e3e3e3', bd = 4)
clear_Results.grid(row = 8, column = 9)


label1 = Label(textvar = var1, fg = 'black', bg = '#d9d9d9', font = 'arial 10', width = 25)
label1.grid(row = 6, column = 7,sticky = W)
    
label2 = Label(textvar = var2, fg = 'black', bg = '#d9d9d9', font = 'arial 10', width = 25)
label2.grid(row = 7, column = 7,sticky = W)
    
label3 = Label(textvar = var3, fg = 'black', bg = '#d9d9d9', font = 'arial 10', width = 25)
label3.grid(row = 8, column = 7,sticky = W)

label4 = Label(textvar = var4, fg = 'black', bg = '#d9d9d9', font = 'arial 10', width = 25)
label4.grid(row = 9, column = 7,sticky = W)
    
label_d = Label(window, textvar = var5, fg = 'black', bg = '#d9d9d9', font = 'Arial 10 normal', width = 30)
label_d.grid(row = 4, column =7)



update_User_Status()
update_Manual_Status()
display_Set_Angle()
gather_Initial_Feedback()



window.after(10,display_Feedback)
window.mainloop()