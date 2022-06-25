from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from pdf2image import convert_from_bytes
import pandas as pd
import datetime

def create_papers(filename):
    table = pd.read_csv(filename)
    
    # Creating full name part
    name_column = table['Имя получателя']
    patronymic_column = table['Отчество']
    fio_column = name_column + ' ' + patronymic_column

    # Creating address part
    address_column = table['Адрес доставки']
    city_column = table['Город доставки']
    full_address_column = address_column + ', ' + city_column
    index_column = table['Индекс']
    columns = [fio_column, full_address_column, index_column]
    quantity_of_customers = len(fio_column)

    ready_for_print_orders = []

    i = 0
    while i < quantity_of_customers:
        fio = columns[0][i]
        fio_list = fio.split(" ")
        fio = fio_list[1] + ' ' + fio_list[0]
        if fio_list[2] != '-': fio += ' ' + fio_list[2]
        address = columns[1][i]
        full_info = [fio, address, index_column[i]]
        ready_for_print_orders.append(full_info)
        i += 1

    # Creating PDF part

    pdfmetrics.registerFont(TTFont('TNR', 'staff_only/Roboto-Regular.ttf'))
    style = getSampleStyleSheet()
    styleTest = ParagraphStyle('main_style',
                            fontName="TNR",
                            fontSize=10,
                            parent=style['Heading2'],
                            spaceAfter=14,
                            wordWrap="allowWidows",
                            )

    indexes = []
    names = []
    address = []

    for i in range(len(ready_for_print_orders)):
        names.append(ready_for_print_orders[i][0])
        indexes.append(ready_for_print_orders[i][2])
        address.append(ready_for_print_orders[i][1])

    little = 50
    big = 160

    orders_quantity = len(names)
    number_of_lists = (orders_quantity // 20)+1
    not_enough = number_of_lists*20 - orders_quantity

    for i in range(not_enough):
        names.append(' ')
        indexes.append(' ')
        address.append(' ')

    for i in range(len(names)):
        names[i] = Paragraph(names[i], styleTest)
        indexes[i] = Paragraph(str(indexes[i]), styleTest)
        address[i] = Paragraph(address[i], styleTest)

    komu = Paragraph('Кому', styleTest)
    kuda = Paragraph('Куда', styleTest)
    index = Paragraph('Индекс', styleTest)

    i = 0
    list_num = 0
    
    while list_num < number_of_lists:
        data = []
        for j in range(0,19,4):
            data.append([komu,names[i+j],komu,names[i+(j+1)],komu,names[i+(j+2)],komu,names[i+(j+3)]])
            data.append([kuda,address[i+j],kuda,address[i+(j+1)],kuda,address[i+(j+2)],kuda,address[i+(j+3)]])
            data.append([index,indexes[i+j],index,indexes[i+(j+1)],index,indexes[i+(j+2)],index,indexes[i+(j+3)]])

        # Building layout for PDF
        style_for_table = [('GRID',(0,0),(-1,-1),0,colors.lightgrey)]
        cascades_first = []
        cascades_second = []
        for j in range(0, 13, 3):
            for k in range(0, 7, 2):
                cascades_first.append((k, j))
        
        for j in range(2, 15, 3):
            for k in range(1, 8, 2):
                cascades_second.append((k, j))

        for n in range(len(cascades_first)):
            style_for_table.append(('BOX', cascades_first[n], cascades_second[n], 0, colors.black))

        t = Table(data, colWidths=[little if i%2!=0 else big for i in range(1,9)],style=style_for_table)

        # Building jpg
        canvas = Canvas("papers_"+str(list_num+1)+".pdf", pagesize=(A4[1],A4[0]))
        canvas.setFont('TNR', 32)
        t.wrapOn(canvas, 2.9*inch, 1.6*inch)
        t.drawOn(canvas, 0, 0)
        image = convert_from_bytes(canvas.getpdfdata(), poppler_path="poppler-0.68.0\\bin")[0]
        image.save("papers/papers_"+str(list_num+1)+"_"+str(datetime.date.today())+".jpg")

        print("List #"+str(list_num)+' created')
        i += 20
        list_num += 1
