# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %% 
# import data
df = pd.read_csv("combined.csv", on_bad_lines='skip')
col = df.columns.tolist()
# drop null column
df = df.loc[:, df.notnull().any()]
# filter columns related to title and language
df1 = df[['008-Fixed-Length Data Elements-General Information','040$b-Language of cataloging', '041$a-Language code of text','546$a-Language note', '245$a-Title', '245$b-Remainder of title', '245$c-Statement of responsibility','245$f-Inclusive dates', '245$n', '245$p-Name of part/section of work']]
df1 = pd.DataFrame(df1)
# %% split the 008 column by position 35-37
df1['008-language'] = df1['008-Fixed-Length Data Elements-General Information'].str.slice(35, 38)
# %% combined 008 and 041 only the case 008 have multi langauge. 
# 008+041 column - langauge result
# 041 are used for only case that 008 has multiple 
# if 041 is na, use 008; 041 is only used for multiple lang
df1['008+041'] = np.where(pd.isna(df1['041$a-Language code of text']), 
                            df1['008-language'],  # Use '008-language' if '041$a-Language code of text' is NaN
                            df1['041$a-Language code of text']) 
# %%
def split_language(df, col_name, delimiter):

    df[col_name] = df[col_name].str.strip()
    split_df = df[col_name].str.split(delimiter, expand=True)
    split_df.columns = [f"{col_name}_part{i+1}" for i in range(split_df.shape[1])]
    # split_df = split_df.fillna('None')
    df = pd.concat([df, split_df], axis=1)
    
    return df
# %%
# The function needs to use a delimiter in the way r'delimiter'
df1 = split_language(df1, '008+041', r';')
# %%
result1 = df1.groupby('008+041').size().reset_index(name='count').sort_values(by='count', ascending=False)
result1

# %% combined 245a and 245b (title and subtitle)
df1['245$ab'] = df1['245$a-Title'] + ' ' + df1['245$b-Remainder of title'].fillna('')
# %% when they use delimiter = in differetn context , it can bring error.
def split_title(df, col_name, delimiter):
    df[col_name] = df[col_name].str.strip()
    
    def should_split(value):
        if '= :' in value:
            return False  
        return delimiter in value
    
    split_df = df[col_name].apply(lambda x: x.split(delimiter) if should_split(x) else [x])
    
    split_df = pd.DataFrame(split_df.tolist(), index=df.index)

    split_df.columns = [f"{col_name}_part{i+1}" for i in range(split_df.shape[1])]
    
    # split_df = split_df.fillna('None')
    
    df = pd.concat([df, split_df], axis=1)
    
    return df

df1 = split_title(df1, '245$ab', r'=')
#%% langauage finder library
import langid
# %%
# Function to detect the language
def detect_language(text):
    try:
        lang, _ = langid.classify(text)
        return lang
    except:
        return np.nan
# %%
# Language code to language name mapping
language_mapping = {
    'en': 'eng',  # English
    'de': 'ger',  # German
    'es': 'spa',  # Spanish
    'fr': 'fre',  # French
    'sv': 'swe',  # Swedish
    'da': 'dan',  # Danish
    'nl': 'dut',  # Dutch
    'no': 'nor',  # Norwegian
    'pt': 'por',  # Portuguese
    'it': 'ita',  # Italian
    'fi': 'fin',  # Finnish
    'cs': 'cze',  # Czech
    'gl': 'glg',  # Galician
    'hu': 'hun',  # Hungarian
    'la': 'lat',  # Latin
    'id': 'ind',  # Indonesian
    'pl': 'pol',  # Polish
    'ms': 'may',  # Malay
    'nn': 'nno',  # Norwegian (Nynorsk)
    'sk': 'slo',  # Slovak
    'is': 'ice',  # Icelandic
    'af': 'afr',  # Afrikaans
    'cy': 'wel',  # Welsh
    'vo': 'vol',  # Volapük
    'ca': 'cat',  # Catalan
    'ro': 'rum',  # Romanian
    'lt': 'lit',  # Lithuanian
    'nb': 'nob',  # Norwegian (Bokmål)
    'eu': 'baq',  # Basque
    'sw': 'swa',  # Swahili
    'hr': 'hrv',  # Croatian
    'fo': 'fao',  # Faroese
    'et': 'est',  # Estonian
    'sl': 'slv',  # Slovenian
    'mg': 'mlg',  # Malagasy
    'lv': 'lav',  # Latvian
    'ga': 'gle',  # Irish
    'tr': 'tur',  # Turkish
    'qu': 'que',  # Quechua
    'tl': 'tgl',  # Tagalog
    'jv': 'jav',  # Javanese
    'ja': 'jpn',  # Japanese
    'lb': 'ltz',  # Luxembourgish
    'eo': 'epo',  # Esperanto
    'xh': 'xho',  # Xhosa
    'rw': 'kin',  # Kinyarwanda
    'mt': 'mlt',  # Maltese
    'an': 'arg',  # Aragonese
    'ru': 'rus',  # Russian
    'hy': 'arm',  # Armenian
    'oc': 'oci',  # Occitan (post-1500)
    'bg': 'bul',  # Bulgarian
    'se': 'sme',  # Northern Sami
    'ht': 'hat',  # Haitian French Creole
    'wa': 'wln',  # Walloon
    'zh': 'chi',   # Chinese
    'sr': 'srp'   # Serbian
}
#%% function to apply the lanague detection
def apply_language(df, columns):
    for i, col in enumerate(columns, start=1):
        new_col = f"{col}_lan{i}"
        df[new_col] = df[col].apply(detect_language)
        df[new_col] = df[new_col].replace(language_mapping)
    
    return df
# %%
columns_to_detect = ['245$ab_part1', '245$ab_part2', '245$ab_part3', '245$ab_part4', '245$ab_part5']
df1 = apply_language(df1, columns_to_detect)
# %%
def get_language_counts(df, columns):
    value_counts_list = [df[col].value_counts() for col in columns] 
    title_lan = pd.concat(value_counts_list, axis=1) 
    title_lan.columns = columns
    title_lan = title_lan.fillna(0)  
    title_lan['Total'] = title_lan.sum(axis=1)  
    
    return title_lan

# Define the columns to calculate value counts for
columns_to_count = ['245$ab_part1_lan1', '245$ab_part2_lan2', '245$ab_part3_lan3', '245$ab_part4_lan4', '245$ab_part5_lan5']
title_lan = get_language_counts(df1, columns_to_count)

title_lan
# %% 
# order
# List of the columns you're interested in
title_cols = ['245$ab_part1_lan1', '245$ab_part2_lan2', '245$ab_part3_lan3', '245$ab_part4_lan4', '245$ab_part5_lan5']
lan_cols = ['008+041_part1', '008+041_part2', '008+041_part3', '008+041_part4', '008+041_part5', '008+041_part6']

# %%
# def create_ordered_lang(row):
#     # Get the values from the specified columns, drop 'None' values, and sort alphabetically
#     values = [row[col] for col in title_cols if row[col] not in [None, np.nan, '']]  # Exclude 'None' and empty strings
#     # Sort the values alphabetically and join them into a single string
#     return ', '.join(sorted(values)) if values else np.nan

# df1['245$ab_lang_order'] = df1.apply(create_ordered_lang, axis=1)
# # %%
# def clean_lang_order(value):
#     # Split the string by commas, strip whitespace, and remove duplicates
#     lang_list = [lang.strip() for lang in value.split(',') if lang.strip() != '']
#     unique_langs = list(set(lang_list))  # Remove duplicates by converting to a set
    
#     # Join the unique languages back into a string, separated by commas
#     cleaned_value = ', '.join(sorted(unique_langs))  # Optional: sorted for consistency
#     return cleaned_value

# # Apply the function to the '245ab_lang_order' column
# df1['245$ab_lang_order'] = df1['245$ab_lang_order'].apply(clean_lang_order)
# %%
df1 = df1.fillna('None')
def compare_columns(row):
    matching_values = []
    lan_not_matching = []
    title_not_matching = []
    
    # Iterate over corresponding column pairs
    for lan_col, title_col in zip(lan_cols, title_cols):
        lan_value = row.get(lan_col, '')
        title_value = row.get(title_col, '')
        
        # If both lan_value and part_value match and are non-empty ('none' excluded)
        if lan_value == title_value and lan_value != np.nan and title_value != 'None':  # Non-empty, matching values
            matching_values.append(lan_value)
        else:
            # If lan_value is not 'none' and doesn't match part_value, add it to lan_not_matching
            if lan_value != 'None' and lan_value != title_value:
                lan_not_matching.append(lan_value)
            
            # If part_value is not 'none' and doesn't match lan_value, add it to part_not_matching
            if title_value != 'None' and title_value != lan_value:
                title_not_matching.append(title_value)
    
    # Prepare the results
    matching_value_result = ', '.join(matching_values) if matching_values else 'None'
    lan_not_matching_result = ', '.join(lan_not_matching) if lan_not_matching else 'None'
    title_not_matching_result = ', '.join(title_not_matching) if title_not_matching else 'None'
    
    return matching_value_result, lan_not_matching_result, title_not_matching_result

# Apply the function across the DataFrame and expand results into new columns
df1[['matching_value', 'mul-Language', 'mul-title']] = df1.apply(compare_columns, axis=1, result_type='expand')
# %%
def update_language_columns(row):
    # Split the 'matching_value' into individual language values
    matching_values = [value.strip() for value in row['matching_value'].split(',') if value.strip() != 'None']
    
    if row['mul-title'] in matching_values:
        row['mul-title'] = 'None'
    
    if row['mul-Language'] in matching_values:
        row['mul-Language'] = 'None'
    
    return row

df1 = df1.apply(update_language_columns, axis=1)

# Clean the 'matching_value' column and remove 'None' entries
df1['matching_value'] = df1['matching_value'].apply(lambda x: ', '.join(value.strip() for value in x.split(',') if value.strip() != 'None'))
# %%
def clean_none(value):
    return ', '.join([lang for lang in value.split(', ') if lang.strip() != 'None']) if value else 'None'

df1['mul-Language'] = df1['mul-Language'].apply(clean_none).fillna('None').replace('', 'None')
df1['mul-title'] = df1['mul-title'].apply(clean_none).fillna('None').replace('', 'None')
# %%
# Create a column to check if both 'language_245' and 'language_008+041' are matching
df1['both_matching'] = (df1['mul-Language'] == 'None') & (df1['mul-title'] == 'None')

# %% Find the cases
filtered = df1[['245$a-Title','both_matching','matching_value', 'mul-Language', 'mul-title']]

case1 = filtered[filtered['both_matching'] == True]
case2 = filtered[(filtered['mul-title']== "None") & (filtered['both_matching'] == False)] 
case3 = filtered[(filtered['mul-Language']== "None") & (filtered['both_matching'] == False)] 
case4 = filtered[(filtered['mul-title'] != 'None') & (filtered['mul-Language'] != 'None') ] 

# %% final result
# Count rows in each case
counts = {
    "Case 1": case1.shape[0],
    "Case 2": case2.shape[0],
    "Case 3": case3.shape[0],
    "Case 4": case4.shape[0]
}

# Convert to DataFrame for plotting
counts_df = pd.DataFrame(list(counts.items()), columns=['Case', 'Count'])

# Plot
plt.figure(figsize=(8, 6))
bars = plt.bar(counts_df['Case'], counts_df['Count'], color='skyblue')

# Add counts on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

plt.xlabel("Case")
plt.ylabel("Count")
plt.title("Number of Rows per Case")
plt.show()
# %% save as excel
with pd.ExcelWriter('output_cases.xlsx') as writer:
    df1.to_excel(writer, sheet_name='All', index=True)
    case1.to_excel(writer, sheet_name='Case1', index=True)
    case2.to_excel(writer, sheet_name='Case2', index=True)
    case3.to_excel(writer, sheet_name='Case3', index=True)
    case4.to_excel(writer, sheet_name='Case4', index=True)
