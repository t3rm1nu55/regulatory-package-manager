#!/usr/bin/env python3
"""
Generate professional PDF for Technical Overview (Sections 3-6)
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime

def create_technical_pdf():
    pdf_file = "NYQST_Technical_Overview.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm
    )

    # Get standard styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=8,
        spaceBefore=14,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderPadding=0,
        borderColor=colors.HexColor('#0066cc'),
        borderRadius=0,
        leftIndent=0
    )

    h3_style = ParagraphStyle(
        'Heading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#004999'),
        spaceAfter=6,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    h4_style = ParagraphStyle(
        'Heading4',
        parent=styles['Heading4'],
        fontSize=10,
        textColor=colors.HexColor('#004999'),
        spaceAfter=4,
        spaceBefore=8,
        fontName='Helvetica-Bold',
        fontStyle='italic'
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9.5,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=12,
        fontName='Helvetica'
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        backColor=colors.HexColor('#f5f5f5'),
        borderWidth=1,
        borderColor=colors.HexColor('#ddd'),
        borderPadding=6,
        leftIndent=10,
        spaceAfter=8,
        leading=10
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=3
    )

    # Build document
    elements = []

    # Title page
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("Regulatory Package Management", title_style))
    elements.append(Paragraph("Technical Overview", subtitle_style))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(
        "Applying proven software dependency management to regulatory compliance",
        ParagraphStyle('tagline', parent=body_style, alignment=TA_CENTER, fontSize=10, textColor=colors.HexColor('#666'))
    ))
    elements.append(Spacer(1, 2*cm))

    # --- Section 3 ---
    elements.append(Paragraph(
        "3. Why Treating Regulatory Documents as Code Enables 30 Years of Learned Benefits",
        h2_style
    ))

    elements.append(Paragraph("The Software Dependency Problem (Solved in 1990s-2000s)", h3_style))
    elements.append(Paragraph(
        "Before package managers, software development faced identical problems:",
        body_style
    ))

    elements.append(Paragraph("<b>Pre-Maven/NPM/pip era:</b>", body_style))
    for item in [
        "Developers manually downloaded library JAR files from project websites",
        "No standard way to declare \"I need library X version 2.3\"",
        "Dependency conflicts: Library A needs XML parser v1.0, Library B needs v2.0",
        "No automated verification: \"Did I get the correct file from a trusted source?\"",
        "\"Works on my machine\" syndrome: Different developers had different library versions"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph("<b>Post-package manager:</b>", body_style))
    for item in [
        "Declare dependencies in manifest file (pom.xml, package.json, requirements.txt)",
        "Package manager resolves transitive dependencies automatically",
        "Checksums verify integrity",
        "Version ranges allow compatible updates: \"any 2.x version\"",
        "Reproducible builds: Same inputs produce identical outputs"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("Direct Parallels to Regulatory Documents", h3_style))

    # Comparison table
    table_data = [
        ['Software Development', 'Regulatory Compliance'],
        ['Library JAR file', 'Regulation PDF/XSD'],
        ['Library version (e.g., 2.3.1)', 'Consolidated version date (e.g., 2024.01.09)'],
        ['Dependency: "Needs library X"', 'Dependency: "RTS implements Article 9"'],
        ['Transitive dependencies', 'Schema needs RTS needs base law'],
        ['SHA-256 checksum', '(Currently absent)'],
        ['Maven Central repository', '(Currently absent - our proposal)'],
        ['pom.xml dependency declaration', '(Currently manual)'],
        ['mvn install downloads all files', '(Currently manual downloads)'],
        ['Version conflict detection', '(Currently undetected)']
    ]

    comparison_table = Table(table_data, colWidths=[8*cm, 8*cm])
    comparison_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
    ]))
    elements.append(comparison_table)

    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("Lessons from 30 Years of Package Management", h3_style))

    # Lessons (shortened for space)
    lessons = [
        ("Lesson 1: Namespacing Prevents Collisions",
         "Structured coordinates like <font face='Courier' size='8'>eu.regulation.emir:law-648-2012:article-9</font> are unambiguous, unlike \"Article 9\" which could refer to EMIR, MiFIR, or SFTR."),
        ("Lesson 2: Semantic Versioning Communicates Intent",
         "Hybrid approach combines date-based versioning for law (2024.01.09) with semantic versioning for technical artifacts (schemas-3.0-mar2023) to indicate breaking changes."),
        ("Lesson 3: Dependency Resolution Prevents Conflicts",
         "Dependency graphs ensure RTS, schemas, and validation rules are compatible versions, preventing undefined behavior."),
        ("Lesson 4: Checksums Ensure Integrity",
         "SHA-256 hashes verify document authenticity and detect corruption or tampering."),
        ("Lesson 5: Bill of Materials (BOM) Manages Complexity",
         "One BOM request (<font face='Courier' size='8'>emir-bom:2024.11.0</font>) retrieves complete tested package: law + RTS + ITS + schemas + validation rules."),
        ("Lesson 6: Reproducibility Enables Auditability",
         "pom.xml from Q2 2023 provides complete specification of exact regulatory versions used, enabling audit reproduction.")
    ]

    for title, desc in lessons:
        elements.append(Paragraph(f"<b>{title}</b>", h4_style))
        elements.append(Paragraph(desc, body_style))

    elements.append(PageBreak())

    # --- Section 4: Maven ---
    elements.append(Paragraph("4. Maven Explainer", h2_style))
    elements.append(Paragraph(
        "Apache Maven is a build automation and dependency management tool for Java projects, created in 2003. "
        "While initially designed for software builds, its dependency management concepts are applicable to any versioned artifacts.",
        body_style
    ))

    elements.append(Paragraph("Core Concepts", h3_style))
    elements.append(Paragraph("Coordinates (GAV)", h4_style))
    elements.append(Paragraph(
        "Every artifact is uniquely identified by: <font face='Courier' size='8'>groupId : artifactId : version</font>",
        body_style
    ))
    elements.append(Paragraph(
        "Example (regulations): <font face='Courier' size='8'>eu.regulation.emir : law-648-2012 : 2024.01.09</font>",
        body_style
    ))

    elements.append(Paragraph("POM (Project Object Model)", h4_style))
    elements.append(Paragraph("XML file describing artifact and its dependencies:", body_style))

    pom_code = """<project>
  <groupId>eu.regulation.emir</groupId>
  <artifactId>rts-2015-2205</artifactId>
  <version>2023.05.15</version>
  <dependencies>
    <dependency>
      <groupId>eu.regulation.emir</groupId>
      <artifactId>law-648-2012</artifactId>
      <version>2024.01.09</version>
    </dependency>
  </dependencies>
</project>"""

    elements.append(Preformatted(pom_code, code_style))

    elements.append(Paragraph("Dependency Resolution", h4_style))
    elements.append(Paragraph("When you declare a dependency, Maven:", body_style))
    for step in [
        "Downloads the POM file",
        "Reads its dependencies",
        "Recursively downloads transitive dependencies",
        "Detects version conflicts",
        "Verifies checksums",
        "Stores in local cache (~/.m2/repository/)"
    ]:
        elements.append(Paragraph(f"• {step}", bullet_style))

    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph("What Maven Provides", h4_style))
    for item in [
        "Standardized coordinates: Globally unique artifact identification",
        "Transitive dependency resolution: Automatically fetch what you need",
        "Checksum verification: Integrity guarantees",
        "Version management: Track available versions, identify latest",
        "Local caching: Download once, reuse across projects",
        "Mature tooling: 20+ years of ecosystem development"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph("What Maven Doesn't Provide", h4_style))
    for item in [
        "Content analysis: Doesn't understand PDFs or extract obligations",
        "Semantic understanding: No knowledge of regulatory relationships",
        "Change tracking: Doesn't detect what changed between versions",
        "Workflow: No approval process, check-in/check-out, branching",
        "Search: Basic artifact search only, not full-text content search"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(PageBreak())

    # --- Section 5: Nexus ---
    elements.append(Paragraph("5. Nexus Repository Manager Explainer", h2_style))
    elements.append(Paragraph(
        "Sonatype Nexus Repository Manager is a repository server for storing and managing binary artifacts. "
        "It acts as a central hub for Maven artifacts (and other package formats: npm, PyPI, Docker, etc.).",
        body_style
    ))
    elements.append(Paragraph(
        "<b>Two editions:</b> Nexus Repository OSS (free, open-source) and Nexus Repository Pro (commercial).",
        body_style
    ))

    elements.append(Paragraph("Core Functions", h3_style))

    functions = [
        ("Artifact Storage", "Stores artifacts in Maven format with automatic checksum generation (SHA-256, SHA-1, MD5) and metadata management."),
        ("Repository Types", "Hosted (your artifacts), Proxy (cache from remote), Group (combine multiple repositories)."),
        ("Access Control", "Role-based access control (RBAC): anonymous read for public, authentication for premium, deploy permissions controlled."),
        ("REST API", "Programmatic access for searching, uploading, and managing artifacts."),
        ("Web UI", "Browser-based interface for browsing, searching, downloading, and viewing dependencies.")
    ]

    for title, desc in functions:
        elements.append(Paragraph(f"<b>{title}:</b> {desc}", body_style))

    elements.append(Paragraph("Infrastructure Requirements", h3_style))
    elements.append(Paragraph("<b>Nexus Repository OSS:</b>", body_style))
    for item in [
        "Cost: Free (open-source, Eclipse Public License)",
        "Server: 4-8 CPU cores, 8-16GB RAM recommended for production",
        "Storage: 1-10GB per regulatory regime (all versions)",
        "Deployment: Docker container, cloud-native (AWS, Azure, GCP)"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(Paragraph(
        "<b>Typical setup:</b> AWS EC2 t3.large (~$60/month) + 1TB EBS storage (~$100/month) + data transfer = $200-500/month.",
        body_style
    ))

    elements.append(Paragraph("What Nexus Doesn't Provide", h4_style))
    for item in [
        "Git workflow: No branching, pull requests, or code review",
        "Document processing: Doesn't parse PDFs or extract content",
        "Analysis: No understanding of regulatory semantics",
        "Notifications: Basic webhooks only, not \"alert when EMIR updated\"",
        "Gap analysis: No concept of entity profile or compliance requirements"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(PageBreak())

    # --- Section 6: NYQST System ---
    elements.append(Paragraph("6. NYQST Regulatory Package Manager: System Design", h2_style))
    elements.append(Paragraph("Architecture Overview", h3_style))
    elements.append(Paragraph(
        "NYQST builds three layers on top of Nexus + Maven:",
        body_style
    ))

    arch_text = """┌───────────────────────────────────────────────┐
│  Layer 3: Intelligence Services               │
│  (Obligation Extraction, CDE Mapping, Gap     │
│   Analysis, Impact Assessment)                │
├───────────────────────────────────────────────┤
│  Layer 2: Document Management & Workflow      │
│  (Git Workflow, Change Detection, Update      │
│   Monitor, MCP Server, API)                   │
├───────────────────────────────────────────────┤
│  Layer 1: Package Management (Nexus + Maven)  │
│  (Maven Coordinates, Nexus Repository,        │
│   Artifact Storage, Dependency Resolution)    │
└───────────────────────────────────────────────┘"""

    elements.append(Preformatted(arch_text, ParagraphStyle('arch', parent=code_style, fontSize=7, leading=9)))

    elements.append(Paragraph("Layer 1: Package Management Foundation", h3_style))
    elements.append(Paragraph(
        "<b>Uses Maven + Nexus as-is</b>, applying their patterns to regulatory documents.",
        body_style
    ))
    elements.append(Paragraph("<b>Artifact types:</b> Laws/Regulations (PDFs), Technical Standards (RTS/ITS), Schemas (XSD in ZIP), Validation Rules (Excel), BOMs (POM-only).", body_style))
    elements.append(Paragraph("<b>Repository structure:</b>", body_style))
    for item in [
        "Public hosted repository: Freely available regulatory documents (anonymous read)",
        "Premium hosted repository: Analyzed documents (authenticated access, billing integration)"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(Paragraph("<b>Client usage:</b>", body_style))
    client_code = """mvn dependency:get -Dartifact=eu.regulation:emir-bom:2024.11.0

# Downloads to ~/.m2/repository/eu/regulation/emir-bom/2024.11.0/
# Automatically fetches all dependencies listed in BOM"""
    elements.append(Preformatted(client_code, code_style))

    elements.append(Paragraph("Layer 2: Document Management & Workflow", h3_style))
    elements.append(Paragraph("<b>Git integration</b> for document lifecycle:", body_style))
    for step in [
        "Check-in: Team member adds new regulatory document to Git",
        "Pull request: Changes reviewed by compliance team",
        "Approval: Legal sign-off required before merge",
        "CI/CD pipeline: Validates POM, computes checksums, runs quality checks, deploys to Nexus",
        "Git tag: Release tagged (e.g., emir-bom-2024.11.0)"
    ]:
        elements.append(Paragraph(f"• {step}", bullet_style))

    elements.append(Paragraph("<b>Change detection:</b> Monitor regulator websites (EUR-Lex, FCA), compare checksums, generate change reports, notify subscribers.", body_style))
    elements.append(Paragraph("<b>MCP Server:</b> LLM agents can query regulatory repository, retrieve obligations, analyze changes between versions.", body_style))

    elements.append(Paragraph("Layer 3: Intelligence Services", h3_style))
    elements.append(Paragraph(
        "<b>This layer is where NYQST adds commercial value</b> beyond free document hosting.",
        body_style
    ))

    services = [
        ("Document Ingestion & Parsing", "PDF text extraction (pdfplumber), OCR (Tesseract), structure identification (articles, sections), metadata enrichment (CELEX numbers, effective dates)."),
        ("Obligation Extraction", "Identify normative language (\"shall\", \"must\"), parse components (actor, action, object, recipient, timing, conditions), publish as Maven artifact with dependency on source document."),
        ("CDE Mapping", "Map regulatory fields to CPMI-IOSCO Critical Data Elements, indicate harmonization across regimes (EMIR, MiFIR, SFTR, CFTC, etc.)."),
        ("ISO 20022 Integration", "Link regulatory fields to ISO 20022 message elements (message name, XPath, data type, occurrence)."),
        ("Gap Analysis", "Input entity profile (jurisdiction, activities, products), query canonical model, compute gaps (required - installed), prioritize (critical, recommended, optional).")
    ]

    for title, desc in services:
        elements.append(Paragraph(f"<b>{title}:</b> {desc}", body_style))

    elements.append(Paragraph("Technology Stack", h3_style))
    elements.append(Paragraph("<b>Core:</b> Nexus OSS, Maven, Git, PostgreSQL", body_style))
    elements.append(Paragraph("<b>Analysis:</b> Python, Neo4j (graph DB), PyPDF2/pdfplumber, spaCy/NLTK", body_style))
    elements.append(Paragraph("<b>Integration:</b> FastAPI, MCP Server, Webhooks", body_style))
    elements.append(Paragraph("<b>Clients:</b> Maven CLI, custom CLI (nyqst-reg), web dashboard", body_style))

    elements.append(Paragraph("Access Tiers", h3_style))
    tiers = [
        ("Public (Free)", "Raw regulatory documents from public sources, basic Maven repository, version tracking, checksums."),
        ("Premium (Subscription)", "Public + structured obligations + CDE mappings + ISO 20022 links, API access, gap analysis, update notifications."),
        ("Enterprise (Custom)", "Premium + client-specific analysis + custom BOMs, dedicated support, custom integrations, priority updates.")
    ]

    for title, desc in tiers:
        elements.append(Paragraph(f"<b>{title}:</b> {desc}", body_style))

    elements.append(PageBreak())

    # Conclusion
    elements.append(Paragraph("Conclusion", h2_style))
    elements.append(Paragraph(
        "The software development industry solved library dependency management 20+ years ago through package managers "
        "like Maven and repository servers like Nexus.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph(
        "NYQST Regulatory Package Manager applies these proven patterns to regulatory compliance:",
        body_style
    ))
    for item in [
        "<b>Maven</b> provides standardized coordinates, dependency resolution, and version management",
        "<b>Nexus</b> provides centralized storage, access control, and APIs",
        "<b>Git + workflows</b> add approval processes and change tracking",
        "<b>Analysis services</b> extract structured obligations, map to CDEs and ISO 20022, and enable gap analysis"
    ]:
        elements.append(Paragraph(f"• {item}", bullet_style))

    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(
        "The foundation (Layer 1) uses open-source tools with zero licensing cost. The value-add (Layer 3) is where "
        "commercial services differentiate. The result is a system that provides single-version-of-truth, automated "
        "dependency resolution, integrity verification, and auditability—benefits that the software industry has relied "
        "upon for decades, now applied to regulatory compliance.",
        body_style
    ))

    # Footer
    elements.append(Spacer(1, 1*cm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=body_style,
        fontSize=8,
        textColor=colors.HexColor('#666'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        f"NYQST Regulatory Intelligence Platform | Document Version 1.0 | {datetime.now().strftime('%B %Y')}",
        footer_style
    ))

    # Build PDF
    doc.build(elements)
    print(f"✓ PDF generated: {pdf_file}")

    import os
    size_kb = os.path.getsize(pdf_file) / 1024
    print(f"✓ Size: {size_kb:.1f} KB")
    print(f"✓ Location: {os.path.abspath(pdf_file)}")

if __name__ == "__main__":
    create_technical_pdf()
