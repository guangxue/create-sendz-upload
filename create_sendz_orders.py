import sys
import csv
import pprint
from datetime import datetime

filename = sys.argv[1]

# Column names for writing into csv file
column_names=['Name', 'Email', 'Paid at', 'Total', 'Lineitem quantity', 'Lineitem name', 'Lineitem price','Lineitem sku',
'Shipping Name','Shipping Address1', 'Shipping Address2', 'Shipping Company', 'Shipping City', 'Shipping Zip',
'Shipping Province','Shipping Country','Shipping Phone']



def getEBNumber(orderNum):
    print("[order number]:", orderNum)
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
    row_count = 0
    with open(filename, 'r', encoding='utf-8-sig',errors='ignore') as ebayOrdersFile:
        eBayOrders = csv.DictReader(ebayOrdersFile, restkey='Rest')
        eBayOrderList = list(eBayOrders)
        for r in eBayOrderList:
            if r:
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
                row_count += 1
                
    return sendz_rows, row_count


def write_file(filename, rows):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(rows)


print("[Read -", filename, ']')
sendz_rows, row_count = read_file(filename)

newFileName = "sendz_upload.csv"

if row_count > 1:
    print("[Write -", newFileName, ']')
    write_file(newFileName, sendz_rows)
    print("[Created -", newFileName, ']')

