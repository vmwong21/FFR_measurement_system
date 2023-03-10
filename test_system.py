from src.system import System
import unittest
import time
import pandas as pd

class Test(unittest.TestCase):
    """
    Unit test for System
    """
    def setUp(self):
        self.system = System()
        self.user_changelist = [10006, 'Doctor_FN6', 'Doctor_LN6', 'Vdh36%@#FGd']
        self.patient_changelist = [11116, 'Patient_FN6', 'Patient_LN6', 'M', '09/21/1987']
        self.measurement_changelist = ['2023_0308_16: 55_14', 'LCX', 99, 80, .81, 1, 103]
        self.case_changelist = [103, 11115, 10002]
        self.count_changelist = [101]

        # NEED TO VERIFY THAT THE DATABASE WITH ALL THE ORIGINAL TEST/DEMO DATA.
        # OR BUILD IN A FUNCTION TO WRITE A FILE THAT HAS THE DATA YOU NEED .. BUT WILL NEED TO CHANGE HOW FILE IS CALLED
        # time.sleep(2)
###
# Reset files
###

    def reset_files(self):
        pass
        # __file__path_user = "data_user.csv"
        # __file__path_patient = "data_patient.csv"
        # __file__path_measurement = "data_measurement.csv"
        # __file__path_case = "data_case.csv"
        # __file__path_count = "system_count.csv"
        #
        # # dictionaries to write in
        # default_user =
        # default_patient =
        # default_measurement = {}
        # default_case =
        # default_count = 100
        #
        # dictionary = []
        #
        # # look into merging the paths
        # file_path_user = os.path.join(current_folder, System.__file__path_user)
        # file_path_patient = os.path.join(current_folder, System.__file__path_patient)
        # file_path_measurement = os.path.join(current_folder, System.__file__path_measurement)
        # file_path_case = os.path.join(current_folder, System.__file__path_case)
        # file_path_count = os.path.join(current_folder, System.__file__path_count)
        #
        # paths = [file_path_user, file_path_patient, file_path_measurement, file_path_case, file_path_count]
        # for item in range(len(paths)):
        #     print(paths[item])
        #     file = open(paths[item], "r+")
        #     file.truncate()
        #     #



###
# TEST - Reading functions
###
    def test_load_data_user(self):
        # 1. (User) Test that a user dictionary is loaded.
        # How: For key in user dictionary, verify in value that the unique key 'ID_user' exists.
        output = self.system.load_data('user')
        self.assertIn('ID_user', output[10001])

    def test_load_data_patient(self):
        # 2. (Patient) Test that a patient dictionary is loaded.
        # How: For key in patient dictionary, verify in value that the unique key 'ID_patient' exists.
        output = self.system.load_data('patient')
        # print(output)
        self.assertIn('ID_patient', output[11112])

    def test_load_data_measurement(self):
        # 3. (Measurement) Test that a measurement dictionary is loaded.
        # How: For key in measurement dictionary, verify in value that the unique key 'Datetime' exists.
        output = self.system.load_data('measurement')
        # print(output)
        self.assertIn('Datetime', output['2023_0107_06:55_23'])

    def test_load_data_case(self):
        # 4. (Case) Test that a case dictionary is loaded.
        # How: For key in case dictionary, verify in value that the unique key 'ID_case' exists.
        output = self.system.load_data('case')
        # print(output)
        self.assertIn('ID_case', output[102])

    def test_load_data_count(self):
        # 5. (Count) Test that a count is loaded, by verifying it is greater or equal to 100.
        output = self.system.load_data('count')
        # print(type(output)) - TYPE IS 'INT'
        self.assertGreaterEqual(output, 100)

    def test_load_patients(self):
        # verify that the columns for the load patients query are in the list of returned columns
        output = self.system.load_patients()
        # print(output.columns)
        patients_columns = ['First_name', 'Last_name', 'Gender', 'Date_of_birth']
        for item in patients_columns:
            self.assertIn(item, output.columns)

    def test_load_users(self):
        # verify that the columns for the load users query are in the list of returned columns
        output = self.system.load_users()
        # print(output.columns)
        users_columns = ['First_name_user', 'Last_name_user']
        for item in users_columns:
            self.assertIn(item, output.columns)

    def test_load_all_data(self):
        # verify all columns for the load_all_data query are returned
        output = self.system.load_all_data()
        # print(output.columns)
        all_columns = ['Datetime', 'Vessel', 'Pd', 'Pa', 'FFR', 'Iteration', 'ID_case', 'ID_patient',
                       'ID_user', 'First_name', 'Last_name', 'Gender', 'Date_of_birth', 'First_name_user',
                       'Last_name_user', 'Password']
        for item in all_columns:
            self.assertIn(item, output.columns)

    def test_load_cases_of_user(self):
        # verify for a given user, the results returned are specific just for that user
        output = self.system.load_cases_of_user('10004') # 10004 has multiple rows
        output.reset_index()
        for index, row in output.iterrows():
            self.assertEqual(row['ID_user'],10004)
        # if extra time: verify sort is earliest to latest by date

    def test_load_cases_of_patient(self):
        # verify for a given patient, the results returned are specific just for that patient
        output = self.system.load_cases_of_patient('11113') # 11113 has multiple rows
        output.reset_index()
        for index, row in output.iterrows():
            self.assertEqual(row['ID_patient'], 11113)
        # if extra time: verify sort is earliest to latest by date

###
# Test - Functions that use load_write, to check databases
# Values may be hard coded because the Setup function is too far to
# scroll up to
###
    def test_login_true(self):
        # correct pairing - 10005,'d^dg23g)@'
        output = self.system.login(10005,'d^dg23g)@')
        self.assertEqual(output,True)

    def test_login_false(self):
        # wrong username, correct password
        output = self.system.login(10004,'d^dg23g)@')
        self.assertEqual(output,False)
        # correct username, wrong password
        output = self.system.login(10005,'WRONGd^dg23g)@')
        self.assertEqual(output,False)
        # wrong username, wrong password
        output = self.system.login(10004,'WRONGd^dg23g)@')

    def test_check_existing_user_true(self):
        output = self.system.check_existing_user(10005)
        self.assertEqual(output, True)

    def test_check_existing_user_false(self):
        output = self.system.check_existing_user(12345)
        self.assertEqual(output, False)

    def test_check_existing_patient_true(self):
        output = self.system.check_existing_patient(11115)
        self.assertEqual(output, True)

    def test_check_existing_patient_false(self):
        output = self.system.check_existing_patient(12345)
        self.assertEqual(output, False)
###
# TEST - Writing functions
###
    def test_change_data_user(self):
        # 1. (User) Test that the dictionary is updated. Verify unique key is in dictionary made by function.
        output = self.system.change_data('user',self.user_changelist)
        self.assertIn('ID_user', output[10006])

    def test_change_data_patient(self):
        # 2. (Patient) Test that the dictionary is updated. Verify unique key is in dictionary made by function.
        output = self.system.change_data('patient', self.patient_changelist)
        self.assertIn('ID_patient', output[11116])

    def test_change_data_measurement(self):
        # 4. (Measurement) Test that the dictionary is updated. Verify unique key is in dictionary made by function.
        output = self.system.change_data('measurement', self.measurement_changelist)
        self.assertIn('Datetime', output['2023_0308_16: 55_14'])

    def test_change_data_case(self):
        # 5. (Case) Test that the dictionary is updated. Verify unique key is in dictionary made by function.
        output = self.system.change_data('case', self.case_changelist)
        self.assertIn('ID_case', output[103])

    def test_change_data_count(self):
        # 5. (Case) Test that the dictionary is updated. Verify unique key is in dictionary made by function.
        output = self.system.change_data('count', self.count_changelist)
        self.assertEqual(101, output)

    def test_commit_write_user(self):
        self.system.change_data('user',self.user_changelist)
        output = self.system.load_data('user')
        self.assertIn('ID_user', output[10006])

    # duplicate unit test above Thursday morning

    def test_commit_write_patient(self):
        self.system.change_data('patient', self.patient_changelist)
        output = self.system.load_data('patient')
        self.assertIn('ID_patient', output[11116])

    def test_commit_write_measurement(self):
        self.system.change_data('measurement', self.measurement_changelist)
        output = self.system.load_data('measurement')
        self.assertIn('Datetime', output['2023_0308_16: 55_14'])

    # ASSUMPTION for code: patient/doctor pairing for a case is the SAME
    def test_commit_write_case(self):
        self.system.change_data('case', self.case_changelist)
        output = self.system.load_data('case')
        self.assertIn('ID_case', output[103])

    def test_commit_write_count(self):
        self.system.change_data('count', self.count_changelist)
        output = self.system.load_data('count')
        self.assertGreaterEqual(output, 101)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
