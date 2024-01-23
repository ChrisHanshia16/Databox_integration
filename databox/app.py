from fastapi import FastAPI, Query
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


@app.get("/v1/pipelines")
async def call_external_api(
    pipeline: str = None,
    opportunities: str = None,
    source: str = None,
    name: str = None,
    status: str = None,
    monetaryValue: int = None,
):
    try:
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6IlhSMnFRc1JyWHAyMWIzQUdlcVZWIiwiY29tcGFueV9pZCI6IjZDa0tGR2d4Q0JwTUpXU082RlZWIiwidmVyc2lvbiI6MSwiaWF0IjoxNjk4MjI0MDc0NTY3LCJzdWIiOiJ1c2VyX2lkIn0.eKR11ubo3AoZxa2M9EamAfY6RCkwiIV9WsaiePFpiYg"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://rest.gohighlevel.com/v1/pipelines/", headers=headers
            )
            response.raise_for_status()

            pipelines = response.json()["pipelines"]

            pipeline_id = next(
                (p["id"] for p in pipelines if p["name"] == pipeline), None
            )
            stage_id = ""
            if opportunities:
                for i in pipelines:
                    if pipeline_id == i["id"]:
                        for j in i["stages"]:
                            if opportunities == j["name"]:
                                stage_id = j["id"]
                                break

            if pipeline_id is None:
                raise HTTPException(status_code=404, detail="Pipeline not found")

            opportunities_response = await client.get(
                f"https://rest.gohighlevel.com/v1/pipelines/{pipeline_id}/opportunities",
                headers=headers,
            )
            opportunities_response.raise_for_status()

            opportunities_data = opportunities_response.json()["opportunities"]

            if opportunities is not None:
                filtered_opportunities = [
                    op for op in opportunities_data if op["pipelineStageId"] == stage_id
                ]

            elif source is not None:
                filtered_opportunities = [
                    op for op in opportunities_data if op["source"] == source
                ]
            elif name is not None:
                filtered_opportunities = [
                    op for op in opportunities_data if op["name"] == name
                ]
            elif status is not None:
                filtered_opportunities = [
                    op for op in opportunities_data if op["status"] == status
                ]
            elif monetaryValue is not None:
                filtered_opportunities = [
                    op
                    for op in opportunities_data
                    if op["monetaryValue"] == monetaryValue
                ]
            else:
                filtered_opportunities = opportunities_data
            if not filtered_opportunities:
                return {"message": "No values found"}

            return filtered_opportunities

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error calling external API: {e}")
