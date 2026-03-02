import asyncio
from patchright.async_api import async_playwright

TARGET_URL = "https://arena.ai/search/direct/"


async def run() -> None:
	async with async_playwright() as p:
		browser = await p.chromium.launch_persistent_context(
            user_data_dir="...",
            channel="chrome",
            headless=False,
            no_viewport=True
        )
		page = await browser.new_page()
		await page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)

		# Wait for the model button and get the AI model name
		button_span = page.locator('#chat-area button span').nth(1)
		await button_span.wait_for(state="attached", timeout=30000)
		model_name = await button_span.inner_text()
		print(f"AI Model: {model_name}")

		# Fill the textarea with a message
		textarea = page.locator("textarea[name='message']").first
		await textarea.fill("latest news of monarch series")
		await textarea.press("Enter")
		print("Message sent. Waiting for response...")

		# Wait for tooltip-trigger buttons to appear, then click the last one to copy
		await page.locator('button[data-slot="tooltip-trigger"]').last.wait_for(state="visible", timeout=60000)
		# await page.locator('button[data-slot="tooltip-trigger"]').last.click()
		
		# print the text content of div.prose element
		prose_div = page.locator('div.prose').first
		await prose_div.wait_for(state="visible", timeout=60000)
		prose_text = await prose_div.inner_text()
		print("Response from AI:")
		print(prose_text)

		await browser.close()


if __name__ == "__main__":
	try:
		asyncio.run(run())
	except KeyboardInterrupt:
		print("Stopped.")
