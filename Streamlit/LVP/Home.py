import streamlit as st

st.set_page_config(
    page_title="Family History Library - Metadata Cleanup",
    page_icon="assets/Family Search Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App Title and Introduction
st.title("Family History Library Digital Record Metadata Analysis")

st.write("""
The Family History Library is one of the world's largest collections of genealogical records, historical texts, and other resources. Due to the sheer length of time and variety of records involved,
the metadata of these records has grown unwieldy. This application aims to provide a user-friendly interface for analyzing and visualizing the metadata of these records in an effort to help update and standardize them.
""")

# Sections for Points of Focus
st.header("Currently Available Tools")

st.markdown("### 1. Format Comparisons")
st.write("""
Metadata formats can vary widely between sources. Create visualizations to compare standards across various MARC columns. 
Answer questions like: Do records published primarily in English follow a certain pattern of publication date formatting?
""")

st.markdown("### 2. Language Comparison")
st.write("""
Family history records span numerous languages, with each language presenting its own complexities in translation and interpretation.
This tool provides language comparison utilities to detect and standardize terminology across multiple languages, reducing the barriers for multilingual record access.
""")

st.subheader("3. Record Types")
st.write("""
From birth and marriage certificates to census records and immigration documents, the types of records are diverse.
Each record type may contain different sets of metadata, requiring specialized approaches to clean-up.
This tool supports identifying and categorizing records by type, ensuring that metadata fields are standardized accordingly.
""")

# Final Note and Next Steps
st.write("""
---
Through format comparisons, language standardization, and tailored handling of various record types, this app aims to help family history enthusiasts and researchers
enhance the quality of their metadata, making family records more accessible, searchable, and reliable. Explore the features in the sidebar to begin!
""")
