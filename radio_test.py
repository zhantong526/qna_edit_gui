
from tkinter import * 
a=tkinter() # obj "a" is build
a.geometry ("500*300")

a.configure(bg="blue")

def func():  #command call here
		s="You have selected option"+str(v1.get()) #"v1.get" took a value from radiobutton
		l1.configure(text=s) #put the string into label
		
v1=InVar()
r1=Radiobutton(a,text="Option 1",bg="yellow", font=(None,20), variable=v1,value=10,command=func)
r1=grid() 

l1=Label(a,font=(None,20))
l1.grid()
a=mainloop()