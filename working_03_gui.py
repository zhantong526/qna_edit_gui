'''
Created on August 08, 2018

@author: Maulik Madhavi
'''
import tkinter
from tkinter import ttk,filedialog
import numpy as np
import pandas as pd
import os
from Sent_embed import InferSentClass 
from general_functions import *

class guiclass(tkinter.Frame):
    '''
    classdocs
    '''  
    def reset(self):
        # Set the treeview
        self.tree = ttk.Treeview( self.parent, columns=('Question', 'Answer'))
        self.tree.heading('#0', text='Item')
        self.tree.heading('#1', text='Question')
        self.tree.heading('#2', text='Answer')
        self.tree.column('#1', stretch=tkinter.YES)
        self.tree.column('#2', stretch=tkinter.YES)
        self.tree.column('#0', stretch=tkinter.YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0
        self.already=0


    def __init__(self, parent):
        '''
        Constructor
        '''
        tkinter.Frame.__init__(self, parent)
        self.parent=parent
        self.initialize_user_interface()
        file = 'AVbus_Dialogue_System_template.xlsx'
        xl = pd.ExcelFile(file)
        # Print the sheet names
        print(xl.sheet_names)

		# Load a sheet into a DataFrame by name: df1
        df1 = xl.parse('QA')
        self._Q=list(df1['Question'])
        self._A=list(df1['Answer'])

        self._c=InferSentClass()
        self._message_embed=np.zeros((len(self._Q),4096))
        for var in range(len(self._Q)):
            print(var+1)
            x=self._c.run(self._Q[var])[0]
            x=x/np.linalg.norm(x)
            self._message_embed[var]=x


    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("Data Editing Interface")       
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.config(background="white")
        self.already=0

        # Define the different GUI widgets
        self.Q_label = tkinter.Label(self.parent, bg="white", text = "Question:")
        self.Q_entry = tkinter.Entry(self.parent)
        self.Q_label.grid(row = 0, column = 0, sticky = tkinter.W)
        self.Q_entry.grid(row = 0, column = 1)

        self.A_label = tkinter.Label(self.parent, bg="white", text = "Answer:")
        self.A_entry = tkinter.Entry(self.parent)
        self.A_label.grid(row = 1, column = 0, sticky = tkinter.W)
        self.A_entry.grid(row = 1, column = 1)

        self.R_label = tkinter.Label(self.parent, bg="white", text = "Select (0 for your custom answer): ")
        self.R_entry = tkinter.Entry(self.parent)
        self.R_label.grid(row = 2, column = 0, sticky = tkinter.W)
        self.R_entry.grid(row = 2, column = 1)

        self.submit_button = tkinter.Button(self.parent, text = "Insert", command = self.insert_data)
        self.submit_button.grid(row = 2, column = 3, sticky = tkinter.W)

        self.compare_button = tkinter.Button(self.parent, text = "Compare", command = self.compare_data)
        self.compare_button.grid(row = 1, column = 3, sticky = tkinter.W)
        self.exit_button = tkinter.Button(self.parent, text = "Save", command = self.createfile_close)
        self.exit_button.grid(row = 0, column = 3)

        self.tree = ttk.Treeview( self.parent, columns=('Question', 'Answer'))
        self.tree.heading('#0', text='Item')
        self.tree.heading('#1', text='Question')
        self.tree.heading('#2', text='Answer')
        self.tree.column('#1', stretch=tkinter.YES)
        self.tree.column('#2', stretch=tkinter.YES)
        self.tree.column('#0', stretch=tkinter.YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0
    
    def createfile_close(self):
         print('inside create')
         df = pd.DataFrame({'question': self._Q, 'Answer': self._A})
         df.to_excel('test.xlsx', sheet_name='sheet1', index=False)


    def insert_data(self):
        """
        Insertion method.
        """
        #self.treeview.insert('', 'end', text="Item_"+str(self.i), values=(self.Q_entry.get()+"", self.A_entry.get()))
        # Increment counter
        #self.i = self.i + 1
        #self.i=0
        if self.already!=1:

            indx=int(self.R_entry.get())
	        #self.treeview.insert('', 'end', text="Item_"+str(self.i), values=(self.Q_entry.get()+"", self._Aall[indx]))
	        #print(type(self.Q_entry.get()))
	        #print(type(self._Aall[indx-1]))
	        #print(self.Q_entry.get())
	        #print(self._Aall[indx-1])
            self._Q+=[str(self.Q_entry.get())]

            if indx<=5 and indx>=1:
                self._A+=[str(self._Aall[indx-1])]
            else:
                self._A+=[self.A_entry.get()]

            x=self._c.run(self._Q[-1])[0]
            #print(self._Q)
            #print(self._A)
            x=x/np.linalg.norm(x)        
            #self._message_embed.append(x)
            self._message_embed=np.concatenate((self._message_embed, [x]))
           #print(self._message_embed.shape)
            df = pd.DataFrame({'question': self._Q, 'Answer': self._A})
            df.to_excel('test.xlsx', sheet_name='sheet1', index=False)


            # Set the treeview
            # Set the treeview
            self.tree = ttk.Treeview( self.parent, columns=('Question', 'Answer'))
            self.tree.heading('#0', text='Item')
            self.tree.heading('#1', text='Question')
            self.tree.heading('#2', text='Answer')
            self.tree.column('#1', stretch=tkinter.YES)
            self.tree.column('#2', stretch=tkinter.YES)
            self.tree.column('#0', stretch=tkinter.YES)
            self.tree.grid(row=4, columnspan=4, sticky='nsew')
            self.treeview = self.tree
            # Initialize the counter
            self.i = 0
	    
        else:
            self.tree = ttk.Treeview( self.parent, columns=('Question', 'Answer'))
            self.tree.heading('#0', text='Item')
            self.tree.heading('#1', text='Question')
            self.tree.heading('#2', text='Answer')
            self.tree.column('#1', stretch=tkinter.YES)
            self.tree.column('#2', stretch=tkinter.YES)
            self.tree.column('#0', stretch=tkinter.YES)
            self.tree.grid(row=4, columnspan=4, sticky='nsew')
            self.treeview = self.tree
            # Initialize the counter
            self.i = 0
            self.already=0

            self.treeview.insert('', 'end', text="0", values=("Question already exists", "Answer already exists"))
            self.already=0
    
    def compare_data(self):
        """
        Compare with previous data
        """        
        #self.treeview.insert('', 'end', text="Item_"+str(self.i), values=(self.Q_entry.get()+"", self.A_entry.get()))
        
        # Set the treeview
        self.tree = ttk.Treeview( self.parent, columns=('Question', 'Answer'))
        self.tree.heading('#0', text='Item')
        self.tree.heading('#1', text='Question')
        self.tree.heading('#2', text='Answer')
        self.tree.column('#1', stretch=tkinter.YES)
        self.tree.column('#2', stretch=tkinter.YES)
        self.tree.column('#0', stretch=tkinter.YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0

        print(self.Q_entry.get())
        print("comparing now : "+self.Q_entry.get())
        tic()
        # Load spreadsheet        
        x=self._c.run(self.Q_entry.get())[0]
        x=x/np.linalg.norm(x)
        matching=np.dot(self._message_embed,x)

        ind = np.argmax(matching)
        ind1=np.argsort(-1*matching)

        print('The matched query is :' + self._Q[ind])
        print('The matching score is :' + str(matching[ind]))
        toc()
        self._Qall=[]
        self._Aall=[]
        for i in range(5):
            ind=ind1[i]
            self._Qall.append(self._Q[ind])
            self._Aall.append(self._A[ind])
            if (self._Q[ind]==self.Q_entry.get()) and (self._A[ind]==self.A_entry.get()):
                self.already=1
            self.treeview.insert('', 'end', text="Item_"+str(i+1), values=(self._Q[ind]+"", self._A[ind]))
	

        self.i = 0

def main():    
    root=tkinter.Tk()
    root.geometry("400x300")
    d=guiclass(root)
    root.mainloop()

if __name__=="__main__":    
    main()
