import agentql
import asyncio
from agentql.ext.playwright.async_api import Page
from playwright.async_api import async_playwright


CREDIT_CARDS_URL = "https://popularenlinea.com/tarjetas"


async def _do_extract_credit_card_data(page: Page) -> list:
    """Extracts credit card data from the main page."""
    credit_cards = """{
            tarjetas_de_creditos[] {
                name
                conoce_mas
            }
    }"""

    response = await page.query_data(credit_cards)
    return response.get("tarjetas_de_creditos", [])


async def _do_extract_credit_card_details(page: Page, url: str) -> dict:
    """Open url and extract credit card details."""
    await page.goto(url)

    query = """{
        detalles_tarjeta {
            title,
            description
            beneficios[]
        }
    }"""

    response = await page.query_data(query)
    return response.get("detalles_tarjeta", {})


async def main():
    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=True
    ) as browser:
        page = await agentql.wrap_async(browser.new_page())

        await page.goto(CREDIT_CARDS_URL) 
        credit_card_data = await _do_extract_credit_card_data(page)

        detailed_data = []
        for card in credit_card_data:
            url = card.get("conoce_mas")
            if url:
                details = await _do_extract_credit_card_details(page, url)
                detailed_data.append({
                    "name": card["name"],
                    "conoce_mas": url,
                    "details": details
                })

        print(detailed_data)


if __name__ == "__main__":
    asyncio.run(main())