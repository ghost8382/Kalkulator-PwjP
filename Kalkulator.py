import tkinter as tk

symbols = ['7', '8', '9', '/', '\u21BA', 'C', '4', '5', '6', '*', '(', ')', '1', '2', '3',
           '-', 'x^2', '\u221A', '0', '.', '%', '+']


def inicjalizacjaOkienka():
    root = tk.Tk()
    root.geometry('500x500')
    root.title('Czadowy Kalkulator')
    return root


def screenIni(root):
   
    screen = [tk.Label(root, width=65, bg="#DBE3DE", anchor='w', borderwidth=2) for i in range(3)]
    root.configure(bg='light grey')
    for i in range(len(screen)):
        screen[i].grid(row=i, columnspan=6, ipady=15, ipadx=1)
    return screen


def dataAreaIni(root, ekran):
   
    dataArea = tk.Entry(root, borderwidth=0, highlightcolor='white', highlightbackground='white')
    dataArea.grid(row=len(ekran), columnspan=6, ipady=15, ipadx=140)
    
    info = tk.Label(root, text="Ostatnie wyrażenie:", width=65, bg="#DBE3DE", anchor='w', borderwidth=2)
    info.grid(row=len(ekran) + 1, columnspan=6, ipady=15, ipadx=1)
    return dataArea, info


def clickButton(dataArea, symbol):
    def f():
        if symbol == '\u21BA':  # Cofnięcie ostatniego znaku
            current_text = dataArea.get()[:-1]
            dataArea.delete(0, tk.END)
            dataArea.insert(tk.END, current_text)
        elif symbol == 'C':  # Czyszczenie pola
            dataArea.delete(0, tk.END)
        elif symbol == 'x^2':  # Kwadrat liczby
            try:
                current_text = dataArea.get()
                squared_value = str(eval(current_text) ** 2)
                dataArea.delete(0, tk.END)
                dataArea.insert(tk.END, squared_value)
            except:
                dataArea.delete(0, tk.END)
                dataArea.insert(tk.END, "Błąd")
        else:  # Dodanie symbolu
            dataArea.insert(tk.END, symbol)

    return f


def oblicz(dataArea, info, results, screen):
    try:
        expression = dataArea.get()
        expression = expression.replace('x^2', '**2').replace('\u221A', 'sqrt')
        result = str(eval(expression))  # Obliczenie wyniku
        dataArea.delete(0, tk.END)
        dataArea.insert(tk.END, result)

        results.insert(0, f"{expression} = {result}")
        if len(results) > 3:  # Jeśli mamy więcej niż 3 wyniki, usuń najstarszy
            results.pop()

       
        for i in range(min(3, len(results))):
            screen[i].config(text=results[i])

      
        info.config(text=f"Ostatnie wyrażenie: {expression} = {result}")
    except:
        dataArea.delete(0, tk.END)
        dataArea.insert(tk.END, "Błąd")
        info.config(text="Ostatnie wyrażenie: Błąd")


def KeysIni(root, screen, dataArea, info, results):
    keys = [tk.Button(root, text=symbol, font=('Arial Unicode MS', 12), bg='light grey', borderwidth=0)
            for symbol in symbols]
    j = len(screen) + 2  # Początkowy wiersz dla przycisków
    for i in range(len(keys)):
        if i % 6 == 0 and i > 0:
            j += 1
        keys[i].configure(command=clickButton(dataArea, keys[i]['text']))
        keys[i].grid(row=j, column=i % 6, ipady=10, ipadx=20, padx=5, pady=5)

    equalitySign = tk.Button(root, text='=', font=('Arial Unicode MS', 14), bg='#00BFFF', borderwidth=0,
                             command= lambda: oblicz(dataArea, info, results, screen))
    equalitySign.grid(row=j, column=4, columnspan=2, ipady=15, ipadx=40)
    return keys


if __name__ == '__main__':
    root = inicjalizacjaOkienka()  # start okienka
    screen = screenIni(root)
    dataArea, info = dataAreaIni(root, screen)

    
    results = []

    keys = KeysIni(root, screen, dataArea, info, results)
    root.mainloop()  # nie znikanie okienka
