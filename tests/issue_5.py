from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # Importar Keys para enviar ENTER

import time
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime, timedelta
import random

# Constantes de Configuração
TEST_EMAIL_ADDRESS = "testeappoiaapp@gmail.com"
TEST_EMAIL_APP_PASSWORD = "wvtw icjb qjyx gbla"
EMAIL_SUBJECT_FILTER = "Your pin for Appoia is"
VERIFICATION_CODE_REGEX = r'Your pin for Appoia is (\d{6,})'
APPOIA_LOGIN_URL = "https://appoia-app.glide.page/dl/a400f7" # URL de login original
APPOIA_CALENDAR_URL = "https://appoia-app.glide.page/dl/783bbb" # Nova URL para o calendário
APPOIA_SUCCESS_URL = "https://appoia-app.glide.page/dl/de6ccd" # Nova URL para a página de sucesso

def initialize_driver():
    """
    Inicializa e retorna uma instância do WebDriver do Chrome.
    """
    print("Inicializando WebDriver do Chrome...")
    service = ChromeService(executable_path="chromedriver.exe")
    options = ChromeOptions()
    # options.add_argument("--headless")  # Descomente para rodar em modo headless (sem UI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    print("WebDriver inicializado com sucesso.")
    return driver

def get_latest_verification_code(email_address, app_password, subject_filter, regex_pattern, wait_time=60, check_interval=5):
    """
    Busca o código de verificação mais recente no e-mail.
    Tenta se conectar ao servidor IMAP e procura por e-mails com o assunto e desde a data especificados.
    Extrai o código usando uma expressão regular.
    """
    print(f"Buscando código de verificação no e-mail: {email_address}...")
    
    print("Aguardando 5 segundos antes de conectar ao servidor de e-mail para garantir o recebimento...")
    time.sleep(10) # Aumentado para 10 segundos para dar tempo do e-mail chegar

    time_before_sending_code = datetime.now() 
    date_criteria = time_before_sending_code.strftime("%d-%b-%Y") 

    start_time = time.time()

    while time.time() - start_time < wait_time:
        mail = None
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_address, app_password)
            mail.select('inbox')

            # Tenta buscar por e-mails UNSEEN com o assunto
            unseen_subject_search_command = f'UNSEEN SUBJECT "{subject_filter}"'
            print(f"Tentando buscar com comando IMAP: '{unseen_subject_search_command}'")
            status, email_ids = mail.search(None, unseen_subject_search_command)
            
            # Se nenhum UNSEEN for encontrado, tenta buscar por e-mails recebidos DESDE uma data específica
            if not email_ids[0]:
                print(f"Nenhum e-mail UNSEEN encontrado. Tentando buscar por e-mails recebidos DESDE {date_criteria} e assunto: '{subject_filter}'")
                since_subject_search_command = f'SUBJECT "{subject_filter}" SINCE "{date_criteria}"'
                print(f"Tentando buscar com comando IMAP: '{since_subject_search_command}'")
                status, email_ids = mail.search(None, since_subject_search_command)

            # Se ainda não houver IDs de e-mail, espera e tenta novamente
            if not email_ids[0]:
                print(f"Nenhum e-mail encontrado com os critérios. Tentando novamente em {check_interval} segundos...")
                mail.logout()
                time.sleep(check_interval)
                continue

            list_email_ids = email_ids[0].split()
            latest_email_id = list_email_ids[-1] # Pega o ID do e-mail mais recente

            # Busca o conteúdo completo do e-mail
            status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Decodifica o assunto do e-mail
            decoded_subject = ""
            for s, enc in decode_header(msg["Subject"]):
                if isinstance(s, bytes):
                    decoded_subject += s.decode(enc if enc else "utf-8")
                else:
                    decoded_subject += s
            
            code = None
            # Tenta encontrar o código no assunto
            match_subject = re.search(regex_pattern, decoded_subject)
            if match_subject:
                code = match_subject.group(1)
                print(f"Código encontrado no ASSUNTO: {code}")
            else:
                # Se não encontrado no assunto, tenta no corpo do e-mail
                body = "" 
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdisposition = str(part.get("Content-Disposition"))
                        # Verifica se é texto puro e não um anexo
                        if ctype == "text/plain" and "attachment" not in cdisposition:
                            body = part.get_payload(decode=True).decode()
                            match_body = re.search(regex_pattern, body) 
                            if match_body:
                                code = match_body.group(1)
                                print(f"Código encontrado no CORPO: {code}")
                                break # Sai do loop assim que encontrar o código
                else:
                    body = msg.get_payload(decode=True).decode()
                    match_body = re.search(regex_pattern, body)
                    if match_body:
                        code = match_body.group(1)
                        print(f"Código encontrado no CORPO: {code}")

            if code:
                # Marca o e-mail como lido e desloga
                mail.store(latest_email_id, '+FLAGS', '\\Seen')
                print(f"E-mail {latest_email_id.decode()} marcado como lido.")
                mail.logout()
                return code
            else:
                print(f"E-mail encontrado, mas o código não foi extraído com a regex '{regex_pattern}'.")
                print(f"Assunto do e-mail: {decoded_subject}")
                print(f"Conteúdo parcial do corpo do e-mail:\n{body[:500]}...") # Mostra um pedaço do corpo para depuração
                mail.logout()
                time.sleep(check_interval)
                continue

        except imaplib.IMAP4.error as e:
            print(f"Erro IMAP ao buscar código (verifique credenciais ou configurações IMAP): {e}")
            print(f"Tentando novamente em {check_interval} segundos...")
            if mail:
                try: mail.logout()
                except Exception as ex: print(f"Erro ao deslogar do IMAP: {ex}")
            time.sleep(check_interval)
        except Exception as e:
            print(f"Erro geral ao buscar código no email: {e}. Tentando novamente em {check_interval} segundos...")
            if mail:
                try: mail.logout()
                except Exception as ex: print(f"Erro ao deslogar do IMAP: {ex}")
            time.sleep(check_interval)

    print("Tempo limite excedido. Não foi possível obter o código de verificação.")
    return None

def login_to_appoia(driver, email_address, app_password, subject_filter, regex_pattern):
    """
    Realiza o processo de login no aplicativo Appoia.
    """
    print(f"Navegando para a URL de login: {APPOIA_LOGIN_URL}")
    driver.get(APPOIA_LOGIN_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2) # Pequena pausa para garantir que a página carregou

    print("Iniciando fluxo de login...")
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Insira o seu e-mail']"))
        )
        email_input.send_keys(email_address)
        print(f"E-mail '{email_address}' preenchido.")
    except Exception as e:
        print(f"Não foi possível encontrar ou preencher o campo de e-mail. Erro: {e}")
        return False

    try:
        enter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continuar')]"))
        )
        enter_button.click()
        print("Botão 'Continuar' clicado. Aguardando envio do código.")
    except Exception as e:
        print(f"Não foi possível encontrar ou clicar no botão 'Continuar'. Erro: {e}")
        return False

    verification_code = get_latest_verification_code(
        email_address,
        app_password,
        subject_filter,
        regex_pattern
    )

    if verification_code:
        try:
            code_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='00000']"))
            )
            code_input.send_keys(verification_code)
            print(f"Código de verificação '{verification_code}' preenchido.")
        except Exception as e:
            print(f"Não foi possível encontrar ou preencher o campo do código. Erro: {e}")
            return False

        try:
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Logar')]"))
            )
            confirm_button.click()
            print("Botão 'Logar' clicado. Finalizando login.")
        except Exception as e:
            print(f"Não foi possível encontrar ou clicar no botão 'Logar'. Erro: {e}")
            return False

        time.sleep(5) # Aguarda a navegação pós-login
        print(f"URL atual após login: {driver.current_url}")
        # Uma verificação mais robusta do sucesso do login seria ideal aqui,
        # como verificar um elemento presente apenas após o login bem-sucedido.
        if "Seja bem-vindo" in driver.page_source or APPOIA_LOGIN_URL in driver.current_url:
            print("Login com sucesso! Teste de login passou.")
            return True
        else:
            print("Login falhou ou a página pós-login não carregou como esperado.")
            return False
    else:
        print("Falha: Não foi possível obter o código de verificação do e-mail. Teste de login falhou.")
        return False
    
def get_text_areas_by_data_testid(driver):
    """
    Função auxiliar para obter todas as textareas com data-testid='wf-input'
    e garantir que a lista não esteja vazia.
    """
    # Primeiro, espera por pelo menos uma textarea com data-testid='wf-input'
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@data-testid='wf-input']"))
    )
    # Depois, encontra todas as textareas que correspondem ao XPath
    text_areas = driver.find_elements(By.XPATH, "//textarea[@data-testid='wf-input']")
    
    if not text_areas:
        raise Exception("Nenhuma textarea com data-testid='wf-input' foi encontrada após o carregamento.")
    return text_areas

def edit_event_name(driver, new_event_name):
    """
    Edita o nome de um evento.
    ASSUMIMOS QUE O CAMPO DE NOME É O PRIMEIRO <textarea data-testid='wf-input'> ENCONTRADO.
    """
    print(f"\nTentando editar o nome do evento para: '{new_event_name}'.")
    try:
        text_areas = get_text_areas_by_data_testid(driver)
        if len(text_areas) > 0:
            event_name_input = text_areas[0] 
            event_name_input.clear() # Limpa o campo existente
            event_name_input.send_keys(new_event_name)
            print(f"Novo nome do evento '{new_event_name}' preenchido.")
        else:
            raise Exception("Não há campos de texto suficientes para o nome do evento.")
    except Exception as e:
        print(f"Não foi possível encontrar ou preencher o campo de nome do evento (verifique a ordem ou XPaths). Erro: {e}")
        raise # Re-lança a exceção para ser capturada na função principal

def edit_event_location(driver, new_location):
    """
    Edita o campo de localização do evento.
    ASSUMIMOS QUE O CAMPO DE LOCALIZAÇÃO É O SEGUNDO <textarea data-testid='wf-input'> ENCONTRADO.
    """
    print(f"Tentando editar a localização do evento para: '{new_location}'.")
    try:
        text_areas = get_text_areas_by_data_testid(driver)
        if len(text_areas) > 1: # Verifica se há pelo menos dois campos
            location_input = text_areas[1] 
            location_input.clear()
            location_input.send_keys(new_location)
            print(f"Nova localização '{new_location}' preenchida.")
        else:
            raise Exception("Não há campos de texto suficientes para a localização do evento.")
    except Exception as e:
        print(f"Não foi possível encontrar ou preencher o campo de localização (verifique a ordem ou XPaths). Erro: {e}")
        raise

def edit_event_observation(driver, new_observation):
    """
    Edita o campo de observação do evento.
    """
    print(f"Tentando editar a observação do evento para: '{new_observation}'.")
    try:
        text_areas = get_text_areas_by_data_testid(driver)
        if len(text_areas) > 2: # Verifica se há pelo menos dois campos
            observation_input = text_areas[2] 
            observation_input.clear()
            observation_input.send_keys(new_observation)
            print(f"Nova localização '{new_observation}' preenchida.")
        else:
            raise Exception("Não há campos de texto suficientes para a observação do evento.")
    except Exception as e:
        print(f"Não foi possível encontrar ou preencher o campo de observação (verifique a ordem ou XPaths). Erro: {e}")
        raise


def edit_event_date_time(driver, target_date: datetime):
    """
    Edita a data e hora do evento clicando no calendário pop-up.
    target_date: Um objeto datetime com a data e hora desejadas.
    É CRÍTICO AJUSTAR OS XPATHS PARA O CALENDÁRIO E SELETORES DE HORA.
    """
    print(f"Tentando editar data e hora para: {target_date.strftime('%d/%m/%Y %H:%M')}.")
    try:
        # 1. Clicar no campo de input da data para abrir o calendário
        date_input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@data-test='base-picker-button']"))
        )
        date_input_field.click()
        print("Campo de data clicado. Aguardando calendário...")
        time.sleep(1) # Pequena pausa para o calendário aparecer

        # 2. Navegar no calendário e selecionar o dia
        day_xpath = f"//button[contains(@class, 'MuiPickersDay-root') and text()='{target_date.day}']"
        
        target_day_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, day_xpath))
        )
        target_day_element.click()
        print(f"Dia {target_date.day} clicado no calendário.")
        time.sleep(1) # Aguarda após selecionar o dia

        try:
            ok_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='OK']"))
            )
            ok_button.click()

        except Exception as e:
            print(f"Erro ao selecionar hora/minuto: {e}")


    except Exception as e:
        print(f"Não foi possível editar a data e hora do evento. Erro: {e}")
        # Tenta fechar qualquer calendário/picker que possa ter ficado aberto
        try: driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        except: pass
        raise

def click_save_button(driver):
    """
    Clica no botão de salvar/enviar no final do formulário de edição.
    """
    print("Tentando clicar no botão Salvar/Enviar...")
    try:
        send_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Enviar']"))
        )

        print("Rolando para o botão 'Enviar' e clicando via JavaScript...")
        driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
        time.sleep(0.5) # Pequena pausa para a rolagem ser concluída
        driver.execute_script("arguments[0].click();", send_button)
        print("Botão 'Enviar' clicado com sucesso via JavaScript.")
    except Exception as e:
        print(f"Não foi possível encontrar ou clicar no botão Enviar. Erro: {e}")
        raise

def navigate_and_edit_event(driver):
    """
    Navega para a página do calendário, clica em um evento e tenta editá-lo.
    """
    print(f"Navegando para a URL do calendário: {APPOIA_CALENDAR_URL}")
    driver.get(APPOIA_CALENDAR_URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3) # Aguarda a página do calendário carregar

    try:
        # Tenta encontrar e clicar no primeiro evento do calendário.
        event_to_click = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'rbc-event-content')]")) 
        )
        event_to_click.click()
        print("Evento no calendário clicado para detalhar.")
        time.sleep(3) # Aguarda a página de detalhes do evento carregar
        
        # Edita o nome do evento
        new_event_name = f"Evento Editado {random.randint(100, 999)}"
        edit_event_name(driver, new_event_name) 

        # Edita a localização do evento
        new_location = f"Local Teste {random.randint(1, 100)}"
        edit_event_location(driver, new_location)

        days = random.randint(1, 7)
        target_date_time = datetime.now() + timedelta(days)
        edit_event_date_time(driver, target_date_time)
        
        # Edita a observação do evento
        new_observation = f"Observação gerada automaticamente para o evento {new_event_name}."
        edit_event_observation(driver, new_observation)

        # Clica no botão de salvar após todas as edições
        click_save_button(driver)

        print("\nTodos os testes de navegação e edição de evento concluídos com sucesso!")
        
        # Navega para a página de sucesso após a edição
        print(f"Navegando para a página de sucesso: {APPOIA_SUCCESS_URL}")
        driver.get(APPOIA_SUCCESS_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Navegação para a página de sucesso concluída.")
        time.sleep(3) # Aguarda para visualização da página de sucesso

    except Exception as e:
        print(f"Erro durante os testes de navegação e edição de evento: {e}")
        raise

def main():
    """
    Função principal que orquestra todo o processo de automação.
    """
    driver = None
    try:
        driver = initialize_driver()
        
        # Tenta fazer login na URL de login
        login_success = login_to_appoia(
            driver,
            TEST_EMAIL_ADDRESS,
            TEST_EMAIL_APP_PASSWORD,
            EMAIL_SUBJECT_FILTER,
            VERIFICATION_CODE_REGEX
        )

        if login_success:
            # Se o login foi bem-sucedido, prossegue com os testes de navegação e edição de evento
            navigate_and_edit_event(driver)
        else:
            print("Não foi possível prosseguir com os testes de edição de evento, pois o login falhou.")

    except Exception as e:
        print(f"Ocorreu um erro geral durante a execução do script: {e}")

    finally:
        if driver:
            print("Aguardando 5 segundos antes de fechar o navegador.")
            time.sleep(5)
            driver.quit()
            print("Navegador fechado.")

if __name__ == "__main__":
    main()

