from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import click
import time
import os
import re

class Cliology:
    __login_email = None #TODO make this into an argument with click
    __login_password = None
    __classes = None #TODO scrape for all classes that are being taken

    def __init__(self, login_password):
        self.driver = webdriver.Chrome()
        self.__login_email="khuang922@student.fuhsd.org"
        self.__login_password = login_password

        self.course_names = [0]
        self.assignments = {}
        self.dates = set([])

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

    def getassignments(self,choice):
        current_date = ""
        selected_course = self.driver.find_element_by_link_text(self.course_names[int(choice)])
        selected_course.click()
        time.sleep(1)
        upcoming = self.driver.find_element_by_class_name("upcoming-list")
        upcoming_list = upcoming.text.split("\n")
    
        for c in upcoming_list:
            if c == "No upcoming assignments or events":
                return
            if re.match('\w+, \w+ [0-9]+, [0-9]+', c):
                self.dates.add(c)
                current_date = c
                self.assignments[current_date] = []
            else:
                if bool(self.assignments):
                    self.assignments[current_date].append(c)


    def assignmentchoice(self):
        i = 1
        current_date = " "

        courses = self.driver.find_elements_by_class_name("sections-list") 
        for c in courses:
            self.course_names.append(c.text)
            print("[{}]: {}".format(i, c.text))
            i += 1

        print("[a]ll")
        choice = input("Your course number> ")
        print("\n")
        if choice.upper() == "A":
            for c in tqdm(range(1,i), ncols=i+20):
                self.getassignments(c)
                self.driver.back()

        elif int(choice) <= i and int(choice) > 0:
            self.getassignments(choice) 

        for d in self.assignments.keys():
            print("{}".format(d))
 
            for a in self.assignments[d]:
              print("    {}\n".format(a))

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
