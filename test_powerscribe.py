from powerscribe import Powerscribe
import unittest


class TestPowerscribe(unittest.TestCase):

    def test_sign_in_with_invalid_account(self):

        url = 'http://ps360ServerName/RadPortal'
        username = "invalid"
        password = "invalid"

        with Powerscribe(url) as ps:
            result = ps.sign_in(username, password)
            self.assertEqual(result, False)

    def test_sign_in_with_valid_account(self):
        url = 'http://ps360ServerName/RadPortal'
        username = "*** YOUR USERNAME***"
        password = "*** YOUR PASSWORD ***"

        with Powerscribe(url) as ps:
            result = ps.sign_in(username, password)
            self.assertEqual(result, True)

    def test_set_custom_field_with_valid_field(self):
        url = 'http://ps360ServerName/RadPortal'
        username = "*** YOUR USERNAME***"
        password = "*** YOUR PASSWORD ***"

        accession = "8656512"
        field_name = "CTRAD"
        field_value = "29997"
        result = False
        with Powerscribe(url) as ps:
            if ps.sign_in(username, password):
                result = ps.set_custom_field(
                    accession, field_name, field_value)

        self.assertEqual(result, True)

    def test_set_custom_field_with_invalid_field(self):
        url = 'http://ps360ServerName/RadPortal'
        username = "*** YOUR USERNAME***"
        password = "*** YOUR PASSWORD ***"

        accession = "8656512"
        field_name = "invalid_field"
        field_value = "29997"
        result = False
        with Powerscribe(url) as ps:
            if ps.sign_in(username, password):
                result = ps.set_custom_field(
                    accession, field_name, field_value)

        self.assertEqual(result, False)


"""
#Example
if __name__ == '__main__':
    url = 'http://ps360ServerName/RadPortal'
    username = "*** YOUR USERNAME***"
    password = "*** YOUR PASSWORD ***"

    accession = "8656512"
    field_name = "CTRAD"
    field_value = "29997"

    with Powerscribe(url) as ps:
        if ps.sign_in(username, password):
            print("Signin successfully")
            if ps.set_custom_field(accession, field_name, field_value):
                print(
                    f"Sent field name {field_name} and value {field_value} into accession {accession}")
            else:
                print(
                    f"Error sending field name {field_name} and value {field_value} into accession {accession}")
        else:
            print("Signin failed")
"""
