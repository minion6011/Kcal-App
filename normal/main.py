import customtkinter
import matplotlib.backends
import matplotlib.figure
import matplotlib.figure
# - Py to exe requirements
import os 
import sys
import json
import re

global KcalText

customtkinter.set_appearance_mode("system") #Imposta l'aspetto usando il tema di sistema "dark" / "light"

# - Function Called

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



def tabellaKcal():
    with open(resource_path("attivita.json"), 'r') as r: 
        data_attivita = json.load(r)
    # - start function
    def var_attivita(option):
        try:
            global KcalText
            if option == "Invia":
                value = float(tabellaKcalTime.get()) * data_attivita[str(tabellaKcalOption.get())]
            elif option == "Somma":
                exvalue = re.search(r'\d+\.\d+|\d+', KcalText.cget("text")).group()
                value = (float(tabellaKcalTime.get()) * data_attivita[str(tabellaKcalOption.get())]) + float(exvalue)
            elif option == "Reset":
                value = "0.0"
            tabellaTextKcal.configure(text=f"{value} kcal")
            KcalText.configure(text=f"{value} kcal")
        except:
            tabellaTextKcal.configure(text="Errore, Valori Invalidi")
        bottoneAttivita.set(None)
            
    # - end function
    modalTab = customtkinter.CTkToplevel(app)
    
    modalTab.geometry("300x300")
    modalTab.minsize(300,300)
    modalTab.title("Tabella kcal")
    modalTab.after(20, modalTab.lift) # - Expand App

    modalTab.grid_columnconfigure(1, weight=1)
    modalTab.grid_rowconfigure(1, weight=1)

    # - Ui

    frame = customtkinter.CTkFrame(master=modalTab)
    frame.grid(row=0, column=1, padx=30, pady=30)

    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    # - Frame Ui
    list_values = []
    for data in data_attivita:
        list_values.append(data)

    tabellaKcalOption = customtkinter.CTkOptionMenu(frame, values=list_values,font=("Arial", 12))
    tabellaKcalOption.grid(column=1, row=1, padx=30, pady=20)

    tabellaKcalTime = customtkinter.CTkEntry(frame, placeholder_text="Tempo di attività (minuti)", width=200, height=30)
    tabellaKcalTime.grid(column=1, row=2, padx=30, pady=(20,5))

    tabellaTextKcal = customtkinter.CTkLabel(frame, text="", font=("Roboto", 15))
    tabellaTextKcal.grid(column=1, row=3)

    bottoneAttivita = customtkinter.CTkSegmentedButton(frame, values=["Reset", "Invia", "Somma"], command=var_attivita, height=30, unselected_hover_color="#36719F")
    bottoneAttivita.set(None)
    bottoneAttivita.grid(column=1, row=4, padx=30, pady=(5, 20))



    tabellaKcalText = customtkinter.CTkLabel(frame, text=None)
    tabellaKcalText.grid(column=1, row=5, padx=30, pady=(0,10))


def ms_calc():
    try:
        valuePeso = re.search(r'\d+\.\d+|\d+', InputPeso.get('1.0', 'end')).group()
        valueAltezza = re.search(r'\d+\.\d+|\d+', InputAltezza.get('1.0', 'end')).group()
        valueEta = re.search(r'\d+\.\d+|\d+', InputEta.get('1.0', 'end')).group()

        valueAttivita = re.search(r'\d+\.\d+|\d+', KcalText.cget("text")).group()

        valueGender = OptionGender.get()

        if valuePeso.isdigit() and valueEta.isdigit() and valueAltezza.isdigit():
            if valueGender == "Maschio":
                value = 66.4730 + (13.7516 * float(valuePeso)) + (5.0033 * float(valueAltezza)) - (6.7550 * float(valueEta))
                value = round(value + float(valueAttivita), 2)
            else:
                value = 655.0955 + (9.5634 * float(valuePeso)) + (1.8496 * float(valueAltezza)) - (4.6756 * float(valueEta))
                value = round(value + float(valueAttivita), 2)
            resultModal(value, False)
        else:
            resultModal(None, True)
    except Exception as e:
            resultModal(None, True)


def resultModal(mb, error = False):
    modal = customtkinter.CTkToplevel(app)
    
    modal.after(20, modal.lift) # - Expand App

    modal.grid_columnconfigure(0, weight=1)
    modal.grid_rowconfigure(1, weight=1)

    modal.title("Risultati Metabolismo Basale")
    if error == False:
        modal.geometry("600x600")
        modal.minsize(600,600)
        # - Ui code
        frameChart = customtkinter.CTkFrame(master=modal)
        frameChart.grid(row=1, column=0, padx=0, pady=0)
        # - START Grafico (NON TOCCARE)
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure

        labels = [f'Colazione - {round((mb/100)*25, 2)} kcal', f'Pranzo - {round((mb/100)*40, 2)} kcal', f'Cena - {round((mb/100)*30, 2)} kcal', f'Spuntini - {round((mb/100)*5, 2)} kcal']
        sizes = [25, 40, 30, 5]

        fig = Figure(figsize=(6,6))
        ax = fig.add_subplot()

        wedges, _, _ = ax.pie(sizes, radius=1, autopct='%1.1f%%', shadow=False)

        ax.legend(wedges, labels, title="Valori", loc="upper left",fontsize=10,title_fontsize=12)

        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        chart1 = FigureCanvasTkAgg(fig, frameChart)
        wdg = chart1.get_tk_widget()
        wdg.config(bg=modal.cget("bg"))
        wdg.pack() # - Aggiunta al frame
        # - FINE GRAFICO
        resultText = customtkinter.CTkLabel(modal, text=f"Regime dietetico = {mb} kcal", font=("Roboto", 25))
        resultText.grid(row=2, column=0, padx=0, pady=(0, 140))
    else:
        # - Ui code
        modal.geometry("300x100")
        modal.minsize(300,100)
        errorText = customtkinter.CTkLabel(modal, text=f"Errore, Valori Invalidi", font=("Roboto", 25), text_color="red")
        errorText.grid(row=1, column=0, padx=0, pady=10)

def change_theme(value):
    if value == "Light":
        customtkinter.set_appearance_mode("light")
        themeButton.configure(variable=customtkinter.StringVar(value="Light"), unselected_color="black", selected_color="white")
    else:
        customtkinter.set_appearance_mode("dark")
        themeButton.configure(variable=customtkinter.StringVar(value="Dark"), unselected_color="white", selected_color="black")

# - Setup Ui

app = customtkinter.CTk()
app.title("Calcolo Metabolismo Basale")
app.geometry("850x550")
app.minsize(850,550)

app.grid_columnconfigure(2, weight=1)
app.grid_rowconfigure(1, weight=1) # permetteno di centrare gli elementi orizzontalmente

frame = customtkinter.CTkFrame(master=app)
frame.grid(row=0, columnspan=3, padx=30, pady=30)
frame.grid_columnconfigure(0, weight=1) # permetteno di centrare gli elementi orizzontalmente


# -- Ui visibile

header = customtkinter.CTkLabel(frame, text="𝗖𝗮𝗹𝗰𝗼𝗹𝗮𝘁𝗿𝗶𝗰𝗲 𝗠.𝗕.", font=("Roboto", 25))
header.grid(row=1, column=1, padx=0, pady=20)


themeButton =  customtkinter.CTkSegmentedButton(frame, values=["Dark", "Light"], height=35, text_color="gray", command=change_theme, selected_hover_color="gray29", unselected_hover_color="gray29")
themeButton.grid(row=1, column=2, padx=0, pady=20)
if customtkinter.get_appearance_mode() == "Dark":
    themeButton.configure(variable=customtkinter.StringVar(value="Dark"), unselected_color="white", selected_color="black")
else:
    themeButton.configure(variable=customtkinter.StringVar(value="Light"), unselected_color="black", selected_color="white")

# --
TextGender = customtkinter.CTkLabel(frame, text="ꜱᴇꜱꜱᴏ", font=("Roboto", 20))
TextGender.grid(row=2, column=1, padx=20, pady=(20, 0))

OptionGender = customtkinter.CTkOptionMenu(frame, values=["Maschio", "Femmina"], variable=customtkinter.StringVar(value="Maschio"), hover=True)
OptionGender.grid(row=3, column=1, padx=20, pady=10)

# --

TextPeso = customtkinter.CTkLabel(frame, text="Peso Corporeo (kg)", font=("Roboto", 20))
TextPeso.grid(row=4, column=0, padx=20, pady=(20, 0))
InputPeso = customtkinter.CTkTextbox(frame, height=20)
InputPeso.grid(row=5, column=0, padx=20, pady=10)

TextAltezza = customtkinter.CTkLabel(frame, text="Altezza (cm)", font=("Roboto", 20))
TextAltezza.grid(row=4, column=1, padx=20, pady=(20, 0))
InputAltezza = customtkinter.CTkTextbox(frame, height=20)
InputAltezza.grid(row=5, column=1, padx=20, pady=10)

TextEta = customtkinter.CTkLabel(frame, text="Eta (Anni)", font=("Roboto", 20))
TextEta.grid(row=4, column=2, padx=20, pady=(20, 0))
InputEta = customtkinter.CTkTextbox(frame, height=20)
InputEta.grid(row=5, column=2, padx=20, pady=10)
# --

TextAttivita = customtkinter.CTkLabel(frame, text="Attività fisica giornaliera (kcal)", font=("Roboto", 20))
TextAttivita.grid(row=6, column=1, padx=20, pady=(20, 0))

KcalText = customtkinter.CTkLabel(frame, text="0.0 kcal", font=("Roboto", 18))
KcalText.grid(row=7, column=1, padx=20, pady=10)

ButtonTab = customtkinter.CTkButton(frame, text="Calcola kcal", command=tabellaKcal,height=35)
ButtonTab.grid(row=7, column=2, padx=20, pady=10)
# -- 

ButtonCalc = customtkinter.CTkButton(frame, text="Calcola", command=ms_calc, height=35)
ButtonCalc.grid(row=8, column=1, padx=20, pady=10)


app.mainloop()
