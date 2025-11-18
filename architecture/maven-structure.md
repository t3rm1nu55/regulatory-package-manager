# Maven Structure for Regulatory Documents

## Overview

This document defines how regulatory documents are structured as Maven artifacts, including coordinate systems, versioning strategies, and repository organization.

## Maven Coordinates

### Structure
```
groupId:artifactId:version:type:classifier
```

### Naming Conventions

#### Group IDs
```
{jurisdiction}.{document-type}.{regime}

Examples:
- eu.regulation.emir
- uk.regulation.mifid
- us.regulation.cftc
- global.standard.iso
- org.iosco.principles
- com.nyqst.analysis    # Our proprietary analysis
```

#### Artifact IDs
```
{document-type}-{identifier}

Examples:
- law-648-2012          # EMIR base regulation
- rts-2015-2205         # RTS for Article 9
- schemas-refit         # EMIR REFIT schemas
- validation-rules      # Validation rules
- obligations-extracted # Our analysis output
```

#### Versions
```
Date-based: YYYY.MM.DD
Semantic: major.minor.patch

Examples:
- 2024.01.09           # Consolidated version date
- 3.0-mar2023          # Schema version
- 2024.11.0            # BOM version (year.month.revision)
```

#### Types
```
- pdf     # PDF documents
- xlsx    # Excel files (validation rules)
- xsd     # XML schemas
- zip     # Archive files
- json    # Structured data
- pom     # Bill of Materials
```

#### Classifiers
```
- original      # Original version
- consolidated  # Consolidated with amendments
- en           # English version
- fr           # French version
- structured   # Our structured analysis
```

## Repository Layout

### Physical Structure
```
repository/
├── eu/
│   └── regulation/
│       ├── emir/
│       │   ├── law-648-2012/
│       │   │   ├── 2024.01.09/
│       │   │   │   ├── law-648-2012-2024.01.09.pom
│       │   │   │   ├── law-648-2012-2024.01.09.pdf
│       │   │   │   ├── law-648-2012-2024.01.09.pdf.sha256
│       │   │   │   └── law-648-2012-2024.01.09.pdf.md5
│       │   │   ├── 2023.03.15/
│       │   │   └── maven-metadata.xml
│       │   └── maven-metadata.xml
│       └── emir-bom/
│           ├── 2024.11.0/
│           │   └── emir-bom-2024.11.0.pom
│           └── maven-metadata.xml
```

### Maven Metadata
```xml
<?xml version="1.0" encoding="UTF-8"?>
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
    <lastUpdated>20241118120000</lastUpdated>
  </versioning>
</metadata>
```

## Bill of Materials (BOM) Structure

### BOM POM Example
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>

  <groupId>eu.regulation</groupId>
  <artifactId>emir-bom</artifactId>
  <version>2024.11.0</version>
  <packaging>pom</packaging>

  <name>EMIR Complete Regulatory Package</name>
  <description>Bill of Materials for EU EMIR compliance</description>

  <properties>
    <!-- Version Management -->
    <emir.law.version>2024.01.09</emir.law.version>
    <emir.rts.reporting.version>2023.05.15</emir.rts.reporting.version>
    <emir.its.reporting.version>2023.05.15</emir.its.reporting.version>
    <emir.schemas.version>3.0-mar2023</emir.schemas.version>
    <emir.validation.version>3.0</emir.validation.version>

    <!-- Metadata -->
    <regime.jurisdiction>EU</regime.jurisdiction>
    <regime.name>EMIR</regime.name>
    <regime.scope>OTC derivatives reporting</regime.scope>
  </properties>

  <dependencyManagement>
    <dependencies>
      <!-- Core Law -->
      <dependency>
        <groupId>eu.regulation.emir</groupId>
        <artifactId>law-648-2012</artifactId>
        <version>${emir.law.version}</version>
        <type>pdf</type>
      </dependency>

      <!-- Technical Standards for Article 9 -->
      <dependency>
        <groupId>eu.regulation.emir</groupId>
        <artifactId>rts-2015-2205</artifactId>
        <version>${emir.rts.reporting.version}</version>
        <type>pdf</type>
        <scope>reporting</scope>
      </dependency>

      <dependency>
        <groupId>eu.regulation.emir</groupId>
        <artifactId>its-2015-2447</artifactId>
        <version>${emir.its.reporting.version}</version>
        <type>pdf</type>
        <scope>reporting</scope>
      </dependency>

      <!-- Technical Implementation -->
      <dependency>
        <groupId>eu.regulation.emir</groupId>
        <artifactId>schemas-refit</artifactId>
        <version>${emir.schemas.version}</version>
        <type>zip</type>
        <classifier>xsd</classifier>
        <scope>reporting</scope>
      </dependency>

      <dependency>
        <groupId>eu.regulation.emir</groupId>
        <artifactId>validation-rules</artifactId>
        <version>${emir.validation.version}</version>
        <type>xlsx</type>
        <scope>reporting</scope>
      </dependency>

      <!-- Optional Guidelines -->
      <dependency>
        <groupId>eu.esma.emir</groupId>
        <artifactId>reporting-guidelines</artifactId>
        <version>2023.03</version>
        <type>pdf</type>
        <optional>true</optional>
      </dependency>
    </dependencies>
  </dependencyManagement>
</project>
```

## Dependency Resolution

### Direct Dependencies
```xml
<dependencies>
  <dependency>
    <groupId>eu.regulation</groupId>
    <artifactId>emir-bom</artifactId>
    <version>2024.11.0</version>
    <type>pom</type>
    <scope>import</scope>
  </dependency>
</dependencies>
```

### Transitive Dependencies
```
emir-bom:2024.11.0
├── law-648-2012:2024.01.09
├── rts-2015-2205:2023.05.15
│   └── law-648-2012:2024.01.09 (manages version)
├── its-2015-2447:2023.05.15
│   └── law-648-2012:2024.01.09 (manages version)
├── schemas-refit:3.0-mar2023
│   ├── rts-2015-2205:2023.05.15
│   └── its-2015-2447:2023.05.15
└── validation-rules:3.0
    └── schemas-refit:3.0-mar2023
```

## Versioning Strategy

### Document Versions
1. **Original**: First published version (e.g., 2012.07.04)
2. **Amendments**: Each amendment gets new version (e.g., 2019.06.01)
3. **Consolidated**: Current in-force version (e.g., 2024.01.09)

### BOM Versions
```
YYYY.MM.R

Where:
- YYYY: Year
- MM: Month
- R: Revision within month

Example: 2024.11.0 = November 2024, first revision
```

### Breaking Changes
- Major regulation update → New BOM major version
- Schema incompatibility → New major version
- Field additions only → Minor version

## Repository Types

### Public Repository
- Raw regulatory documents
- Open access
- No authentication

### Premium Repository
- Analyzed documents
- Structured obligations
- Authentication required

### Enterprise Repository
- Client-specific analysis
- Custom BOMs
- Restricted access

## Metadata Extensions

### Custom Properties in POM
```xml
<properties>
  <!-- Regulatory Metadata -->
  <regulation.celex>32012R0648</regulation.celex>
  <regulation.enacted>2012-07-04</regulation.enacted>
  <regulation.effective>2012-08-16</regulation.effective>

  <!-- Coverage Metadata -->
  <coverage.articles>9,11,45</coverage.articles>
  <coverage.scope>reporting,clearing,risk</coverage.scope>

  <!-- Analysis Metadata -->
  <analysis.obligations.count>47</analysis.obligations.count>
  <analysis.cde.fields>142</analysis.cde.fields>
  <analysis.last.updated>2024-11-18</analysis.last.updated>
</properties>
```

## Scoped Dependencies

### Scope Meanings
- **compile**: Always required (base law)
- **runtime**: Required for operation (schemas)
- **provided**: Environment-specific (client rules)
- **test**: Reference only (guidelines)
- **import**: BOM import
- **reporting**: Custom scope for Article 9
- **clearing**: Custom scope for Article 4

## Best Practices

1. **Always specify type**: Even for PDFs
2. **Use classifiers**: For variants (consolidated, en, fr)
3. **Version everything**: Including BOMs
4. **Document scope**: What articles/requirements covered
5. **Include checksums**: SHA-256 for all artifacts
6. **Maintain metadata**: Keep maven-metadata.xml current
7. **Use properties**: For version management in BOMs
8. **Tag releases**: In git when publishing