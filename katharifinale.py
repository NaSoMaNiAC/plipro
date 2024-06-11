#TA MODULES KAI H ENOSI THS DATABASE ME TON KODIKA
from tkinter import *
from tkinter import ttk
import datetime as dt
from myclean import *
from tkinter import messagebox
import pandas as pd 
import sqlite3
import numpy as np
import matplotlib.pyplot as plt 

#METAVLITES TOU KODIKA GLOBALS GIA NA XRISIMOPOIOUNTE SE OLO TON KODIKA
data = Database(db='myclean.db')
count = 0
selected_rowid = 0


#SINARTISI GIA NA EISAGOUME NEA EGGRAFI
def saveRecord():
    try:
        #ELENXOS GIA NA EINAI TO POSO ARITHMOS KAI OXI GRAMMA
        amount = float(item_amt.get())
        if is_expense.get():
            amount = -amount
    except ValueError:
        messagebox.showerror("ΛΑΘΟΣ ΠΑΡΑΚΑΛΩ ΕΙΣΑΓΕΤΕ ΝΟΥΜΕΡΑ")
        return
    
    #ELENXOS GIA SOSTI IMEROMINIA
    try:
        dt.datetime.strptime(transaction_date.get(), "%d %B %Y")
    except ValueError:
        messagebox.showerror("ΠΑΡΑΚΑΛΩ ΕΙΣΑΓΕΤΕ ΣΩΣΤΑ  ΗΜΕΡΑ ΜΗΝΑ ΕΤΟΣ.")
        return

    data.insertRecord(item_name=item_name.get(), item_price=amount, purchase_date=transaction_date.get())
    refreshData()    
#SINARTISI GIA NA VAZOUME IMEROMINIA KAI MALISTA TIN TORINI
def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')
#SINARTISI GIA TON KATHARISMO 
def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    global count
    for item in tv.get_children():
        tv.delete(item)
    f = data.fetchRecord('select rowid, * from καθαρα')
    count = 0
    for rec in f:
        tv.insert(parent='', index='end', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
#SINARTISI GIA NA EPILEGOUME MIA EGGRAFI
def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        namevar.set(val[1])
        amptvar.set(val[2])
        dopvar.set(val[3])
    except Exception as ep:
        pass
 #SINARTISI GIA TROPOPOIISI EGGRAFWN
def update_record():
    global selected_rowid
    try:
        data.updateRecord(namevar.get(), amptvar.get(), dopvar.get(), selected_rowid)
        refreshData()
    except Exception as ep:
        messagebox.showerror('ΛΑΘΟΣ', ep)
#SINARTISI GIA NA IPOLOGIZEI TO SINOLO TWN EGGRAFWN
def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from καθαρα")
    for i in f:
        for j in i:
            messagebox.showinfo('ΤΩΡΙΝΗ ΚΑΤΑΣΤΑΣΗ: ', f"ΣΥΝΟΛΙΚΑ ΕΣΟΔΑ: {j} \nΥΠΟΛΟΙΠΟ ΛΟΓΑΡΙΑΣΜΟΥ: {0 + int(j)}")
#SINARTISI GIA NA DIAGRAFOUME MIA SEIRA
def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

def refreshData():
    fetch_records()
#SINARTISI GIA EXCEL
def export():
    conn = sqlite3.connect('myclean.db')
    df = pd.read_sql_query('SELECT * FROM καθαρα', conn)

    df.to_excel("myclean.xlsx", index=False)
    conn.close
#SINARTISI GIA MATPLOT GRAPH
def graph():
    conn = sqlite3.connect('myclean.db')
    df = pd.read_sql_query('SELECT * FROM καθαρα', conn)
    conn.close()

    if df.empty:
        messagebox.showinfo('ΔΕΝ ΥΠΑΡΧΟΥΝ ΣΤΟΙΧΕΙΑ')
        return
    
    category_totals = df.groupby('item_name')['item_price'].sum()
    plt.figure(figsize=(10, 6))
    category_totals.plot(kind='bar', color='#007FFF')
    plt.title('ΣΥΝΟΛΑ ΕΞΟΔΩΝ')
    plt.xlabel('ΚΑΤΗΓΟΡΙΑ')
    plt.ylabel('ΣΥΝΟΛΙΚΟ ΠΟΣΟ')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

# GUI 
ws = Tk()
ws.title("PersonalFinanceManager")
ws.geometry('1000x600')
#ΜΕΤΑΒΛΗΤΕΣ ΓΙΑ ΤΑ ΚΟΥΜΠΙΑ
f = ('Times new roman', 16)
amptvar = IntVar()
dopvar = StringVar()
namevar = StringVar()
is_expense = BooleanVar()

f2 = Frame(ws)
f2.pack()

f1 = Frame(ws, padx=10, pady=10)
f1.pack(expand=True, fill=BOTH)

Label(f1, text='ΚΑΤΗΓΟΡΙΑ', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ΠΟΣΟ', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='ΗΜΕΡΟΜΗΝΙΑ', font=f).grid(row=2, column=0, sticky=W)

item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amptvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

#ΤΟ ΚΟΥΜΠΙ ΓΙΑ ΤΟ ΑΝ ΕΙΝΑΙ ΕΞΟΔΟ 
expense_checkbtn = Checkbutton(f1, text="ΕΞΟΔΑ", font=f, variable=is_expense)
expense_checkbtn.grid(row=3, column=0, sticky=W, padx=(10, 0))
#ΤΑ ΚΟΥΜΠΙΑ ΤΗΣ ΕΦΑΡΜΟΓΗΣ ΚΑΙ ΟΙ ΕΝΤΟΛΕΣ ΤΟΥΣ ΟΤΑΝ ΤΑ ΠΑΤΗΣΕΙΣ
cur_date = Button(f1, text='ΤΩΡΙΝΗ ΗΜΕΡΟΜΗΝΙΑ', font=f, bg='#8B7D6B', command=setDate, width=15)
submit_btn = Button(f1, text='ΑΠΟΘΗΚΕΥΣΗ', font=f, bg='#D2691E', command=saveRecord, fg='white')
clr_btn = Button(f1, text='ΚΑΘΑΡΙΣΜΟΣ', font=f, bg='#DC143C', command=clearEntries, fg='white')
quit_btn = Button(f1, text='ΕΞΟΔΟΣ', font=f, bg='#6495ED', command=lambda: ws.destroy(), fg='white')
total_bal = Button(f1, text="ΧΡΗΜΑΤΙΚΟ ΥΠΟΛΟΙΠΟ", font=f, bg='#486966', command=totalBalance, fg='white')
update_btn = Button(f1, text='ΤΡΟΠΟΠΟΙΗΣΗ', font=f, bg='#BD2A2E', command=update_record, fg='white')
del_btn = Button(f1, text='ΔΙΑΓΡΑΦΗ', font=f, bg='#C2BB00', command=deleteRow, fg='white')
export_btn = Button(f1, text='Export to Excel', font=f, bg='#F7F7F7', command=export)
matplot_btn = Button(f1, text='Show to Graph', font=f, bg='#8DB6CD', command=graph)

#Η ΤΟΠΟΘΕΤΗΣΗ ΤΩΝ ΚΟΥΜΠΙΩΝ
cur_date.grid(row=4, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))
export_btn.grid(row=3, column=3, sticky=EW, padx=(10, 0))
matplot_btn.grid(row=3, column=2, sticky=EW, padx=(10, 0))

#ΤΟ TREEVIEW INTERFACE
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side='left')

tv.column(1, anchor=CENTER, stretch=NO, width=60)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="No.")
tv.heading(2, text="ΚΑΤΗΓΟΡΙΑ")
tv.heading(3, text='ΠΟΣΟ')
tv.heading(4, text="ΗΜΕΡΟΜΗΝΙΑ")

tv.bind("<ButtonRelease-1>", select_record)
#SCROLLBAR OTAN EXOUME POLLES EGGRAFES
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)
#FETCH RECORDS GIA ANANEOSI OPOTE ANOIGOUME TO PARATHIRO
fetch_records()
#MAINLOOP GIA TO TKINTER GUI NA MHN FREEZAREI STO PRWTO CLICK
ws.mainloop()

