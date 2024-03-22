from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I am on the login page')
def step_impl(context):
    context.browser = webdriver.Firefox()
    context.browser.get('http://localhost:8000/login')

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

@then('I should see login "{text}"')
def step_impl(context, text):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
    )
    assert text in context.browser.page_source

# this has to be implemented for user home page
@then('I should see "{text}" on the home page')
def step_impl(context, text):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
    )
    assert text in context.browser.page_source


@then('I close the browser')
def step_impl(context):
    context.browser.quit()