# import camelot

file = 'media/test_sbPw1nb.pdf'
# # print(file)
# table = camelot.read_pdf(file, pages='2')


# print("Total tables extracted:", table.n)
# print(table[0].df)

import tabula
import os
tables = tabula.read_pdf(file, pages="all")
# save them in a folder
folder_name = "tables"
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)
# iterate over extracted tables and export as excel individually
for i, table in enumerate(tables, start=1):
    table.to_excel(os.path.join(folder_name, f"table_{i}.xlsx"), index=False)