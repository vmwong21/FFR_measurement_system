import os
import pandas as pd

class System:
    # File names initialized here (class variables), to be called by variable constructing file path.
    __file__path_user = "data_user.csv"
    __file__path_patient = "data_patient.csv"
    __file__path_measurement = "data_measurement.csv"
    __file__path_case = "data_case.csv"
    __file__path_count = "system_count.csv"
    # Initialize empty dictionary attributes.
    __credentials = {}
    __patient = {}
    __measurement = {}
    __case = {}
    __count = {}

    def __init__(self): # no instance attributes declared
        pass

#####################################################################################
# A. Reading functions
#####################################################################################
    @classmethod
    def load_data(self, choice): # choice - user, patient, measurement, case, count
        """
        Read data: Reads / loads CSV file.
        Conditional read for data type: users, patients, measurements, cases, count.
        Initialized by other functions. File is opened again with commit_write
        :return: 'output', which is a dictionary read by other higher level functions
        """
        # 1. Get current directory, and identify the correct file of choice
        try:
            current_folder = os.path.dirname(os.path.abspath(__file__))
            if choice == "user":
                file_path = os.path.join(current_folder, System.__file__path_user)
            elif choice == "patient":
                file_path = os.path.join(current_folder, System.__file__path_patient)
            elif choice == "measurement":
                file_path = os.path.join(current_folder, System.__file__path_measurement)
            elif choice == "case":
                file_path = os.path.join(current_folder, System.__file__path_case)
            elif choice == "count":
                file_path = os.path.join(current_folder, System.__file__path_count)
            else:
                print("not a valid choice for file loading - 1")

            # 2. Build file path based on file that the function is called for
            file = open(file_path, "r+")

            # 3. Depending on choice of data type, read lines of file. Construct dictionary, assign keys.
            if choice == "user":
                for line in file:  # read line by line of the file
                    column = line.split(";")   # split based on ';' in the file
                    System.__credentials[int(column[0])] = {   # assign key and value pairings
                        'ID_user' : int(column[0]),
                        'First_name_user': str(column[1]),
                        'Last_name_user': str(column[2]),
                        'Password': str(column[3]),
                    }
                output = System.__credentials    # assign as output to be returned by the function
                return output
            elif choice == "patient":
                for line in file:
                    column = line.split(";")
                    System.__patient[int(column[0])] = {
                        'ID_patient': int(column[0]),
                        'First_name': str(column[1]),
                        'Last_name': str(column[2]),
                        'Gender': str(column[3]),
                        'Date_of_birth': str(column[4]).replace('\n',''),
                    }
                output = System.__patient
                return output
            elif choice == "measurement":
                for line in file:
                    column = line.split(";")
                    System.__measurement[str(column[0])] = {
                        'Datetime': str(column[0]),
                        'Vessel': str(column[1]),
                        'Pd': float(column[2]),
                        'Pa': float(column[3]),
                        'FFR': float(column[4]),
                        'Iteration': int(column[5]),
                        'ID_case': int(column[6]),
                    }
                output = System.__measurement
                return output
            elif choice == "case":
                for line in file:
                    column = line.split(";")
                    System.__case[int(column[0])] = {
                        'ID_case': int(column[0]),
                        'ID_patient': int(column[1]),
                        'ID_user': int(column[2]),
                    }
                output = System.__case
                return output
            elif choice == "count":   # this is a system counter for the case number. so each case number is unique and goes up by 1.
                for line in file:
                    column = line.split(";")
                    System.__count = int(column[0])
                output = System.__count
                return output
            else:
                print("not a valid choice for file loading - 2")
            file.close()
        except FileNotFoundError as e:
            return e

    def load_patients(self):
        """
        Return list of patients.
        First column is ID, but isn't listed as the column.
        :return: patient_list, with format: First_name, Last_name, Gender, Date_of_birth
        """
        System.load_data('patient')             # load patient dictionary
        patient_df = pd.DataFrame(System.__patient).T     # apply transpose
        patient_list = patient_df.loc[:,['First_name', 'Last_name', 'Gender', 'Date_of_birth']]   # locate columns in full dataset
        return patient_list     # return dataframe, to be read by higher level function

    def load_users(self):
        """
        Return list of users/doctors.
        First column is ID, but isn't listed as the column.
        :return: user_list, with format: First_name_user Last_name_user
        """
        System.load_data('user')   # see above comments. similar structure.
        user_df = pd.DataFrame(System.__credentials).T
        user_list = user_df.loc[:,['First_name_user', 'Last_name_user']]
        return user_list

    def load_all_data(self):
        """
        Load all data, among all dictionaries.
        :return: combined_dataset - dataframe for all databases/dictionaries. Gets searched, by other functions.
        """
        # 1. create dictionaries in buffer, for all the data files
        System.load_data('user')
        System.load_data('patient')
        System.load_data('measurement')
        System.load_data('case')

        # 2. create individual dataframes for the 4 dictionaries, apply transpose
        user_df = pd.DataFrame(System.__credentials).T
        patient_df = pd.DataFrame(System.__patient).T
        measurement_df = pd.DataFrame(System.__measurement).T
        case_df = pd.DataFrame(System.__case).T

        # 3. merge the 4 dataframes togetherm, using joins
        combo1 = pd.merge(measurement_df, case_df, how='left', on='ID_case')
        combo2 = pd.merge(combo1, patient_df, how='left', on='ID_patient')
        combined_dataset = pd.merge(combo2, user_df, how='left', on='ID_user')  # final combo

        return combined_dataset

    def load_cases_of_user(self, user):
        combined_dataset = System.load_all_data(self)
        doctor_query = combined_dataset.loc[combined_dataset['ID_user'] == int(user), ['Datetime', 'ID_patient', 'Vessel', 'Pd', 'Pa', 'FFR', 'Iteration', 'ID_user']].sort_values(by="Datetime", ascending=True)
        return doctor_query

    def load_cases_of_patient(self, patient):
        combined_dataset = System.load_all_data(self)
        patient_query = combined_dataset.loc[combined_dataset['ID_patient'] == int(patient), ['Datetime', 'ID_patient', 'Vessel', 'Pd', 'Pa', 'FFR', 'Iteration', 'ID_user']].sort_values(by="Datetime", ascending=True)
        return patient_query

#####################################################################################
# B. Functions that use load_write, to check databases
#####################################################################################

    def login(self, requested_user, check_password):
        """
        Given user and password, check if they're paired in the user dictionary.
        :param requested_user:
        :param check_password:
        :return: True if user/password match in database
        """
        load = System.load_data('user')
        if load[int(requested_user)]['Password'] == check_password:
            return True
        else:
            return False

    def check_existing_user(self, requested_user):
        """
        Check if requested user exists in user dictionary.
        :param requested_user:
        :return: True if requested user is in database
        """
        load = System.load_data('user')
        if requested_user in load:
            return True
        else:
            return False

    def check_existing_patient(self, requested_patient):
        """
        Check if requested patient ID exists in user dictionary.
        :param requested_patient:
        :return: True if requested patient is in database
        """
        load = System.load_data('patient')
        if requested_patient in load:
            return True
        else:
            return False

###
# Writing functions
###

    def change_data(self, choice, changelist):
        """
        Given data type (user, patient, measurement, case, count), and a list of the data,
         convert the values of that list into a dictionary. In preparation to be committed to the file, in commit_write.
        :param choice: choice of database - user, patient, measurement, case, count
        :param changelists: a list of data to be converted into a dictionary.
        :return: output - this is the dictionary
        """
        # 1. Load the database of choice, into buffer.
        System.load_data(choice)  # Needs to be here, to ensure loading of existing data from file

        # 2. Based on choice, assign dictionary entry. Call on commit_write function, to write dictionary entry to file.
        if choice == "user":
            System.__credentials[int(changelist[0])] = {
                        'ID_user' : int(changelist[0]),
                        'First_name_user': str(changelist[1]),
                        'Last_name_user': str(changelist[2]),
                        'Password': str(changelist[3]),
                    }
            output = System.__credentials
            System.commit_write(choice)
            return output
        elif choice == "patient":
            System.__patient[int(changelist[0])] = {
                'ID_patient': int(changelist[0]),
                'First_name': str(changelist[1]),
                'Last_name': str(changelist[2]),
                'Gender': str(changelist[3]),
                'Date_of_birth': str(changelist[4]),
            }
            output = System.__patient
            System.commit_write(choice)
            return output
        elif choice == "measurement": # each time a measurement is done, run this
            System.__measurement[str(changelist[0])] = {
                'Datetime': str(changelist[0]),
                'Vessel': str(changelist[1]),
                'Pd': float(changelist[2]),
                'Pa': float(changelist[3]),
                'FFR': float(changelist[4]),
                'Iteration': int(changelist[5]),
                'ID_case': int(changelist[6]),
            }
            output = System.__measurement
            System.commit_write(choice)
            return output
        elif choice == "case":
            System.__case[int(changelist[0])] = {
                'ID_case': int(changelist[0]),
                'ID_patient': int(changelist[1]),
                'ID_user': int(changelist[2]),
            }
            output = System.__case
            System.commit_write(choice)
            return output
        elif choice == "count":
            System.__count = int(changelist[0])
            output = System.__count
            System.commit_write(choice)
            return output
        else:
            print("not a valid choice for file loading - 1")

    @classmethod
    def commit_write(self, choice):
        """
        Given data type (user, patient, measurement, case, count), write a dictionary line from 'change_data' function
        to the file.
        :param choice:
        :return:
        """
        # Developer note - Make sure to not have 'read data' called here, or it can overwrite new changes to __data

        # 1. Set the file path, to the file that aligns with the choice (ex. user, patient)
        try:
            current_folder = os.path.dirname(os.path.abspath(__file__))     # get current directory
            if choice == "user":
                file_path = os.path.join(current_folder, System.__file__path_user)
            elif choice == "patient":
                file_path = os.path.join(current_folder, System.__file__path_patient)
            elif choice == "measurement":
                file_path = os.path.join(current_folder, System.__file__path_measurement)
            elif choice == "case":
                file_path = os.path.join(current_folder, System.__file__path_case)
            elif choice == "count":
                file_path = os.path.join(current_folder, System.__file__path_count)
            else:
                print("not a valid choice for file loading - 1")
            file = open(file_path, "r+")

            # 2. Erase contents of the file, so that the buffer can be written on.
            # Developer note: be careful with this function.
            file.truncate(0)


            # 3. based on data type, read the edited buffer and translate it into a format for the CSV file.
            # each dictionary line converted is 'vector2' which is written to the file
            if choice == "user":
                for k, v in System.__credentials.items():
                    vector = []
                    vector2 = []
                    for i, j in v.items():
                        vector.append(f"{j};")
                        vector2 = ''.join(vector)
                    file.write(f"{vector2}\n")
            elif choice == "patient":
                for k, v in System.__patient.items():
                    vector = []
                    vector2 = []
                    for i, j in v.items():
                        vector.append(f"{j};")
                        vector2 = ''.join(vector)
                    file.write(f"{vector2}\n")
            elif choice == "measurement":
                for k, v in System.__measurement.items():
                    vector = []
                    vector2 = []
                    for i, j in v.items():
                        vector.append(f"{j};")
                        vector2 = ''.join(vector)
                    file.write(f"{vector2}\n")
            elif choice == "case":
                for k, v in System.__case.items():
                    vector = []
                    vector2 = []
                    for i, j in v.items():
                        vector.append(f"{j};")
                        vector2 = ''.join(vector)
                    file.write(f"{vector2}\n")
            elif choice == "count":
                file.write(f"{System.__count}\n")
            else:
                print("not a valid choice for file loading - 1")
            file.close()
        except FileNotFoundError as e:
            return e

#####################################################################################
# Runner code
#####################################################################################
system = System()

# system.commit_write('user')
# system.load_data('user')

# user_changelist = [10006, 'Doctor_FN6', 'Doctor_LN6', 'Vdh36%@#FGd']
# output = system.change_data('user', user_changelist)
# print(output)

# System().login()
# print(system.load_patients())

# print(system.load_cases_of_patient(10001))