'''
Imlementation of Flask Client
which makes the request to Server
for adding or manipulating user
data in the Database

'''

import numbers
import requests
import json


def register_user():
    '''
    Registers a new User in the Database

    '''

    print "\n---User Registration---\n"
    fname = raw_input("Enter First Name:")
    lname = raw_input("Enter Last Name:")
    uname = raw_input("Enter UserName:")
    pword = raw_input("Enter Password:")
    email = raw_input("Enter Email:")
    phone = raw_input("Enter Phone no:")

    user_data = {"fname": fname, "lname": lname, "uname": uname,
                 "pword": pword, "email": email, "phone": phone}
    headers = {"Content-Type": "application/json"}
    register_response = requests.post("http://127.0.0.1:5000/register",
                                      data=json.dumps(user_data),
                                      headers=headers)
    return register_response


def get_users():
    '''
    Gets all the user records stored in the User Database

    '''

    get_user_response = requests.get("http://127.0.0.1:5000/users")
    return get_user_response


def check_user(id):
    '''
    Checks whether a user exists in the Database or Not
    based on the provided user id.

    '''

    headers = {"Content-Type": "application/json"}
    user_response = requests.get("http://127.0.0.1:5000/getuser/{0}"
                                 .format(id),
                                 headers=headers)
    return user_response


def update_user(id):
    '''
    Updates the details of the user which corresponds to provided user id

    '''

    print("\n---Enter Updated Info of the User---\n".format(id))
    print "UserId: {0}".format(id)
    fname = raw_input("Enter FirstName: ")
    lname = raw_input("Enter LastName: ")
    uname = raw_input("Enter UserName: ")
    pword = raw_input("Enter Password: ")
    email = raw_input("Enter Email id: ")
    phone = raw_input("Enter Phone no: ")

    user_data = {"id": id, "fname": fname, "lname": lname,
                 "uname": uname, "pword": pword, "email": email,
                 "phone": phone}

    headers = {"Content-Type": "application/json"}
    update_response = requests.put("http://127.0.0.1:5000/update",
                                   data=json.dumps(user_data),
                                   headers=headers)
    return update_response


def delete_user(id):
    '''
    Deletes the user records from the database, which correspond
    to the user with the given User Id.
    '''

    user_data = {"id": id}
    headers = {"Content-Type": "application/json"}
    delete_response = requests.delete("http://127.0.0.1:5000/delete",
                                      data=json.dumps(user_data),
                                      headers=headers)
    return delete_response


if __name__ == '__main__':

    while True:
        '''
        Display options to user to choose from.

        '''

        print "\n***User Registration Portal***"
        print "----MENU----"
        print "--> 1.Register a User"
        print "--> 2.View All Users"
        print "--> 3.Update a User"
        print "--> 4.Delete a User"
        print "--> 5.Exit\n"

        choice = raw_input("Enter your choice: ")

        try:
            choice = int(choice)
        except ValueError:
            print "\nInvalid Value Entered!"
            choice = 6

        if choice == 1:
            response = register_user()
            status = response.json()
            print status["Response"]

        elif choice == 2:
            user_entries = get_users().text
            print user_entries

        elif choice == 3:

            id = raw_input("\nEnter User-Id to Update User:")
            emptyList = []
            user = []

            '''
            Perform Update only if a user
            of given User Id Exists in the
            Database

            '''

            try:
                id = int(id)
                user_data = check_user(id).text
                user = json.loads(user_data)
            except:
                print "\nInvalid User Id!"

            # If user exists only then perform the rest
            if user != emptyList:
                response = update_user(id)
                status = response.json()
                print status["Response"]
            else:
                print "Update Operation Failed! User not found"

        elif choice == 4:
            id = raw_input("\nEnter User-Id to Delete User:")
            emptyList = []
            user = []

            '''
            Perform Delete only if a user
            of given User Id Exists in the
            Database

            '''

            try:
                id = int(id)
                user_data = check_user(id).text
                user = json.loads(user_data)
            except:
                print "\nInvalid User Id!"

            # If user exists only then perform the rest
            if user != emptyList:
                response = delete_user(id)
                status = response.json()
                print status["Response"]
            else:
                print "Delete Operation Failed! User not found"

        elif choice == 5:
            print "Exiting Portal... Bye.\n"
            break

        else:
            print "Please Enter a Valid Choice!"

