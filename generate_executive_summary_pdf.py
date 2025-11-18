#!/usr/bin/env python3
"""
Generate a professional 2-page PDF executive summary using reportlab
Based on Anthropic skills PDF generation patterns
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

def create_executive_summary():
    # Initialize PDF document
    pdf_file = "Regulatory_Package_Manager_Executive_Summary.pdf"
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Get standard styles and create custom styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.HexColor('#dddddd'),
        borderPadding=3
    )

    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=10,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=4,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
        leading=11
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=7,
        fontName='Courier',
        backColor=colors.HexColor('#f5f5f5'),
        borderWidth=1,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=4,
        leftIndent=10
    )

    # Build document content
    elements = []

    # Title and subtitle
    elements.append(Paragraph("Regulatory Package Manager: Executive Summary", title_style))
    elements.append(Paragraph("A Maven-based system for managing regulatory documents as versioned packages", subtitle_style))
    elements.append(Spacer(1, 0.3*cm))

    # The Problem
    elements.append(Paragraph("The Problem", heading_style))
    elements.append(Paragraph(
        "Financial institutions struggle to maintain current regulatory documentation across multiple jurisdictions. "
        "Current approaches involve manual document collection, no version control, difficulty tracking amendments, "
        "impossible gap analysis, and each RegTech vendor re-analyzing the same regulations independently.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Result:</b> High compliance costs, fragmented solutions, and risk of using outdated regulations.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*cm))

    # The Solution
    elements.append(Paragraph("The Solution: Regulatory Package Manager", heading_style))
    elements.append(Paragraph(
        "Apply proven software package management patterns (Maven) to regulatory documents. "
        "Each regulation becomes a versioned artifact with dependencies, checksums, and metadata.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*cm))

    # BOM Innovation
    elements.append(Paragraph("Core Innovation: Bill of Materials (BOM)", subheading_style))
    elements.append(Paragraph(
        "A \"regime package\" (e.g., EMIR 2024.11.0) includes: Base law, Technical Standards (RTS, ITS), "
        "Implementation artifacts (XML schemas, validation rules), with all dependencies automatically resolved.",
        body_style
    ))
    elements.append(Paragraph(
        "<font name='Courier' size='7'>eu.regulation.emir:law-648-2012:2024.01.09:pdf</font><br/>"
        "<font name='Courier' size='7'>eu.regulation:emir-bom:2024.11.0:pom</font>",
        body_style
    ))
    elements.append(Spacer(1, 0.2*cm))

    # Key Capabilities
    elements.append(Paragraph("Key Capabilities", subheading_style))
    elements.append(Paragraph(
        "<b>Document Management:</b> Version control, transitive dependency resolution, integrity checking (SHA-256), gap analysis.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Analysis Services:</b> Obligation extraction, CDE mapping to CPMI-IOSCO standards, ISO 20022 integration, "
        "cross-regime impact analysis.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Integration:</b> MCP Server for LLM agents, REST API, CLI, Git workflow with PR approvals.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*cm))

    # Technical Architecture
    elements.append(Paragraph("Technical Architecture", heading_style))
    elements.append(Paragraph(
        "<b>5-Stage Pipeline:</b> (1) Document Ingestion (PDF parsing, OCR), "
        "(2) Structural Analysis (article detection), (3) Semantic Extraction (obligations), "
        "(4) Enrichment (CDE/ISO mapping), (5) Publication (Maven artifacts).",
        body_style
    ))
    elements.append(Spacer(1, 0.15*cm))

    # Repository Tiers Table
    tier_data = [
        ['Tier', 'Content', 'Access', 'Revenue'],
        ['Public', 'Raw regulatory PDFs', 'Free', 'Lead generation'],
        ['Premium', 'Structured obligations, CDE mappings', 'Subscription', 'Primary revenue'],
        ['Enterprise', 'Client-specific analysis, custom BOMs', 'Custom pricing', 'High-margin']
    ]

    tier_table = Table(tier_data, colWidths=[2.5*cm, 5*cm, 3*cm, 3*cm])
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    elements.append(tier_table)
    elements.append(Spacer(1, 0.2*cm))

    # Commercial Model
    elements.append(Paragraph("Commercial Model", heading_style))

    # Revenue table
    revenue_data = [
        ['Year', 'Premium Clients', 'Enterprise Clients', 'Total Revenue'],
        ['Year 1', '20 × $30K = $600K', '2 × $200K = $400K', '$1.0M'],
        ['Year 2', '100 × $30K = $3.0M', '10 × $200K = $2.0M', '$5.0M'],
        ['Year 3', '500 × $30K = $15.0M', '25 × $200K = $5.0M', '$20.0M']
    ]

    revenue_table = Table(revenue_data, colWidths=[2*cm, 4.5*cm, 4.5*cm, 2.5*cm])
    revenue_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    elements.append(revenue_table)
    elements.append(Spacer(1, 0.2*cm))

    # Investment
    elements.append(Paragraph("Investment Required", subheading_style))
    elements.append(Paragraph(
        "<b>Development:</b> $216K (6 FTE × 8 weeks × $4.5K/week) - Backend engineers, data engineer, "
        "regulatory analyst, frontend engineer, DevOps engineer.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Infrastructure Year 1:</b> $0 (Nexus OSS, cloud-hosted Neo4j free tier, existing AWS)",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Total Initial Investment:</b> $216K for 8-week MVP | <b>ROI:</b> 4.6× Year 1, 23× Year 3",
        body_style
    ))
    elements.append(Spacer(1, 0.3*cm))

    # PAGE BREAK
    elements.append(PageBreak())

    # Competitive Advantages
    elements.append(Paragraph("Competitive Advantages", heading_style))
    elements.append(Paragraph(
        "<b>vs. Manual Management:</b> Automated updates, dependency awareness, systematic gap analysis.",
        body_style
    ))
    elements.append(Paragraph(
        "<b>vs. Existing RegTech:</b> Open architecture, standard Maven tooling, composable services, "
        "multi-tenant (analyze once, serve many).",
        body_style
    ))
    elements.append(Paragraph(
        "<b>vs. Building In-House:</b> Network effects, continuous professional updates, pre-analyzed obligations.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*cm))

    # Implementation Timeline
    elements.append(Paragraph("Implementation Timeline (8-Week MVP)", heading_style))

    timeline_data = [
        ['Weeks', 'Milestone', 'Deliverables'],
        ['1-2', 'Foundation', 'Nexus setup, Maven coordinates, first BOM (EMIR)'],
        ['3-4', 'Document Ingestion', 'PDF pipeline, metadata extraction, initial uploads (EMIR/MiFID/SFTR)'],
        ['5-6', 'Analysis Pipeline', 'Obligation extraction, CDE mapping, Neo4j graph schema'],
        ['7-8', 'Integration Layer', 'MCP Server, REST API, CLI tool, dashboard prototype'],
        ['9+', 'Production', 'Security, auth, monitoring, customer onboarding']
    ]

    timeline_table = Table(timeline_data, colWidths=[2*cm, 3.5*cm, 8*cm])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    elements.append(timeline_table)
    elements.append(Spacer(1, 0.2*cm))

    # Success Metrics
    elements.append(Paragraph("Success Metrics", heading_style))

    metrics_data = [
        ['Category', 'Metric', 'Target'],
        ['Technical', 'Document version accuracy', '99%'],
        ['Technical', 'Dependency resolution time', '<5 minutes'],
        ['Technical', 'Obligation extraction accuracy', '90%+'],
        ['Technical', 'CDE mapping confidence', '95%+'],
        ['Business', 'Design partners signed (6 months)', '20'],
        ['Business', 'Paying customers (9 months)', '5'],
        ['Business', 'ARR (12 months)', '$1M'],
        ['Business', 'Gross margin', '50%+']
    ]

    metrics_table = Table(metrics_data, colWidths=[3*cm, 6.5*cm, 4*cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.2*cm))

    # Next Steps
    elements.append(Paragraph("Next Steps", heading_style))
    next_steps = [
        "<b>1. Validate with design partners:</b> 5-10 target clients for feedback",
        "<b>2. Secure funding:</b> $216K for 8-week MVP development",
        "<b>3. Hire core team:</b> Regulatory analyst + 2 engineers to start",
        "<b>4. Build MVP:</b> EMIR + MiFID II regimes with basic analysis",
        "<b>5. Beta launch:</b> Q1 2025 with design partners",
        "<b>6. Commercial launch:</b> Q2 2025"
    ]
    for step in next_steps:
        elements.append(Paragraph(step, body_style))
    elements.append(Spacer(1, 0.3*cm))

    # Conclusion Box
    elements.append(Paragraph("Conclusion", heading_style))
    elements.append(Paragraph(
        "The Regulatory Package Manager applies battle-tested software engineering practices (Maven, dependency management, "
        "versioning) to solve a $10B+ market problem in RegTech. By treating regulations as versioned packages and building "
        "reusable analysis on top, we can:",
        body_style
    ))

    conclusion_points = [
        "• <b>Reduce compliance costs</b> by 60-80% through automation",
        "• <b>Improve accuracy</b> through systematic version control",
        "• <b>Enable new use cases</b> (gap analysis, impact assessment, automated monitoring)",
        "• <b>Create network effects</b> through shared document repository",
        "• <b>Build defensible moats</b> through accumulated analysis artifacts"
    ]
    for point in conclusion_points:
        elements.append(Paragraph(point, body_style))
    elements.append(Spacer(1, 0.3*cm))

    # Investment Summary Box
    summary_box_style = ParagraphStyle(
        'SummaryBox',
        parent=body_style,
        fontSize=9,
        backColor=colors.HexColor('#e8f4f8'),
        borderWidth=2,
        borderColor=colors.HexColor('#3498db'),
        borderPadding=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    elements.append(Paragraph(
        "<b>Investment ask:</b> $216K for 8-week MVP<br/>"
        "<b>Projected return:</b> $1M Year 1, $20M Year 3<br/>"
        "<b>Time to first revenue:</b> 6 months",
        summary_box_style
    ))
    elements.append(Spacer(1, 0.2*cm))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=body_style,
        fontSize=8,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=0
    )

    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("Date: November 18, 2024", footer_style))

    # Build PDF
    doc.build(elements)
    print(f"✓ PDF generated successfully: {pdf_file}")
    return pdf_file

if __name__ == "__main__":
    pdf_path = create_executive_summary()

    # Print file info
    import os
    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"✓ File size: {size_kb:.1f} KB")
    print(f"✓ Location: {os.path.abspath(pdf_path)}")
