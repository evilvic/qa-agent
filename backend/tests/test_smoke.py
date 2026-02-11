import pytest
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI, Browser
load_dotenv()

@pytest.mark.asyncio
async def test_home_smoke():
    browser = Browser(headless=True, allowed_domains=["minu.mx"])
    agent = Agent(
        task="Abre https://pwa.minu.mx y confirma que cargó.",
        llm=ChatOpenAI(model="gpt-4.1-mini"),
        browser=browser,
    )
    result = await agent.run()
    assert result