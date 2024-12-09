# Family History Library Catalog Metadata Clean-up

This project involves analyzing and cleaning metadata from the Family History Library Catalog. The goal is to improve data quality, identify inconsistencies, and provide actionable insights to enhance catalog usability.

## Project Overview

### Purpose
The Family History Library Catalog contains metadata with varied formats and structures. This project identifies and addresses inconsistencies, including missing fields, improper formatting, and redundant data.

### Objectives
1. **Identify Issues:** Analyze metadata to uncover missing, inconsistent, or incorrect values.
2. **Clean and Standardize:** Apply rules to format, standardize, and enrich metadata fields.
3. **Generate Insights:** Use visualizations and summaries to showcase trends and results of the clean-up process.

## Methodology

### Steps
1. **Data Extraction:** Metadata was imported from various files in `.xlsx` and `.csv` formats.
2. **Data Exploration:** Key fields such as language, publication location, publisher name, and publication date were examined for inconsistencies.
3. **Data Cleaning:** 
   - Removed special characters and unnecessary formatting.
   - Standardized naming conventions and date formats.
   - Identified and addressed missing or null values.
4. **Visualization and Analysis:** Used tools like Seaborn and Matplotlib for trend analysis and reporting.

### Tools and Technologies
- **Python Libraries:**
  - Polars for data manipulation.
  - Pandas for processing and cleaning.
  - Matplotlib and Seaborn for data visualization.
- **File Formats:**
  - `.xlsx` for raw metadata files.
  - `.csv` for combined and processed datasets.

## Results

- Cleaned metadata with consistent formats and reduced redundancy.
- Visualizations highlight key patterns and areas needing attention.
- Enhanced metadata quality for better usability in the catalog.

## Team Members
- Talon Hintze
- Sam Anderson
- Karen Castillo
- Dali Li
- Z

---

### How to Use
1. Load the cleaned metadata file for analysis or integration.
2. Use the included scripts to further refine or analyze new datasets.
