#!/usr/bin/env python3
"""
Music Store Data Analysis
A comprehensive analysis of the online music store database to answer key business questions.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class MusicStoreAnalyzer:
    def __init__(self, data_path="SQL_Music_Store_Analysis-main/music store data/"):
        """Initialize the analyzer with data path."""
        self.data_path = data_path
        self.customers = None
        self.invoices = None
        self.invoice_lines = None
        self.tracks = None
        self.genres = None
        self.albums = None
        self.artists = None
        
    def load_data(self):
        """Load all CSV files into pandas DataFrames."""
        print("Loading data files...")
        
            # Load core tables
        self.customers = pd.read_csv(f"{self.data_path}customer.csv")
        self.invoices = pd.read_csv(f"{self.data_path}invoice.csv")
        self.invoice_lines = pd.read_csv(f"{self.data_path}invoice_line.csv")
        self.tracks = pd.read_csv(f"{self.data_path}track.csv")
        self.genres = pd.read_csv(f"{self.data_path}genre.csv")
        self.albums = pd.read_csv(f"{self.data_path}album.csv")
        self.artists = pd.read_csv(f"{self.data_path}artist.csv")
            
        print(f"✓ Loaded {len(self.customers)} customers")
        print(f"✓ Loaded {len(self.invoices)} invoices")
        print(f"✓ Loaded {len(self.invoice_lines)} invoice line items")
        print(f"✓ Loaded {len(self.tracks)} tracks")
        print(f"✓ Loaded {len(self.genres)} genres")
        print(f"✓ Loaded {len(self.albums)} albums")
        print(f"✓ Loaded {len(self.artists)} artists")

    
    def clean_and_preprocess(self):
        """Clean and preprocess the data."""
        print("\nCleaning and preprocessing data...")
        
        # Convert invoice_date to datetime
        self.invoices['invoice_date'] = pd.to_datetime(self.invoices['invoice_date'])
        self.invoices['year'] = self.invoices['invoice_date'].dt.year
        
        # Handle missing values
        print(f"Missing values in customers: {self.customers.isnull().sum().sum()}")
        print(f"Missing values in invoices: {self.invoices.isnull().sum().sum()}")
        print(f"Missing values in invoice_lines: {self.invoice_lines.isnull().sum().sum()}")
        
        # Check for duplicates
        print(f"Duplicate customers: {self.customers.duplicated().sum()}")
        print(f"Duplicate invoices: {self.invoices.duplicated().sum()}")
        print(f"Duplicate invoice_lines: {self.invoice_lines.duplicated().sum()}")
        
        # Basic data validation
        print(f"Invoice totals range: ${self.invoices['total'].min():.2f} - ${self.invoices['total'].max():.2f}")
        print(f"Date range: {self.invoices['invoice_date'].min()} to {self.invoices['invoice_date'].max()}")
        
        print("✓ Data cleaning completed")
    
    def get_countries_with_most_customers(self):
        """Answer: Which country has the most customers?"""
        print("\n" + "="*60)
        print("QUESTION 1: Which country has the most customers?")
        print("="*60)
        
        country_counts = self.customers['country'].value_counts()
        print("\nTop 10 countries by customer count:")
        print(country_counts.head(10))
        
        top_country = country_counts.index[0]
        top_count = country_counts.iloc[0]
        
        print(f"\n🏆 ANSWER: {top_country} has the most customers with {top_count} customers")
        
        return country_counts
    
    def get_top_spending_customer(self):
        """Answer: Which customer has spent the most money?"""
        print("\n" + "="*60)
        print("QUESTION 2: Which customer has spent the most money?")
        print("="*60)
        
        # Join customers with invoices to get total spending per customer
        customer_spending = (self.invoices.groupby('customer_id')['total']
                           .sum()
                           .reset_index()
                           .merge(self.customers[['customer_id', 'first_name', 'last_name', 'country']], 
                                  on='customer_id'))
        
        customer_spending = customer_spending.sort_values('total', ascending=False)
        
        print("\nTop 10 customers by total spending:")
        top_customers = customer_spending.head(10)
        for idx, row in top_customers.iterrows():
            print(f"{row['first_name']} {row['last_name']} ({row['country']}): ${row['total']:.2f}")
        
        top_customer = customer_spending.iloc[0]
        print(f"\n🏆 ANSWER: {top_customer['first_name']} {top_customer['last_name']} from {top_customer['country']} has spent the most money: ${top_customer['total']:.2f}")
        
        return customer_spending
    
    def get_revenue_by_genre(self):
        """Answer: How much revenue was generated from each music genre?"""
        print("\n" + "="*60)
        print("QUESTION 3: How much revenue was generated from each music genre?")
        print("="*60)
        
        # Join invoice_lines -> tracks -> genres to get revenue by genre
        genre_revenue = (self.invoice_lines
                        .merge(self.tracks[['track_id', 'genre_id']], on='track_id')
                        .merge(self.genres[['genre_id', 'name']], on='genre_id'))
        
        # Calculate revenue (unit_price * quantity)
        genre_revenue['revenue'] = genre_revenue['unit_price'] * genre_revenue['quantity']
        
        # Group by genre and sum revenue
        genre_totals = (genre_revenue.groupby('name')['revenue']
                       .sum()
                       .sort_values(ascending=False)
                       .reset_index())
        
        print("\nRevenue by music genre:")
        for idx, row in genre_totals.iterrows():
            print(f"{row['name']}: ${row['revenue']:.2f}")
        
        top_genre = genre_totals.iloc[0]
        print(f"\n🏆 ANSWER: {top_genre['name']} generated the most revenue: ${top_genre['revenue']:.2f}")
        
        return genre_totals
    
    def get_average_transaction_value(self):
        """Answer: What is the average transaction value per customer?"""
        print("\n" + "="*60)
        print("QUESTION 4: What is the average transaction value per customer?")
        print("="*60)
        
        # Calculate average transaction value per customer
        customer_avg = (self.invoices.groupby('customer_id')['total']
                       .mean()
                       .reset_index()
                       .merge(self.customers[['customer_id', 'first_name', 'last_name', 'country']], 
                              on='customer_id'))
        
        customer_avg = customer_avg.sort_values('total', ascending=False)
        
        # Overall statistics
        overall_avg = self.invoices['total'].mean()
        median_avg = customer_avg['total'].median()
        
        print(f"\nOverall average transaction value: ${overall_avg:.2f}")
        print(f"Median customer average transaction value: ${median_avg:.2f}")
        
        print("\nTop 10 customers by average transaction value:")
        top_avg_customers = customer_avg.head(10)
        for idx, row in top_avg_customers.iterrows():
            print(f"{row['first_name']} {row['last_name']} ({row['country']}): ${row['total']:.2f}")
        
        print(f"\n🏆 ANSWER: The overall average transaction value is ${overall_avg:.2f}")
        print(f"The median customer has an average transaction value of ${median_avg:.2f}")
        
        return customer_avg, overall_avg
    
    def get_yearly_revenue(self):
        """Answer: What is the total revenue for each year?"""
        print("\n" + "="*60)
        print("QUESTION 5: What is the total revenue for each year?")
        print("="*60)
        
        # Group by year and sum total revenue
        yearly_revenue = (self.invoices.groupby('year')['total']
                         .sum()
                         .reset_index()
                         .sort_values('year'))
        
        print("\nTotal revenue by year:")
        for idx, row in yearly_revenue.iterrows():
            print(f"{int(row['year'])}: ${row['total']:,.2f}")
        
        # Calculate year-over-year growth
        yearly_revenue['growth_rate'] = yearly_revenue['total'].pct_change() * 100
        
        print("\nYear-over-year growth rates:")
        for idx, row in yearly_revenue.iterrows():
            if pd.notna(row['growth_rate']):
                print(f"{int(row['year'])}: {row['growth_rate']:+.1f}%")
        
        best_year = yearly_revenue.loc[yearly_revenue['total'].idxmax()]
        print(f"\n🏆 ANSWER: {int(best_year['year'])} had the highest revenue: ${best_year['total']:,.2f}")
        
        return yearly_revenue
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        print("\n" + "="*80)
        print("EXECUTIVE SUMMARY - MUSIC STORE ANALYSIS REPORT")
        print("="*80)
        
        # Key metrics
        total_customers = len(self.customers)
        total_invoices = len(self.invoices)
        total_revenue = self.invoices['total'].sum()
        avg_order_value = self.invoices['total'].mean()
        
        print(f"\n📊 KEY BUSINESS METRICS:")
        print(f"   • Total Customers: {total_customers:,}")
        print(f"   • Total Orders: {total_invoices:,}")
        print(f"   • Total Revenue: ${total_revenue:,.2f}")
        print(f"   • Average Order Value: ${avg_order_value:.2f}")
        
        # Date range
        date_range = f"{self.invoices['invoice_date'].min().strftime('%Y-%m-%d')} to {self.invoices['invoice_date'].max().strftime('%Y-%m-%d')}"
        print(f"   • Analysis Period: {date_range}")
        
        print(f"\n🎯 BUSINESS INSIGHTS & RECOMMENDATIONS:")
        print(f"   1. Geographic Focus: Target marketing efforts in top customer countries")
        print(f"   2. Customer Retention: Develop loyalty programs for high-value customers")
        print(f"   3. Genre Strategy: Focus inventory on top-performing music genres")
        print(f"   4. Revenue Growth: Analyze yearly trends to optimize seasonal campaigns")
        
        return {
            'total_customers': total_customers,
            'total_invoices': total_invoices,
            'total_revenue': total_revenue,
            'avg_order_value': avg_order_value,
            'date_range': date_range
        }
    
    def run_complete_analysis(self):
        """Run the complete analysis workflow."""
        print("🎵 MUSIC STORE DATA ANALYSIS")
        print("="*80)
        
        # Task 1: Data Ingestion & Initial Exploration
        self.load_data()
        
        # Task 2: Data Cleaning & Preprocessing
        self.clean_and_preprocess()
        
        # Task 3: Data Integration & Aggregation + Task 4: Insight Generation
        country_counts = self.get_countries_with_most_customers()
        customer_spending = self.get_top_spending_customer()
        genre_revenue = self.get_revenue_by_genre()
        customer_avg, overall_avg = self.get_average_transaction_value()
        yearly_revenue = self.get_yearly_revenue()
        
        # Generate final report
        summary = self.generate_summary_report()
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📋 Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return {
            'country_counts': country_counts,
            'customer_spending': customer_spending,
            'genre_revenue': genre_revenue,
            'customer_avg': customer_avg,
            'yearly_revenue': yearly_revenue,
            'summary': summary
        }

if __name__ == "__main__":
    # Initialize and run the analysis
    analyzer = MusicStoreAnalyzer()
    results = analyzer.run_complete_analysis()
