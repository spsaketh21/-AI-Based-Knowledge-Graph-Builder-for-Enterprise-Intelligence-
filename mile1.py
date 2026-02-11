# Data Ingestion
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/datatset_consumer_complaints.csv")
df.head()
df.info()
df.isnull().sum()

# Data Cleaning
df.columns = df.columns.str.strip() # to clean the column names
df.drop_duplicates(inplace=True) # to remove duplicates
df.fillna("Unknown", inplace=True) # to check missing values and to correct it

# Data Transformation
df['Date received'] = pd.to_datetime(df['Date received'])
df['Date resolved'] = pd.to_datetime(df['Date resolved'], errors='coerce')
df['Resolution_Days'] = (
    df['Date resolved'] - df['Date received']
).dt.days

# Data Normalization
df['Company'] = df['Company'].str.upper().str.strip()
df['Product'] = df['Product'].str.lower().str.strip()
df['Issue'] = df['Issue'].str.lower().str.strip()
df['State'] = df['State'].str.upper()

# Data Enrichment
df['Delayed_Resolution'] = df['Resolution_Days'].apply(
    lambda x: "Yes" if x != "Unknown" and x > 30 else "No"
)
df['Timely_Flag'] = df['Timely response?'].apply(
    lambda x: 1 if x == "Yes" else 0
)

# To Show Output
print("Final Dataset Shape:", df.shape)
df.head()

# Statistics
print("Total Complaints:", len(df))
print("Unique Companies:", df['Company'].nunique())
print("Average Resolution Days:", df['Resolution_Days'].mean())

# Classification According to Complaint Status
df['Complaint_Status'] = df['Delayed_Resolution'].apply(
    lambda x: "High Risk" if x == "Yes" else "Normal"
)
df['Complaint_Status'].value_counts()

# To Save Dataset that is Prepared
df.to_csv("cleaned_consumer_complaints.csv", index=False)

# visualization of normal complains VS Delayed
df['Delayed_Resolution'].value_counts().plot(kind='bar')
plt.title("Delayed vs Normal Complaints")
plt.show()
