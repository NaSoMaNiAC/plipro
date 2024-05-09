from tkinter import *
from tkinter import ttk
import datetime as dt
from myclean import *
from tkinter import messagebox

data = Database(db='myclean.db')

count = 0
selected_rowid = 0

def saveRecord():
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())
    refreshData()

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0,'end')
    item_amt.delete(0,'end')
    transaction_date.delete(0,'end')

def fetch_records():
    global count
    for item in tv.get_children():
        tv.delete(item)
    f = data.fetchRecord('select rowid, * from καθαρα')
    count = 0
    for rec in f:
        tv.insert(parent='',index='end', iid=count,values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected,'values')

    try:
        selected_rowid = val[0]
        namevar.set(val[1])
        amptvar.set(val[2])
        dopvar.set(val[3])
    except Exception as ep:
        pass
 
def update_record():
    global selected_rowid
    try:
        data.updateRecord(namevar.get(), amptvar.get(), dopvar.get(), selected_rowid)
        refreshData()
    except Exception as ep:
        messagebox.showerror('ΛΑΘΟΣ', ep)

def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from καθαρα")
    for i in f:
        for j in i:
            messagebox.showinfo('ΤΩΡΙΝΗ ΚΑΤΑΣΤΑΣΗ: ', f"ΣΥΝΟΛΙΚΑ ΕΞΟΔΑ: {j} \nΥΠΟΛΟΙΠΟ ΛΟΓΑΡΙΑΣΜΟΥ: {5000 - int(j)}")

def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

def refreshData():
    fetch_records()

ws = Tk()
ws.title("PersonalFinanceManager")
ws.geometry('1000x600')
 
f = ('Times new roman', 16)
amptvar = IntVar()
dopvar = StringVar()
namevar = StringVar()

f2 = Frame(ws)
f2.pack()

f1 = Frame(ws,padx=10,pady=10)
f1.pack(expand=True,fill=BOTH)

Label(f1,text='ΚΑΤΗΓΟΡΙΑ',font=f).grid(row=0,column=0,sticky=W)
Label(f1,text='ΠΟΣΟ',font=f).grid(row=1,column=0,sticky=W)
Label(f1,text='ΗΜΕΡΟΜΗΝΙΑ',font=f).grid(row=2,column=0,sticky=W)

item_name = Entry(f1,font=f,textvariable=namevar)
item_amt = Entry(f1,font=f,textvariable=amptvar)
transaction_date = Entry(f1,font=f,textvariable=dopvar)

item_name.grid(row=0, column=1,sticky=EW,padx=(10,0))
item_amt.grid(row=1,column=1,sticky=EW,padx=(10,0))
transaction_date.grid(row=2,column=1,sticky=EW,padx=(10,0))

cur_date = Button(f1,text='ΤΩΡΙΝΗ ΗΜΕΡΟΜΗΝΙΑ',font=f,bg='#8B7D6B',command=setDate,width=15)
submit_btn = Button(f1,text='ΑΠΟΘΗΚΕΥΣΗ',font=f,bg='#D2691E',command=saveRecord,fg='white')
clr_btn = Button(f1,text='ΚΑΘΑΡΙΣΜΟΣ',font=f,bg='#DC143C',command=clearEntries,fg='white')
quit_btn = Button(f1,text='ΕΞΟΔΟΣ',font=f,bg='#6495ED',command=lambda:ws.destroy(),fg='white')
total_bal = Button(f1,text="ΧΡΗΜΑΤΙΚΟ ΥΠΟΛΟΙΠΟ",font=f,bg='#486966',command=totalBalance,fg='white')
update_btn = Button(f1,text='ΤΡΟΠΟΠΟΙΗΣΗ',font=f,bg='#BD2A2E',command=update_record,fg='white')
del_btn = Button(f1,text='ΔΙΑΓΡΑΦΗ',font=f,bg='#C2BB00',command=deleteRow,fg='white')

cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

tv= ttk.Treeview(f2, columns=(1,2,3,4),show='headings',height=8, )
tv.pack(side='left')

tv.column(1, anchor=CENTER, stretch=NO, width=60)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="No.")
tv.heading(2,text="ΚΑΤΗΓΟΡΙΑ")
tv.heading(3,text='ΠΟΣΟ')
tv.heading(4,text="ΗΜΕΡΟΜΗΝΙΑ")

tv.bind("<ButtonRelease-1>", select_record)

scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

fetch_records()

ws.mainloop()
