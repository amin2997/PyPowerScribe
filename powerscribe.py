import requests
import re


class Powerscribe():

    def __init__(self, url):
        self.client = requests.session()
        self.url = url.rstrip('/')
        self.username = ""
        self.password = ""

    def sign_in(self, username, password):
        """signin to Powerscribe 360        
        Arguments:
            username {string} -- PowerScribe 360 service username
            password {string} -- PowerScribe 360 service password
        """
        if StringHelper.is_null_or_whitespace(self.url) or StringHelper.is_null_or_whitespace(username) or StringHelper.is_null_or_whitespace(password):
            return False
        self.username = username
        self.password = password
        uri = "/services/auth.asmx/SignIn"
        payload = f"systemID=0&accessCode=&username={self.username}&password={self.password}"
        success, _ = self.web_request(uri, payload)
        return success

    def sign_out(self):
        """signout of PowerScribe dispose of connection
        """
        uri = "/services/auth.asmx/SignOut"
        success, _ = self.web_request(uri, "")

        self.client.close()
        return success

    def web_request(self, uri, data):
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = self.client.request(
            "POST", self.url + uri, data=data.encode('ascii'), headers=headers)
        success = 200 <= response.status_code <= 299

        if not success:
            print(response.text)

        return success, response.text

    def set_custom_field(self, accession, field_name, field_value):
        """set_custom_field allow you sent field to powerscribe 360

        Arguments:
            accession {string} -- accession number in powerscribe
            field_name {string} -- custom field name in powerscribe
            field_value {string} -- custom field value that will be sent into powerscribe
        """
        if StringHelper.is_null_or_whitespace(accession) or StringHelper.is_null_or_whitespace(field_name):
            return False

        uri = "/services/customfield.asmx/SetOrderCustomFieldByName"
        has_order_id, order_id = self.try_get_order(accession)
        if not has_order_id:
            return False

        payload = f"orderID={order_id}&name={field_name}&value={field_value}"
        success, _ = self.web_request(uri, payload)
        return success

    def try_get_order(self, accession):
        uri = "/services/explorer.asmx/SearchByAccession"
        payload = f"site=&accessions={accession}&sort="
        success, response_text = self.web_request(uri, payload)
        if success:
            order_id_search = re.search(
                '<OrderID>(\d+)</OrderID>', response_text, re.IGNORECASE | re.MULTILINE)
            return success, order_id_search.group(1)
        else:
            return success, None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sign_out()


class StringHelper():
    @staticmethod
    def is_null_or_whitespace(str):
        """Indicates whether the specified string is null or empty string.
        Returns: True if the str parameter is null, an empty string ("") or contains 
        whitespace. Returns false otherwise."""
        if (str is None) or (str == "") or (str.isspace()):
            return True
        return False


if __name__ == '__main__':
    url = 'http://ps360ServerNameServerName/RadPortal'
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
