#!/usr/bin/env python3

from __future__ import print_function
from time import sleep
from sys import version_info, stdout
from tkinter import *
from PIL import Image
from PIL import ImageTk
from decimal import Decimal

from daqhats import mcc118, mcc152, OptionFlags, HatIDs, HatError
from daqhats_utils import select_hat_device, enum_mask_to_string, chan_list_to_mask

import tkinter as tk
import time

#initial output state on start-up
running = False
runningII = False
value_convert = None
slider_state = DISABLED
value = 0
start_pressure = -1
end_pressure = 0
ramp_time = 1
time_o = 0
time_f = 0
y = 0
valueII = 0
x = 0


#Obtain the Board Information
address = select_hat_device(HatIDs.MCC_152)
hat = mcc152(address)
options = OptionFlags.DEFAULT
info = mcc152.info().NUM_AO_CHANNELS
channel = 0

#Setup the GUI Window
GUI = Tk()

GUI.grid_rowconfigure(1, minsize=10)
GUI.grid_rowconfigure(2, minsize=8)
GUI.grid_rowconfigure(3, minsize=10)
GUI.grid_rowconfigure(4, minsize=8)
GUI.grid_rowconfigure(5, minsize=10)
GUI.grid_rowconfigure(6, minsize=8)
GUI.grid_rowconfigure(7, minsize=10)
GUI.grid_rowconfigure(8, minsize=8)
GUI.grid_rowconfigure(9, minsize=10)
GUI.grid_rowconfigure(10, minsize=8)
GUI.grid_rowconfigure(11, minsize=10)


GUI.grid_columnconfigure(0, minsize=10)
GUI.grid_columnconfigure(1, minsize=75)
GUI.grid_columnconfigure(3, minsize=25)
GUI.grid_columnconfigure(7, minsize=10)

GUI.configure(background='honeydew4')
GUI.title('Pressure Control Module - Channel 01')

var = StringVar()
varII = StringVar()
var.set("Current Pressure Set At: %s" % value + " psi")
varII.set("Current Time Set At: %s" % valueII + " sec")

    
#Function to control programed output
def scan_func():
    global ramp_time
    global start_pressure
    global end_pressure
    global running
    global channel
    global value
    global value_convert
    global current_output
    global var
    global varII
    global y
    global x
    global time_f
    global time_o
        
    
    if running:
        
        y = start_pressure
        m = (end_pressure - start_pressure)/ramp_time
                
        if x < ramp_time:
            time_o = Decimal(time.time())
            y = m*x+start_pressure
            value_convert = Decimal(y)*Decimal(.034482758)
            hat.a_out_write(channel=channel,value=value_convert,options=options)
            time_f = Decimal(time.time())
            time.sleep(.025)
            print(x,y,)
            x = (x + (time_f-time_o) + Decimal(.025))
            valueII = round(x,5)
            value = round(y,5)
                        
            var.set("Current Pressure Set At: %s" % value + " psig")
            
            varII.set("Current Time Set At: %s" % valueII + " sec")
            
        if x >= ramp_time:
            #hat.a_out_write(channel=channel,value=value_convert,options=options)
            running = False
            
            y = end_pressure
            valueII = round(x,5)
            value = round(y,5)
            slider["state"] = "normal"
            slider.set(y)
            slider["state"] = "disabled"
            x = 0
            n = 0
            value_convert = Decimal(y)*Decimal(.034482758)
            hat.a_out_write(channel=channel,value=value_convert,options=options)
            var.set("Current Pressure Set At: %s" % value + " psig")
            varII.set("Current Time Set At: %s" % valueII + " sec")
                        
    GUI.after(2,scan_func)
    
#Function to control manual output
def manual_func():
    global runningII
    global running
    global value
    global value_convert
    global current_output
    global var
    global varII
    global channel
        
    if runningII:
        running = False
        value = slider.get()
        value_convert = (value*.034482758)
        hat.a_out_write(channel=channel,value=value_convert,options=options)
        var.set("Output Value Set At: %s" % value + "psi")
        slider.update_idletasks()
        
    GUI.after(5,manual_func)   
    
#Function to start program output      
def start_program_func():
    global running
    global runningII
    global slider_state
    global pressure_start
    
    running = True
    runningII = False
    slider["state"] = "disabled"

#Function to end program output
def stop_program_func():
    global running
    global pressure_start
    global value
    
    slider["state"] = "normal"
    slider.set(y)
    slider["state"] = "disabled"
    running = False

#Function to start manual output      
def start_manual_func():
    global runningII
    global slider_state
    
    runningII = True
    running = False
    slider["state"] = "normal"

#Function to end manual output
def stop_manual_func():
    global runningII
    global slider_state
    
    runningII = False
    slider["state"] = "disabled"

#Function to define the end pressure
def end_func():
    global end_ret
    global end_pressure
        
    if end_ret is not None:
        end_ret.destroy()
        
    end_pressure = Decimal(end.get())
    
    
    end_ret = Label(GUI, text="End Pressure Magnitude Set to: %s" % end_pressure + "psi", fg='red4', background='honeydew4')
    end_ret.grid(row=5, columnspan=3, sticky=W)
     
    end.delete(0,'end')

#Function to define the start pressure
def start_func():
    global start_ret
    global start_pressure
        
    if start_ret is not None:
        start_ret.destroy()
        
    start_pressure = Decimal(start.get())
    
    
    start_ret = Label(GUI, text="Start Pressure Magnitude Set to: %s" % start_pressure + "psi", fg='red4', background='honeydew4')
    start_ret.grid(row=2, columnspan=3, sticky=W)
     
    start.delete(0,'end')
    
    
#Function to define the ramp time
def ramp_func():
    global ramp_ret
    global ramp_time
        
    if ramp_ret is not None:
        ramp_ret.destroy()
        
    ramp_time = Decimal(ramp.get())
    
    
    ramp_ret = Label(GUI, text="Ramp Time Set to: %s" % ramp_time + "sec", fg='red4', background='honeydew4')
    ramp_ret.grid(row=8, columnspan=3, sticky=W)
     
    ramp.delete(0,'end')
    

#Function to reset the elapsed time
def reset_time_func():
    global ramp_time
    global x
    global valueII
    
    x=0
    valueII = x
    varII.set("Current Time Set At: %s" % valueII + " sec")

#Function to reset the pressure
def reset_pressure_func():
    global ramp_time
    global x
    global valueII
    
    value = 0
    
    var.set("Current Pressure Set At: %s" % value + " psig")
    slider["state"] = "normal"
    slider.set(value)
    slider["state"] = "disabled"
    
    value_convert = (value*.034482758)
    hat.a_out_write(channel=channel,value=value_convert,options=options)
    
#Function to exit the program    
def system_exit():
    global center_pos
    global channel
    global options
    global value_convert
    
    if value_convert is None:
        hat.a_out_write(channel=channel,value=0,options=options)
    if value_convert is not None:
        hat.a_out_write(channel=channel,value=0,options=options)

                         
    sys.exit()

#Buttons and Labels
    #Control headers/titles - LABELS
program_control_header= Label(GUI, text="Ramp Up/Down Control Settings",background='honeydew4', font='Helvetica 16 bold underline').grid(row=0, column=0, columnspan=4, padx=150, pady=10)
manual_control_header= Label(GUI, text="Manual Control Settings ",background='honeydew4', font='Helvetica 16 bold underline').grid(row=0, column=4, columnspan=2, pady=10)

    #Start Pressure Buttons and Labels - LABEL ENTRY
start_pressure = Label(GUI, text="Starting Pressure (psi):",background='honeydew4', font = 'Helvetica 10 bold').grid(row=1, column=0, sticky=W)
start_pressure = Button(GUI, text='   Enter Starting Pressure    ', command=start_func, height = 1, width =20, borderwidth=.5, relief='solid').grid(row=1, column=2, sticky=W)
start = Entry(GUI)
start.grid(row=1, column=1, sticky=W)
start_ret = Label(GUI, text="Start Pressure Magnitude Set to: ",background='honeydew4')
start_ret.grid(row=2, columnspan=3, sticky=W)
start.bind('<KP_Enter>', (lambda event: start_func()))
start.bind('<Return>', (lambda event: start_func()))
   
   #End Pressure Buttons and Labels - LABEL ENTRY
end_pressure = Label(GUI, text="Ending Pressure (psi):",background='honeydew4', font = 'Helvetica 10 bold').grid(row=4, column=0, sticky=W)
end_pressure = Button(GUI, text='   Enter Ending Pressure    ', command=end_func, height = 1, width =20, borderwidth=.5, relief='solid').grid(row=4, column=2, sticky=W)
end = Entry(GUI)
end.grid(row=4, column=1, sticky=W)
end_ret = Label(GUI, text="End Pressure Magnitude Set to: ",background='honeydew4')
end_ret.grid(row=5, columnspan=3, sticky=W)
end.bind('<KP_Enter>', (lambda event: end_func()))
end.bind('<Return>', (lambda event: end_func()))

    #Ramp Time Buttons and Labels - LABEL ENTRY
ramp_time= Label(GUI, text="Ramp Time (sec):",background='honeydew4', font = 'Helvetica 10 bold').grid(row=7, column=0, sticky=W)
ramp_time = Button(GUI, text='   Enter Ramp Time    ', command=ramp_func, height = 1, width =20, borderwidth=.5, relief='solid').grid(row=7, column=2, sticky=W)
ramp = Entry(GUI)
ramp.grid(row=7, column=1, sticky=W)
ramp_ret = Label(GUI, text="Ramp Time Set to:",background='honeydew4')
ramp_ret.grid(row=8, columnspan=3, sticky=W)
ramp.bind('<KP_Enter>', (lambda event: ramp_func()))
ramp.bind('<Return>', (lambda event: ramp_func()))

    #Display the current pressure magnitude command signal in real time - LABEL ENTRY
current_output = Label(GUI, textvariable=var, background='gray77', borderwidth=.5, relief='solid', font = 'Helvetica 10 bold')
current_output.grid(row=5, column=4, columnspan=2, rowspan=2, sticky=W, pady=2)

    #Display the current time elapsed in real time - LABEL ENTRY
current_output = Label(GUI, textvariable=varII, background='gray77', borderwidth=.5, relief='solid', font = 'Helvetica 10 bold')
current_output.grid(row=7, column=4, columnspan=2, sticky=W, pady=2)

    #Signal program start/stop - BUTTON COMMAND
Endable_Program_ch01 = Button(GUI, text='Enable Program', command = start_program_func, height = 1, width =18, borderwidth=.5, relief='solid').grid(row=10, column=1, sticky=W)
Disable_Program_ch01 = Button(GUI, text='Disable Program', command = stop_program_func, height = 1, width =20, borderwidth=.5, relief='solid').grid(row=10, column=2, padx=1, sticky=W)

    #Signal manual command start/stop - BUTTON COMMAND
Endable_Manual_ch01 = Button(GUI, text='Enable Manual Control', command = start_manual_func, height = 1, width =20, borderwidth=.5, relief='solid').grid(row=2, rowspan=3, column=4, sticky=W)
Disable_Manual_ch01 = Button(GUI, text='Disable Manual Control', command = stop_manual_func, height = 1, width =20, borderwidth=.5, relief='solid').grid(row=2, rowspan=3, column=5, sticky=W, padx=3, pady=1)
    
    #Manual Position Slider - SLIDER WIDGET
slider=Scale(GUI, from_=0, to=145, orient=HORIZONTAL, resolution=0.01, repeatdelay=1, repeatinterval=1, background='firebrick4', sliderlength=10, borderwidth = 1.5, foreground='black',length=373, width=10, state=slider_state)
slider.grid(row=1,column=4, columnspan=4, rowspan=1, sticky=W)

    #Program Exit - BUTTON COMMAND
exitButton = tk.Button(GUI, text="EXIT NOW",command=system_exit, background='orangered4', highlightbackground='yellow', activebackground='orangered3', borderwidth=.5, relief='solid')
exitButton.grid(row=10, column=0, padx=20)

    #Reset Time - BUTTON COMMAND
resetTimeButton = tk.Button(GUI, text="Reset Time (0.0 sec)",command=reset_time_func, background='RosyBrown4', highlightbackground='RosyBrown4', activebackground='RosyBrown3', borderwidth=.5, relief='solid')
resetTimeButton.grid(row=10, column=5)

    #Reset Pressure - BUTTON COMMAND
resetPressureButton = tk.Button(GUI, text="Reset Pressure (0.0 psig)",command=reset_pressure_func, background='RosyBrown4', highlightbackground='RosyBrown4', activebackground='RosyBrown3', borderwidth=.5, relief='solid')
resetPressureButton.grid(row=10, column=4)


GUI.after(1, scan_func)
GUI.after(1, manual_func)
GUI.mainloop()