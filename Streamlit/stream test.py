import streamlit as st
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
from marc_bibliography_mapping import marc_field_mapping_bibliographic_flat

def remove_non_special_chars(series: pl.Series) -> pl.Series:
    # Define the regex pattern to keep only the specified special characters
    pattern = r"[^@_!#$%^&*()<>?/\|}{~:]"
    
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

    # Convert to Pandas for use with seaborn
    heatmap_data = long_df.fill_null(0).to_pandas()

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="g", cmap='coolwarm')
    plt.title(f'Heatmap of {x_col} vs {y_col}')
    plt.xlabel(y_col)
    plt.ylabel(x_col)
    
    # Return the matplotlib figure
    return plt

# Create file uploader
uploaded_file = st.file_uploader("Choose files", accept_multiple_files=False)

if uploaded_file is not None:
    raw = pl.read_excel(uploaded_file)

    df = raw.rename({tag: marc_field_mapping_bibliographic_flat.get(tag, tag) for tag in raw.columns})
    df = drop_columns_that_are_all_null(df)

    with st.sidebar:
        # Select x-axis column and display rocker button for x-axis
        possible_x = df.columns
        selected_x = st.selectbox("Select an x-axis:", possible_x)
        x_option = st.radio(
            "Choose an action for x-axis data:",
            options=["Remove Non-special Characters", "Remove Digits"],
            key="x_action"
        )
        if x_option == "Remove Non-special Characters":
            df = df.with_columns(remove_non_special_chars(df[selected_x]).alias(selected_x))
        else:
            df = df.with_columns(remove_digits(df[selected_x]).alias(selected_x))
        
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

    heatmap = plot_heatmap(df, selected_x, selected_y)
    st.pyplot(heatmap.figure)