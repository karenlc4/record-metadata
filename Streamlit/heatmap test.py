#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

flights = sns.load_dataset("flights")

flights_matrix = flights.pivot_table(index="month", columns="year", values="passengers")
# %%
