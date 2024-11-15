#%% Imports, data, and functions
import polars as pl
import lets_plot
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

#%% Working through 260

## 260$a
place = remove_non_special_chars(data, ["260$a-Place of publication, distribution, etc."])\
    .select(["index", "260$a-Place of publication, distribution, etc."])

place_agg = (
    place
    .group_by("260$a-Place of publication, distribution, etc.")
    .agg(pl.len().alias("Count"))  # Apply alias to the aggregation
)

## 260$b
name = remove_non_special_chars(data, ["260$b-Name of publisher, distributor, etc."])

name_agg = (
    name
    .group_by("260$b-Name of publisher, distributor, etc.")
    .agg(pl.len().alias("Count"))
    .sort("Count", descending=True)
)

## 260$c
date_pub = remove_numbers(data, ["260$c-Date of publication"])

date_pub_agg = (
    date_pub
    .group_by("260$c-Date of publication")
    .agg(pl.len().alias("Count"))  # Apply alias to the aggregation
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
formats = remove_non_special_chars(data, ["260$a-Place of publication, distribution, etc.", "260$b-Name of publisher, distributor, etc.",  "260$c-Date of publication", "264$a-Place of production, publication, distribution, manufacture", "264$b-Name of producer, publisher, distributor, manufacturer", "264$c-Date of production, publication, or distribution"])

formats = formats.select("260$a-Place of publication, distribution, etc.", "260$b-Name of publisher, distributor, etc.",  "260$c-Date of publication", "264$a-Place of production, publication, distribution, manufacture", "264$b-Name of producer, publisher, distributor, manufacturer", "264$c-Date of production, publication, or distribution").clone()

test = (
    formats
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

ggplot(test_long, aes(y="260$a-Place of publication, distribution, etc.", x="264$a-Place of production, publication, distribution, manufacture")) +\
    geom_tile(aes(fill="count")) +\
    labs(title="Most Common 264$a Formats for Each 260$a Format",
         x = "264$a Format",
         y = "260$a Format") +\
    theme_minimal()

# %% Comparing Record Language with 264 columns

