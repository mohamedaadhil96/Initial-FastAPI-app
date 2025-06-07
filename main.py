from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse

app = FastAPI()

# In-memory store for call statuses
call_status_store = {}

@app.post("/twilio/call-status")
async def call_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    To: str = Form(...),
    From: str = Form(...)
):
    print(f"[CALL STATUS] SID: {CallSid} | Status: {CallStatus} | To: {To} | From: {From}")
    
    # Store/update status
    call_status_store[CallSid] = {
        "status": CallStatus,
        "to": To,
        "from": From
    }

    return JSONResponse(content={"message": "Callback received"}, status_code=200)

@app.get("/twilio/final-status")
def get_final_status():
    # Filter for only completed calls
    final_statuses = {
        sid: info for sid, info in call_status_store.items()
        if info["status"] == "completed"
    }
    return JSONResponse(content={"completed_calls": final_statuses})
