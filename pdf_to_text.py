from pdfminer.high_level import extract_pages
from secrets import secret

# add key for shipping 
tot_dict = {'OrderID': [], 'Item': [], 'Unit_Price': [], 'Quantity': [], 'Total': [], 'Date': []}

def build_dict(path):
    page_dict = {}
    for page in extract_pages(path):
        for i, element in enumerate(page):
            try:
                page_dict[i] = element.get_text()
            except:
                pass
    if len(page_dict) <= 67:

        for i in range(len(page_dict)):
            if 'Order #' in page_dict[i]:
                order_id = int(page_dict[i].split('Order ')[1].lstrip('#').rstrip('\n'))
            if 'Order Placed: ' in page_dict[i]:
                date = page_dict[i].split(': ')[1].split('\n')[0]
            if page_dict[i] == 'Qty\n':
                tot_dict['Quantity'].append(int(page_dict[i+4].rstrip('\n')))
                tot_dict['Item'].append(page_dict[i+5].rstrip('\n'))
                tot_dict['Unit_Price'].append(float(page_dict[i+6].rstrip('\n').lstrip('$')))
                tot_dict['Total'].append(float(page_dict[i+7].rstrip('\n').lstrip('$')))
                tot_dict['Date'].append(date)
                tot_dict['OrderID'].append(order_id)
    if len(page_dict) > 67:
        for i in range(len(page_dict)):
            if 'Order #' in page_dict[i]:
                order_id = int(page_dict[i].split('Order ')[1].lstrip('#').rstrip('\n'))
            if 'Order Placed: ' in page_dict[i]:
                date = page_dict[i].split(': ')[1].split('\n')[0]
            if page_dict[i] == 'Qty\n':
                tot_dict['Quantity'].append(int(page_dict[i+3].rstrip('\n')))
                tot_dict['Quantity'].append(int(page_dict[i+4].rstrip('\n')))
                tot_dict['Item'].append(page_dict[i+5].rstrip('\n'))
                tot_dict['Item'].append(page_dict[i+6].rstrip('\n'))
            if page_dict[i] == 'Unit Price\n':
                tot_dict['Unit_Price'].append(float(page_dict[i+2].rstrip('\n').lstrip('$')))
                tot_dict['Unit_Price'].append(float(page_dict[i+3].rstrip('\n').lstrip('$')))
                tot_dict['Total'].append(float(page_dict[i+4].rstrip('\n').lstrip('$')))
                tot_dict['Total'].append(float(page_dict[i+5].rstrip('\n').lstrip('$')))
                tot_dict['Date'].append(date)
                tot_dict['OrderID'].append(order_id)
    return


if __name__ == "__main__":
    import os
    import pandas as pd

    directory = os.fsencode('data')
    n = 0
    for _file in os.listdir(directory):
        n +=1
        filename = os.fsdecode(_file)
        build_dict('data/' + filename)
        print(n)
    
    df = pd.DataFrame(tot_dict)
    df.to_csv(secret['outfile'])
