from patchright.sync_api import sync_playwright

TARGET_URL = "https://arena.ai/search/direct/"


def run() -> None:
	with sync_playwright() as p:
		browser = p.chromium.launch_persistent_context(
            user_data_dir="...",
            channel="chrome",
            headless=False,
            no_viewport=True
        )
		page = browser.new_page()
		try:
			page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)

			# Wait for the model button and get the AI model name
			button_span = page.locator('#chat-area button span').nth(1)
			button_span.wait_for(state="attached", timeout=30000)
			model_name = button_span.inner_text()
			print(f"AI Model: {model_name}")

			# Fill the textarea with a message
			textarea = page.locator("textarea[name='message']").first
			textarea.fill("hi")
			textarea.press("Enter")
			print("Message sent. Waiting for response...")

			# Wait for tooltip-trigger buttons to appear, then click the last one to copy
			page.locator('button[data-slot="tooltip-trigger"]').last.wait_for(state="visible", timeout=60000)
			# page.locator('button[data-slot="tooltip-trigger"]').last.click()
			
			# print the text content of div.prose element
			prose_div = page.locator('div.prose').first
			prose_div.wait_for(state="visible", timeout=5000)
			prose_text = prose_div.inner_text()
			print("Response from AI:")
			print(prose_text)
		except Exception as e:
			page.screenshot(path="error_screenshot.png", timeout=60000)
			print(f"Error occurred, screenshot saved to error_screenshot.png: {e}")
			raise
		finally:
			browser.close()


if __name__ == "__main__":
	try:
		run()
	except KeyboardInterrupt:
		print("Stopped.")
