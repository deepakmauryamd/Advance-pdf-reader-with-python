'''
From the annual reports and other company documents in the shared folder, extract financial data - Net Revenue, Total Revenue, EBITDA, EBIT, Net Income, Total Assets, Total debt (or liabilities), total equity, Retained earnings, etc. 
Store data in database and report the results in PDF format. Create interactive webpage to display and search these pdf output reports.
'''
import PyPDF2
import tabula
import pandas
import csv, sqlite3

cnx = sqlite3.connect("db.sqlite")


pdfobject = open('BHARTI-AIRTEL-standalone-balance-sheet (1).pdf','rb')
path = 'BHARTI-AIRTEL-standalone-balance-sheet (1).pdf'
pdfReader = PyPDF2.PdfFileReader(pdfobject)

'''
if pdfReader.isEncrypted:
    pdfReader.decrypt('')
'''

    
total_pages = pdfReader.numPages

for page in range(total_pages):
    page = pdfReader.getPage(page) 

    content = page.extractText()
    #content = "".join(content.split("|"))

    #print(content)
    df = tabula.read_pdf(path,output_format="dataframe",encoding="utf-8",java_options=None,
                         pandas_options={'header': None},multiple_tables=False)
    dd = tabula.convert_into(path,"output.csv",output_format="csv")
    #print(type(df))
    print(df)
    
with open("output.csv",newline='') as f:
    reader = csv.reader(f)
    next(reader)
    next(reader)
    next(reader)
    
    with open("newfile.csv",'w',newline='') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(['Particulars','Notes','As of March 31,2017','As of March 31,2016','As of March 31,2015'])
        for line in reader:
            csv_writer.writerow(line)


dfs = pandas.read_csv("newfile.csv")
dfs.to_sql('Alldata',cnx)
'''
select * from Alldata
where Particulars="Total Liabilities"   
'''


    
