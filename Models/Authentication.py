# from Utilities import Constants
import getpass

# from Models.CreateDatabase import CreateDatabase
# from Utilities import Logger

# from Query_Execution_Engine import Main
#
# logger = Logger.getLogger()

# User Authentication
print('Username:')
userName = input()
# print('Password:')
# password = input()
password = getpass.getpass()
if userName == 'root' and password == 'root':
    print('Login Successful!')
    # logger.info('Login Successful')

    # Updating user info on successful login
    # Constants.CURRENT_USER = userName

    print('Present User: ' + userName)
    # logger.info('Present User: ' + userName)
elif userName == 'admin' and password == 'admin':
    print('Login Successful!')
    # logger.info('Login Successful')

    # Updating user info on successful login
    # Constants.CURRENT_USER = userName

    print('Present User: ' + userName)
    # logger.info('Present User: ' + userName)
else:
    print('Username or Password is incorrect ')
    # logger.error('Username or Password is incorrect ')

    print('Login Failed!')
    # logger.error('Username or Password is incorrect ')
