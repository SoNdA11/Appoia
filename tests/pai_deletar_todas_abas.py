import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



nome_elemento_deletado = ""
service = Service(executable_path="chromedriver.exe")
google = webdriver.Chrome(service=service)
url = "https://appoia-app.glide.page/"
google.get(url)
    

def abrir_aba(nome_aba):
    # Abas -> Definir Tarefa | Definir Rota | Definir Recompensas | Definir Eventos
    try:
        aba = google.find_element("xpath", f"//span[contains(text(),'{nome_aba}')]")
    except (TimeoutException, NoSuchElementException):
        print(f"Elemento '{nome_aba}' não encontrado!")
    else:
        print(f"Elemento '{nome_aba}' encontrado!")
        aba.click()

def deletar_geral():
    try: 
        dropdown_menu = WebDriverWait(google, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Menu' and contains(@class, 'wire-button')]"))
        )
    except (TimeoutException, NoSuchElementException): 
        print("Elemento não encontrado, não há elementos na página")
    else: 
        print("Elemento encontrado!")
        dropdown_menu.click()
        time.sleep(1)
        print("Buscando informações do item selecionado")
        
        # Segunda etapa - Pegar informações do Item
        try:
            elemento_selecionado = WebDriverWait(google, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'card-collection-list___StyledP2-s6kvv4-19')]"))
            )
            global nome_elemento_deletado
            nome_elemento_deletado = elemento_selecionado.get_attribute("innerHTML")
        except (TimeoutException, NoSuchElementException): 
            print("Não foi possível pegar as informações do elemento selecionado")
        else:
            print("Informações do Elemento Adquiridas, teste de deleção pode ser realizado.")
        
        # Terceira etapa - Clicar no Botão de Excluir
        try: 
            btn_deletar = WebDriverWait(google, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-testid='mb-li' and text()='Deletar']"))
            )
        except (TimeoutException, NoSuchElementException): 
            print("Botão não encontrado")
        else: 
            print("Botão encontrado, a exclusão será feita agora")
            btn_deletar.click()
            time.sleep(3)
    
    

def confirmar_delecao_geral():
    # Pensar na possibilidade de alterar para analisar a quantidade de itens.
    try:
        global nome_elemento_deletado
        elemento_deletado = google.find_element("xpath", f"//p[contains(@class, 'card-collection-list___StyledP2-s6kvv4-19') and normalize-space(text())='{nome_elemento_deletado}']")
    except NoSuchElementException:  # Substitua ValueError por NoSuchElementException
        print("Elemento não encontrado, a Exclusão foi Realizada com Sucesso")
    else:
        print("Elemento encontrado, a exclusão não ocorreu corretamente")


def finalizar_testes(): 
    google.quit()

def iniciar_testes(aba):
    confirmacao = input("\n\n\nPRESS ENTER TO CONTINUE \n\n\n")
    abrir_aba(aba)
    deletar_geral()
    confirmar_delecao_geral()
    confirmacao = input("\n\n\nPRESS ENTER TO FINISH \n\n\n")
    finalizar_testes()
