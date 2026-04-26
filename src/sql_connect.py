import pandas as pd
import urllib.parse
from sqlalchemy import create_engine

# Load cleaned dataset
df = pd.read_csv("cleaned_Country_data.csv")

# Connection string: MySQL credentials
user = "root"
password = urllib.parse.quote_plus("Root@123")
host = "localhost"
database = "global_socioeco_devrisk"

# Create SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Save DataFrame to MySQL table
df.to_sql("country_stats", con=engine, if_exists="replace", index=False)

print("✅ Cleaned dataset successfully loaded into MySQL table 'country_stats'")