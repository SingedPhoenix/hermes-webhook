from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class WebhookPayload(BaseModel):
    Routine_Task: str
    Category: str
    Frequency: str
    Status: str
    Last_Completed: str
    Streak_Count: int
    Longest_Streak: int
    Streak_Date_Range: str
    Reminder_Time: str
    Alert_Status: str
    Tags_Deity_Links: list[str]
    Notes: str

@app.post("/")
async def receive_webhook(payload: WebhookPayload):
    try:
        print("✅ Webhook received successfully!")
        print(payload.dict())
        return JSONResponse(content={"status": "success", "data": payload.dict()})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
