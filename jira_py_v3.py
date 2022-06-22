from jira import JIRA
import tkinter as tk
from fillpdf import fillpdfs
import csv
import tempfile

#b9c7837a-b330-14b6-7a2d-b8kjdc0d93j4
#1j3buF2dEsagR06o8Hg4
#user api token: wa6oM1DpwpBegq52GPoA02E8
jira = JIRA("https://westmedwa.atlassian.net", basic_auth=("joshua@westmedwa.com","wa6oM1DpwpBegq52GPoA02E8"))
master = tk.Tk()
master.title("PyJira")

tsc = jira.attachment(11304)
#g serial_date = jira.attachment(11338)

tsc_file = tsc.get()

with open("tsc.pdf", 'wb') as f:
    f.write(tsc_file)

#g with open("serialDate.csv","wb") as f:
#g    f.write(serial_date.get())

#g csv_file = csv.reader(open('serialDate.csv', "r"), delimiter=",")
#g csv_file = csv.reader(open('sn_date.csv', "r"), delimiter=",")

#pdf_template = current_dir + "/TSC_pyfiller.pdf"

pdf_template = "tsc.pdf"

with open('sn_date.csv', 'r') as file:
    csv_file = csv.reader(file)
    sn = []
    pdate = []
    for row in csv_file:
        # print(row)
        sn.append(row[0])
        pdate.append(row[1])
        # print(sn, pdate)

    list_len = len(sn)
    # for row in range(0, list_len):
        # print(sn[row], pdate[row])


    # for row in range(0, list_len):
        # print(row, sn[row], pdate[row])
        # if num2[row] == find_num:
            # print(txt3[row])



def findProcDate(s_n):
    for row in range(0, list_len):
        #print (row)
        if sn[row] == s_n:
            return pdate[row]
            
       
            


p1 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=1)
p2 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=2)
p3 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=3)
p4 = fillpdfs.get_form_fields(pdf_template, sort=False, page_number=4)


def onClick():
    global issues
    issues = str(e1.get())
    master.quit()


tk.Label(master, text="Enter JQL query").grid(row=0)


e1 = tk.Entry(master)

e1.grid(row=0, column=1)

tk.Button(master,text='Enter', command = onClick ).grid(row=3,column=1,sticky=tk.W,pady=4)


tk.mainloop()

print("JQL query: " + "\"" + issues + "\"")



for issue in jira.search_issues(issues):
    key = issue.key

    if 'RPH' in key:

        assignee = issue.fields.assignee.displayName
        initals = ''.join([x[0].upper() for x in assignee.split(' ')])
        s_n = issue.fields.customfield_10166
        drug_lib = issue.fields.customfield_10172
        proc_date = findProcDate(s_n)
        p_2 = round(issue.fields.customfield_10173,1)
        p_5 = round(issue.fields.customfield_10174,1)
        p_9 = round(issue.fields.customfield_10175,1)
        pmax = round(issue.fields.customfield_10176,1)
        pmin = round(issue.fields.customfield_10177,1)
        pdoor = round(issue.fields.customfield_10178,1)
        acc = int(issue.fields.customfield_10179)
        airval = issue.fields.customfield_10182
        tdif = issue.fields.customfield_10101
        hsp = issue.fields.customfield_10183.value
        waterval = issue.fields.customfield_10188
        tsc_date = issue.fields.customfield_10015
        update_date = issue.fields.updated[:10]
        update_date_2 = str(int(tsc_date[:4])+2) + '-' + tsc_date[5:]

    elif 'SCGH' in key:
        assignee = issue.fields.assignee.displayName
        initals = ''.join([x[0].upper() for x in assignee.split(' ')])
        drug_lib = issue.fields.customfield_10155
        s_n = issue.fields.customfield_10187

        proc_date = findProcDate(s_n)
    
        p_2 = round(issue.fields.customfield_10156,1)
        p_5 = round(issue.fields.customfield_10157,1)
        p_9 = round(issue.fields.customfield_10184,1)
        pmax = round(issue.fields.customfield_10158,1)
        pmin = round(issue.fields.customfield_10159,1)
        pdoor = round(issue.fields.customfield_10160,1)
        acc = int(issue.fields.customfield_10161)
        airval = issue.fields.customfield_10163
        tdif = issue.fields.customfield_10185
        hsp = issue.fields.customfield_10186.value
        waterval = issue.fields.customfield_10194

        tsc_date = issue.fields.customfield_10193
        update_date = issue.fields.updated[:10]
        update_date_2 = str(int(tsc_date[:4])+2) + '-' + tsc_date[5:]
        p4.update({'Textfield-15':'Air in line sensor replaced, Drug Lib: '+ drug_lib})

    # print(hsp, proc_date, s_n, key)

    p1.update({'Textfield':' ' + hsp,'Textfield-1':' ' + proc_date[-4:],'Serial No':' ' + s_n,'Equipment No':' ' + key,})
    

    p2.update({'Textfield-3':p_2,'Textfield-4':p_5,'Textfield-5':p_9,'Textfield-6':pmin,'Pmax 18  25 bar-0':pmax,'Textfield-7':pdoor,'Textfield-8':acc})

    p3.update({'Water value 600 mV-0':int(waterval),'Textfield-11':tdif,'Air value  100 mV-0':int(airval)})

    p4.update({'Textfield-16':' ' + assignee,'Textfield-17':' ' + initals,'Textfield-18':' ' + tsc_date,'Textfield-19':' ' + update_date_2,'Textfield-20':' ' + hsp})

    p2.update(p1)
    p3.update(p2)
    p4.update(p3)

    fillpdfs.write_fillable_pdf(pdf_template,'TSC '+s_n+'.pdf', p4)
    fillpdfs.flatten_pdf('TSC '+s_n+'.pdf', 'TSC '+s_n+'.pdf', as_images=False)
    jira.add_attachment(issue=issue, attachment= 'TSC '+s_n+'.pdf')
