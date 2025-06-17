# Import necessary libraries and initial setup
import datetime as dt
import pandas as pd


# Set preferred display options
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


# TASK 1: UNDERSTANDING AND PREPARING THE DATA

# Step 1: Read the "flo_data_20k.csv" file and create a copy of the DataFrame.
df_ = pd.read_csv("flo_data_20k.csv")
df = df_.copy()

# Step 2: Perform initial data exploration.
print(df.head(10))                # Display the first 10 rows
print(df.columns)                 # List of column names
print(df.describe())              # Summary statistics for numerical columns
print(df.isnull().values.any())   # Check if there are any missing values
print(df.isnull().sum())          # Count of missing values per column
print(df.info())                  # Overview of dataframe: column types, non-null values
print(df.dtypes)                  # Data types of each column

# Step 3: Omnichannel customers are those who shop from both online and offline platforms.
# Create new variables for the total number of purchases and total spending per customer.
df["order_num_total_ever_omni"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total_ever_omni"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

# Step 4: Examine variable types and convert date-related variables to datetime format.
print(df.dtypes)  # Check data types of all variables.

# Identify columns that contain "date" in their name (these will be converted to datetime).
need_change_cols = [col for col in df.columns if "date" in col]

# Convert all values in the identified columns to datetime format.
df[need_change_cols] = df[need_change_cols].apply(pd.to_datetime)

# Verify that the conversion was successful.
print(df[need_change_cols].dtypes)

# Step 5: Analyze the distribution of customer count, total number of products purchased, and total spending across shopping channels.
summary_df = df.groupby("order_channel").agg({
            "master_id": "count",                             # Number of customers per channel
            "order_num_total_ever_omni": "sum",               # Total number of orders per channel
            "customer_value_total_ever_omni": "sum"           # Total spending per channel
            })
print(summary_df.head())   # # Display the summary dataframe

# Step 6: List the top 10 customers generating the highest revenue.

# IDs of the top 10 customers by total revenue
print(df.sort_values(by="customer_value_total_ever_omni", ascending=False)["master_id"].head(10))

# All details of these top 10 customers
print(df.sort_values(by="customer_value_total_ever_omni", ascending=False).head(10))

# Step 7: List the top 10 customers with the highest number of orders

# IDs of the top 10 customers by total number of orders
print(df.sort_values(by="order_num_total_ever_omni", ascending=False)["master_id"].head(10))

# All details of these top 10 customers
print(df.sort_values(by="order_num_total_ever_omni", ascending=False).head(10))

# Step 8: Create a function for the data preprocessing steps

def data_preparation(dataframe):

    # Prepare omnichannel variables
    dataframe["order_num_total_ever_omni"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["customer_value_total_ever_omni"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    # Convert date columns to datetime format
    dataframe["first_order_date"] = pd.to_datetime(dataframe["first_order_date"])
    dataframe["last_order_date"] = pd.to_datetime(dataframe["last_order_date"])
    dataframe["last_order_date_online"] = pd.to_datetime(dataframe["last_order_date_online"])
    dataframe["last_order_date_offline"] = pd.to_datetime(dataframe["last_order_date_offline"])

    return dataframe

# Calling and using the function
df_ = pd.read_csv("flo_data_20k.csv")
df = df_.copy()
df = data_preparation(df)
print(df.head())


# TASK 2: CALCULATING RFM METRICS
# Note: To calculate recency, you can set the analysis date as 2 days after the maximum date in the dataset.

# Step 1: Calculate Recency, Frequency, and Monetary metrics for each customer and assign the calculated metrics to a variable named 'rfm'.

# Reference date for the analysis
df["last_order_date"].max()  # # The most recent date in the dataset.
today_date = dt.datetime(2021, 5, 30) + pd.Timedelta(days=2)  # Analysis date set as 2 days after the most recent date

# Calculate the metrics
rfm = df.groupby("master_id").agg({
    # Recency: Number of days since the customer's last purchase until the analysis date.
    "last_order_date": lambda last_order_date: (today_date - last_order_date.max()).days,
    "order_num_total_ever_omni": "sum",         # Frequency: Total number of orders by the customer.
    "customer_value_total_ever_omni": "sum"})   # Monetary: Total spending by the customer.

# Step 3: Rename the columns to recency, frequency, and monetary.
rfm.columns = ["recency", "frequency", "monetary"]
print(rfm.head())    # Display the dataframe.


# TASK 3: CALCULATING THE RF SCORES

# Step 1: Convert Recency, Frequency, and Monetary metrics into scores between 1 and 5 using qcut,
# and save these scores as recency_score, frequency_score, and monetary_score respectively.

# Since lower recency is better, recency values are split into 5 equal parts with the lowest recency values assigned the highest score (5),
# and the highest recency values assigned the lowest score (1).
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])

# Frequency scores are assigned using rank to preserve the order of tied values,
# then divided into 5 equal groups with labels from 1 (lowest) to 5 (highest).
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

# Monetary values are split into 5 equal groups with labels from 1 (lowest) to 5 (highest).
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
print(rfm.head())    # Display the dataframe

# Step 3: Combine recency_score and frequency_score into a single variable named RF_SCORE.
rfm["RF_SCORE"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
print(rfm.head())    # Display the dataframe


# TASK 4: DEFINING SEGMENTS BASED ON RF SCORES

# Step 1: Define customer segments based on the RF scores
# Step 2: Use the seg_map dictionary to map RF_SCORE patterns to segment names

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4,5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

# Using regex patterns, we match RF_SCORE values to specific customer segments.
# This categorizes customers into meaningful groups for targeted marketing strategies.
rfm["SEGMENT"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

print(rfm.head())  # Display the dataframe with the new SEGMENT column


# TASK 5: ACTION TIME

# Step 1: Analyze the average Recency, Frequency, and Monetary values for each segment
mean_rfm_metrics = rfm[["SEGMENT", "recency", "frequency", "monetary"]].groupby("SEGMENT").agg("mean")
print(mean_rfm_metrics.head())  # Display the average RFM metrics per segment

# Step 2: Identify and export customer IDs for two marketing cases based on RFM analysis and customer interests.

# Case a: FLO is introducing a new women's shoe brand priced above average.
# Special communication will be made with loyal customers ('champions', 'loyal_customers') who have shopped in the women's category.
# Export these customers' IDs to a CSV file.

# Merge rfm segments with customer category interests
merged_dataframes = pd.merge(
    rfm.reset_index()[["master_id", "SEGMENT"]],
    df[["master_id", "interested_in_categories_12"]],
    on="master_id"
)

# Filter for loyal customers interested in women's products
premium_cust_a = merged_dataframes[
    (merged_dataframes["SEGMENT"].isin(["champions", "loyal_customers"])) &
    (merged_dataframes["interested_in_categories_12"].str.contains("KADIN", na=False))
]

print(premium_cust_a.head())  # Preview of filtered loyal women-interested customers

# Export to CSV
premium_cust_a[["master_id"]].to_csv("premium_customers_a.csv", index=False)

# Case b: There is an upcoming ~40% discount on men's and children's products.
# Target customers who have previously been good buyers but haven't shopped recently.
# Segments: 'need_attention', 'about_to_sleep', 'new_customers' interested in men's or children's categories.
# Export these customers' IDs to a CSV file.

premium_cust_b = merged_dataframes[
    (merged_dataframes["SEGMENT"].isin(["need_attention", "about_to_sleep", "new_customers"])) &
    (merged_dataframes["interested_in_categories_12"].str.contains("ERKEK|COCUK", na=False))
]

print(premium_cust_b.head())  # Preview of targeted customers for men's & kids' discount

# Export to CSV
premium_cust_b[["master_id"]].to_csv("premium_customers_b.csv", index=False)