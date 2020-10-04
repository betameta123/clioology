from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import click
import time
import os
import re

class Cliology:
    __login_email = None #TODO make this into an argument with click
    __login_password = None
    __classes = None #TODO scrape for all classes that are being taken

    def __init__(self, login_password):
        #  chrome_options = Options()
        #  chrome_options.add_argument("--headless")
        #  chrome_options.binary_location = '/usr/bin/chromium'
        #  options = Options()
        #  options.headless = True
        #  options.add_argument("--headless")
        self.driver = webdriver.Chrome()
        self.__login_email="khuang922@student.fuhsd.org"
        self.__login_password = login_password

        self.login()

    def login(self):
        self.driver.get("https://fuhsd.schoology.com/courses")
        email = self.driver.find_element_by_id("identifierId")
        email.send_keys(self.__login_email)
        email.send_keys(Keys.RETURN)

        try:
            password_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME,"password"))
            )
            password_field = self.driver.find_element_by_name("password")
            password_field.send_keys(self.__login_password)
            password_field.send_keys(Keys.RETURN)
            #TODO: Check if you are actually at google log in or not
            #TODO: If password is incorrect
        except:
            self.driver.quit()

    def prompt(self):
        print("-------------------------------------------------------------------------------------------")
        print("\n")
        print(r" ________  ___       ___  ________  ________  ___       ________  ________      ___    ___ ")
        print(r"|\   ____\|\  \     |\  \|\   __  \|\   __  \|\  \     |\   __  \|\   ____\    |\  \  /  /|")
        print(r"\ \  \___|\ \  \    \ \  \ \  \|\  \ \  \|\  \ \  \    \ \  \|\  \ \  \___|    \ \  \/  / / ")
        print(r" \ \  \    \ \  \    \ \  \ \  \\\  \ \  \\\  \ \  \    \ \  \\\  \ \  \  ___   \ \    / / ")
        print(r"  \ \  \____\ \  \____\ \  \ \  \\\  \ \  \\\  \ \  \____\ \  \\\  \ \  \|\  \   \/  /  /  ")
        print(r"   \ \_______\ \_______\ \__\ \_______\ \_______\ \_______\ \_______\ \_______\__/  / /    ")
        print(r"    \|_______|\|_______|\|__|\|_______|\|_______|\|_______|\|_______|\|_______|\___/ /     ")
        print(r"                                                                              \|___|/      ")
        print("\n")
        print("-------------------------------------------------------------------------------------------")

    def getzoom(self):
        pass
    
    def assignmentchoice(self):
        i = 1
        course_names = [0]
        assignments = {}
        dates = set([])
        current_date = ""

        courses = self.driver.find_elements_by_class_name("sections-list") 
        for c in courses:
            course_names.append(c.text)
            print("[{}]: {}".format(i, c.text))
            i += 1

        print("[a]ll")
        choice = input("Your course number> ")
        print("\n")
        
        selected_course = self.driver.find_element_by_link_text(course_names[int(choice)])
        selected_course.click()
        time.sleep(1)
        upcoming = self.driver.find_element_by_class_name("upcoming-list")
        upcoming_list = upcoming.text.split("\n")
        for c in upcoming_list:
            if re.match('\w+, \w+ [0-9]+, [0-9]+', c):
                dates.add(c)
                current_date = c
            else:
                assignments[current_date] = []
                assignments[current_date].append(c)

        for d in assignments.keys():
           for a in assignments[d]:
              print("{}\n    {}".format(d,a))

    def getgrades(self):
        pass

    def getHelp(self):
        pass
        
    def options(self):                                                                                           
        print("\n\n")
        print("  [z]oom:")
        print("  [a]ssignments:")
        print("  [g]rades: ")
        print("  [h]elp")
        print("  [e]xit: ")
        print("\n")
        choice = input("Your choice > ")

        if 'Z' == choice.upper() or 'ZOOM' == choice.upper():
            self.getzoom()
        elif 'A' == choice.upper() or 'ASSIGNMENTS' == choice.upper():
            self.assignmentchoice()
        elif 'G' == choice.upper() or 'GRADES' == choice.upper():
            self.getgrades()
        elif 'H' == choice.upper() or 'HELP' == choice.upper():
            self.getHelp()
        elif 'E' == choice.upper() or 'EXIT' == choice.upper():
            self.driver.quit()
            exit(1)

    def run(self):
        self.prompt()
        while True:
            self.options()
            choice = self.options()
                        
@click.command()
@click.option("--login-password", prompt=True, hide_input=True) 
def cli(login_password):
    Cliology(login_password).run()
