from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# --- CONFIGURA O CHROMEDRIVER ---
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)  # tempo de espera reduzido para elementos

# --- 1) LOGIN ---
driver.get("https://appoia-app.glide.page/dl/a400f7")

try:
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Insira o seu e-mail']"))).send_keys("appoiaappfilho@gmail.com")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Continuar']"))).click()
    print("Credenciais enviadas.")
except TimeoutException:
    print("Falha localizando campo de e-mail ou botão Continuar.")
    driver.quit()
    quit()

# --- 2) ESPERA VOCÊ INSERIR O PIN MANUALMENTE ---
print("Aguardando você inserir o PIN e concluir o login manualmente (20 segundos)...")
time.sleep(20)

# --- 3) CONFIRMA QUE ENTROU PELO <h2> COM NOME ---
try:
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Lucas Pereira Silva']")))
    print("Login confirmado: nome do usuário localizado.")
except TimeoutException:
    print("Não encontrei o nome do usuário após o login.")
    driver.quit()
    quit()

# --- 4) ABRE O MENU LATERAL (se houver ícone '☰') ---
try:
    menu_icon = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[@aria-label='Abrir menu'] | //div[@role='button' and (text()='☰' or .='☰')]"
    )))
    menu_icon.click()
    print("Menu lateral aberto.")
except TimeoutException:
    # Se não existir, o menu já deve estar visível — segue adiante
    pass

# --- 5) CLICA NO BOTÃO "RECOMPENSAS" ---
try:
    recompensas_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[.//span[normalize-space()='Recompensas']]"
    )))
    recompensas_btn.click()
    print("Botão 'Recompensas' clicado.")
except TimeoutException:
    print("Botão 'Recompensas' não localizado.")
    driver.quit()
    quit()

# --- 6) CLICA NA RECOMPENSA COM NOME ESPECÍFICO ABAIXO DE "Disponível" ---
recompensa_desejada = "Ir ao Cinema"  # <- Altere aqui conforme quiser

try:
    print(f"Procurando recompensa '{recompensa_desejada}' na seção 'Disponível'...")

    # Localiza o título da seção "Disponível"
    secao_disponivel = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[normalize-space()='Disponível']")))

    # Encontra o container logo abaixo dessa seção
    container = secao_disponivel.find_element(By.XPATH, "./following-sibling::div[1]")

    # Dentro do container, procura pela recompensa desejada usando o XPath atualizado
    recompensa = container.find_element(By.XPATH, f".//p[normalize-space()='{recompensa_desejada}']/ancestor::div[contains(@class, 'card-collection-list___StyledDiv6')]")

    recompensa.click()
    print(f"Recompensa '{recompensa_desejada}' selecionada com sucesso.")
except TimeoutException:
    print(f"❌ Não foi possível encontrar a recompensa '{recompensa_desejada}'.")
    driver.quit()
    quit()

# --- 7) VERIFICA E CLICA NO BOTÃO "Trocar por Recompensa" ---
try:
    botao_trocar = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[normalize-space()='Trocar por Recompensa']"
    )))
    botao_trocar.click()
    print("Botão 'Trocar por Recompensa' clicado.")
except TimeoutException:
    print("❌ Botão 'Trocar por Recompensa' não encontrado.")
    driver.quit()
    quit()

# --- 8) VERIFICA NOTIFICAÇÃO OU ALTERAÇÃO VISUAL QUE INDIQUE SUCESSO ---
try:
    notificacao = wait.until(EC.any_of(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Recompensa trocada')]")),
        EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'sucesso')]")),
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Você resgatou')]")),
        EC.invisibility_of_element_located((By.XPATH, "//button[normalize-space()='Trocar por Recompensa']"))
    ))
    print("✅ Recompensa trocada com sucesso.")
except TimeoutException:
    print("⚠ Nenhuma confirmação clara de resgate foi detectada.")

input("Pressione Enter para fechar o navegador…")
driver.quit()