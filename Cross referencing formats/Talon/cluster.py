#%% Imports, data, and functions
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
from lets_plot import *
LetsPlot.setup_html()

data = pl.read_csv("D:\\School\\Fall24\\Data Science Consulting\\xlsx data\\combined.csv", ignore_errors=True)
data = data.with_row_index(name="index")

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
#%% Working through 260

df2 = (
    data
    # First, remove non-special characters in specified columns
    .pipe(remove_non_special_chars, [
        "260$a-Place of publication, distribution, etc.", 
        "260$b-Name of publisher, distributor, etc.", 
        "264$a-Place of production, publication, distribution, manufacture", 
        "264$b-Name of producer, publisher, distributor, manufacturer"
    ])
    # Then, remove numbers in specified date columns
    .pipe(remove_numbers, ["260$c-Date of publication", "264$c-Date of production, publication, or distribution"])
    # Finally, select only the required columns
    .select([
        "index", 
        "040$b-Language of cataloging",
        "260$a-Place of publication, distribution, etc.", 
        "260$b-Name of publisher, distributor, etc.", 
        "260$c-Date of publication", 
        "264$a-Place of production, publication, distribution, manufacture", 
        "264$b-Name of producer, publisher, distributor, manufacturer", 
        "264$c-Date of production, publication, or distribution"
    ])
)

# %% Working through 264

## 264$a-c
place_new = remove_non_special_chars(data, ["264$a-Place of production, publication, distribution, manufacture"])\
    .select(["index", "264$a-Place of production, publication, distribution, manufacture"])\
    .group_by("264$a-Place of production, publication, distribution, manufacture")\
    .agg(pl.col("264$a-Place of production, publication, distribution, manufacture").count().alias("Count"))

name_new = remove_non_special_chars(data, ["264$b-Name of producer, publisher, distributor, manufacturer"])\
    .select(["index", "264$b-Name of producer, publisher, distributor, manufacturer"])\
    .group_by("264$b-Name of producer, publisher, distributor, manufacturer")\
    .agg(pl.col("264$b-Name of producer, publisher, distributor, manufacturer").count().alias("Count"))

date_pub_new = remove_numbers(data, ["264$c-Date of production, publication, or distribution"])\
    .select(["index", "264$c-Date of production, publication, or distribution"])\
    .group_by("264$c-Date of production, publication, or distribution")\
    .agg(pl.col("264$c-Date of production, publication, or distribution").count().alias("Count"))

#%% Comparing 260 and 264

test = (
    df2
    .group_by(
        ['260$a-Place of publication, distribution, etc.', 
         '264$a-Place of production, publication, distribution, manufacture']
    )
    .agg(pl.len().alias("count"))  # Ensure to name the count column
    .pivot(
        on='264$a-Place of production, publication, distribution, manufacture', 
        index='260$a-Place of publication, distribution, etc.', 
        values='count'
    )
)

# Convert to long format for plotting
test_long = test.unpivot(
    index=['260$a-Place of publication, distribution, etc.'],  # Keep this as identifier
    on=test.columns[1:],  # Use all other columns as value variables
    variable_name='264$a-Place of production, publication, distribution, manufacture',  # Name for the variable column
    value_name='count'  # Name for the value column
)


# %% Heatmap for comparison (260$a)



# %% Comparing Catalog Language with 264 columns

test2 = (
    df2
    .group_by(
        ['264$a-Place of production, publication, distribution, manufacture', 
         '040$b-Language of cataloging']
    )
    .agg(pl.len().alias("count"))  # Ensure to name the count column
    .pivot(
        on='040$b-Language of cataloging', 
        index='264$a-Place of production, publication, distribution, manufacture', 
        values='count'
    )
)

# Convert to long format for plotting
test_long2 = test2.unpivot(
    index=['264$a-Place of production, publication, distribution, manufacture'],  # Keep this as identifier
    on=test2.columns[1:],  # Use all other columns as value variables
    variable_name='040$b-Language of cataloging',  # Name for the variable column
    value_name='count'  # Name for the value column
)

ggplot(test_long2, aes(y="040$b-Language of cataloging", x="264$a-Place of production, publication, distribution, manufacture")) +\
    geom_tile(aes(fill="count")) +\
    labs(title="Most Common 264$a Formats for Each 260$a Format",
         x = "264$a Format",
         y = "Language Catalog") +\
    theme_minimal() +\
    ggsize(1000, 600)
# %%
long_df, heatmap = plot_heatmap(df2, x_col="264$a-Place of production, publication, distribution, manufacture", y_col="040$b-Language of cataloging")

heatmap

# %%
