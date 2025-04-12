from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint
from time import sleep

'''
This program was written entirely for fun (and to explore Selenium), and was not distributed to any third parties. 
The code uses a very specific set of instructions and will not work for any assignment.
I do not support Academic Dishonesty of any kind.
'''

# Login and assignment link
username = "..."
password = "..."
site = "..."

def show(step):
    "Used to print colored text in the terminal to show the program working."
    return '\033[92m' + step + '\033[0m'

def randsleep():
    "Sleep for a random number of miliseconds"
    sleep(randint(100,1000)/1000)

# Using Selenium to navigate to the assignment:
driver = webdriver.Chrome()
driver.get(site)
wait = WebDriverWait(driver, timeout=20) # Timeout to 20s to be lenient. No reason not to have a longer timeout period.

# Log in to homepage
print(show("Logging in..."))
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "login-btn").click()

# Complete homepage 2FA
print(show("Waiting for 2FA... "))
auth2 = wait.until(EC.element_to_be_clickable((By.ID, 'trust-browser-button')))
auth2.click()   

# Open course assignment page
print(show("Opening course assignment page..."))
open_page = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn')))
open_page.click()
driver.close()

# Open assignment
print(show("Opening assignment..."))
driver.switch_to.window(driver.window_handles[0])
open_assignment = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "MuiButton-label")))
open_assignment.click()
driver.implicitly_wait(5)

# Find and store all input boxes
input_boxes = driver.find_elements(By.XPATH, "//input[@type='text']")
print(show(f"\n There are... {len(input_boxes)} parts to the first question.\n"))

# Solve all parts of the question
for i in range(len(input_boxes)):
    guess = float(input(show("Enter a starting value: ")))

    correct = False

    while not correct:
        # Input and submit guess
        input_boxes[i].clear()
        input_boxes[i].send_keys(round(guess, 3))
        driver.find_element(By.XPATH, '//button[text()="Submit Answer"]').click()

        # Increment guess and wait for a moment before repeating
        guess *= 1.05
        randsleep()   

        # Check if the guess is correct (if the input box is still enabled)
        correct = not driver.find_element(By.XPATH, f"//input[@type='text'][{i+1}]").is_enabled()

print(show("Question complete."))