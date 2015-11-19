#!/user/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Jerry'
import time
import sys
import Tkinter as tkinter
import parase
import package


def ToInt(liste):
	tal=0
	for i in range(len(liste)):
		tal+=liste[i]<<((len(liste)-(i+1))*8)
	return tal


def serial_connect():
    if parase.connect_serial(port_set=port_path.get(), baud_rate_set=9600):
        ConnectButton.config(text='connected')
        print "Connected."

def send_input():
    command = int(InputString.get(), 16)  # convert to integer and command must be HEX like 0-f etc.0xff is OK.
    command = parase.send_frame(command, repeat=RepeatString.get())  # list


def receive():
    reading = parase.receive_data()
    global RecievedString
    if reading:
        hex_string = ''
        for i in reading:
            hex_string += hex(i)[2:]+' '
        RecievedField.insert(tkinter.INSERT,RecievedString.get()+hex_string+'\n')
        RecievedField.see('end')
    top.after(1, receive)  # 1ms after to exe the receive

# Main Windows
top = tkinter.Tk()
RWidth=top.winfo_screenwidth()
RHeight=top.winfo_screenheight()
top.minsize(50, 50)
top.maxsize(RWidth, RHeight)
InputString=tkinter.StringVar() #String for the input window
RecievedString=tkinter.StringVar()
RepeatString=tkinter.StringVar()
RepeatString.set('1')
port_path = tkinter.StringVar()
ports = parase.serial_ports()
# Windows default comport
port_path.set(ports[0])
print("Port Can be use:")
for item in ports:
    print item
SendButton = tkinter.Button(top, command=send_input, text="Send", anchor='w')  # Button to send
PortField = tkinter.Entry(top, textvariable=port_path)
PortField.grid(row=90, column=0, sticky="nsew")
ConnectButton = tkinter.Button(top, command=serial_connect, text="Connect")
ConnectButton.grid(row=90, column=1, columnspan=2, sticky="nsew")
InputLabel=tkinter.Label(top,text="Input:")
InputLabel.grid(row=100, column=0, sticky="nsew")
RepeatLabel=tkinter.Label(top,text="Repeats:")

InputField=tkinter.Entry(top,textvariable=InputString)  # Field for user input
RepeatField=tkinter.Entry(top,textvariable=RepeatString)  # Field for user input
RepeatLabel.grid(row=100,column=1)
RepeatField.grid(row=100,column=2)
InputField.grid(row=110, column=0, sticky="nsew") #Show input Field
SendButton.grid(row=110, column=1, columnspan=2, sticky="nsew") #Draw the button
RecievedScrool=tkinter.Scrollbar(top)
RecievedScrool.grid(row=1200,column=1000,sticky="nsew")
RecievedField=tkinter.Text(top,bg='white',yscrollcommand=RecievedScrool.set)
RecievedField.grid(row=1200,columnspan=999,  sticky="nsew")

#RecievedField.pack()
top.columnconfigure(0, weight=1)
top.columnconfigure(1, weight=1)
top.rowconfigure(100, weight=0) # not needed, this is the default behavior
top.rowconfigure(11, weight=0)
top.rowconfigure(120, weight=1)
top.after(1, receive)
top.mainloop()  # Start main loop

