from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given('I am on the registration page')
def step_impl(context):
    context.browser = webdriver.Firefox()  # You can also use other browsers
    context.browser.get('http://localhost:8000/register/')  # Replace with your registration URL

#When I enter username "new_user" and email "user1@one.com" and password1 "password123" and password2 "password123" and RegistrationCode "abcd1"
#@when('I enter username "{username}" and email "{email}" password1 "{password1}" and password2 "{password2}" and RegistrationCode "{RegistrationCode}"')
@when(u'I enter username "{username}" and email "{email}" and password1 "{password1}" and password2 "{password2}" and RegistrationCode "{code}"')
def step_impl(context, username, email, password1, password2, code):
    #print(f">>> CHECKING")
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_field = context.browser.find_element(By.NAME, "username")
    username_field.send_keys(username)

    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_field = context.browser.find_element(By.NAME, "email")
    email_field.send_keys(email)

    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.NAME, "password1"))
    )
    password_field1 = context.browser.find_element(By.NAME, "password1")
    password_field1.send_keys(password1)

    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.NAME, "password2"))
    )
    password_field2 = context.browser.find_element(By.NAME, "password2")
    password_field2.send_keys(password2)

    WebDriverWait(context.browser, 30).until(
        EC.presence_of_element_located((By.NAME, "RegistrationCode"))
    )
    RegistrationCode = context.browser.find_element(By.NAME, "RegistrationCode")
    RegistrationCode.send_keys(code)

@when('I click the registration "{button}" button')
def step_impl(context, button):
    WebDriverWait(context.browser, 30).until(
        EC.presence_of_element_located((By.NAME, button))
    )
    login_button = context.browser.find_element(By.NAME, button)
    login_button.click()

@then('I should see registration "{text}"')
def step_impl(context, text):
    WebDriverWait(context.browser, 30).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
    )
    assert text in context.browser.page_source


@given('I am on the login page')
def step_impl(context):
    context.browser.get('http://localhost:8000/login')  # Replace with your login URL



@when('I enter email "{email}" and password "{password}"')
def step_impl(context, email, password):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_field = context.browser.find_element(By.NAME, "email")
    email_field.send_keys(email)

    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field = context.browser.find_element(By.NAME, "password")
    password_field.send_keys(password)

@when('I click the login "{button}" button')
def step_impl(context, button):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.NAME, button))
    )
    login_button = context.browser.find_element(By.NAME, button)
    login_button.click()

# this has to be implemented for user home page
@then('I should see login "{text}"')
def step_impl(context, text):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
    )
    assert text in context.browser.page_source



@then('I close the browser')
def step_impl(context):
    context.browser.quit()




