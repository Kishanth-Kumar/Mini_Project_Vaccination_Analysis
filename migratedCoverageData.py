import pandas as pd
import mysql.connector
from mysql.connector import Error

# Load the Excel File from 'Data Source' folder and only 'Data' sheet
file_path = 'Data Source/coverage-data.xlsx'
df = pd.read_excel(file_path, sheet_name='Data')

# Basic Cleaning
df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]  # Normalize column names
df.dropna(how='all', inplace=True)  # Drop completely empty rows
df = df.drop_duplicates()  # Drop duplicate rows

# Fill NaN values in 'target_number' column with 0
df['target_number'] = df['target_number'].fillna(0)

# Fill NaN values in 'doses' column with 0
df['doses'] = df['doses'].fillna(0)

# Fill NaN values in 'coverage' column with 0
df['coverage'] = df['coverage'].fillna(0)

# Convert 'year' column to integers (removing decimal point)
# Drop rows where 'year' is NaN
df = df.dropna(subset=['year'])

# Convert 'year' column to integers (removing decimal point)
df['year'] = df['year'].astype(int)

# Replace NaN values with 'N/A'
df.fillna('N/A', inplace=True)

# MySQL Connection Info
db_config = {
    'host': 'localhost',
    'user': 'root',        
    'password': 'Kishu31101999', 
    'database': 'vaccination_analysis'
}

table_name = 'coverage'

# Connect to MySQL and run migration
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # cursor.execute(create_table_query)

    # Insert cleaned data
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO {table_name} ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({placeholders})"

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row.fillna('').astype(str)))

    conn.commit()
    print("✅ Data migrated successfully to MySQL.")

except Error as e:
    print("❌ Error:", e)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
