# FLO Customer Segmentation - Miuul Bootcamp

## Project Overview
This project aims to segment FLO customers based on their shopping behavior to create better marketing strategies. The dataset includes past purchases of customers who shopped both online and offline (OmniChannel) between 2020 and 2021. Using RFM (Recency, Frequency, Monetary) analysis, customers are grouped into segments for more personalized communication and marketing.

## Dataset
The dataset used in this project comes from the Miuul Bootcamp and contains customer purchase data from FLO, a popular shoe retailer. It includes variables such as customer ID, shopping channels, dates of first and last orders, total purchase counts, total spending, and interest in product categories over the last 12 months.

	master_id: Unique customer ID
	order_channel: Platform through which the customer placed orders (e.g., Android, iOS, Desktop, Mobile)
	last_order_channel: Channel used for the most recent purchase
	first_order_date: Date of the customer's first purchase
	last_order_date: Date of the customer's most recent purchase
	last_order_date_online: Date of the customer's last online purchase
	last_order_date_offline: Date of the customer's last offline purchase
	order_num_total_ever_online: Total number of purchases made online
	order_num_total_ever_offline: Total number of purchases made offline
	customer_value_total_ever_online: Total monetary value of online purchases
	customer_value_total_ever_offline: Total monetary value of offline purchases
	interested_in_categories_12: List of product categories the customer purchased from in the last 12 months


**Note:** The dataset cannot be shared publicly. To run the project, you need access to the original data provided by Miuul Bootcamp.

## Key Steps
- Data loading and initial exploration  
- Data cleaning and preparation  
- Calculation of RFM metrics (Recency, Frequency, Monetary)  
- Scoring and segmentation of customers based on RFM values  
- Identification of target customer groups for specific marketing campaigns  
- Exporting selected customer IDs for campaign execution  

## How to Run
1. Ensure you have access to the `flo_data_20k.csv` dataset provided by Miuul Bootcamp.  
2. Install required libraries (pandas, datetime) if not already installed.  
3. Run the Python scripts or Jupyter notebook step-by-step as outlined.  

## Contact
For questions or collaboration, please feel free to reach out.
