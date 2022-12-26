import zlib
import json
from hashlib import sha256
from itertools import count




class AadharCard:

    def __init__(self, base10data) -> None:
        self.base10data = base10data
        self.delimeterIndex = [-1]
        self.data = {}

        if isinstance(self.base10data,str):
            self.base10data=int(self.base10data)
        
        self._base10_to_bytesArray()
        self._bytesArray_to_decompressed()
        self._get_delimiter_index()

        self.fields = ["version","email_mobile_status","referenceid", "name", "date_of_birth", "gender", "care_of", "district", "landmark", "house", "location", "pincode", "post_office", "state", "street", "subdistrict", "vtc"]

        self._populate_data()
        self.email=False
        self.mobile=False

        self._verify_email_mobile_status()
        self._get_version()

    def __str__(self) -> json:
        return json.dumps(self.data)

    def __repr__(self) -> str:
        return "Aadhar Card"

    def _base10_to_bytesArray(self) -> None:
        self.bytesArray=self.base10data.to_bytes(5000, "big").lstrip(b'\x00')
    
    def _bytesArray_to_decompressed(self) -> None:
        self.decompressedBytesArray=zlib.decompress(self.bytesArray,32+zlib.MAX_WBITS)

    def _get_delimiter_index(self) -> None:
        for i in range(len(self.decompressedBytesArray)):
            if self.decompressedBytesArray[i]==255:
                self.delimeterIndex.append(i)

    def _populate_data(self) -> None:
        for i in range(len(self.fields)):
            self.data[self.fields[i]]=self.decompressedBytesArray[self.delimeterIndex[i]+1:self.delimeterIndex[i+1]].decode("ISO-8859-1")
    
    def _verify_email_mobile_status(self) -> None:
        if self.data['email_mobile_status'] == "3":
            self.email=True
            self.mobile=True
        elif self.data['email_mobile_status'] == "2":
            self.mobile=True
        elif self.data['email_mobile_status'] == "1":
            self.email=True
    
    def _get_version(self) -> None:
        self.version=self.decompressedBytesArray[0:2].decode("ISO-8859-1")
    #Return Functions

    def getAadharData(self) -> dict:
        return self.data

    def getAadharLastFourDigits(self) -> str:
        lastFourDigits=str(self.data["referenceid"][0:4])
        return f"{lastFourDigits}"

    def getDateOfBirth(self) -> str:
        return self.data["date_of_birth"]
    
    def getName(self) -> str:
        return self.data["name"]
    
    def getEmailHash(self) ->str:
        if not self.email:
            return None
        hash=""
        if self.email and self.mobile:
            hash=self.decompressedBytesArray[len(self.decompressedBytesArray)-1-256-(32*2):len(self.decompressedBytesArray)-1-256-32][::-1].hex()
        elif self.email:
            hash=self.decompressedBytesArray[len(self.decompressedBytesArray)-256-(32):len(self.decompressedBytesArray)-256].hex()
        return hash

    def getMobileHash(self) ->str:
        if not self.mobile:
            return None
        hash=""
        if self.mobile:
            hash=self.decompressedBytesArray[len(self.decompressedBytesArray)-1-256-(32):len(self.decompressedBytesArray)-1-256][::-1].hex()
        return hash
    
    def shaEncoder(self,chars) -> int:
        chars=chars
        lastFourDigits=self.getAadharLastFourDigits()
        lastDigit=int(lastFourDigits[3])

        if lastDigit==0 or lastDigit==1:
            chars=sha256(chars.encode()).hexdigest()
        else:
            for i in range(lastDigit):
                chars=sha256(chars.encode()).hexdigest()
        print(chars)
        return chars

    def verifyEmail(self,chars) -> bool:
        if self.getEmailHash() == self.shaEncoder(chars):
            return True
        else:
            return False

    def verifyMobile(self,chars) -> bool:
        if self.getMobileHash() == self.shaEncoder(chars):
            return True
        else:
            return False
    
    def isMobile(self) -> bool:
        return self.mobile
    
    def isEmail(self) -> bool:
        return self.email

    def getVersion(self) -> str:
        return self.version