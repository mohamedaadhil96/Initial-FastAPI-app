from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

# Store full status history per CallSid
call_status_history = {}

@app.post("/twilio/call-status")
async def call_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    To: str = Form(...),
    From: str = Form(...)
):
    status_update = {
        "status": CallStatus,
        "to": To,
        "from": From,
        "timestamp": datetime.utcnow().isoformat()
    }

    if CallSid not in call_status_history:
        call_status_history[CallSid] = []

    call_status_history[CallSid].append(status_update)

    print(f"[CALL STATUS] SID: {CallSid} | Status: {CallStatus} | To: {To} | From: {From}")
    return JSONResponse(content={"message": "Callback received"}, status_code=200)


@app.get("/twilio/status-history")
def get_status_history():
    return JSONResponse(content={"call_status_history": call_status_history})


@app.get("/twilio/final-status")
def get_final_status():
    final_statuses = {}
    for sid, updates in call_status_history.items():
        if updates:
            latest_update = updates[-1]
            final_statuses[sid] = {
                "final_status": latest_update["status"],
                "to": latest_update["to"],
                "from": latest_update["from"],
                "timestamp": latest_update["timestamp"]
            }
    print(f"[FINAL STATUS] Total calls tracked: {len(final_statuses)}")
    return JSONResponse(content={"final_call_statuses": final_statuses})
