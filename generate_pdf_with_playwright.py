#!/usr/bin/env python3
"""
Generate PDF from HTML using Playwright (headless Chromium)
This ensures perfect rendering of all CSS styles
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def generate_pdf():
    html_path = Path(__file__).parent / "executive_summary_beautiful.html"
    pdf_path = Path(__file__).parent / "NYQST_Regulatory_Package_Manager_Executive_Summary.pdf"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load the HTML file
        await page.goto(f'file://{html_path.absolute()}')

        # Generate PDF with proper settings for A4, 2 pages
        await page.pdf(
            path=str(pdf_path),
            format='A4',
            print_background=True,
            margin={
                'top': '0mm',
                'right': '0mm',
                'bottom': '0mm',
                'left': '0mm'
            }
        )

        await browser.close()

    print(f"✓ PDF generated successfully: {pdf_path.name}")

    # Print file info
    size_kb = pdf_path.stat().st_size / 1024
    print(f"✓ File size: {size_kb:.1f} KB")
    print(f"✓ Location: {pdf_path}")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
