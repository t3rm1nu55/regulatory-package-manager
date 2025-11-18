#!/usr/bin/env python3
"""
Convert beautiful HTML executive summary to PDF
"""
from weasyprint import HTML
from pathlib import Path

# Input and output paths
html_path = Path(__file__).parent / "executive_summary_beautiful.html"
pdf_path = Path(__file__).parent / "NYQST_Regulatory_Package_Manager_Executive_Summary.pdf"

# Convert HTML to PDF
try:
    HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    print(f"✓ PDF generated successfully: {pdf_path.name}")

    # Print file info
    size_kb = pdf_path.stat().st_size / 1024
    print(f"✓ File size: {size_kb:.1f} KB")
    print(f"✓ Location: {pdf_path}")
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nTrying alternative method with reportlab...")

    # Fallback: Try opening in browser for manual print
    import webbrowser
    import os
    webbrowser.open('file://' + os.path.abspath(html_path))
    print(f"✓ Opened HTML in browser: {html_path}")
    print("  Please use Print > Save as PDF from your browser")
