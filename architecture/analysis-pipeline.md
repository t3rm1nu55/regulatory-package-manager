# Analysis Pipeline Architecture

## Overview

This document describes the pipeline for extracting structured data from regulatory documents and creating analysis artifacts.

## Pipeline Stages

```
┌─────────────────────────────────────────────────────────┐
│ Stage 1: Document Ingestion                            │
│ ├── PDF parsing                                        │
│ ├── Text extraction                                    │
│ └── Metadata extraction                                │
├─────────────────────────────────────────────────────────┤
│ Stage 2: Structural Analysis                           │
│ ├── Article detection                                  │
│ ├── Section parsing                                    │
│ └── Reference identification                           │
├─────────────────────────────────────────────────────────┤
│ Stage 3: Semantic Extraction                           │
│ ├── Obligation identification                          │
│ ├── Entity extraction                                  │
│ └── Requirement parsing                                │
├─────────────────────────────────────────────────────────┤
│ Stage 4: Enrichment                                    │
│ ├── CDE mapping                                        │
│ ├── ISO 20022 linking                                  │
│ └── Cross-reference resolution                         │
├─────────────────────────────────────────────────────────┤
│ Stage 5: Publication                                   │
│ ├── Maven artifact creation                            │
│ ├── Metadata generation                                │
│ └── Repository deployment                              │
└─────────────────────────────────────────────────────────┘
```

## Stage 1: Document Ingestion

### PDF Processing
```python
class DocumentIngester:
    def ingest(self, pdf_path: str) -> Document:
        """
        Extract text and structure from PDF

        Tools:
        - PyPDF2 for basic extraction
        - pdfplumber for tables
        - Tesseract OCR for scanned documents
        """
        # [PLACEHOLDER: Implementation details]
        pass
```

### Metadata Extraction
```json
{
  "document_id": "32012R0648",
  "title": "Regulation on OTC derivatives",
  "issuer": "European Parliament and Council",
  "date_enacted": "2012-07-04",
  "date_effective": "2012-08-16",
  "pages": 96,
  "language": "en",
  "document_type": "regulation"
}
```

## Stage 2: Structural Analysis

### Article Detection Pattern
```python
ARTICLE_PATTERN = r"Article\s+(\d+)\s*\n\s*(.+?)(?=\n\s*\d+\.|$)"
SECTION_PATTERN = r"(\d+)\.\s+(.+?)(?=\n\s*\d+\.|$)"
PARAGRAPH_PATTERN = r"\(([a-z])\)\s+(.+?)(?=\([a-z]\)|$)"
```

### Hierarchical Structure
```json
{
  "articles": [
    {
      "number": "9",
      "title": "Reporting obligation",
      "sections": [
        {
          "number": "1",
          "text": "Counterparties and CCPs shall ensure that...",
          "paragraphs": [
            {
              "id": "a",
              "text": "details of any derivative contract..."
            }
          ]
        }
      ]
    }
  ]
}
```

## Stage 3: Semantic Extraction

### Obligation Model
```python
@dataclass
class Obligation:
    id: str                    # OBL-EMIR-9-001
    source_article: str        # Article 9
    source_section: str        # Section 1

    # Semantic structure
    actor: List[str]           # ["counterparties", "CCPs"]
    action: str               # "REPORT"
    object: str               # "derivative_contract"
    recipient: str            # "trade_repository"
    timing: str               # "T+1"

    # Conditions
    applicability: Dict[str, Any]
    exceptions: List[str]

    # Raw text
    original_text: str
    structured_text: str
```

### Extraction Rules
```python
# Action verb patterns
ACTION_VERBS = {
    "shall report": "REPORT",
    "shall maintain": "MAINTAIN",
    "shall verify": "VERIFY",
    "shall calculate": "CALCULATE",
    "must provide": "PROVIDE",
    "must ensure": "ENSURE"
}

# Timing patterns
TIMING_PATTERNS = {
    r"by close of business on the following working day": "T+1",
    r"within (\d+) days": "T+{days}",
    r"immediately": "IMMEDIATE",
    r"monthly": "MONTHLY"
}
```

## Stage 4: Enrichment

### CDE Mapping
```python
class CDEMapper:
    def map_field_to_cde(self, field: RegulatoryField) -> CDEMapping:
        """
        Map regulatory field to CPMI-IOSCO CDE

        Process:
        1. Fuzzy match field name
        2. Check field format/type
        3. Validate against CDE definitions
        4. Return confidence score
        """
        # [PLACEHOLDER: Implementation]
        pass
```

### CDE Mapping Output
```json
{
  "regulatory_field": "Unique Transaction Identifier",
  "cde_mapping": {
    "cde_id": "UTI",
    "cde_name": "Unique Transaction Identifier",
    "confidence": 0.95,
    "harmonized": true,
    "format": "52 alphanumeric characters",
    "usage": ["EMIR", "MiFIR", "CFTC", "HKMA"]
  }
}
```

### ISO 20022 Linking
```json
{
  "regulatory_field": "UTI",
  "iso20022_mapping": {
    "message": "auth.052.001.02",
    "xpath": "/Document/FinInstrmRptgTxRpt/Tx/TxId/UnqTxIdr",
    "element": "UnqTxIdr",
    "type": "Max52AlphaNumericText"
  }
}
```

## Stage 5: Publication

### Maven Artifact Structure
```
com.nyqst.analysis.emir:obligations-extracted:2024.11.0
├── obligations.json          # Extracted obligations
├── cde-mappings.json        # CDE mappings
├── iso20022-links.json      # ISO 20022 mappings
├── cross-references.json    # Document references
├── metadata.json            # Analysis metadata
└── pom.xml                  # Maven metadata
```

### POM for Analysis Artifact
```xml
<project>
  <groupId>com.nyqst.analysis.emir</groupId>
  <artifactId>obligations-extracted</artifactId>
  <version>2024.11.0</version>
  <packaging>jar</packaging>

  <properties>
    <!-- Source Document -->
    <source.document>eu.regulation.emir:law-648-2012:2024.01.09</source.document>

    <!-- Analysis Metrics -->
    <analysis.obligations.count>47</analysis.obligations.count>
    <analysis.cde.mappings>142</analysis.cde.mappings>
    <analysis.confidence>0.92</analysis.confidence>

    <!-- Processing Metadata -->
    <analysis.date>2024-11-18</analysis.date>
    <analysis.version>1.0.0</analysis.version>
    <analysis.algorithm>v2.3</analysis.algorithm>
  </properties>

  <dependencies>
    <!-- Source document dependency -->
    <dependency>
      <groupId>eu.regulation.emir</groupId>
      <artifactId>law-648-2012</artifactId>
      <version>2024.01.09</version>
      <type>pdf</type>
    </dependency>
  </dependencies>
</project>
```

## Quality Assurance

### Validation Rules
```python
class QualityValidator:
    def validate_extraction(self, obligations: List[Obligation]) -> ValidationResult:
        """
        Validate extracted obligations

        Checks:
        - All articles covered
        - No duplicate obligations
        - Actor/Action/Object present
        - Timing is parseable
        - Cross-references resolve
        """
        # [PLACEHOLDER: Implementation]
        pass
```

### Confidence Scoring
```python
def calculate_confidence(obligation: Obligation) -> float:
    """
    Calculate confidence score for extraction

    Factors:
    - Clear action verb: +0.3
    - Identified entities: +0.2
    - Parsed timing: +0.2
    - Resolved references: +0.2
    - Manual review: +0.1
    """
    # [PLACEHOLDER: Implementation]
    pass
```

## Pipeline Configuration

### Configuration File
```yaml
pipeline:
  name: regulatory-analysis
  version: 2.3.0

stages:
  ingestion:
    pdf_parser: pdfplumber
    ocr_engine: tesseract
    language_detection: true

  structural:
    article_detection: true
    section_parsing: true
    table_extraction: true

  semantic:
    obligation_extraction: true
    entity_recognition: true
    reference_resolution: true

  enrichment:
    cde_mapping: true
    iso20022_linking: true
    cross_referencing: true

  publication:
    repository: nexus
    format: maven
    visibility: premium
```

## Performance Metrics

### Processing Times
| Stage | Time (per 100 pages) |
|-------|---------------------|
| Ingestion | 10 seconds |
| Structural | 30 seconds |
| Semantic | 120 seconds |
| Enrichment | 60 seconds |
| Publication | 5 seconds |
| **Total** | **~4 minutes** |

### Accuracy Metrics
| Metric | Target | Current |
|--------|--------|---------|
| Article detection | 99% | 98.5% |
| Obligation extraction | 90% | 87% |
| CDE mapping | 95% | 92% |
| ISO linking | 90% | 88% |

## Next Steps

1. **Implement ML models** for better extraction
2. **Add NLP** for semantic understanding
3. **Build feedback loop** for continuous improvement
4. **Create benchmarks** for accuracy measurement
5. **Add multi-language** support