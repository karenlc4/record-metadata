#%% Imports and functions
import streamlit as st
import polars as pl
import pandas as pd
import altair as alt
import re
import numpy as np
import matplotlib.pyplot as plt
from marc_bibliography_mapping import marc_field_mapping_bibliographic_flat

if "df" not in st.session_state:
    st.session_state["df"] = None

def remove_non_special_chars(series: pl.Series) -> pl.Series:
    # Define the regex pattern to keep only the specified special characters
    pattern = r"[^@_!#$%^&*()<>?/\|}{~:.]"
    
    # Apply the regex pattern to the series, replacing everything except special characters
    return series.str.replace_all(pattern, "")

def remove_digits(series: pl.Series) -> pl.Series:
    # Define the regex pattern for numbers (digits 0-9)
    pattern = r"\d"
    
    # Apply the regex pattern to the series, replacing numbers with an empty string
    return series.str.replace_all(pattern, "")

def drop_columns_that_are_all_null(_df: pl.DataFrame) -> pl.DataFrame:
    return _df[[s.name for s in _df if not (s.null_count() == _df.height)]]

def process_and_combine_files(file_names: list) -> pl.DataFrame:

    # Read and cast all uploaded files to String type
    dataframes = [pl.read_csv(file_name).cast(pl.String) for file_name in file_names]
    
    # Combine all DataFrames vertically
    combined = pl.concat(dataframes, how="vertical")
    
    # Cast '001' column to Int64 type
    combined = combined.with_columns(pl.col("001").cast(pl.Int64))
    
    # Rename columns using the mapping
    combined = combined.rename({tag: marc_field_mapping_bibliographic_flat.get(tag, tag) for tag in combined.columns})
    
    # Drop columns that are all null
    combined_new = drop_columns_that_are_all_null(combined)

    return combined_new

def validate_column_format(column_data):
    """
    Validate whether the column matches the expected format.
    Criteria:
    - Missing values allowed.
    - Patterns such as 'YYYY', 'YYYY-YYYY', or 'Other' formats only.

    Returns:
    - True if valid, False otherwise.
    """
    pattern_valid = column_data.drop_nulls().map_elements(
        lambda x: bool(re.match(r'^\d{4}$|^\d{4}-\d{4}$', x))
    ).all()
    return pattern_valid

def categorize_date_pattern(date: str) -> str:
    if not date or date == "":
        return "Missing"
    elif re.match(r'^\d{4}-\d{4}$', date):
        return "Date Range"
    elif re.match(r'^\d{4}$', date):
        return "Single Year"
    else:
        return "Other"

def count_special_characters(series: pl.Series) -> pl.DataFrame:
    char_counts = Counter()
    special_char_pattern = re.compile(r"[@_!#$%^&*()<>?/\|}{~:]+")
    
    for entry in series.drop_nulls():
        matches = special_char_pattern.findall(entry)
        char_counts.update(matches)
    
    char_df = (
        pl.DataFrame(list(char_counts.items()), schema=["Character Sequence", "Count"])
        .with_columns((pl.col("Count") / pl.col("Count").sum() * 100).round(2).alias("Percentage"))
    )
    return char_df

@st.cache_data
def convert_df(_df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.write_csv().encode("utf-8")

################################## End of Imports and Function Declarations ##################################

st.set_page_config(
    page_title="Family History Library - Metadata Cleanup",
    page_icon="assets/Family Search Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
    )

tab1, tab2 = st.tabs(["Comparing Formats", "Comparing Dates"])

uploaded_file = st.file_uploader(
    "Upload your MARC records file",
    type=["xlsx"],
    accept_multiple_files=False,
    key="file_uploader"
)

if uploaded_file:
    # Load data into Polars DataFrame
    raw = pl.read_excel(uploaded_file)
    
    # Rename columns using your mapping logic
    df = raw.rename({tag: marc_field_mapping_bibliographic_flat.get(tag, tag) for tag in raw.columns})
    df = drop_columns_that_are_all_null(df)
    
    # Save DataFrame to session state
    st.session_state["df"] = df

if "df" in st.session_state and st.session_state["df"] is not None:
    df = st.session_state["df"]

    with tab1:
        st.title("Identify Formatting Patterns")

        st.markdown("""### Instructions
        This page helps identify relationships between categorical columns and continuous columns.
        1. Upload your MARC data file.
        2. Use the sidebar to configure x/y axes and formatting options.
        3. Generate a heatmap to explore relationships.
        """)

        with st.sidebar:
            # Define possible x-axis columns
            possible_x = df.columns  # Ensure it's a list for easier indexing
            
            # Set the default x-axis value
            default_x_value = "040$b-Language of cataloging"  # Replace with your desired default column name
            default_x_index = possible_x.index(default_x_value) if default_x_value in possible_x else 0
            
            # Create the selectbox with the default x-axis value
            selected_x = st.selectbox(
                "Select an x-axis (categorical):", 
                possible_x, 
                index=default_x_index
            )
            
            # Define possible y-axis columns, excluding the selected x-axis column
            possible_y = [col for col in possible_x if col != selected_x]
            
            # Set the default y-axis value
            default_y_value = "264$a-Place of production, publication, distribution, manufacture"  # Replace with your desired default column name
            default_y_index = possible_y.index(default_y_value) if default_y_value in possible_y else 0  # Fallback to the first item
            
            # Create the selectbox with the default y-axis value
            selected_y = st.selectbox(
                "Select a y-axis:", 
                possible_y, 
                index=default_y_index
            )


            y_option = st.radio(
                "Choose an action for y-axis data:",
                options=["Remove Non-special Characters", "Remove Digits"],
                key="y_action"
            )
            if y_option == "Remove Non-special Characters":
                df = df.with_columns(remove_non_special_chars(df[selected_y]).alias(selected_y))
            else:
                df = df.with_columns(remove_digits(df[selected_y]).alias(selected_y))

        test2 = (
            df
            .group_by(
                [selected_x,
                selected_y,]
            )
            .agg(pl.len().alias("count"))  # Ensure to name the count column
            .pivot(
                on=selected_y, 
                index=selected_x,
                values='count'
            )
        ).to_pandas()

        test2_melted = test2.melt(id_vars=selected_x, var_name="Format", value_name="Count")

        heatmap = alt.Chart(test2_melted).mark_rect().encode(
            x=alt.X(f'{selected_x}:O', axis=alt.Axis(labelAngle=-60)),
            y=alt.Y('Format:O', axis=alt.Axis(title=f'{selected_y.split('-')[0].strip()} Formats')),
            color='Count:Q'
            #tooltip=[selected_y, selected_x, 'Count']  # Tooltip with Student, Subject, and Score
        ).properties(
            title=f"{selected_x} VS {selected_y} Heatmap"
        ).configure_view(
            strokeWidth=0  # Removes border around the plot
        )

        # Displaying the Altair heatmap in Streamlit
        st.altair_chart(heatmap, use_container_width=True)
        
        csv = convert_df(df)

        st.download_button(
        label="Download heatmap data as CSV",
        data=csv,
        file_name="large_df.csv",
        mime="text/csv",
    )

    with tab2:
        st.markdown("""### Instructions
        This page analyzes date patterns in your data.
        1. Select a column to analyze.
        2. View a distribution of date formats (e.g., 'YYYY', 'YYYY-YYYY').
        """)

        if uploaded_file:
            st.title("Analyze Date Patterns")

            df_date = df.select([col for col in df.columns if "date" in col.lower()])

            # Allow user to select a column for analysis
            selected_column = st.selectbox("Select a column for analysis:", df_date.columns)

            if selected_column:
                st.write(f"Analyzing column: **{selected_column}**")
                
                if validate_column_format(df[selected_column]):
                    st.header("Step 2: Categorize Date Patterns")

                    df = df.with_columns(
                        pl.col(selected_column).apply(categorize_date_pattern).alias("date_pattern")
                    )
                    
                    date_pattern_counts = df.select("date_pattern").group_by("date_pattern").agg(pl.count()).sort("date_pattern")
                    total_date_patterns = date_pattern_counts.select(pl.col("count").sum()).item()
                    
                    date_pattern_df = date_pattern_counts.with_columns(
                        (pl.col("count") / total_date_patterns * 100).round(2).alias("Percentage")
                    )

                    st.subheader("Date Pattern Distribution")
                    st.dataframe(date_pattern_df.to_pandas())

                    # Visualization
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.bar(date_pattern_df["date_pattern"], date_pattern_df["count"], color=['blue', 'green', 'orange', 'red'])
                    ax.set_xlabel("Date Pattern Category")
                    ax.set_ylabel("Count of Records")
                    ax.set_title(f"Distribution of Date Patterns in '{selected_column}'")
                    st.pyplot(fig)

                    # Special Character Analysis
                    st.header("Step 3: Special Character Analysis")
                    if st.checkbox("Analyze Special Characters"):
                        df_cleaned = df.with_columns(remove_non_special_chars(pl.col(selected_column)).alias("Cleaned"))
                        char_df = count_special_characters(df_cleaned["Cleaned"])
                        
                        st.subheader("Special Character Analysis")
                        st.dataframe(char_df.to_pandas())

                    # Download Updated Data
                    st.header("Step 4: Download Updated Data")
                    new_csv = df.to_csv()
                    st.download_button(
                        label="Download Updated Dataset",
                        data=new_csv,
                        file_name="updated_data.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"The selected column '{selected_column}' does not match the expected format. Please select a column with patterns like 'YYYY' or 'YYYY-YYYY'.")