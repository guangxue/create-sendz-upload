import sys
import csv
import pprint
from datetime import datetime


filename = sys.argv[1]

print("filename: ", filename) #Column names for reading from csv file
read_cols = ['Order Number', 'Paid On Date', 'Total Price', 'Quantity', 'Item Title', 'Sold For', 'Custom Label',
    'Post To Name', 'Post To Address 1', 'Post To Address 2', 'Post To City', 'Post To Postal Code','Post To State', 'Post To Phone']

# Column names for writing into csv file
column_names=['Name', 'Email', 'Paid at', 'Total', 'Lineitem quantity', 'Lineitem name', 'Lineitem price','Lineitem sku',
'Shipping Name','Shipping Address1', 'Shipping Address2', 'Shipping Company', 'Shipping City', 'Shipping Zip',
'Shipping Province','Shipping Country','Shipping Phone']



def getEBNumber(orderNum):
    on = orderNum.split('-')
    if len(on) == 3:
        return 'EB'+on[2]

def getPriceNumber(orderPrice):
    price_list = orderPrice.split('$')
    if len(price_list) == 2:
        return price_list[1]

def getPostAddress(address1, address2):
    if "ebay:" in address1:
        return address2
    else:
        return address1


def getDateFormat(dstr):
    if dstr.strip():
        d = datetime.strptime(dstr, '%d-%b-%y')
        d2 = d.strftime("%d/%m/%y")
        return str(d2)

def read_file(filename):
    sendz_rows = []
    with open(filename) as ebayOrdersFile:
        eBayOrders = csv.DictReader(ebayOrdersFile)
        eBayOrderList = list(eBayOrders)
        for r in eBayOrderList:
            if len(r['Order Number']) > 6:
                urow = {}
                urow['Name']=getEBNumber(r['Order Number'])
                urow['Email']= ''
                urow['Paid at']=getDateFormat(r['Paid On Date'])
                urow['Total']=getPriceNumber(r['Total Price'])
                urow['Lineitem quantity']=r['Quantity']
                urow['Lineitem name']=r['Item Title']
                urow['Lineitem price']=getPriceNumber(r['Sold For'])
                urow['Lineitem sku']=r['Custom Label']
                urow['Shipping Name']=r['Post To Name']
                urow['Shipping Address1']=getPostAddress(r['Post To Address 1'], r['Post To Address 2'])
                urow['Shipping Address2']=''
                urow['Shipping Company']=''
                urow['Shipping City']=r['Post To City']
                urow['Shipping Zip']=r['Post To Postal Code']
                urow['Shipping Province']=r['Post To State']
                urow['Shipping Country']='AU'
                urow['Shipping Phone']=r['Post To Phone']
                sendz_rows.append(urow)
    return sendz_rows


def write_file(filename, rows):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(rows)


print("Start reading file: ", filename)
sendz_rows = read_file(filename)

newFileName = "sendz_upload.csv"

print("writing to file: ", newFileName)
write_file(newFileName, sendz_rows)

print("File:", newFileName, " created.")

