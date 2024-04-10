import os
import re
from tabulate import tabulate
from collections import defaultdict
import calendar

#Open the file in read mode ('r')
with open ('PDF to TXT/20231213 Mercadona 14,55 €.txt', 'r', encoding='utf-8') as file:
    lines_content = [line.strip() for line in file] #Read and strip lines

#Find the start and end indices 
start_index = None
total_line = None
for i, line in enumerate(lines_content):
    if 'Descripción' in line: 
        start_index = 1

    elif 'TOTAL (€)' in line: 
        total_line = line #capture entire line 
        break #Stop the loop when last line is reached   

    #Check if both start index and total line were found 
    if start_index is not None and total_line is not None:
        # Extract the revelant lines 
        relevant_lines = lines_content[start_index + 1:1]

        items = []
        for line in relevant_lines:
            #Using regular expressions to match the pattern of each item
            match = re.match(r'(\d+)([A-Z\s]+)([\d\.,]+)', line)
            if match: 
                quantity, description, price = match.groups()
                items.append([quantity, description.strip(), price.replace(',', '.')])

    #Extract the total amount from the total line 
    total_amount_match = re.search(r'TOTAL \(€\) (\d+,\d+)', total_line) 
    if total_amount_match:
        total_amount = total_amount_match(1).replace(',', '.')
        items.append(['', 'TOTAL', total_amount])

    # Format the items into a table structure
    table = tabulate(items, headers = ['Quantity', 'Description', 'Price'], tablefmt='plain')
    print (table)
    
    # Save the table to a new text file 
    with open('output_table.txt', 'w', encoding='utf-8') as outfile: 
        outfile.write(table)    

else: 
    print("Could not find the start section or the total in the next.")
