from crewai import Crew
from fastapi import FastAPI

from agents import scraper, scraping_task, writer, writing_task

app = FastAPI()

crew = Crew(
    agents=[scraper, writer],
    tasks=[scraping_task, writing_task],
    verbose=True,
)


@app.get("/ask_crew")
async def ask_crew(topic: str):
    """
    Endpoint to ask the crew to perform a task based on the provided topic.
    """
    try:
        result = crew.kickoff({"topic": topic})
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
