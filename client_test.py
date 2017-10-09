'''
Test Cases for Unit Testing client.py

'''

import mock
import unittest
import client


def mocked_call(*args, **kwargs):
    '''
    Mock Function which is used to
    mock responses when a particular
    URL is called.

    '''

    if args[0] == "http://127.0.0.1:5000/register":
        return {"register_method": 200}

    elif args[0] == "http://127.0.0.1:5000/update":
        return {"update_method": 200}

    elif args[0] == "http://127.0.0.1:5000/users":
        return {"get_users_method": 200}

    elif args[0] == "http://127.0.0.1:5000/getuser/1":
        return {"check_user_method": 200}

    elif args[0] == "http://127.0.0.1:5000/delete":
        return {"delete_method": 200}

    else:
        return {"method": "Invalid"}


class TestClient(unittest.TestCase):

    @mock.patch("requests.post", side_effect=mocked_call)
    def test_register_user(self, m):
        '''
        Mocking the call to REST API by Replacing
        requests.post with mocked_call response

        '''

        json_data = client.register_user()
        self.assertEqual(json_data, {"register_method": 200})

    @mock.patch("requests.put", side_effect=mocked_call)
    def test_update_user(self, m, uid=1):
        '''
        Mocking the call to REST API by Replacing
        requests.put with mocked_call response

        '''

        json_data = client.update_user(uid)
        self.assertEqual(json_data, {"update_method": 200})

    @mock.patch("requests.get", side_effect=mocked_call)
    def test_get_users(self, m):
        '''
        Mocking the call to REST API by Replacing
        requests.get with mocked_call response

        '''
        json_data = client.get_users()
        self.assertEqual(json_data, {"get_users_method": 200})

    @mock.patch("requests.get", side_effect=mocked_call)
    def test_check_user(self, m, uid=1):
        '''
        Mocking the call to REST API by Replacing
        requests.get with mocked_call response

        '''
        json_data = client.check_user(uid)
        self.assertEqual(json_data, {"check_user_method": 200})

    @mock.patch("requests.delete", side_effect=mocked_call)
    def test_delete_user(self, m, uid=1):
        '''
        Mocking the call to REST API by Replacing
        requests.delete with mocked_call response

        '''
        json_data = client.delete_user(uid)
        self.assertEqual(json_data, {"delete_method": 200})

if __name__ == '__main__':
    '''
    Executing the Test cases.

    '''

    unittest.main()

