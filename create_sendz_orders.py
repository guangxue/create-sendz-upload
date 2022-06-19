import sys
import csv
import pprint
import re
from datetime import datetime, date


original_file = sys.argv[1]

# Column names for writing into csv file
column_names=['Name', 'Email', 'Paid at', 'Total', 'Lineitem quantity', 'Lineitem name', 'Lineitem price','Lineitem sku',
'Shipping Name','Shipping Address1', 'Shipping Address2', 'Shipping Company', 'Shipping City', 'Shipping Zip',
'Shipping Province','Shipping Country','Shipping Phone']


def getFinalFilename():
    td = date.today()
    today = td.strftime("%Y.%m.%d")
    final_filename = today+".csv"
    print(f"[filename]: {final_filename}")
    return final_filename

def matchOrderNumber(numstr):
    pattern = re.compile("^[0-9]{2}-[0-9]{5}-[0-9]{5}")
    return pattern.match(numstr)


def getEBNumber(orderNum):
    #print("[order number]:", orderNum)
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

def csv_reformat(original_file):
    # send column must match pattern "06-08743-80550"
    pattern = re.compile("^[0-9]{2}-[0-9]{5}-[0-9]{5}")
    reformatted_filename = 'eBay_OrdersReport_reformatted.csv'
    with open(original_file, 'r', encoding='utf-8-sig', errors='ignore') as eBayReport:
        # read file row by row
        rows = csv.reader(eBayReport)
        for r in rows:
            # if 2nd column is NOT empty & match pattern "06-08743-80550" || 2nd column name is "Order Number"
            if (r[1] and pattern.match(r[1])) or r[1] == 'Order Number':
                # create a reformatted csv and write the row by row with "append" mode
                with open(reformatted_filename, mode='a') as untitled_file:
                    untitled_filewriter = csv.writer(untitled_file, delimiter=',')
                    untitled_filewriter.writerow(r)
    return reformatted_filename


def create_dictRows(filename):
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


def create_sendz_file(filename):
    dictRows, rowCounts = create_dictRows(filename)
    print("[count]: ", rowCounts)
    final_filename = getFinalFilename()
    if rowCounts > 1:
        with open(final_filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=column_names)
            writer.writeheader()
            writer.writerows(dictRows)


reformatted_filename = csv_reformat(original_file)
print(f'[reformatted]: {reformatted_filename}')
create_sendz_file(reformatted_filename)
