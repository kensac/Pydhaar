
# Pydhaar

A Library that allows the user to read data from the new Secure QR Code implmented
on the Aadhaar card by the UIDAI. The library has features to deocde the information and provide
demographic data. There are also features to verify user data by taking in the e-mail/mobile number
and hashing to verify the data. Based on authentication documentaion from [https://uidai.gov.in/images/resource/User_manulal_QR_Code_15032019.pdf]()

Also includes API that allows the user to fetch data from preexisting qrcode information allowing user to primarily verify validity of the information provided by hash comparision.



## Installation and Usage


```py
from pydhaar import AadharCard

instance = AadharCard({data from QR Code})
print(instance)
```
To use API Locally, run server using 
```bash
uvicorn API:app --reload
```
Then access documentation at [http://127.0.0.1:8000/docs#/]() or [http://127.0.0.1:8000/redoc]()

The API has only get requests as storage of data to a server is restricted to essential information only based on authentication documntation by UIDAI
