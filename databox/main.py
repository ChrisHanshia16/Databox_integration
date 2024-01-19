from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


@app.get("/v1/get")
def get_hello():
    return {"message": "Hello, this is a FastAPI GET API!"}


@app.get("/v1/post")
async def call_external_api():
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6IlhSMnFRc1JyWHAyMWIzQUdlcVZWIiwiY29tcGFueV9pZCI6IjZDa0tGR2d4Q0JwTUpXU082RlZWIiwidmVyc2lvbiI6MSwiaWF0IjoxNjk4MjI0MDc0NTY3LCJzdWIiOiJ1c2VyX2lkIn0.eKR11ubo3AoZxa2M9EamAfY6RCkwiIV9WsaiePFpiYg"
            }
            response = await client.get(
                "https://rest.gohighlevel.com/v1/pipelines/", headers=headers
            )

            response.raise_for_status()
            id = response.json()

            print(id["pipelines"][0]["id"])
            # Raise an HTTPError for bad responses (4xx and 5xx status codes)
            return 0
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=500, detail=f"Error calling external API: {e}"
            )
