from pydantic import BaseModel, EmailStr

class AadharOut(BaseModel):
    version: str
    email_mobile_status: str
    referenceid: str
    name: str
    date_of_birth: str
    gender: str
    care_of: str
    district: str
    landmark: str
    house:str
    location: str
    pincode: str
    post_office: str
    state: str
    street: str
    subdistrict: str
    vtc: str

class isEmailOut(BaseModel):
    isEmail: bool

class isMobileOut(BaseModel):
    isMobile: bool

class getEmailHashOut(BaseModel):
    emailHash: str

class getMobileHashOut(BaseModel):
    mobileHash: str