import datetime
from fastapi import FastAPI, HTTPException, Request
import urllib
import config.database as db
from config.database import payment_info
from fastapi.middleware.cors import CORSMiddleware
from bson.objectid import ObjectId


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
  	return {"message": "Hello, World!"}


@app.get("/payment")
async def get_payments(request: Request):
    params = request.query_params
    
    limit = int(params.get("limit"))
    skip = int(params.get("skip"))

    filter_criteria = {}
    params.get("payee_first_name")
    if(params.get("payee_first_name") != None and params.get("payee_first_name") != ""):
        first_name = urllib.parse.unquote(params.get("payee_first_name"))
        filter_criteria["payee_first_name"] = {
            "$regex": first_name,
            "$options": "i"
        }
    if(params.get("payee_last_name") != None and params.get("payee_last_name") != ""):
        last_name = urllib.parse.unquote(params.get("payee_last_name"))
        filter_criteria["payee_last_name"] = {
            "$regex": last_name,
            "$options": "i"
        }
    if(params.get("payee_due_date_e") != None and params.get("payee_due_date_e") != ""):
        due_date_e = urllib.parse.unquote(params.get("payee_due_date_e"))
        due_date_e = datetime.datetime.fromisoformat(due_date_e.replace('Z', '+00:00'))
        filter_criteria["payee_due_date"] = {
            "$lte": due_date_e
        }
    if(params.get("payee_due_date_s") != None and params.get("payee_due_date_s") != ""):
        due_date_s = urllib.parse.unquote(params.get("payee_due_date_s"))
        due_date_s = datetime.datetime.fromisoformat(due_date_s.replace('Z', '+00:00'))
        if("payee_due_date" in filter_criteria):
            filter_criteria["payee_due_date"]["$gte"] = due_date_s
        else:
            filter_criteria["payee_due_date"] = {
                "$gte": due_date_s
            }

    try:
        payments = list(payment_info.find(filter_criteria, limit=limit, skip=skip))
        count = payment_info.count_documents(filter_criteria)

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

@app.delete("/payment/{id}")
async def delete_payment_by_id(id: str):
    try:
        result = payment_info.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {
            "message": "Record deleted successfully",
            "status": 200,
        }
    except Exception as e:
        print(f"Error deleting payment info: {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
