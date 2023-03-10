from src.error import UserNotFoundError
from src.system import System
from src.user import User

class Main(System):
    def main(self):
        """
        Program starts here. This is the prelogin page.
        Right click and run, in the 'runner code' below, or hit green arrow in Pycharm.
        :return: Return error or logged_in.
        """
        try:
            # Welcome line. Prompt for username and password.
            userid = int(input("FFR Measurement System. \n Student project only. Not for clinical use. \n Please log in: \n User ID: "))
            password = input("Password: ")
            if System.login(self, userid, password): # Calls on a function in System to verify access. If function return is True, go forward.
                print('Access granted...')
                User(userid).menu()
                logged_in = True # Return is defined here, for unit testing.
                return logged_in
            else:  # When System's return is False, this is prompted.
                print("Incorrect credentials. \n Exiting program. \n")
                logged_in = False
                return logged_in
        except KeyError: # Prompted, if user ID is not in database.
            print("User does not exist. \n Exiting program. \n")
        except ValueError:
            print("User ID can only be a number. \n Exiting program. \n")
            # Developer note: if there are extra things in the files "ex. ;;;", a value error can be returned.
        except UserNotFoundError as e:
            print(e)

####################
# Runner code

going = Main()
going.main()