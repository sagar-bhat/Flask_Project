'''
Test cases for Testing server.py

'''

import os
import unittest
import tempfile
import json
import server


class TestServer(unittest.TestCase):

    '''
    Test Class which has test functions
    for the server.
    Database is Mocked by creating a
    temporary file.

    '''

    def setUp(self):
        '''
        This sets up temporary Database
        everytime a test function is
        called.

        '''

        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.testing = True
        self.app = server.app.test_client()

        with server.app.app_context():
            server.init_db()

    def tearDown(self):
        '''
        Closes the mocked Database after
        calling each Test Function
        '''

        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def test_register_user(self):
        '''
        Tests whether the server function for registering
        a user in Database is called properly or not.

        '''

        user_data = {"fname": "Sagar", "lname": "Bhat", "uname": "sagar123",
                     "pword": "sgr123", "email": "sagar@gmail.com",
                     "phone": " 7776018567"}
        headers = {"Content-Type": "application/json"}
        response = self.app.post('/register', data=json.dumps(user_data),
                                 headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self, uid=1):
        '''
        Tests whether the server function for updating
        the user details in Database is called properly or not.

        '''

        user_data = {"id": uid, "fname": "Sagar", "lname": "Bhat",
                     "uname": "sgr321", "pword": "falcon",
                     "email": "s@gmail.com", "phone": "7776018567"}
        headers = {"Content-Type": "application/json"}
        response = self.app.put('/update', data=json.dumps(user_data),
                                headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        '''
        Tests whether the server function for retrieving
        all the users from Database is called properly or not.

        '''

        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self, uid=1):
        '''
        Tests whether the server function for Deleting the
        user in Database is called properly or not.

        '''
        user_data = {"id": uid}
        headers = {"Content-Type": "application/json"}
        response = self.app.delete('/delete', data=json.dumps(user_data),
                                   headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_check_user(self, uid=1):
        '''
        Tests whether the server function for Checking the
        User in the Database, is called properly or not.

        '''
        user_data = {"id": uid}
        headers = {"Content-Type": "application/json"}
        response = self.app.get('/getuser/1', data=json.dumps(user_data),
                                headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':

    '''
    Execute the Test Cases

    '''

    unittest.main()

