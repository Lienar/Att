import os
import csv
from tabulate import tabulate


class PriceMachine:
    
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, file_path=''):
        file_names = []
        for file_name in os.listdir(file_path):
            if os.path.isfile(os.path.join(file_path, file_name)):
                if 'price' in file_name:
                    file_names.append(file_name)

        data_temp2 = []
        data_temp3 = []

        for file in file_names:
            with open(f"{file_path}\\{file}", "r", encoding="utf-8", ) as csvfile:
                readed = csv.reader(csvfile, delimiter=",")
                for row in readed:
                    data_temp3.append(row)
                data_temp2.append(data_temp3)
                data_temp3 = []

        data_temp = []
        file_name_index = 0
        for data in data_temp2:
            i_index = self._search_product_price_weight(data[0])
            i_name = i_index[0]
            i_cost = i_index[1]
            i_weight = i_index[2]
            temp_name = data[0][i_name]
            for item in data:
                if temp_name != item[i_name]:
                    cost_per_kg = float('{:.2f}'.format(int(item[i_cost]) / int(item[i_weight])))
                    data_temp4 = [item[i_name], item[i_cost], item[i_weight], file_names[file_name_index],
                                  cost_per_kg]
                    data_temp.append(data_temp4)
            file_name_index += 1

        for i in range(0, len(data_temp)):
            for j in range(0, len(data_temp) - i - 1):
                if float(data_temp[j][4]) > float(data_temp[j + 1][4]):
                    tempo = data_temp[j]
                    data_temp[j] = data_temp[j + 1]
                    data_temp[j + 1] = tempo

        for i in range(0, len(data_temp)):
            temp = data_temp[i].copy()
            data_temp[i] = [i+1]
            data_temp[i].extend(temp)

        self.data = data_temp.copy()
        # with open('eggs.csv', newline='') as csvfile:
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        
    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        costs = ['розница', 'цена']
        names = ['товар', 'название', 'наименование', 'продукт']
        weights = ['вес', 'масса', 'фасовка']
        i_name = 0
        i_cost = 0
        i_weight = 0
        for i in range(0, len(headers)):
            for name in names:
                if name == headers[i]:
                    temp_name = name
                    i_name = i
            for cost in costs:
                if cost == headers[i]:
                    i_cost = i
            for weight in weights:
                if weight == headers[i]:
                    i_weight = i
        i_index = [i_name, i_cost, i_weight]
        return i_index



    def export_to_html(self, fname='output.html'):
        result = '''<!DOCTYPE html>
<html>
    <head>
        <title>Позиции продуктов</title>
    </head>
    <body>
        <table>
            <tr>
                <th>Номер</th>
                <th>Название</th>
                <th>Цена</th>
                <th> </th>
                <th>Фасовка</th>
                <th>Файл</th>
                <th>Цена за кг.</th>
            </tr>
            '''
        for item in self.data:
            if item[1] != 'наименование':
                value, product_name, price, weight, file_name, cost_per_kg = item
                if value == 1:
                    result += '<tr>' + '\n'
                else:
                    result += '\t' + '\t' + '\t' + '<tr>' + '\n'
                result += f'\t\t\t\t<td align="center">{value}</td>\n'
                result += f'\t\t\t\t<td align="center">{product_name}</td>\n'
                result += f'\t\t\t\t<td align="center">{price}</td>\n'
                result += f'\t\t\t\t<td align="center"> </td>\n'
                result += f'\t\t\t\t<td align="center">{weight}</td>\n'
                result += f'\t\t\t\t<td align="center">{file_name}</td>\n'
                result += f'\t\t\t\t<td align="center">{cost_per_kg}</td>' + '\n'
                result += '\t\t\t</tr>' + '\n'
        result += '\t' + '\t' + '</table>' + '\n'
        result += '\t' + '</body>' + '\n'
        result += '</html>'

        with open(f"{fname}", "w", encoding="utf-8", ) as fd:
            fd.write(result)
        return (fname)
    
    def find_text(self, text):
        headers = ['№', 'наименование', 'цена', 'фасовка', 'файл', 'цена за кг']
        data_temp5 = []
        for data in self.data:
            if data[1] != 'наименование':
                if text.lower() in data[1].lower():
                    data_temp5.append(data)
        print(tabulate(data_temp5, headers=headers, tablefmt="grid"))


pm = PriceMachine()
pm.load_prices('F:\\Users\\Attestat\\data')
text = " "
while text != 'exit':
    print('------------------------------------------------------------------------')
    print('| для поиска данных укажите часть названия продукта в строке для ввода |')
    print('| для вывода данных в файл введите "вывод"                             |')
    print('| для выхода введите "exit"                                            |')
    print('------------------------------------------------------------------------')
    text = input('Строка для ввода: ')
    if text == 'вывод':
        pm.export_to_html()
    elif text != 'exit':
        pm.find_text(text)

'''
    Логика работы программы
'''
print('the end')
print(pm.export_to_html())
