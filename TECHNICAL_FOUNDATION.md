# Regulatory Package Management: Technical Foundation

**A pragmatic approach to applying software dependency management patterns to regulatory documents**

---

## 1. How Regulatory Documents Are Currently Stored by Regulators

### European Union (EUR-Lex)

The EU publishes all legislation through EUR-Lex (https://eur-lex.europa.eu/), a free online repository. Each document receives a CELEX number (e.g., 32012R0648 for EMIR). Documents are available in:

- **Original versions**: As first published in the Official Journal
- **Consolidated versions**: Incorporating all amendments up to a specific date
- **Multiple formats**: PDF, HTML, XML (Formex format)
- **All EU languages**: 24 official languages

**Current state:**
- Documents are freely downloadable
- Consolidated versions are manually curated by EUR-Lex staff
- No structured dependency information (you must manually know that RTS 2015/2205 implements Article 9 of Regulation 648/2012)
- No checksums or version hashes for integrity verification
- Users must track "consolidated as of date" manually

### United Kingdom (FCA Handbook, Legislation.gov.uk)

The UK maintains two primary sources:

**Legislation.gov.uk** for primary and secondary legislation:
- Acts of Parliament and Statutory Instruments
- Point-in-time versions showing law as it stood on specific dates
- HTML and PDF formats
- Manual navigation between amendments

**FCA Handbook** (https://www.handbook.fca.org.uk/):
- Rulebook organized by topic
- "In force" vs "historic" versions
- No structured linking between related rules
- PDF downloads available but not versioned systematically

### United States (Federal Register, Code of Federal Regulations)

**Federal Register** (https://www.federalregister.gov/):
- Daily publication of proposed and final rules
- Individual rule documents
- No consolidated view of current law

**Code of Federal Regulations** (CFR):
- Codified version updated annually
- 50 titles organized by subject
- E-CFR provides unofficial daily updates
- No dependency tracking between related rules

### Technical Standards (ESMA, EBA, EIOPA)

European Supervisory Authorities publish:
- **Regulatory Technical Standards (RTS)**: Delegated acts with legal force
- **Implementing Technical Standards (ITS)**: Implementation details
- **Guidelines and Recommendations**: Non-binding interpretations
- **Schemas and Validation Rules**: Technical implementation artifacts (XSD, Excel files)

**Current state:**
- Published on authority websites (ESMA, EBA, EIOPA)
- No central registry
- Schemas often in ZIP files with version numbers in filenames
- No structured linking between RTS and parent regulation
- Validation rules distributed as Excel files with manual version tracking

### ISO 20022 and Industry Standards

ISO 20022 message standards:
- Managed by ISO (paid access) and SWIFT (MyStandards)
- Multiple versions (e.g., auth.052.001.02)
- XSD schemas with dependencies
- No automated dependency resolution
- Mapping between regulatory requirements and message fields is manual

---

## 2. The Problem: Document Management Waste

### The Seven Wastes (Kaizen) Applied to Regulatory Document Management

Drawing from lean manufacturing's concept of "muda" (waste), we can identify analogous wastes in regulatory document management:

#### 2.1 Transport (Unnecessary Movement)
- Downloading the same PDF from EUR-Lex hundreds of times across an organization
- Manually copying schemas from ESMA website to local development environments
- Email chains distributing "the latest version" of validation rules
- Consultants re-downloading documents they already have because they don't know which version they previously used

#### 2.2 Inventory (Excess Storage)
- Multiple copies of the same regulation stored in different folders, SharePoint sites, network drives
- Unknown whether copies are identical or have been annotated/modified
- No centralized inventory of what documents the organization possesses
- Duplicate storage costs across teams

#### 2.3 Motion (Unnecessary Work)
- Manually checking EUR-Lex for updates ("Is there a new consolidated version?")
- Reading through amendment documents to understand what changed
- Reconciling version numbers between different document types (law vs. schemas vs. validation rules)
- Searching across multiple regulator websites to assemble complete picture

#### 2.4 Waiting (Delays)
- Waiting for legal team to confirm "which version applies on date X"
- Delayed project starts because team is assembling regulatory requirements
- Blocked development waiting for schemas to be downloaded and validated
- Compliance reviews delayed while gathering correct document versions

#### 2.5 Overproduction (Doing More Than Required)
- Creating internal summaries of regulations that already exist elsewhere
- Building custom parsers for each regulatory regime
- Every consulting firm re-analyzing the same EMIR Article 9 obligations
- RegTech vendors duplicating extraction work across competitors

#### 2.6 Over-processing (Unnecessary Steps)
- Manual verification that downloaded PDF matches official version
- Comparing file sizes and dates to determine if update is needed
- Reading entire regulation to find specific article when structured access would suffice
- Converting between formats (PDF → Word → Excel) for analysis

#### 2.7 Defects (Errors and Rework)
- **Using outdated regulations**: Most serious risk—basing implementation on superseded version
- Incorrect consolidation: Applying amendments out of order or missing amendments
- Broken references: Internal links that reference "Article 9" without specifying which document
- Schema mismatches: Using validation rules version 2.0 with schemas version 3.0
- Compliance failures discovered in audit when version discrepancy found

### The Single Version of Truth Problem

**Scenario**: A trading firm must implement EMIR reporting obligations as of January 2024.

**Questions with no easy answers:**
1. Which consolidated version of Regulation 648/2012 is in force on 2024-01-09?
2. Which version of RTS 2015/2205 applies to that base regulation?
3. Do the REFIT schemas (version 3.0, March 2023) match the current RTS?
4. Are the ESMA validation rules (version 3.0) compatible with those schemas?
5. Have any of these been superseded between download date and implementation date?

**Current solution**: Manual tracking in spreadsheets, document metadata, or institutional knowledge.

**Risk**: Using EUR-Lex consolidated version dated 2024-01-09 with ESMA schemas dated 2023-03-15 and validation rules version 2.0 creates undefined behavior. No automated way to verify compatibility.

### Audit Trail and Provenance

**Compliance question**: "Which version of the regulation did you use for this transaction?"

**Current answer methodology:**
- Check file properties for download date
- Search email for "sent from legal on DD/MM/YYYY"
- Rely on developer memory
- Reference issue tracker: "JIRA-1234 implemented using regs from Q2 2023"

**Absent:**
- Cryptographic proof of document integrity (SHA-256 hash)
- Structured metadata recording source URL and download timestamp
- Dependency tree showing which RTS/ITS versions were used together
- Automated detection of "this code was built against outdated regulations"

### Knowledge Waste and Duplication

Every financial institution performs similar analysis:
1. Download EMIR package (law + RTS + ITS + schemas + validation rules)
2. Extract obligations from Article 9
3. Map fields to ISO 20022 message elements
4. Identify Critical Data Elements (CDEs) per CPMI-IOSCO standards
5. Build internal taxonomy

**This analysis is duplicated:**
- Across 100+ banks globally
- Across 20+ RegTech vendors
- Across consulting firms supporting multiple clients
- Results are not shared (competitive advantage, or simply no mechanism exists)

**Result**: The same regulatory text is analyzed thousands of times, with slight variations in interpretation, no shared learning, and no network effects.

---

## 3. Why Treating Regulatory Documents as Code Enables 30 Years of Learned Benefits

### The Software Dependency Problem (Solved in 1990s-2000s)

Before package managers, software development faced identical problems:

**Pre-Maven/NPM/pip era:**
- Developers manually downloaded library JAR files from project websites
- No standard way to declare "I need library X version 2.3"
- Dependency conflicts: Library A needs XML parser v1.0, Library B needs v2.0
- No automated verification: "Did I get the correct file from a trusted source?"
- "Works on my machine" syndrome: Different developers had different library versions

**Post-package manager:**
- Declare dependencies in manifest file (pom.xml, package.json, requirements.txt)
- Package manager resolves transitive dependencies automatically
- Checksums verify integrity
- Version ranges allow compatible updates: "any 2.x version"
- Reproducible builds: Same inputs produce identical outputs

### Direct Parallels to Regulatory Documents

| Software Development | Regulatory Compliance |
|---------------------|----------------------|
| Library JAR file | Regulation PDF/XSD |
| Library version (e.g., 2.3.1) | Consolidated version date (e.g., 2024.01.09) |
| Dependency: "Needs library X" | Dependency: "RTS implements Article 9" |
| Transitive dependencies | Schema needs RTS needs base law |
| SHA-256 checksum | (Currently absent) |
| Maven Central repository | (Currently absent - our proposal) |
| pom.xml dependency declaration | (Currently manual) |
| `mvn install` downloads all needed files | (Currently manual downloads) |
| Version conflict detection | (Currently undetected) |

### Lessons from 30 Years of Package Management

#### Lesson 1: Namespacing Prevents Collisions

**Software**: Java package naming convention `com.company.project.module` ensures globally unique names.

**Regulatory**: Currently ambiguous references like "Article 9" could mean:
- EMIR Regulation 648/2012, Article 9
- MiFIR Regulation 600/2014, Article 9
- SFTR Regulation 2015/2365, Article 9

**Solution**: Structured coordinates `eu.regulation.emir:law-648-2012:article-9` are unambiguous.

#### Lesson 2: Semantic Versioning Communicates Intent

**Software**: Version 2.3.1 tells you:
- Major version 2: Breaking changes from v1
- Minor version 3: New features, backward compatible
- Patch version 1: Bug fixes only

**Regulatory**: Date-based versioning (2024.01.09) tells you consolidation date, but not:
- Is this a minor clarification or major restructuring?
- Are schemas backward compatible?
- Can I safely upgrade from 2023.03.15 version?

**Hybrid approach**: Combine date for law (2024.01.09) with semantic versioning for technical artifacts (schemas-3.0-mar2023 where major version 3 indicates breaking change from v2).

#### Lesson 3: Dependency Resolution Prevents Conflicts

**Software**: Maven's dependency mediation algorithm selects compatible versions when conflicts arise.

**Regulatory**: If RTS 2015/2205 (v2023.05.15) depends on EMIR (v2024.01.09), but schemas (v3.0-mar2023) were built against EMIR (v2023.03.15), potential incompatibility exists.

**Solution**: Dependency graph where RTS declares `<dependency>law-648-2012:2023.03.15</dependency>` and dependency manager ensures compatibility.

#### Lesson 4: Checksums Ensure Integrity

**Software**: Every artifact in Maven Central has SHA-1 and MD5 checksums. Download corruption or tampering is detected immediately.

**Regulatory**: If you download EMIR PDF from EUR-Lex, you trust:
- DNS wasn't hijacked
- TLS certificate is valid
- EUR-Lex server wasn't compromised
- File wasn't corrupted in transit

But you have no checksum to verify against. If someone emails you "EMIR_consolidated_2024.pdf", you cannot verify it's authentic.

**Solution**: Publish SHA-256 hash: `law-648-2012-2024.01.09.pdf.sha256` allows verification.

#### Lesson 5: Bill of Materials (BOM) Manages Complexity

**Software**: Spring Boot BOM declares 100+ libraries with tested compatible versions. Developers import BOM and automatically get compatible ecosystem.

**Regulatory**: EMIR compliance requires:
- Base law 648/2012
- Commission Delegated Regulation 2015/2205 (RTS for Article 9)
- Commission Implementing Regulation 2015/2447 (ITS for Article 9)
- ESMA schemas version 3.0
- ESMA validation rules version 3.0
- Potentially ISO 20022 message definitions

**Solution**: BOM defines tested combination:
```xml
<dependencyManagement>
  <dependencies>
    <dependency>law-648-2012:2024.01.09</dependency>
    <dependency>rts-2015-2205:2023.05.15</dependency>
    <dependency>its-2015-2447:2023.05.15</dependency>
    <dependency>schemas-refit:3.0-mar2023</dependency>
    <dependency>validation-rules:3.0</dependency>
  </dependencies>
</dependencyManagement>
```

User requests `emir-bom:2024.11.0` and receives all compatible components.

#### Lesson 6: Reproducibility Enables Auditability

**Software**: Maven guarantees same pom.xml produces same build six months later (assuming artifacts remain available).

**Regulatory**: "Reproduce the compliance implementation from Q2 2023" requires knowing exact versions used. Currently tracked manually; with package management, `pom.xml` from Q2 2023 provides complete specification.

**Audit answer**: "We used emir-bom:2023.06.0 which resolved to law-648-2012:2023.03.15, rts-2015-2205:2022.11.30, schemas-refit:2.0..."

---

## 4. Maven Explainer

### What is Maven?

Apache Maven is a build automation and dependency management tool for Java projects, created in 2003. While initially designed for software builds, its dependency management concepts are applicable to any versioned artifacts.

### Core Concepts

#### 4.1 Coordinates (GAV)

Every artifact is uniquely identified by:

```
groupId : artifactId : version
```

**Example (software library):**
```
org.apache.commons : commons-lang3 : 3.12.0
```

- **groupId**: Reverse domain name ensuring global uniqueness
- **artifactId**: Specific library name
- **version**: Version number

**Example (adapted for regulations):**
```
eu.regulation.emir : law-648-2012 : 2024.01.09
```

- **groupId**: Jurisdiction + document type + regime
- **artifactId**: Specific law/regulation identifier
- **version**: Consolidated version date

#### 4.2 Optional Qualifiers

Full coordinates can include:

```
groupId : artifactId : version : type : classifier
```

- **type**: File format (pdf, xsd, xlsx, zip)
- **classifier**: Variant (en, fr, consolidated, original)

**Example:**
```
eu.regulation.emir : law-648-2012 : 2024.01.09 : pdf : en-consolidated
```

#### 4.3 POM (Project Object Model)

XML file describing artifact and its dependencies:

```xml
<project>
  <groupId>eu.regulation.emir</groupId>
  <artifactId>rts-2015-2205</artifactId>
  <version>2023.05.15</version>
  <packaging>pdf</packaging>

  <dependencies>
    <!-- This RTS implements Article 9 of base regulation -->
    <dependency>
      <groupId>eu.regulation.emir</groupId>
      <artifactId>law-648-2012</artifactId>
      <version>2024.01.09</version>
      <type>pdf</type>
    </dependency>
  </dependencies>
</project>
```

This POM declares: "RTS 2015/2205 (version 2023.05.15) depends on EMIR base law (version 2024.01.09)."

#### 4.4 Dependency Resolution

When you declare dependency on an artifact, Maven:

1. Downloads the POM file
2. Reads its dependencies
3. Recursively downloads those dependencies (transitive dependencies)
4. Detects conflicts (if multiple versions of same artifact needed)
5. Applies mediation strategy to select one version
6. Verifies checksums
7. Stores in local repository cache

**User experience:**
```bash
mvn dependency:get -Dartifact=eu.regulation:emir-bom:2024.11.0
```

Maven automatically retrieves:
- emir-bom POM
- All artifacts listed in BOM
- All transitive dependencies
- Verifies SHA-256 checksums
- Stores locally in `~/.m2/repository/`

#### 4.5 Repository Structure

Physical directory layout:

```
repository/
└── eu/
    └── regulation/
        └── emir/
            └── law-648-2012/
                ├── 2024.01.09/
                │   ├── law-648-2012-2024.01.09.pom
                │   ├── law-648-2012-2024.01.09.pdf
                │   ├── law-648-2012-2024.01.09.pdf.sha256
                │   └── law-648-2012-2024.01.09.pdf.md5
                ├── 2023.03.15/
                │   └── ...
                └── maven-metadata.xml
```

`maven-metadata.xml` lists all available versions:

```xml
<metadata>
  <groupId>eu.regulation.emir</groupId>
  <artifactId>law-648-2012</artifactId>
  <versioning>
    <latest>2024.01.09</latest>
    <release>2024.01.09</release>
    <versions>
      <version>2012.07.04</version>
      <version>2023.03.15</version>
      <version>2024.01.09</version>
    </versions>
  </versioning>
</metadata>
```

### What Maven Provides

1. **Standardized coordinates**: Globally unique artifact identification
2. **Transitive dependency resolution**: Automatically fetch what you need
3. **Checksum verification**: Integrity guarantees
4. **Version management**: Track available versions, identify latest
5. **Local caching**: Download once, reuse across projects
6. **Conflict detection**: Identify incompatible version requirements
7. **Mature tooling**: 20+ years of ecosystem development

### What Maven Doesn't Provide

1. **Content analysis**: Maven doesn't understand PDFs or extract obligations
2. **Semantic understanding**: No knowledge that "Article 9" relates to reporting
3. **Change tracking**: Doesn't detect what changed between versions
4. **Workflow**: No approval process, check-in/check-out, branching
5. **Rich metadata**: POM properties are flat key-value pairs
6. **Search**: Basic artifact search only, not full-text content search

---

## 5. Nexus Repository Manager Explainer

### What is Nexus?

Sonatype Nexus Repository Manager is a repository server for storing and managing binary artifacts. It acts as a central hub for Maven artifacts (and other package formats: npm, PyPI, Docker, etc.).

**Two editions:**
- **Nexus Repository OSS**: Free, open-source (Eclipse Public License)
- **Nexus Repository Pro**: Commercial, adds security scanning and advanced features

### Core Functions

#### 5.1 Artifact Storage

Nexus stores artifacts in Maven repository format with:
- Directory structure following Maven conventions
- Automatic checksum generation (SHA-256, SHA-1, MD5)
- Metadata management (maven-metadata.xml)
- Search indexing

#### 5.2 Repository Types

**Hosted repositories**: Store your own artifacts
- Example: `nyqst-regulatory-public` for freely available regulations
- Example: `nyqst-regulatory-premium` for analyzed documents (auth required)

**Proxy repositories**: Cache artifacts from remote repositories
- Example: Proxy to Maven Central, cache locally for faster access
- Reduce bandwidth and improve reliability

**Group repositories**: Combine multiple repositories
- Example: Group that includes hosted + proxy repositories
- Clients query one URL, Nexus searches all backing repositories

#### 5.3 Access Control

Nexus provides role-based access control (RBAC):
- **Anonymous read**: Public regulatory documents freely downloadable
- **Authenticated read**: Premium analysis requires login
- **Deploy permissions**: Only authorized users can publish artifacts
- **Repository-level security**: Different access rules per repository

#### 5.4 REST API

Nexus exposes REST API for:
- Searching artifacts
- Retrieving metadata
- Uploading artifacts
- Managing repositories

**Example search:**
```bash
curl "http://nexus.nyqst.com/service/rest/v1/search?name=emir"
```

Returns JSON listing all artifacts with "emir" in coordinates.

#### 5.5 Web UI

Browser-based interface for:
- Browsing repository contents
- Searching artifacts
- Downloading files
- Viewing artifact details and dependencies
- Uploading new artifacts (if authorized)

### Infrastructure Requirements

**Nexus Repository OSS:**
- **Cost**: Free (open-source)
- **Server requirements**:
  - Minimum: 4 CPU cores, 8GB RAM
  - Recommended: 8 CPU cores, 16GB RAM for production
- **Storage**: Depends on repository size (estimate 1-10GB per regulatory regime including all versions)
- **Deployment**:
  - Can run on single server
  - Docker container available
  - Cloud-native (AWS, Azure, GCP)

**Typical setup:**
- AWS EC2 t3.large instance: ~$60/month
- 1TB EBS storage: ~$100/month
- Data transfer: Varies with usage
- **Total estimate**: $200-500/month for production deployment

Alternatively, Sonatype offers hosted Nexus Repository Pro (pricing varies).

### What Nexus Provides

1. **HTTP/HTTPS access**: Web-based artifact retrieval
2. **Storage management**: Artifact retention policies, cleanup tasks
3. **Caching**: Proxy repositories improve performance
4. **Security**: Authentication, authorization, TLS
5. **APIs**: Programmatic access for automation
6. **Web UI**: Human-friendly browsing and management
7. **High availability**: Clustering support (Pro edition)

### What Nexus Doesn't Provide

1. **Git workflow**: No branching, pull requests, or code review
2. **Document processing**: Doesn't parse PDFs or extract content
3. **Analysis**: No understanding of regulatory semantics
4. **Notifications**: Basic webhooks only, not "alert when EMIR updated"
5. **Gap analysis**: No concept of entity profile or compliance requirements

---

## 6. NYQST Regulatory Package Manager: System Design

### Architecture Overview

NYQST Regulatory Package Manager builds three layers on top of Nexus + Maven:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Intelligence Services (Premium/Enterprise)       │
│  ┌────────────┬──────────────┬─────────────┬──────────────┐│
│  │ Obligation │ CDE Mapping  │ Gap         │ Impact       ││
│  │ Extraction │              │ Analysis    │ Assessment   ││
│  └────────────┴──────────────┴─────────────┴──────────────┘│
├─────────────────────────────────────────────────────────────┤
│  Layer 2: Document Management & Workflow                    │
│  ┌────────────┬──────────────┬─────────────┬──────────────┐│
│  │ Git        │ Change       │ Update      │ MCP Server / ││
│  │ Workflow   │ Detection    │ Monitor     │ API          ││
│  └────────────┴──────────────┴─────────────┴──────────────┘│
├─────────────────────────────────────────────────────────────┤
│  Layer 1: Package Management (Nexus + Maven)                │
│  ┌────────────┬──────────────┬─────────────┬──────────────┐│
│  │ Maven      │ Nexus        │ Artifact    │ Dependency   ││
│  │ Coordinates│ Repository   │ Storage     │ Resolution   ││
│  └────────────┴──────────────┴─────────────┴──────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Package Management Foundation

**Uses Maven + Nexus as-is**, applying their patterns to regulatory documents:

**Artifact types:**
- **Laws/Regulations**: PDFs with Maven coordinates
- **Technical Standards**: RTS/ITS as PDF artifacts with dependencies on parent law
- **Schemas**: XSD files in ZIP artifacts
- **Validation Rules**: Excel files as artifacts
- **BOMs**: POM-only artifacts that group related documents

**Repository structure:**
- **Public hosted repository**: Freely available regulatory documents
  - Source: Downloaded from EUR-Lex, FCA Handbook, etc.
  - Access: Anonymous read access
  - Publishing: Controlled via authentication

- **Premium hosted repository**: Analyzed documents (structured obligations, mappings)
  - Access: Authenticated users only
  - Billing integration

**Example workflow:**
1. Monitor EUR-Lex for new EMIR consolidated version
2. Download PDF, verify against EUR-Lex checksum (if available)
3. Generate Maven coordinates: `eu.regulation.emir:law-648-2012:2024.01.09:pdf:en-consolidated`
4. Create POM declaring metadata and dependencies
5. Compute SHA-256 checksum
6. Deploy to Nexus using Maven deploy plugin
7. Update EMIR BOM to reference new version

**Client usage:**
```bash
# Install EMIR complete package
mvn dependency:get -Dartifact=eu.regulation:emir-bom:2024.11.0

# Downloads to ~/.m2/repository/eu/regulation/emir-bom/2024.11.0/
# Automatically fetches all dependencies listed in BOM
```

### Layer 2: Document Management & Workflow

**Git integration** for document lifecycle:

**Repository structure:**
```
regulatory-documents/
├── eu/
│   └── regulation/
│       └── emir/
│           └── law-648-2012/
│               ├── 2024.01.09/
│               │   ├── source.pdf
│               │   ├── pom.xml
│               │   ├── metadata.json
│               │   └── README.md
│               └── ...
└── maven-metadata.xml
```

**Workflow:**
1. **Check-in**: Team member adds new regulatory document to Git
2. **Pull request**: Changes reviewed by compliance team
3. **Approval**: Legal sign-off required before merge
4. **CI/CD pipeline**:
   - Validates POM structure
   - Computes checksums
   - Runs quality checks
   - Deploys to Nexus if tests pass
5. **Git tag**: Release tagged (e.g., `emir-bom-2024.11.0`)

**Change detection:**
- Monitor regulator websites for updates (RSS feeds, web scraping, APIs where available)
- Compare checksums with existing versions
- Generate change reports: "EMIR consolidated version updated from 2023.03.15 to 2024.01.09"
- Notify subscribers via webhook/email

**Update monitoring service:**
- Periodic checks of EUR-Lex, FCA Handbook, Federal Register
- Detect new publications matching subscribed regimes
- Queue for review and ingestion
- Alert clients: "New version available for regimes in your profile"

**MCP Server (Model Context Protocol):**
- LLM agents can query regulatory repository
- Ask: "What is the latest EMIR consolidated version?"
- Retrieve: "Download EMIR Article 9 obligations"
- Analyze: "What changed between versions 2023.03.15 and 2024.01.09?"

**REST API:**
```
GET /api/v1/regimes/emir/versions
GET /api/v1/regimes/emir/latest
GET /api/v1/bom/emir-bom/2024.11.0
GET /api/v1/search?q=article+9+reporting
POST /api/v1/gap-analysis (with entity profile)
```

### Layer 3: Intelligence Services

**This layer is where NYQST adds commercial value** beyond free document hosting.

#### 3.1 Document Ingestion & Parsing

**PDF processing:**
- Extract text with layout preservation (pdfplumber)
- OCR for scanned documents (Tesseract)
- Identify document structure (articles, sections, paragraphs)
- Extract tables (validation rules, field definitions)

**Metadata enrichment:**
- Parse CELEX numbers, regulation identifiers
- Extract effective dates, amendment references
- Identify cross-references to other documents
- Tag language, jurisdiction, regime

#### 3.2 Obligation Extraction

**Structured analysis:**
- Identify normative language: "shall", "must", "required to"
- Parse obligation components:
  - **Actor**: Who must comply (counterparties, CCPs, trading venues)
  - **Action**: What must be done (report, maintain, verify, calculate)
  - **Object**: What is acted upon (derivative contract, collateral, margin)
  - **Recipient**: To whom (trade repository, competent authority)
  - **Timing**: When (T+1, monthly, immediately upon occurrence)
  - **Conditions**: Under what circumstances (if notional exceeds threshold)

**Example extraction from EMIR Article 9:**

```json
{
  "id": "OBL-EMIR-9-1-a",
  "source": {
    "regulation": "eu.regulation.emir:law-648-2012:2024.01.09",
    "article": "9",
    "section": "1",
    "paragraph": "a"
  },
  "obligation": {
    "actors": ["counterparties", "CCPs"],
    "action": "REPORT",
    "object": "details of derivative contract",
    "recipient": "trade repository",
    "timing": "T+1 working day",
    "conditions": {
      "contract_type": "OTC derivative",
      "event": "conclusion, modification, termination"
    }
  },
  "original_text": "Counterparties and CCPs shall ensure that the details of any derivative contract they have concluded and of any modification or termination of the contract are reported to a trade repository registered in accordance with Article 55 or recognised in accordance with Article 77. The details shall be reported no later than the working day following the conclusion, modification or termination of the contract.",
  "confidence": 0.95
}
```

**Output:** Structured obligations published as Maven artifact:
```
com.nyqst.analysis.emir:obligations-extracted:2024.11.0:json
```

With dependency on source document:
```xml
<dependency>
  <groupId>eu.regulation.emir</groupId>
  <artifactId>law-648-2012</artifactId>
  <version>2024.01.09</version>
</dependency>
```

#### 3.3 CDE (Critical Data Element) Mapping

CPMI-IOSCO defines harmonized data elements for derivatives reporting. Map regulatory fields to CDEs:

```json
{
  "regulatory_field": "Unique Transaction Identifier",
  "source": "EMIR RTS Article 3, Table 2, Field 1",
  "cde_mapping": {
    "cde_id": "UTI",
    "cde_name": "Unique Transaction Identifier",
    "cde_format": "ISO 23897 (52 alphanumeric)",
    "harmonized": true,
    "used_in_regimes": ["EMIR", "MiFIR", "SFTR", "CFTC", "MAS", "HKMA", "ASIC"],
    "confidence": 0.99
  }
}
```

**Output:** CDE mappings as artifact:
```
com.nyqst.analysis.emir:cde-mappings:2024.11.0:json
```

#### 3.4 ISO 20022 Integration

Link regulatory fields to ISO 20022 message elements:

```json
{
  "regulatory_field": "UTI",
  "iso20022_mapping": {
    "message": "auth.052.001.02",
    "message_name": "DerivativesTradeReportV02",
    "xpath": "/Document/FinInstrmRptgTxRpt/Tx/TxId/UnqTxIdr",
    "element": "UnqTxIdr",
    "data_type": "Max52Text",
    "occurrence": "1..1"
  }
}
```

#### 3.5 Gap Analysis

**Input:** Entity profile
```json
{
  "entity": {
    "jurisdiction": "UK",
    "entity_type": "investment_firm",
    "activities": ["execution", "portfolio_management"],
    "products": ["equities", "derivatives"],
    "aum_gbp": 10000000000
  }
}
```

**Process:**
1. Query canonical obligation model for applicable regimes
2. Filter obligations by entity profile
3. Check installed packages: `GET /api/v1/client/{id}/installed-packages`
4. Compute gaps: Required documents - Installed documents
5. Prioritize: Critical (must have), Recommended (should have), Optional (nice to have)

**Output:**
```json
{
  "coverage": {
    "total_documents_required": 120,
    "installed": 87,
    "missing": 33,
    "coverage_percentage": 72.5
  },
  "gaps": {
    "critical": [
      {
        "artifact": "uk.regulation.emir:validation-rules:3.0",
        "reason": "Required for transaction reporting submission validation",
        "remediation": "mvn dependency:get -Dartifact=uk.regulation.emir:validation-rules:3.0"
      }
    ],
    "recommended": [...],
    "optional": [...]
  }
}
```

### Technology Stack

**Core infrastructure:**
- **Nexus Repository OSS**: Artifact storage and retrieval
- **Maven**: Dependency management (client-side tooling)
- **Git**: Version control for documents and metadata
- **PostgreSQL**: Metadata database (document properties, user accounts, subscriptions)

**Analysis pipeline:**
- **Python**: PDF processing, text extraction, NLP
- **Neo4j**: Graph database for relationships (document→obligation→CDE→ISO)
- **PyPDF2 / pdfplumber**: PDF parsing
- **spaCy / NLTK**: Natural language processing

**Integration layer:**
- **FastAPI**: REST API server
- **Model Context Protocol Server**: LLM agent integration
- **Webhooks**: Event notifications

**Client tools:**
- **Maven CLI**: Standard Maven commands for artifact retrieval
- **Custom CLI**: `nyqst-reg` wrapper providing enhanced commands
- **Web dashboard**: Browse, search, analyze

### Access Tiers

**Public (Free):**
- Access: Anonymous
- Content: Raw regulatory documents (PDFs, XSDs) from public sources
- Features: Basic Maven repository, version tracking, checksums
- Revenue: Lead generation

**Premium (Subscription):**
- Access: Authenticated users
- Content: Public documents + structured obligations + CDE mappings + ISO 20022 links
- Features: API access, gap analysis, update notifications, dashboard
- Revenue: Primary subscription revenue

**Enterprise (Custom):**
- Access: Authenticated with SLA
- Content: Premium + client-specific analysis + custom BOMs
- Features: Dedicated support, custom integrations, priority updates
- Revenue: High-margin custom services

### Open Questions and Challenges

1. **Legal status**: Are we republishing copyrighted materials, or simply organizing links to official sources?
   - Mitigation: Link to EUR-Lex for download, store locally for analysis but require clients to fetch from official source

2. **Verification**: How do we verify our Maven artifact matches official EUR-Lex version?
   - Solution: Publish checksums; encourage regulators to publish official checksums

3. **Amendment tracking**: EUR-Lex consolidation may lag; how to handle gap between amendment publication and consolidated version?
   - Solution: Store both "original + amendments" and "consolidated"; clearly mark which is used

4. **Jurisdiction expansion**: Extending beyond EU to US, APAC requires understanding each regulator's publication model
   - Approach: Start narrow (EU + UK), expand systematically

5. **Schema evolution**: What if ESMA updates schemas incompatibly?
   - Solution: Semantic versioning (major version bump) + BOM declares compatible combination

6. **Commercial licensing**: If we extract obligations and sell access, what are IP implications?
   - Consult legal counsel on copyright vs. database rights vs. factual information

---

## Conclusion

Regulatory document management suffers from wastes analogous to pre-automation manufacturing: unnecessary movement, excess inventory, waiting, and defects. The software development industry solved an isomorphic problem (library dependency management) 20+ years ago through package managers like Maven and repository servers like Nexus.

NYQST Regulatory Package Manager applies these proven patterns to regulatory compliance:
- **Maven** provides standardized coordinates, dependency resolution, and version management
- **Nexus** provides centralized storage, access control, and APIs
- **Git + workflows** add approval processes and change tracking
- **Analysis services** extract structured obligations, map to CDEs and ISO 20022, and enable gap analysis

The foundation (Layer 1) uses open-source tools with zero licensing cost. The value-add (Layer 3) is where commercial services differentiate. The result is a system that provides single-version-of-truth, automated dependency resolution, integrity verification, and auditability—benefits that the software industry has relied upon for decades, now applied to regulatory compliance.

---

**Document Version**: 1.0
**Date**: November 2024
**Status**: Technical Foundation Document
