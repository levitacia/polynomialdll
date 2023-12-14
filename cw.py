import tkinter as tk
import ctypes
from tkinter import filedialog
import datetime

import psycopg2

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lib = ctypes.CDLL('./polynomial.dll')
        self.geometry("400x300")
        self.title("Калькулятор многочленов")

        # Добавляем соединение с базой данных PostgreSQL
        self.conn = psycopg2.connect(
            host = "127.0.0.1",
            user="postgres",
            password="nasralvkamish",
            dbname="postgres",
            port="5432"
        )
        self.cur = self.conn.cursor()

        self.addButton("Деление", self.openDivisionWindow, width=20, height=2, font=("Arial", 12))
        self.addButton("Умножение", self.openMultiplicationWindow, width=20, height=2, font=("Arial", 12))
        self.addButton("Сложение", self.openAdditionWindow, width=20, height=2, font=("Arial", 12))
        self.addButton("Вычитание", self.openSubtractionWindow, width=20, height=2, font=("Arial", 12))
        self.addButton("Вычисление значения", self.openEvaluationWindow, width=20, height=2, font=("Arial", 12))

    
    def saveToDatabase(self, case, arr1, arr2, arr3):
        if case == 0:
            # Функция для записи значений в базу данных
            result_str = ' '.join(map(str, arr1))
            ostatok_str = ' '.join(map(str, arr2))
            self.cur.execute("INSERT INTO division (result, ostatok) VALUES (%s, %s)", (result_str, ostatok_str))
            self.conn.commit()
        if case == 1:
            arr1_str = ' '.join(map(str, arr1))
            arr2_str = ' '.join(map(str, arr2))
            result_str = ' '.join(map(str, arr3))
            self.cur.execute("INSERT INTO multiply (arr1, arr2, result) VALUES (%s, %s, %s)", (arr1_str, arr2_str, result_str))
            self.conn.commit()
        if case == 2:
            arr1_str = ' '.join(map(str, arr1))
            arr2_str = ' '.join(map(str, arr2))
            result_str = ' '.join(map(str, arr3))
            self.cur.execute("INSERT INTO sum (arr1, arr2, result) VALUES (%s, %s, %s)", (arr1_str, arr2_str, result_str))
            self.conn.commit()
        if case == 3:
            arr1_str = ' '.join(map(str, arr1))
            arr2_str = ' '.join(map(str, arr2))
            result_str = ' '.join(map(str, arr3))
            self.cur.execute("INSERT INTO subtraction (arr1, arr2, result) VALUES (%s, %s, %s)", (arr1_str, arr2_str, result_str))
            self.conn.commit()
        if case == 4:
            arr1_str = ' '.join(map(str, arr1))
            x_str = str(arr2)
            result_str = str(arr3)
            self.cur.execute("INSERT INTO evaluation (arr1, x, result) VALUES (%s, %s, %s)", (arr1_str, x_str, result_str))
            self.conn.commit()


    def openDivisionWindow(self):
        division_window = tk.Toplevel(self)
        division_window.title("Деление многочленов")
        division_window.geometry("400x220")

        label1 = tk.Label(division_window, text="Введите коэффициенты первого многочлена (через пробел):", font=("Arial", 10))
        label1.pack()
        entry_coef1 = tk.Entry(division_window, validate="key")
        entry_coef1['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef1.pack()

        label2 = tk.Label(division_window, text="Введите коэффициенты второго многочлена (через пробел):", font=("Arial", 10))
        label2.pack()
        entry_coef2 = tk.Entry(division_window, validate="key")
        entry_coef2['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef2.pack()

        # Добавление флажка
        checkbox_var = tk.IntVar()
        checkbox = tk.Checkbutton(division_window, text="Запись в файл", variable=checkbox_var)
        checkbox.pack()

        # Добавление флажка запись из файла
        checkboxread_var = tk.IntVar()
        checkbox = tk.Checkbutton(division_window, text="Запись из файла", variable=checkboxread_var)
        checkbox.pack()

        result_label = tk.Label(division_window, text="Результат деления:", font=("Arial", 10))
        result_label.pack()

        ostatok_label = tk.Label(division_window, text="Остаток", font=("Arial", 10))
        ostatok_label.pack()

        
        def performDivision():
            if checkboxread_var.get() == 1:
                file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                if file_path:
                    with open(file_path, 'r') as file:
                        data = file.readlines()
                        #print(data)
                        k1 = (ctypes.c_double * len(data[0].split()))()
                        k1[:] = [float(x) for x in data[0].split()]
                        degp1 = len(k1) - 1
                        k2 = (ctypes.c_double * len(data[1].split()))()
                        k2[:] = [float(x) for x in data[1].split()]
                        degp2 = len(k2) - 1
                    
                        self.lib.division.restype = ctypes.POINTER(ctypes.c_double)
                        self.lib.division.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int]

                        result = self.lib.division(k1, degp1, k2, degp2)

                        if checkbox_var.get() == 1:
                            result_str = ""
                            for i in range(degp1 - degp2, -1, -1):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)

                            ostatok_str = ""
                            for i in range(degp2 - 1, -1, -1):
                                ostatok_str += str(k1[i]) + " "
                            ostatok_label.config(text=ostatok_str)
                        
                            with open('result.txt', 'a') as file:
                                file.write(f"Operation: Division\n")
                                file.write(f"Result: {result_str}\n")
                                file.write(f"ostatok: {ostatok_str}\n\n")
                            
                            self.saveToDatabase(0, result_str, ostatok_str, 0)
                        else:
                            result_str = "Результат деления: "
                            for i in range(degp1 - degp2, -1, -1):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)

                            ostatok_str = "Остаток: "
                            for i in range(degp2 - 1, -1, -1):
                                ostatok_str += str(k1[i]) + " "
                            ostatok_label.config(text=ostatok_str)

                            self.saveToDatabase(0, result_str, ostatok_str, 0)

            else: 
                k1 = (ctypes.c_double * len(entry_coef1.get().split()))()
                k1[:] = [float(x) for x in entry_coef1.get().split()]
                degp1 = len(k1) - 1

                k2 = (ctypes.c_double * len(entry_coef2.get().split()))()
                k2[:] = [float(x) for x in entry_coef2.get().split()]
                degp2 = len(k2) - 1

                self.lib.division.restype = ctypes.POINTER(ctypes.c_double)
                self.lib.division.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int]

                start = datetime.datetime.now()
                result = self.lib.division(k1, degp1, k2, degp2)
                finish = datetime.datetime.now()
                print('Время работы: ' + str(finish - start))

                if checkbox_var.get() == 1:
                    result_str = ""
                    for i in range(degp1 - degp2, -1, -1):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str)

                    ostatok_str = ""
                    for i in range(degp2 - 1, -1, -1):
                        ostatok_str += str(k1[i]) + " "
                    ostatok_label.config(text=ostatok_str)
                
                    with open('result.txt', 'a') as file:
                        file.write(f"Operation: Division\n")
                        file.write(f"Result: {result_str}\n")
                        file.write(f"ostatok: {ostatok_str}\n\n")
                    self.saveToDatabase(0, result_str, ostatok_str, 0)
                else:
                    result_str = ""
                    for i in range(degp1 - degp2, -1, -1):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str)

                    ostatok_str = ""
                    for i in range(degp2 - 1, -1, -1):
                        ostatok_str += str(k1[i]) + " "
                    ostatok_label.config(text=ostatok_str)
                    self.saveToDatabase(0, result_str, ostatok_str, 0)

        calculate_button = tk.Button(division_window, text="Посчитать", command=performDivision, font=("Arial", 10))
        calculate_button.pack()


    def openMultiplicationWindow(self):
        multiplication_window = tk.Toplevel(self)
        multiplication_window.title("Умножение многочленов")
        multiplication_window.geometry("400x220")

        label1 = tk.Label(multiplication_window, text="Введите коэффициенты первого многочлена (через пробел):")
        label1.pack()
        entry_coef1 = tk.Entry(multiplication_window, validate='key')
        entry_coef1['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef1.pack()

        label2 = tk.Label(multiplication_window, text="Введите коэффициенты второго многочлена (через пробел):")
        label2.pack()
        entry_coef2 = tk.Entry(multiplication_window, validate='key')
        entry_coef2['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef2.pack()

        # Добавление флажка
        checkbox_var = tk.IntVar()
        checkbox = tk.Checkbutton(multiplication_window, text="Запись в файл", variable=checkbox_var)
        checkbox.pack()

        # Добавление флажка запись из файла
        checkboxread_var = tk.IntVar()
        checkbox = tk.Checkbutton(multiplication_window, text="Запись из файла", variable=checkboxread_var)
        checkbox.pack()

        result_label = tk.Label(multiplication_window, text="Результат умножения:")
        result_label.pack()

        def performMultiplication():
            if checkboxread_var.get() == 1:
                file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                if file_path:
                    with open(file_path, 'r') as file:
                        data = file.readlines()
                        #print(data)
                        k3 = [float(x) for x in data[0].split()]
                        degp3 = len(k3)
                        k4 = [float(x) for x in data[1].split()]
                        degp4 = len(k4)
                        DoubleArray = ctypes.c_double * degp3
                        arr3 = DoubleArray(*k3)
                        DoubleArray = ctypes.c_double * degp4
                        arr4 = DoubleArray(*k4)
                        self.lib.multiply.restype = ctypes.POINTER(ctypes.c_double)
                        result = self.lib.multiply(arr3, degp3, arr4, degp4)
                        if checkbox_var.get() == 1:
                            result_str = ""
                            for i in range(degp3 + degp4 - 2, -1, -1):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)
                            with open('result.txt', 'a') as file:
                                file.write(f"Operation: Multiply\n")
                                file.write(f"arr1: {k3}\n")
                                file.write(f"arr2: {k4}\n")
                                file.write(f"arr2: {result_str}\n\n")
                            self.saveToDatabase(1, k3, k4, result_str)
                        else:   
                            result_str = ""
                            for i in range(degp3 + degp4 - 2, -1, -1):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)
                            self.saveToDatabase(1, k3, k4, result_str) 
            else:
                k3 = [float(x) for x in entry_coef1.get().split()]
                degp3 = len(k3)
                k4 = [float(x) for x in entry_coef2.get().split()]
                degp4 = len(k4)

                DoubleArray = ctypes.c_double * degp3
                arr3 = DoubleArray(*k3)
                DoubleArray = ctypes.c_double * degp4
                arr4 = DoubleArray(*k4)
                self.lib.multiply.restype = ctypes.POINTER(ctypes.c_double)
                result = self.lib.multiply(arr3, degp3, arr4, degp4)

                if checkbox_var.get() == 1:
                    result_str = ""
                    for i in range(degp3 + degp4 - 2, -1, -1):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str)

                    with open('result.txt', 'a') as file:
                        file.write(f"Operation: Multiply\n")
                        file.write(f"arr1: {k3}\n")
                        file.write(f"arr2: {k4}\n")
                        file.write(f"arr2: {result_str}\n\n")
                    self.saveToDatabase(1, k3, k4, result_str)
                else:   
                    result_str = ""
                    for i in range(degp3 + degp4 - 2, -1, -1):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str) 
                    self.saveToDatabase(1, k3, k4, result_str)          

        calculate_button = tk.Button(multiplication_window, text="Посчитать", command=performMultiplication)
        calculate_button.pack()


    def openAdditionWindow(self):
        addition_window = tk.Toplevel(self)
        addition_window.title("Сложение многочленов")
        addition_window.geometry("400x220")

        label1 = tk.Label(addition_window, text="Введите коэффициенты первого многочлена (через пробел):")
        label1.pack()
        entry_coef1 = tk.Entry(addition_window, validate='key')
        entry_coef1['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef1.pack()

        label2 = tk.Label(addition_window, text="Введите коэффициенты второго многочлена (через пробел):")
        label2.pack()
        entry_coef2 = tk.Entry(addition_window, validate='key')
        entry_coef2['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef2.pack()

        # Добавление флажка
        checkbox_var = tk.IntVar()
        checkbox = tk.Checkbutton(addition_window, text="Запись в файл", variable=checkbox_var)
        checkbox.pack()

        # Добавление флажка запись из файла
        checkboxread_var = tk.IntVar()
        checkbox = tk.Checkbutton(addition_window, text="Запись из файла", variable=checkboxread_var)
        checkbox.pack()

        result_label = tk.Label(addition_window, text="Результат сложения:")
        result_label.pack()

        def performAddition():
            if checkboxread_var.get() == 1:
                file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                if file_path:
                    with open(file_path, 'r') as file:
                        data = file.readlines()
                        #print(data)
                        k5 = [float(x) for x in data[0].split()]
                        degp5 = len(k5)
                        k6 = [float(x) for x in data[1].split()]
                        degp6 = len(k6)
                        DoubleArray = ctypes.c_double * degp5
                        arr5 = DoubleArray(*k5)
                        DoubleArray = ctypes.c_double * degp6
                        arr6 = DoubleArray(*k6)
                        self.lib.Sum.restype = ctypes.POINTER(ctypes.c_double)
                        result = self.lib.Sum(arr5, degp5, arr6, degp6)

                        if checkbox_var.get() == 1:
                            result_str = ""
                            for i in range(max(degp5, degp6)):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)

                            with open('result.txt', 'a') as file:
                                file.write(f"Operation: Sum\n")
                                file.write(f"arr1: {k5}\n")
                                file.write(f"arr2: {k6}\n")
                                file.write(f"arr2: {result_str}\n\n")
                            self.saveToDatabase(2, k5, k6, result_str)
                        else:                
                            result_str = ""
                            for i in range(max(degp5, degp6)):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)
                            self.saveToDatabase(2, k5, k6, result_str)
            else:
                k5 = [float(x) for x in entry_coef1.get().split()]
                degp5 = len(k5)
                k6 = [float(x) for x in entry_coef2.get().split()]
                degp6 = len(k6)
                DoubleArray = ctypes.c_double * degp5
                arr5 = DoubleArray(*k5)
                DoubleArray = ctypes.c_double * degp6
                arr6 = DoubleArray(*k6)
                self.lib.Sum.restype = ctypes.POINTER(ctypes.c_double)
                result = self.lib.Sum(arr5, degp5, arr6, degp6)

                if checkbox_var.get() == 1:
                    result_str = ""
                    for i in range(max(degp5, degp6)):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str)

                    with open('result.txt', 'a') as file:
                        file.write(f"Operation: Sum\n")
                        file.write(f"arr1: {k5}\n")
                        file.write(f"arr2: {k6}\n")
                        file.write(f"arr2: {result_str}\n\n")
                    self.saveToDatabase(2, k5, k6, result_str)
                else:                
                    result_str = ""
                    for i in range(max(degp5, degp6)):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str)
                    self.saveToDatabase(2, k5, k6, result_str)
            
        
        calculate_button = tk.Button(addition_window, text="Посчитать", command=performAddition)
        calculate_button.pack()
    
    def openSubtractionWindow(self):
        subtraction_window = tk.Toplevel(self)
        subtraction_window.title("Вычитание многочленов")
        subtraction_window.geometry("400x220")

        label1 = tk.Label(subtraction_window, text="Введите коэффициенты первого многочлена (через пробел):")
        label1.pack()
        entry_coef1 = tk.Entry(subtraction_window, validate='key')
        entry_coef1['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef1.pack()

        label2 = tk.Label(subtraction_window, text="Введите коэффициенты второго многочлена (через пробел):")
        label2.pack()
        entry_coef2 = tk.Entry(subtraction_window, validate='key')
        entry_coef2['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef2.pack()

        # Добавление флажка
        checkbox_var = tk.IntVar()
        checkbox = tk.Checkbutton(subtraction_window, text="Запись в файл", variable=checkbox_var)
        checkbox.pack()

        # Добавление флажка запись из файла
        checkboxread_var = tk.IntVar()
        checkbox = tk.Checkbutton(subtraction_window, text="Запись из файла", variable=checkboxread_var)
        checkbox.pack()

        result_label = tk.Label(subtraction_window, text="Результат вычитания:")
        result_label.pack()

        def performSubtraction():
            if checkboxread_var.get() == 1:
                file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                if file_path:
                    with open(file_path, 'r') as file:
                        data = file.readlines()
                        #print(data)
                        k7 = [float(x) for x in data[0].split()]
                        degp7 = len(k7)
                        k8 = [float(x) for x in data[1].split()]
                        degp8 = len(k8)

                        DoubleArray = ctypes.c_double * (degp7)
                        arr7 = DoubleArray(*k7)
                        DoubleArray = ctypes.c_double * (degp7)
                        arr8 = DoubleArray(*k8)
                        self.lib.evaluate.restype = ctypes.c_double
                        result = self.lib.evaluate(arr7, degp7, arr8, degp8)

                        if checkbox_var.get() == 1:
                            result_str = ""
                            for i in range(max(degp7, degp8)):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)
                            with open('result.txt', 'a') as file:
                                file.write(f"Operation: Subtraction\n")
                                file.write(f"arr1: {k7}\n")
                                file.write(f"arr2: {k8}\n")
                                file.write(f"arr2: {result_str}\n\n")
                            self.saveToDatabase(3, k7, k8, result_str)
                        else:
                            result_str = ""
                            for i in range(max(degp7, degp8)):
                                result_str += str(result[i]) + " "
                            result_label.config(text=result_str)
                            self.saveToDatabase(3, k7, k8, result_str)
            else:            
                k7 = [float(x) for x in entry_coef1.get().split()]
                degp7 = len(k7)
                k8 = [float(x) for x in entry_coef2.get().split()]
                degp8 = len(k8)

                DoubleArray = ctypes.c_double * degp7
                arr7 = DoubleArray(*k7)
                DoubleArray = ctypes.c_double * degp8
                arr8 = DoubleArray(*k8)
                self.lib.subtraction.restype = ctypes.POINTER(ctypes.c_double)
                result = self.lib.subtraction(arr7, degp7, arr8, degp8)

                if checkbox_var.get() == 1:
                    result_str = ""
                    for i in range(max(degp7, degp8)):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str)
                    with open('result.txt', 'a') as file:
                        file.write(f"Operation: Subtraction\n")
                        file.write(f"arr1: {k7}\n")
                        file.write(f"arr2: {k8}\n")
                        file.write(f"arr2: {result_str}\n\n")
                    self.saveToDatabase(3, k7, k8, result_str)
                else:
                    result_str = ""
                    for i in range(max(degp7, degp8)):
                        result_str += str(result[i]) + " "
                    result_label.config(text=result_str)
                    self.saveToDatabase(3, k7, k8, result_str)
            
        calculate_button = tk.Button(subtraction_window, text="Посчитать", command=performSubtraction)
        calculate_button.pack()

    def openEvaluationWindow(self):
        evaluation_window = tk.Toplevel(self)
        evaluation_window.title("Вычисление значения многочлена")
        evaluation_window.geometry("400x220")

        label1 = tk.Label(evaluation_window, text="Введите коэффициенты многочлена (через пробел):")
        label1.pack()
        entry_coef = tk.Entry(evaluation_window, validate='key')
        entry_coef['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_coef.pack()

        label2 = tk.Label(evaluation_window, text="Введите значение x для вычисления многочлена:")
        label2.pack()
        entry_x = tk.Entry(evaluation_window, validate='key')
        entry_x['validatecommand'] = (self.register(self.validate_input), '%S')
        entry_x.pack()

        # Добавление флажка запись в файл
        checkbox_var = tk.IntVar()
        checkbox = tk.Checkbutton(evaluation_window, text="Запись в файл", variable=checkbox_var)
        checkbox.pack()

        # Добавление флажка запись из файла
        checkboxread_var = tk.IntVar()
        checkbox = tk.Checkbutton(evaluation_window, text="Запись из файла", variable=checkboxread_var)
        checkbox.pack()

        result_label = tk.Label(evaluation_window, text="Результат вычисления:")
        result_label.pack()
            

        def performEvaluation():
            if checkboxread_var.get() == 1:
                file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                if file_path:
                    with open(file_path, 'r') as file:
                        data = file.readlines()
                        #print(data)
                        k9 = [float(x) for x in data[0].split()]
                        degp9 = len(k9)
                        x = float(data[1])
                        DoubleArray = ctypes.c_double * (degp9)
                        arr9 = DoubleArray(*k9)
                        self.lib.evaluate.restype = ctypes.c_double
                        result = self.lib.evaluate(arr9, degp9, ctypes.c_double(x))

                        if checkbox_var.get() == 1:                
                            result_str = f"{x} => {result}"
                            result_label.config(text=result_str)

                            with open('result.txt', 'a') as file:
                                file.write(f"Operation: Evaluation\n")
                                file.write(f"arr1: {k9}\n")
                                file.write(f"x: {x}\n")
                                file.write(f"Result: {result_str}\n\n")
                            self.saveToDatabase(4, k9, x, result)
                        else:
                            result_str = f"Результат вычисления: {x} => {result}"
                            result_label.config(text=result_str)
                            self.saveToDatabase(4, k9, x, result)
            else:

                k9 = [float(x) for x in entry_coef.get().split()]
                degp9 = len(k9)
                x = float(entry_x.get())

                DoubleArray = ctypes.c_double * (degp9)
                arr9 = DoubleArray(*k9)
                self.lib.evaluate.restype = ctypes.c_double
                result = self.lib.evaluate(arr9, degp9, ctypes.c_double(x))

                if checkbox_var.get() == 1:                
                    result_str = f"Результат вычисления: {x} => {result}"
                    result_label.config(text=result_str)

                    with open('result.txt', 'a') as file:
                        file.write(f"Operation: Evaluation\n")
                        file.write(f"arr1: {k9}\n")
                        file.write(f"x: {x}\n")
                        file.write(f"Result: {result_str}\n\n")
                    self.saveToDatabase(4, k9, x, result)
                else:
                    result_str = f"Результат вычисления: {x} => {result}"
                    result_label.config(text=result_str)
                    self.saveToDatabase(4, k9, x, result)

        calculate_button = tk.Button(evaluation_window, text="Посчитать", command=performEvaluation)
        calculate_button.pack()

    def validate_input(self, char):
        return char.isdigit() or char in [' ', '.', '-']


    def addButton(self, text, command, width, height, font):
        button = tk.Button(self, text=text, command=command, width=width, height=height, font=font)
        button.pack(pady=5)

app = Application()
app.mainloop()