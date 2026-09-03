import ast
import pandas as pd

# Load the dataset
df = pd.read_csv('startup_clean.csv')

df.rename(columns = {'InvestmentAmount_USD' : 'amount(cr.)'}, inplace = True)