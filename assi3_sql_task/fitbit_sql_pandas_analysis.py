"""
Fitbit Data Analysis - Bellabeat Case Study 
Using BOTH SQL and Pandas for Analysis
"""

import pandas as pd
import sqlite3
import os

def setup_database(daily_activity, sleep_data, hourly_steps):
    """Create SQLite database and load data"""
    # Remove existing database if it exists
    if os.path.exists('fitbit_analysis.db'):
        os.remove('fitbit_analysis.db')
    
    # Create connection
    conn = sqlite3.connect('fitbit_analysis.db')
    
    # Load data into SQLite tables
    daily_activity.to_sql('daily_activity_merged', conn, index=False, if_exists='replace')
    sleep_data.to_sql('sleep_day_merged', conn, index=False, if_exists='replace')
    hourly_steps.to_sql('hourly_steps_merged', conn, index=False, if_exists='replace')
    
    print("✓ SQLite database created with Fitbit data")
    return conn

def load_data():
    """Load Fitbit datasets with pandas"""
    daily_activity = pd.read_csv('mturkfitbit_dataset/Fitabase_Data/dailyActivity_merged.csv')
    sleep_data = pd.read_csv('mturkfitbit_dataset/Fitabase_Data/sleepDay_merged.csv')
    hourly_steps = pd.read_csv('mturkfitbit_dataset/Fitabase_Data/hourlySteps_merged.csv')
    
    # Convert dates
    daily_activity['ActivityDate'] = pd.to_datetime(daily_activity['ActivityDate'])
    sleep_data['SleepDay'] = pd.to_datetime(sleep_data['SleepDay'])
    hourly_steps['ActivityHour'] = pd.to_datetime(hourly_steps['ActivityHour'])
    
    return daily_activity, sleep_data, hourly_steps

def fact_1_user_engagement_sql(conn):
    """FACT 1: User Engagement using SQL"""
    print("\nFACT 1: USER ENGAGEMENT ANALYSIS")
    print("="*50)
    
    # SQL Query
    sql_query = """
    SELECT 
        Id,
        COUNT(*) as DaysWorn,
        CASE 
            WHEN COUNT(*) >= 25 THEN 'Active User (25+ days)'
            WHEN COUNT(*) >= 15 THEN 'Moderate User (15-24 days)'
            ELSE 'Light User (0-14 days)'
        END as UserType
    FROM daily_activity_merged
    GROUP BY Id
    ORDER BY DaysWorn DESC
    """
    
    # Execute SQL and get results as pandas DataFrame
    result = pd.read_sql_query(sql_query, conn)
    
    # Analysis using pandas
    total_users = len(result)
    active_users = len(result[result['UserType'] == 'Active User (25+ days)'])
    
    # print(f"SQL Query: {sql_query.strip()}")
    print(f"Results: {active_users}/{total_users} users ({active_users/total_users*100:.1f}%) wore Fitbit 25+ days")
    print(f"Average days worn: {result['DaysWorn'].mean():.1f}")
    
    return result

def fact_2_activity_levels_sql(conn):
    """FACT 2: Activity Levels using SQL"""
    print("\nFACT 2: ACTIVITY LEVELS ANALYSIS")
    print("="*50)
    
    # SQL Query
    sql_query = """
    SELECT 
        Id,
        AVG(TotalSteps) as AvgSteps,
        AVG(Calories) as AvgCalories,
        CASE 
            WHEN AVG(TotalSteps) < 5000 THEN 'Inactive (<5,000 steps)'
            WHEN AVG(TotalSteps) < 7500 THEN 'Low Active (5,000-7,499 steps)'
            WHEN AVG(TotalSteps) < 10000 THEN 'Average Active (7,500-9,999 steps)'
            WHEN AVG(TotalSteps) < 12500 THEN 'Active (10,000-12,499 steps)'
            ELSE 'Very Active (12,500+ steps)'
        END as ActivityLevel
    FROM daily_activity_merged
    GROUP BY Id
    ORDER BY AvgSteps DESC
    """
    
    # Execute SQL and get results as pandas DataFrame
    result = pd.read_sql_query(sql_query, conn)
    
    # Analysis using pandas
    inactive_low = len(result[result['ActivityLevel'].isin(['Inactive (<5,000 steps)', 'Low Active (5,000-7,499 steps)'])])
    total_users = len(result)
    
    #print(f"SQL Query: {sql_query.strip()}")
    print(f"Results: {inactive_low}/{total_users} users ({inactive_low/total_users*100:.1f}%) are inactive/low-active")
    print(f"Average steps per day: {result['AvgSteps'].mean():.0f}")
    
    return result

def fact_3_peak_hours_sql(conn):
    """FACT 3: Peak Activity Hours using SQL"""
    print("\nFACT 3: PEAK ACTIVITY HOURS ANALYSIS")
    print("="*50)
    
    # SQL Query
    sql_query = """
    SELECT 
        CAST(strftime('%H', ActivityHour) AS INTEGER) as Hour,
        SUM(StepTotal) as TotalSteps,
        AVG(StepTotal) as AvgStepsPerUser
    FROM hourly_steps_merged
    GROUP BY Hour
    ORDER BY TotalSteps DESC
    LIMIT 5
    """
    
    # Execute SQL and get results as pandas DataFrame
    result = pd.read_sql_query(sql_query, conn)
    
    # Analysis using pandas
    peak_hour = result.iloc[0]['Hour']
    
    #print(f"SQL Query: {sql_query.strip()}")
    print(f"Results: Peak activity at {peak_hour}:00")
    print("Top 5 hours:")
    for _, row in result.iterrows():
        print(f"  {row['Hour']}:00 - {row['TotalSteps']:,} total steps")
    
    return result

def fact_4_sleep_correlation_sql(conn):
    """FACT 4: Sleep and Activity Correlation using SQL"""
    print("\nFACT 4: SLEEP AND ACTIVITY CORRELATION")
    print("="*50)
    
    # SQL Query
    sql_query = """
    SELECT 
        a.Id,
        AVG(s.TotalMinutesAsleep/60.0) as AvgSleepHours,
        AVG(a.TotalSteps) as AvgSteps,
        AVG(a.Calories) as AvgCalories,
        CASE 
            WHEN AVG(s.TotalMinutesAsleep/60.0) < 6 THEN 'Insufficient (<6 hours)'
            WHEN AVG(s.TotalMinutesAsleep/60.0) < 7 THEN 'Below Recommended (6-7 hours)'
            WHEN AVG(s.TotalMinutesAsleep/60.0) <= 9 THEN 'Adequate (7-9 hours)'
            ELSE 'Excessive (>9 hours)'
        END as SleepCategory
    FROM daily_activity_merged a
    INNER JOIN sleep_day_merged s ON a.Id = s.Id AND a.ActivityDate = s.SleepDay
    GROUP BY a.Id
    ORDER BY AvgSleepHours DESC
    """
    
    # Execute SQL and get results as pandas DataFrame
    result = pd.read_sql_query(sql_query, conn)
    
    # Analysis using pandas
    correlation = result['AvgSleepHours'].corr(result['AvgSteps'])
    sleep_counts = result['SleepCategory'].value_counts()
    
    #print(f"SQL Query: {sql_query.strip()}")
    print(f"Results: Sleep-activity correlation: {correlation:.3f}")
    print("Sleep category distribution:")
    for category, count in sleep_counts.items():
        print(f"  {category}: {count} users")
    
    return result

def fact_5_weekly_patterns_sql(conn):
    """FACT 5: Weekly Activity Patterns using SQL"""
    print("\nFACT 5: WEEKLY ACTIVITY PATTERNS")
    print("="*50)
    
    # SQL Query
    sql_query = """
    SELECT 
        CAST(strftime('%w', ActivityDate) AS INTEGER) as DayOfWeek,
        CASE CAST(strftime('%w', ActivityDate) AS INTEGER)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END as DayName,
        AVG(TotalSteps) as AvgSteps,
        AVG(Calories) as AvgCalories
    FROM daily_activity_merged
    GROUP BY DayOfWeek, DayName
    ORDER BY DayOfWeek
    """
    
    # Execute SQL and get results as pandas DataFrame
    result = pd.read_sql_query(sql_query, conn)
    
    # Analysis using pandas
    most_active = result.loc[result['AvgSteps'].idxmax(), 'DayName']
    least_active = result.loc[result['AvgSteps'].idxmin(), 'DayName']
    
    #print(f"SQL Query: {sql_query.strip()}")
    print(f"Results: Most active: {most_active}, Least active: {least_active}")
    print("Weekly averages:")
    for _, row in result.iterrows():
        print(f"  {row['DayName']}: {row['AvgSteps']:.0f} avg steps")
    
    return result

def main():
    """Main function using both SQL and Pandas"""
    print("FITBIT DATA ANALYSIS - USING BOTH SQL AND PANDAS")
    print("="*60)
    
    # Load data with pandas
    daily_activity, sleep_data, hourly_steps = load_data()
    print(f"Data loaded: {len(daily_activity)} daily records, {len(sleep_data)} sleep records, {len(hourly_steps)} hourly records")
    
    # Setup SQLite database
    conn = setup_database(daily_activity, sleep_data, hourly_steps)
    

        # Perform analysis using SQL queries with pandas for results processing
    fact_1_user_engagement_sql(conn)
    fact_2_activity_levels_sql(conn)
    fact_3_peak_hours_sql(conn)
    fact_4_sleep_correlation_sql(conn)
    fact_5_weekly_patterns_sql(conn)
        
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("✓ Used SQL queries to extract data")
    print("✓ Used pandas to process and analyze results")
    print("✓ Database file: fitbit_analysis.db")
        

    conn.close()

if __name__ == "__main__":
    main()
