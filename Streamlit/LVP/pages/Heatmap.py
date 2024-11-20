#%% Imports and functions
import streamlit as st
import polars as pl
import altair as alt

from marc_bibliography_mapping import marc_field_mapping_bibliographic_flat

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
    
    # Function to drop columns that are entirely null
    def drop_columns_that_are_all_null(_df: pl.DataFrame) -> pl.DataFrame:
        return _df[[s.name for s in _df if not (s.null_count() == _df.height)]]
    
    # Drop columns that are all null
    combined_new = drop_columns_that_are_all_null(combined)

    return combined_new

@st.cache_data
def convert_df(_df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.write_csv().encode("utf-8")
#%% Streamlit start

st.set_page_config(
    page_title="Family History Library - Metadata Cleanup",
    page_icon="D:\\School\\Fall24\\Data Science Consulting\\Family Search Logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create file uploader
uploaded_file = st.file_uploader("Choose files", accept_multiple_files=False)

if uploaded_file is not None:
    raw = pl.read_excel(uploaded_file)

    df = raw.rename({tag: marc_field_mapping_bibliographic_flat.get(tag, tag) for tag in raw.columns})
    df = drop_columns_that_are_all_null(df)

    with st.sidebar:
        # Select x-axis column and display rocker button for x-axis
        possible_x = df.columns
        selected_x = st.selectbox("Select an x-axis (categorical):", possible_x)
        
        # Select y-axis column and display rocker button for y-axis
        possible_y = [col for col in df.columns if col != selected_x]
        selected_y = st.selectbox("Select a y-axis:", possible_y)
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