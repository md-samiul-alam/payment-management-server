import datetime
from fastapi import FastAPI, HTTPException
import config.database as db
from config.database import payment_info
from fastapi.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # If you need to send cookies or use authentication
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
  	return {"message": "Hello, World!"}


@app.get("/payment")
async def get_payments(limit: int = 10, skip: int = 0):
    try:
        payments = list(payment_info.find({}, limit=limit, skip=skip))
        count = payment_info.count_documents({})

        for payment in payments:
            payment["_id"] = str(payment["_id"])
   
            payment_date = payment["payee_due_date"].date()
            today_date = datetime.date.today()
            
            if(payment_date == today_date):
                payment["payee_payment_status"] =  "DUE NOW"
            elif(payment_date < today_date):
                payment["payee_payment_status"] =  "OVER DUE"
            else:
                payment["payee_payment_status"] =  "DUE"

            total_due_before_tax =  payment["due_amount"] -  payment["due_amount"] * (payment["discount_percent"]/100.0); 
            payment["total_due"] = total_due_before_tax +  total_due_before_tax * (payment["tax_percent"]/100.0);
            
                            
        return {
            "payments": payments,
            "count": count,
        }

    except Exception as e:
        print(f"Error fetching payment info: {e}")
        raise HTTPException(status_code=500, detail=f"{e}")


@app.get("/payment/{id}")
async def get_payment_by_id(id: str):
    try:
        payment = payment_info.find_one({"_id": ObjectId(id)})

        payment["_id"] = str(payment["_id"])

        payment_date = payment["payee_due_date"].date()
        today_date = datetime.date.today()
        
        if(payment_date == today_date):
            payment["payee_payment_status"] =  "DUE NOW"
        elif(payment_date < today_date):
            payment["payee_payment_status"] =  "OVER DUE"
        else:
            payment["payee_payment_status"] =  "DUE"

        total_due_before_tax =  payment["due_amount"] -  payment["due_amount"] * (payment["discount_percent"]/100.0); 
        payment["total_due"] = total_due_before_tax +  total_due_before_tax * (payment["tax_percent"]/100.0);
                            
        return payment

    except Exception as e:
        print(f"Error fetching payment info: {e}")
        raise HTTPException(status_code=500, detail=f"{e}")