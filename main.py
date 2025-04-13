from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from notion_client import Client
import os

app = FastAPI()

# Notion auth
notion = Client(auth=os.getenv("NOTION_API_KEY"))

# Replace this with your actual Notion database ID
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

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

        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Routine Task": {"title": [{"text": {"content": payload.Routine_Task}}]},
                "Category": {"select": {"name": payload.Category}},
                "Frequency": {"select": {"name": payload.Frequency}},
                "Status": {"select": {"name": payload.Status}},
                "Last Completed": {"date": {"start": payload.Last_Completed}},
                "Streak Count": {"number": payload.Streak_Count},
                "Longest Streak": {"number": payload.Longest_Streak},
                "Streak Date Range": {"rich_text": [{"text": {"content": payload.Streak_Date_Range}}]},
                "Reminder Time": {"rich_text": [{"text": {"content": payload.Reminder_Time}}]},
                "Alert Status": {"select": {"name": payload.Alert_Status}},
                "Tags/Deity Links": {"multi_select": [{"name": tag} for tag in payload.Tags_Deity_Links]},
                "Notes": {"rich_text": [{"text": {"content": payload.Notes}}]},
            }
        )

        return JSONResponse(content={"status": "success", "data": payload.dict()})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
