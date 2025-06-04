import os

from crewai import LLM, Agent, Task
from dotenv import load_dotenv

from crew_tools import search_and_scrape

load_dotenv()

HUGGING_FACE_MODEL = "huggingface/meta-llama/Llama-3.3-70B-Instruct"

llm = LLM(
    model=HUGGING_FACE_MODEL,
    max_tokens=256,
    temperature=0.7,
    top_p=0.9,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    api_key=os.getenv("HUGGING_FACE_API_KEY"),
)


scraper = Agent(
    role="Research Analyst",
    goal="Find relevant online articles about a topic",
    backstory="Expert in internet research, skilled at extracting accurate and relevant information.",
    tools=[search_and_scrape],
    allow_delegation=False,
    llm=llm,
)

writer = Agent(
    role="Technical Writer",
    goal="Write a well-structured document from scraped content",
    backstory="Experienced writer who summarizes and formats information into clear, insightful documents.",
    allow_delegation=False,
    llm=llm,
)

scraping_task = Task(
    description="Search the web and scrape content about '{topic}'. Return up to 3 good articles.",
    expected_output="Scraped text from multiple articles with URLs.",
    agent=scraper,
)

writing_task = Task(
    description="Read the scraped content and write a document summarizing the main points. Use markdown structure with sections.",
    expected_output="A well-structured document in markdown format with title, sections, and conclusions.",
    agent=writer,
)
