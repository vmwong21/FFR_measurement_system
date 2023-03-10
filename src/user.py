import pandas as pd
import datetime, time, random
from src.system import System
from src.ffr_measure import FFR_measure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

opts = ChromeOptions()
# opts.add_argument("--headless")

class User:
    def __init__(self, userid):
        # userid that is logged into is a instance variable, used by multiple functions.
        self.userid = userid

    def menu(self):
        """
        Menu for the 4 user options. Displays user ID at the top.
        :return:
        """
        print(f"\nUser {self.userid} \n Menu: \n 1. Begin case \n 2. Review case \n 3. Create user account \n 4. Exit (terminate program)")
        choice_1 = int(input("\nEnter number (ex. '1', '2', '3') for action: "))

        if choice_1 == 1: # Begin case
            User.one_begin_case(self)
        elif choice_1 == 2: # 2. Review case
            User.two_review_case(self)
        elif choice_1 == 3: # 3. Create user account
            User.three_create_user_account(self)
        elif choice_1 == 4: # 4. Exit
            exit()

    # 1. Begin Case
    def one_begin_case(self):
        """
        Menu option 1, to run a case.
        :return:
        """
        # 1. Display patients to the user, to pick from.
        print("List of patients on system:")
        print(System.load_patients(self))

        #2. Prompt choice of patient in system, or to create new patient.
        choice_2 = int(input("\n (1) Select existing patient. \n (2) Create a new patient. \n \n Choice ('1' or '2'): "))

        #3. Depending on choice, launch a new case.
        if choice_2 == 1: # existing patient
            requested_patient = int(input("\n Enter patient ID: "))
            # Check if patient ID is in database, and start new case with patient ID if True.
            if System.check_existing_patient(self, requested_patient): # is True
                User.case_new(self, requested_patient) # Initialize case with patient ID.
            else:
                print("\n Patient doesn't exist. Return to menu. ")
        elif choice_2 == 2: # new patient
            # Create new patient, as a list. Take patient number as an integer, and initialize case with patient ID.
            new_patient_list = User.create_patient(self)
            new_patient = int(new_patient_list[0])
            User.case_new(self, new_patient) # proceed to FFR ===============work on this
        else:
            print("Invalid choice. Pick a valid choice.")
            User.one_begin_case(self)

        # 4. After measurement is done, prompt performing another case. Or go to menu.
        choice_3 = int(input("\n Next action: \n (1) Perform another case? \n (2) Exit to menu? \n Choice: "))
        if choice_3 == 1:
            User.one_begin_case(self)
        else:
            User.menu(self)

    # 2. Review Case
    def two_review_case(self):
        """
        Option 2 on the menu. Query the databases and return contents.
        :return:
        """
        # 1. Prompt user choice.
        choice = int(input("\nSelect a query: \n(1) Cases by patient \n(2) cases by user. \nChoice: "))

        # 2. Based on choice, run function in System class, to return dataframe for query.
        # Display dataframe, and prompt another query, or exit to menu.
        # A. Patients
        if choice == 1:
            print("\nList of patients on system:")
            print(System.load_patients(self))
            self.chosen_patient = int(input("\nSelect a patient by ID: "))
            print(System.load_cases_of_patient(self, self.chosen_patient))
            choice = int(input("\nNext action: \n(1) Do another query \n (2) Go to Menu \n Choice: "))
            if choice == 1:
                User.two_review_case(self)
            else:
                User.menu(self)
        # B. Users
        elif choice == 2:
            print("\nList of users on system:")
            print(System.load_users(self))
            self.chosen_user = int(input("\nSelect a user by ID: "))
            print(System.load_cases_of_user(self, self.chosen_user))
            choice = int(input("\nNext action: \n(1) Do another query \n (2) Go to Menu \n Choice: "))
            if choice == 1:
                User.two_review_case(self)
            else:
                User.menu(self)
        else:
            print("\n Returning to menu...")
            User.menu(self)

    # 3. Create User Account
    def three_create_user_account(self):
        """
        Option 3 on menu to create a new user account. Take in user ID first and check if it's in the database already.
        If not, prompt data entry for new user. Pass as a list to System, to write to the user database file.
        :return:
        """
        print("\nFor new user, enter:")
        new_id = int(input(
            "\nUnique user ID, as a number (5 digits): "))
        if System.check_existing_user(self, new_id) is False:
            first_name = str(input("First name: "))
            last_name = str(input("Last name: "))
            password = str(input("Password: "))
            user_new = [new_id, first_name, last_name, password]
            print(f"\nUser summary: {user_new}")
            System.change_data(self, 'user', user_new)
            print("\nExiting to main menu...")
            User.menu(self)
        # prompt new user ID
        else:
            print("ID already exists. Pick new ID.")
            User.three_create_user_account(self)

    def create_patient(self):
        """
        Create a new patient. Take in patient ID first and check if it's in the database already.
        If not, prompt data entry for new patient. Pass as a list to System, to write to the patient database file.
        :return:
        """
        print("\nFor new patient, enter:")
        new_id = int(input("\nUnique patient ID, as a number (5 digits): "))
        if System.check_existing_patient(self, new_id) is False:
            first_name = str(input("First name: "))
            last_name = str(input("Last name: "))
            gender = str(input("Gender, M or F: "))
            dob = str(input("Date of Birth, as MM/DD/YYYY:: "))
            patient_new = [new_id, first_name, last_name, gender, dob]
            print(f"\nPatient summary: {patient_new}")
            System.change_data(self, 'patient', patient_new)
            return patient_new
        else:
            print("\n Exiting to Menu. Pick a different patient ID. ")
            User.menu(self)

    def case_new(self, requested_patient):
        """
        Create a new case for given patient (which can have one or more measurements).
        When this is called, the current case number is called from database, and is updated up 1, and is written back to dictionary.
        Note that a case is written to the database, before a measurement is performed.
        After that, do a measurement, given the new case number.
        :param requested_patient:
        :return:
        """
        self.requested_patient = requested_patient
        # Read the current case number update up 1
        new_case = [System.load_data('count') + 1] # developer note: needs to be a list to pass into load/write function in System
        new_case_int = int(new_case[0])
        print(f"\n Case number: {new_case_int}")

        # write new case number to database (system_count.csv)
        System.change_data(self, 'count', new_case)  # update case count to file

        # write new case number to database (data_case.csv)
        case_new = [new_case_int, requested_patient, int(self.userid)]
        print(f"\nCase summary: {case_new}")
        System.change_data(self, 'case', case_new)      # write case list into file

        # initialize measurement based on case number
        User.measure_new(self, new_case_int)
        return case_new

    def measure_new(self, new_case_int):
        """
        Given a case number, perform measurements for a vessel, until the user decides to stop.
         Run FFR test function to get all the data for a measurement, as a list. Measurement list is written to database, with attribution to case number.
        :param new_case_int:
        :return:
        """
        # This is the iteration number, within the case. So first run of case is 1, second run is 2, etc.
        self.iter = 1

        # A while loop and break is used, to perform measurements until the user decides to stop.
        procedure_active = True
        while procedure_active == True:
            # choose the vessel
            vessel_choice = int(input("\nMeasure which vessel? \n (1) LCX, (2) LAD, or (3) RCA. \n\nEnter number for choice: "))
            if vessel_choice == 1:
                vessel = 'LCX'
            elif vessel_choice == 2:
                vessel = 'LAD'
            elif vessel_choice == 3:
                vessel = 'RCA'
            else:
                print('Not a valid vessel choice')

            # run a FFR procedure for the vessel selected, and get results as a list returned by that function
            ffr = ffr = User.ffr_selenium(self)
            measure_new = [ffr[0], vessel, ffr[1], ffr[2], ffr[3], self.iter, new_case_int]
            print(f"\n Measurement summary: {measure_new}")

            # commit the new measurement list to database
            System.change_data(self, 'measurement', measure_new)        # write measurement list into file

            # prompt to choose to measure another vessel, and increase iteration if so. Or else break out of loop.
            choice_4 = int(input("\n (1) Measure another vessel? (2) End procedure?: "))
            self.iter += 1
            if choice_4 == 1:
                procedure_active = True
            elif choice_4 == 2:
                procedure_active = False
                break

    def ffr_selenium(self):
        """
        Performs a FFR measurement. 2 input values are randomly generated, are fed into a website (using Selenium) where they're divided.
        Returned output value is displayed, with messages given based on conditional criteria.
        :return:
        """
        # 1. Randomly generate pressure values in ranges. Source - https://pynative.com/python-get-random-float-numbers/
        pd = round(random.uniform(75,110),1) # look into improving FFR ranges
        pa = round(random.uniform(75,85),1)

        # 2. WEBDRIVER: open Chrome, access through headless
        self.driver = webdriver.Chrome(options=opts)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get('http://saric.us/echonomy/FFR.htm')
        time.sleep(2)

        # 3. Locate Pd, Pa, and send keys for pd and pa. Obtain value. Close Chrome.
        self.driver.find_element(By.XPATH, "//input[@name='txt_MAP']").send_keys(pa) # Enter in Pa into field
        self.driver.find_element(By.XPATH, "//input[@name='txt_MPP']").send_keys(pd) # Enter in Pd into field
        self.driver.find_element(By.XPATH, "//input[@name='b1']").click()  # press "calculate" button
        time.sleep(2)
        ffr = round(float(self.driver.find_element(By.XPATH, "//input[@name='txt_FFR']").get_attribute('value')),1) # access the returned FFR value
        self.driver.quit()

        # 4. Get the current datetime, once the procedure is done. (code from lecture)
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m%d_%H:%M_%S')

        # 5. Conditional messages on value of FFR.
        # source - https://my.clevelandclinic.org/health/diagnostics/23556-fractional-flow-reserve#:~:text=A%20normal%20result%20ranges%20from,a%2025%25%20decrease%20in%20pressure.
        print(f"\n FFR: {ffr}, with Pd {pd} and Pa {pa}, at datetime: {st} \n")
        if ffr >= 0.94:
            print("Normal")
        elif 0.80 <= ffr < 0.94:
            print("Low blood supply/flow. (≥ 0.80) \n Recommended treatment: medicine.")
        elif 0.75 <= ffr < 0.80:
            print("Lower blood supply/flow ('grey zone'). (0.75 to 0.80) \n Recommended treatment: Angioplasty and stent or medicine.")
        else:
            print("Lowest blood supply/flow. (<0.75) \n Angioplasty and stent")

        ffr_measure = [st, pd, pa, ffr]
        return ffr_measure

####
