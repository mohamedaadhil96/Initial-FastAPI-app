from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/twilio/call-status")
async def call_status(
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
    To: str = Form(...),
    From: str = Form(...)
):
    print(f"[CALL STATUS] SID: {CallSid} | Status: {CallStatus} | To: {To} | From: {From}")
    return JSONResponse(content={"message": "Callback received"}, status_code=200)
