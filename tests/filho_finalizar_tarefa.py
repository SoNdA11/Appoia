from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def iniciar_driver():
    service = Service(executable_path="geckodriver")
    return webdriver.Firefox(service=service)

def login_filho(driver):
    driver.get("https://appoia-app.glide.page")

    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "is-signin")))

    campo_email = driver.find_element(By.CLASS_NAME, "is-signin")
    campo_email.clear()
    campo_email.send_keys("appoiaappfilho@gmail.com" + Keys.ENTER)

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "is-signin")))

    codigo = input("Código recebido no email: ")
    campo_codigo = driver.find_element(By.CLASS_NAME, "is-signin")
    campo_codigo.clear()
    campo_codigo.send_keys(codigo + Keys.ENTER)

def acessar_minhas_tarefas(driver):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Minhas Tarefas')]"))
    )
    botao_tarefas = driver.find_element(By.XPATH, "//span[contains(text(), 'Minhas Tarefas')]/ancestor::button")
    botao_tarefas.click()

def abrir_tarefa(driver):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='collection-item-0']"))
    )
    detalhes_tarefa = driver.find_element(By.CSS_SELECTOR, "[data-testid='collection-item-0']")
    detalhes_tarefa.click()

def finalizar_tarefa(driver):
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Finalizar Tarefa']"))
    )
    finalizar = driver.find_element(By.XPATH, "//button[@aria-label='Finalizar Tarefa']")
    finalizar.click()

def main():
    driver = iniciar_driver()
    try:
        login_filho(driver)
        acessar_minhas_tarefas(driver)
        abrir_tarefa(driver)
        finalizar_tarefa(driver)

        time.sleep(20)  # Tempo para visualização
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
