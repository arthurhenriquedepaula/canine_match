import customtkinter
from tkinter import *
import re
import google.generativeai as genai
import threading

customtkinter.set_appearance_mode("light")
# customtkinter.set_default_color_theme("light")

# Configuração da janela principal
janela = customtkinter.CTk()
janela.geometry("1080x720")
janela.title("Canine Match")
janela.resizable(False, False)

# Configuração do banner
img = PhotoImage(file="image_banner.png")
label_img = customtkinter.CTkLabel(master=janela, image=img, text='')
label_img.place(x=5, y=5)

# Configuração do frame principal
frame = customtkinter.CTkFrame(master=janela, width=350, height=396, fg_color="white")
frame.pack(side=RIGHT)

# Configuração dos widgets
title = customtkinter.CTkLabel(master=frame, text="Canine Match", font=("Arial", 26))
age_label = customtkinter.CTkLabel(master=frame, text="Quantos anos você tem?", font=("Roboto", 14))
age = customtkinter.CTkEntry(master=frame, placeholder_text="Ex: 18", font=("Roboto", 14))
purpose = customtkinter.CTkLabel(master=frame, text="Selecione a finalidade do seu cão:", font=("Roboto", 14))
option_purpose = customtkinter.CTkOptionMenu(master=frame, values=["Companhia", "Guarda", "Apoio ao Tutor"])
option_purpose.set("Companhia")
stroll = customtkinter.CTkLabel(master=frame, text="Você deseja um cachorro com qual nível de atividade:", font=("Roboto", 14))
option_stroll = customtkinter.CTkOptionMenu(master=frame, values=["Baixo", "Médio", "Alto"])
option_stroll.set("Médio")
size = customtkinter.CTkLabel(master=frame, text="Qual o porte desejado:", font=("Roboto", 14))
option_size = customtkinter.CTkOptionMenu(master=frame, values=["Pequeno", "Médio", "Grande"])
option_size.set("Médio")
availability = customtkinter.CTkLabel(master=frame, text="Qual a sua disponibilidade de interatividade com o cão, por dia:", font=("Roboto", 14))
option_availability = customtkinter.CTkOptionMenu(master=frame, values=["Média de 30 min a 1 hr", "Mais de 1 hr"])
option_availability.set("Média de 30 min")
brushing = customtkinter.CTkLabel(master=frame, text="Você está disposto a escovar o pelo do cão:", font=("Roboto", 14))
option_brushing = customtkinter.CTkOptionMenu(master=frame, values=["Sim", "Não"])
option_brushing.set("Sim")
place = customtkinter.CTkLabel(master=frame, text="Qual local você mora:", font=("Roboto", 14))
option_place = customtkinter.CTkOptionMenu(master=frame, values=["Apartamento", "Casa", "Chacára"])
option_place.set("Casa")
divider = customtkinter.CTkFrame(master=frame, height=2, fg_color="gray")

img_loading = PhotoImage(file="loading.png")

def generateFrameSuccess():
    # Remover o frame anterior e a imagem
    frame.pack_forget()
    label_img.destroy()

    # Criar o frame de sucesso
    success_frame = customtkinter.CTkFrame(master=janela, width=1000, height=650, corner_radius=10, fg_color="#d3d3d3")
    success_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Exibir o spinner de carregamento
    show_loading_spinner(success_frame)

    title_success = customtkinter.CTkLabel(master=success_frame, 
        text="Possíveis raças sendo geradas, aguarde um momento ...😴",
        font=("Arial", 28))
    title_success.place(x=120, y=25)

    # Executar a função return_ia() e atualizar a interface
    threading.Thread(target=process_return_ia, args=(success_frame, title_success), daemon=True).start()

# Função para exibir o spinner de carregamento
def show_loading_spinner(success_frame):
    global spinner_label
    spinner_label = customtkinter.CTkLabel(master=success_frame, image=img_loading, text='')
    spinner_label.place(relx=0.5, rely=0.5, anchor="center")
    janela.update()

# Função para ocultar o spinner de carregamento
def hide_loading_spinner():
    global spinner_label
    if spinner_label:
        spinner_label.destroy()

# Função para processar return_ia() e atualizar o frame de sucesso
def process_return_ia(success_frame, title_success):
    result = return_ia()

    # Removendo mensagem de loading
    title_success.destroy()

    title_frame_success = customtkinter.CTkLabel(master=success_frame, 
        text="😃😃 Possíveis raças geradas com sucesso! 😃😃",
        font=("Arial", 28))
    title_frame_success.place(x=200, y=25)

    # Inicia o frame menor com as respostas
    success_in_frame = customtkinter.CTkFrame(master=success_frame, width=750, height=650)
    success_in_frame.place(relx=0.5, rely=0.5, anchor="center")

    text = re.sub(r'\*\*', '', result)

    # Usando re.split() para dividir a string pelos números seguidos de pontos
    partes = re.split(r'\d+\.\s', text)

    # Remover a primeira entrada vazia
    partes = [parte.strip() for parte in partes if parte.strip()]
   
    # Criação e posicionamento dos labels
    for index, parte in enumerate(partes):
        label = customtkinter.CTkLabel(master=success_in_frame, text=parte, font=("Roboto", 18))
        label.pack(padx=12, pady=20)

# Função que realiza a chamada à API
def return_ia():
    API_KEY = 'AIzaSyBeuFrnVhutue0YT8Ju39l1z-qCyw-wYnc'
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    availability = ''
    brushing = ''

    if option_availability.get() == 'Média de 30 min':
        availability = ' O cão deve ser mais independente do seu dono; '
    
    if option_brushing.get() == 'Não':
        brushing = ' O cão deve ser de pelagem curta;'

    prompt = " Cite 3 raças de cachorro que se adequam ao perfil de um dono com as seguintes características: O dono tem:" + age.get() + " anos de idade; " +  " O cão deve exercer a finalidade de: " + option_purpose.get() + '; O cão deve ter necessidade ' + option_stroll.get() + 'de atividade física;' + availability + 'O cão deve ser de porte: ' + option_size.get() + '; ' + brushing + ' O cão deve se sentir bem em: ' + option_place.get() + '; Me apresente uma resposta direta, com as características detalhadas de cada raça citada, RETORNE NO MÁXIMO 750 CARACTERES, utilize essa outra resposta sua como exemplo do padrão de resposta: "**1. Beagle**\n\n* Porte: M\u00e9dio\n* Temperamento: Amig\u00e1vel, curioso e independente\n* Atividade f\u00edsica: Moderada (1 hora por dia)\n* Companheirismo: Excelente, afetuoso e leal\n\n**2. Shiba Inu**\n\n* Porte: M\u00e9dio\n* Temperamento: Independente, inteligente e reservado\n* Atividade f\u00edsica: Moderada (1-2 horas por semana)\n* Companheirismo: Afetuoso com a fam\u00edlia, mas pode ser desconfiado com estranhos\n\n**3. Akita**\n\n* Porte: Grande (masculino at\u00e9 65 cm, feminino at\u00e9 61 cm)\n* Temperamento: Independente, leal e protetor\n* Atividade f\u00edsica: Moderada (1 hora por dia)\n* Companheirismo: Guardi\u00e3es devotados e companheiros amorosos"'
  
    response = model.generate_content(prompt)
   
    # Remove imagem de loading
    hide_loading_spinner()

    return response.text

# Botão para consultar raças
botao = customtkinter.CTkButton(master=frame, text="Consultar raças", command=generateFrameSuccess)

# Empacotar os widgets
title.pack(padx=5, pady=10)
age_label.pack(padx=5, pady=5)
age.pack(padx=5, pady=5)
purpose.pack(padx=5, pady=5)
option_purpose.pack(padx=5, pady=5)
stroll.pack(padx=5, pady=5)
option_stroll.pack(padx=5, pady=5)
availability.pack(padx=5, pady=5)
option_availability.pack(padx=5, pady=5)
size.pack(padx=5, pady=5)
option_size.pack(padx=5, pady=5)
brushing.pack(padx=5, pady=5)
option_brushing.pack(padx=5, pady=5)
place.pack(padx=5, pady=5)
option_place.pack(padx=5, pady=5)
divider.pack(fill="x", padx=2, pady=8)
botao.pack(padx=20, pady=42)

# Iniciar a interface gráfica
janela.mainloop()
