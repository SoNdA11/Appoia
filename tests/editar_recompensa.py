from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="geckodriver")
driver = webdriver.Firefox()

try:
    
    driver.get("https://appoia-app.glide.page")

    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "is-signin"))
    )
    
    campo_email = driver.find_element(By.CLASS_NAME, "is-signin")
    campo_email.clear()
    campo_email.send_keys("appoiaapp@gmail.com" + Keys.ENTER)

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "is-signin"))
    )

    codigo = input("Código recebido no email: ")

    campo_codigo = driver.find_element(By.CLASS_NAME, "is-signin")
    campo_codigo.clear()
    campo_codigo.send_keys(codigo + Keys.ENTER)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Definir Recompensas')]"))
    )

    botao_recompensa = driver.find_element(By.XPATH, "//span[contains(text(), 'Definir Recompensas')]/ancestor::button")
    botao_recompensa.click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='collection-item-0']"))
    )
    
    detalhes_recompensa = driver.find_element(By.CSS_SELECTOR, "[data-testid='collection-item-0']")
    detalhes_recompensa.click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Editar']"))
    )

    editar_recompensa = driver.find_element(By.CSS_SELECTOR, "[aria-label='Editar']")
    editar_recompensa.click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='wf-input']"))
    )

    titulo = input("Digite o Título: ")
    descricao = input("Digite a Descrição: ")

    while True:
        custo = input("Insira o Custo (somente números): ")
        if custo.isdigit():
            break
        else:
            print("Valor inválido! Digite apenas números. ")
        
    disponibilidade = input("Insira a disponibilidade (Disponível / Indisponível?: ").lower()

    campos = driver.find_elements(By.CSS_SELECTOR, "[data-testid='wf-input']")
    
    campos[0].clear()
    campos[0].send_keys(titulo)

    campos[1].clear()
    campos[1].send_keys(descricao)

    campos[2].clear()
    campos[2].send_keys(custo)
    
    if disponibilidade == "disponível":
        opcao = driver.find_element(By.XPATH, "//li[contains(text(), 'Disponível')]")
        opcao.click()
    elif disponibilidade == "indisponível":
        opcao = driver.find_element(By.XPATH, "//li[contains(text(), 'Não Disponível')]")
        opcao.click()
    else:
        print("Opção inválida. Nenhuma alteração foi realizada")
        opcao = None

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[.//div[contains(text(), 'Submit')]]"))
    )

    salvar = driver.find_element(By.XPATH, "//button[.//div[contains(text(), 'Submit')]]")
    driver.execute_script("arguments[0].click();", salvar)
    
    WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.CSS_SELECTOR, ".wire-field___StyledDiv-sc-1nuhqre-2.iBNbMO"))
    )
    
    voltar = driver.find_element(By.CSS_SELECTOR, "[aria-label='Voltar']")
    voltar.click()


    time.sleep(20)

finally:
    driver.quit()
