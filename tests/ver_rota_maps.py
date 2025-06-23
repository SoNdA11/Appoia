from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time # Importar a biblioteca time para pausas

# Inicializa o navegador
# Certifique-se de que 'chromedriver.exe' está no PATH ou no mesmo diretório do script
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Abre o site
driver.get('https://appoia-app.glide.page/dl/a400f7')

# Espera o campo de e-mail aparecer e preenche
wait = WebDriverWait(driver, 20)
try:
    email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Insira o seu e-mail']")))
    email_input.send_keys("appoiaapp@gmail.com")
    print("E-mail preenchido.")
except TimeoutException:
    print("Erro: Campo de e-mail não encontrado após 20 segundos.")
    driver.quit()
    exit()

# Espera o botão 'Continuar' e clica
try:
    botao_continuar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Continuar']")))
    botao_continuar.click()
    print("Botão 'Continuar' clicado.")
except TimeoutException:
    print("Erro: Botão 'Continuar' não encontrado ou não clicável.")
    driver.quit()
    exit()


# Aguarda o usuário inserir o PIN manualmente e a página carregar
print("Aguardando o usuário inserir o PIN e a página carregar (até 180 segundos)...")

# Loop que espera o cartão aparecer (indicando que o login foi feito)
max_wait_time = 180
poll_interval = 2
elapsed_time = 0
card = None
while elapsed_time < max_wait_time:
    try:
        # Verifica se o cartão "Estudar para a prova de Geografia" apareceu
        card = driver.find_element(By.XPATH, "//p[contains(text(), 'Estudar para a prova de Geografia')]")
        if card.is_displayed():
            print("Login concluído com sucesso: Cartão 'Estudar para a prova de Geografia' encontrado.")
            break
    except NoSuchElementException:
        pass  # O elemento ainda não apareceu, continua esperando
    time.sleep(poll_interval)
    elapsed_time += poll_interval

if not card:
    print("Tempo esgotado aguardando o PIN ou o carregamento da página principal. Encerrando o script.")
    driver.quit()
    exit()


try:
    # --- NOVO FLUXO: NAVEGAR PARA 'DEFINIR ROTAS' ---
    print("Aguardando o botão/link 'Definir Rotas' aparecer e clicando...")
    # Assumindo que "Definir Rotas" é um elemento clicável, como um botão ou link,
    # que contém o texto "Definir Rotas" ou "Rotas".
    # Ajuste o XPath conforme a estrutura real do seu site.
    definir_rotas_element = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(., 'Definir Rotas')] | //a[contains(., 'Definir Rotas')] | //div[contains(., 'Definir Rotas') and @role='button']"
    )))
    definir_rotas_element.click()
    print("'Definir Rotas' clicado com sucesso.")

    # --- SELECIONAR ROTA ESPECÍFICA ('Casa para Kumon') PARA ACESSAR OS DETALHES ---
    print("Aguardando a lista de rotas e selecionando a rota 'Casa para Kumon'...")
    # Alterado para clicar no elemento <p> com o texto "Casa para Kumon"
    rota_casa_kumon_element = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//p[contains(text(), 'Casa para Kumon')]"
    )))
    rota_casa_kumon_element.click()
    print("Rota 'Casa para Kumon' selecionada para visualização de detalhes.")

    # --- VERIFICAR A EXISTÊNCIA DO BOTÃO "VER ROTA NO GOOGLE MAPS" ---
    print("Verificando a existência do botão 'Ver rota no Google Maps'...")
    google_maps_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(., 'Ver rota no Google Maps')] | //a[contains(., 'Ver rota no Google Maps')]"
    )))
    print("Botão 'Ver rota no Google Maps' encontrado.")

    # --- CLICAR NO BOTÃO ---
    google_maps_button.click()
    print("Botão 'Ver rota no Google Maps' clicado.")

    # --- VERIFICAR A VISUALIZAÇÃO DA ROTA NO GOOGLE MAPS PELA URL ---
    print("Verificando se a URL do Google Maps foi carregada...")
    # Espera até que a URL contenha 'google.com/maps'
    wait.until(EC.url_contains("google.com/maps"))
    current_url = driver.current_url
    print(f"URL atual: {current_url}")

    if "google.com/maps" in current_url:
        print("Sucesso: A rota foi visualizada no Google Maps.")
    else:
        print("Falha: A URL não corresponde ao Google Maps.")

except (NoSuchElementException, TimeoutException) as e:
    print(f"Ocorreu um erro durante a automação: {e}")
finally:
    input("Pressione Enter para fechar o navegador...")
    driver.quit()