import streamlit as st
import polars as pl
from lets_plot import *
LetsPlot.setup_html()
from marc_bibliography_mapping import marc_field_mapping_bibliographic_flat


## Functions

def remove_non_special_chars(df: pl.DataFrame, column_names: list) -> pl.DataFrame:
    # Define the regex pattern to keep only the specified special characters
    pattern = r"[^@_!#$%^&*()<>?/\|}{~:]"
    
    # Loop through each column name in the provided list
    for column_name in column_names:
        # Apply the regex pattern to the column, replacing everything except special characters with an empty string
        df = df.with_columns(
            pl.col(column_name).str.replace_all(pattern, "").alias(column_name)
        )
    
    return df

def remove_numbers(df: pl.DataFrame, column_names:list) -> pl.DataFrame:
    # Define the regex pattern for numbers (digits 0-9)
    pattern = r"\d"
    
    # Apply the regex pattern to the column, replacing numbers with an empty string
    for column_name in column_names:

        df = df.with_columns(
            pl.col(column_name).str.replace_all(pattern, "").alias(column_name)
        )
    
    return df

def drop_columns_that_are_all_null(_df: pl.DataFrame) -> pl.DataFrame:
    return _df[[s.name for s in _df if not (s.null_count() == _df.height)]]

def process_and_combine_files(file_names: list) -> pl.DataFrame:
    from marc_bibliography_mapping import marc_field_mapping_bibliographic_flat

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

def plot_heatmap(df: pl.DataFrame, x_col: str, y_col: str, count_col: str = 'count'):
    # Group by specified columns and count occurrences
    grouped_df = (
        df
        .group_by([x_col, y_col])
        .agg(pl.len().alias(count_col))  # Use pl.count() for clarity
        .pivot(
            on=y_col,
            index=x_col,
            values=count_col
        )
    )

    # Convert to long format for plotting
    long_df = grouped_df.unpivot(
        index=[x_col],
        on=[col for col in grouped_df.columns if col != x_col], # Specify columns clearly
        variable_name=y_col,
        value_name=count_col
    )

    # Convert to Pandas for plotnine if necessary
    long_df_pd = long_df.to_pandas()

    # Create the heatmap
    heatmap = (
        ggplot(long_df_pd, aes(x=x_col, y=y_col)) +
        geom_tile(aes(fill=count_col)) +
        labs(
            title=f"Heatmap of {x_col} by {y_col}",
            x=x_col,
            y=y_col
        ) +
        theme_minimal() +
        ggsize(800, 800)
    )

    return long_df, heatmap

# Create file uploader
uploaded_file = st.file_uploader("Choose files", accept_multiple_files=False)

if uploaded_file is not None:
    raw = pl.read_excel(uploaded_file)

    df = raw.rename({tag: marc_field_mapping_bibliographic_flat.get(tag, tag) for tag in raw.columns})
    df = drop_columns_that_are_all_null(df)

    st.write(df.head())

    with st.sidebar:
        possible_x = df.columns
        selected_x = st.selectbox("Select an x-axis:", possible_x)

        possible_y = [col for col in df.columns if col != selected_x]
        selected_y = st.selectbox("Select a y-axis:", possible_y)

    #if selected_x and selected_y:
    #    long_df, heatmap = plot_heatmap(df, selected_x, selected_y)
    #    heatmap
