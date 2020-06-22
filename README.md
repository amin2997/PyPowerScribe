# PyPowerscribe360

This is a REST API implementation for Radiology Nuance PowerScribe 360 dictation system. This API will allow you to send and retrieve data points into pre-built custom fields that populates radiologist final report. For example, you can push radiation dose information into custom field that will populate the radiologist final report.

## Sample Implementation

The following will allow you to connect to PowerScribe 360 server and send custom field to the radiologist report.

```python
from powerscribe.Powerscribe import Powerscribe

if __name__ == '__main__':
    url = 'http://ps360ServerName/RadPortal'
    username = "PowerScribe USERNAME"
    password = "PowerScribe Password"

    accession = "12345"
    field_name = "CTRAD"
    field_value = "29997"

    with Powerscribe(url) as ps:
        if ps.sign_in(username, password):
            print("Signin successfully")
            if ps.set_custom_field(accession, field_name, field_value):
                print(f"Sent field name {field_name} and value {field_value} into accession {accession}")
            else:
                print(f"Error sending field name {field_name} and value {field_value} into accession {accession}")
        else:
            print("Signin failed")
```
