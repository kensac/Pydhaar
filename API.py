from fastapi import FastAPI, HTTPException
from main import AadharCard
import json
from apiClass import *

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Base"}

@app.get("/data/{chars}",response_model=AadharOut)
async def root(chars:int):
    try:
        temp=AadharCard(chars)
        if temp.version != "V2":
            raise HTTPException(status_code=401, detail="Value does not belong to a SequreQR code ID")
        return temp.data
    except:
        raise HTTPException(status_code=501, detail="Unable to Process Input")

@app.get("/data/{chars}/isEmail",response_model=isEmailOut)
async def isEmail(chars:int,email:str=""):
    try:
        temp=AadharCard(chars)
        return {"isEmail":temp.verifyEmail(email)}
    except:
        raise HTTPException(status_code=501, detail="Unable to Process Input")

@app.get("/data/{chars}/isMobile",response_model=isMobileOut)
async def isMobile(chars:int,Mobile:str=""):
    try:
        temp=AadharCard(chars)
        return {"isMobile":temp.verifyMobile(Mobile)}
    except:
        raise HTTPException(status_code=501, detail="Unable to Process Input")



@app.get("/data/{chars}/getEmailHash",response_model=getEmailHashOut)
async def getEmailHash(chars:int):
    try:
        temp=AadharCard(chars)
        return {"emailHash":temp.getEmailHash()}
    except:
        raise HTTPException(status_code=501, detail="Unable to Process Input")

@app.get("/data/{chars}/getMobileHash",response_model=getMobileHashOut)
async def getMobileHash(chars:int):
    try:
        temp=AadharCard(chars)
        return {"mobileHash":temp.getMobileHash()}
    except:
        raise HTTPException(status_code=501, detail="Unable to Process Input")