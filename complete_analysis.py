import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import os

print("="*100)
print("WEBSITE TRAFFIC ANALYSIS FOR ALFIDO TECH - COMPLETE")
print("="*100)

# ============================================================================
# CREATE SAMPLE DATA (if CSV doesn't exist)
# ============================================================================
print("\n[STEP 1] Checking for data file...")

csv_file = 'website-traffic-analysis.csv'

if not os.path.exists(csv_file):
    print(f"  ⚠️  File not found. Creating sample data...")
    
    np.random.seed(42)
    n_records = 10000
    
    # Create timestamp list correctly
    timestamps = []
    for i in range(n_records):
        days_back = np.random.randint(0, 30)
        hours_back = np.random.randint(0, 24)
        minutes_back = np.random.randint(0, 60)
        ts = datetime.now() - timedelta(days=days_back, hours=hours_back, minutes=minutes_back)
        timestamps.append(ts)
    
    data = {
        'user_id': np.random.randint(1000, 2000, n_records),
        'session_id': np.random.randint(5000, 7000, n_records),
        'timestamp': timestamps,
        'page_url': np.random.choice([
            '/home', '/products', '/product-details', '/cart', '/checkout',
            '/order-confirmation', '/about', '/contact', '/blog', '/faq'
        ], n_records),
        'referrer': np.random.choice([
            'Direct', 'google.com', 'facebook.com', 'instagram.com', 'twitter.com',
            'linkedin.com', 'youtube.com', 'email'
        ], n_records)
    }
    
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"  ✓ Sample data created: {csv_file}")
    print(f"  ✓ Records: {len(df):,}")

# ============================================================================
# LOAD DATA
# ============================================================================
print("\n[STEP 2] Loading data...")
df = pd.read_csv(csv_file)
print(f"✓ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"  Columns: {list(df.columns)}")

# ============================================================================
# CLEAN DATA
# ============================================================================
print("\n[STEP 3] Cleaning data...")
df_clean = df.dropna(subset=['user_id', 'session_id', 'timestamp']).copy()
df_clean['referrer'] = df_clean['referrer'].fillna('Direct')
df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
df_clean = df_clean.sort_values(['user_id', 'timestamp']).reset_index(drop=True)
df_clean = df_clean.drop_duplicates(subset=['user_id', 'session_id', 'timestamp'], keep='first')
df_clean['session_duration_mins'] = df_clean.groupby('session_id')['timestamp'].transform(
    lambda x: (x.max() - x.min()).total_seconds() / 60
)
df_clean['hour'] = df_clean['timestamp'].dt.hour
df_clean['day_of_week'] = df_clean['timestamp'].dt.day_name()
print(f"✓ Data cleaned: {df_clean.shape[0]:,} rows")

# ============================================================================
# CALCULATE METRICS
# ============================================================================
print("\n[STEP 4] Calculating metrics...")

total_users = df_clean['user_id'].nunique()
total_sessions = df_clean['session_id'].nunique()
total_pageviews = len(df_clean)
bounce_sessions = (df_clean.groupby('session_id').size() == 1).sum()
bounce_rate = (bounce_sessions / total_sessions) * 100
session_durations = df_clean.groupby('session_id')['session_duration_mins'].first()
avg_session_duration = session_durations.mean()
median_session_duration = session_durations.median()

landing_pages = df_clean.groupby('session_id')['page_url'].first().value_counts()
exit_pages = df_clean.groupby('session_id')['page_url'].last().value_counts()
referral_sources = df_clean['referrer'].value_counts()
page_bounce_rate = df_clean.groupby('page_url').apply(
    lambda x: (x.groupby('session_id').size() == 1).sum() / x['session_id'].nunique() * 100
).sort_values(ascending=False)

user_session_count = df_clean.groupby('user_id')['session_id'].nunique()
new_users = (user_session_count == 1).sum()
returning_users = (user_session_count > 1).sum()
return_rate = (returning_users / total_users) * 100

print(f"✓ Metrics calculated")

# ============================================================================
# DISPLAY KEY METRICS
# ============================================================================
print("\n" + "="*100)
print("📊 KEY METRICS SUMMARY")
print("="*100)
print(f"\n👥 USERS & SESSIONS:")
print(f"   Total Users:           {total_users:>10,}")
print(f"   Total Sessions:        {total_sessions:>10,}")
print(f"   Total Pageviews:       {total_pageviews:>10,}")
print(f"   Sessions per User:     {total_sessions/total_users:>10.2f}")
print(f"   Pages per Session:     {total_pageviews/total_sessions:>10.2f}")

print(f"\n📍 BOUNCE RATE:")
print(f"   Overall Bounce Rate:   {bounce_rate:>10.2f}%")
print(f"   Bounced Sessions:      {bounce_sessions:>10,}")

print(f"\n⏱️  SESSION DURATION:")
print(f"   Average:               {avg_session_duration:>10.2f} min")
print(f"   Median:                {median_session_duration:>10.2f} min")

print(f"\n👤 USER TYPES:")
print(f"   New Users:             {new_users:>10,} ({(new_users/total_users)*100:>6.1f}%)")
print(f"   Returning Users:       {returning_users:>10,} ({return_rate:>6.1f}%)")

print(f"\n🌐 TOP CHANNELS:")
print(f"   Landing Page:          {landing_pages.index[0]}")
print(f"   Exit Page:             {exit_pages.index[0]}")
print(f"   Referral Source:       {referral_sources.index[0]} ({referral_sources.iloc[0]:,} views)")

# ============================================================================
# DISPLAY TOP PAGES
# ============================================================================
print("\n" + "="*100)
print("📋 TOP LANDING PAGES")
print("="*100)
for idx, (page, count) in enumerate(landing_pages.head(8).items(), 1):
    pct = (count / total_sessions) * 100
    print(f"{idx:2d}. {page:40s} - {count:6,d} sessions ({pct:5.1f}%)")

print("\n" + "="*100)
print("📋 TOP EXIT PAGES")
print("="*100)
for idx, (page, count) in enumerate(exit_pages.head(8).items(), 1):
    pct = (count / total_sessions) * 100
    print(f"{idx:2d}. {page:40s} - {count:6,d} sessions ({pct:5.1f}%)")

print("\n" + "="*100)
print("📋 TOP REFERRAL SOURCES")
print("="*100)
for idx, (source, count) in enumerate(referral_sources.head(8).items(), 1):
    pct = (count / len(df_clean)) * 100
    print(f"{idx:2d}. {source:40s} - {count:6,d} pageviews ({pct:5.1f}%)")

# ============================================================================
# CREATE VISUALIZATIONS
# ============================================================================
print("\n[STEP 5] Creating visualizations...")

sns.set_style("whitegrid")
fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Landing Pages
ax1 = fig.add_subplot(gs[0, 0])
landing_pages.head(8).plot(kind='barh', ax=ax1, color='#3498db', edgecolor='black')
ax1.set_xlabel('Sessions', fontsize=10)
ax1.set_title('Top 8 Landing Pages', fontsize=12, fontweight='bold')
ax1.invert_yaxis()

# 2. Exit Pages
ax2 = fig.add_subplot(gs[0, 1])
exit_pages.head(8).plot(kind='barh', ax=ax2, color='#e74c3c', edgecolor='black')
ax2.set_xlabel('Sessions', fontsize=10)
ax2.set_title('Top 8 Exit Pages', fontsize=12, fontweight='bold')
ax2.invert_yaxis()

# 3. Referral Sources
ax3 = fig.add_subplot(gs[0, 2])
referral_sources.head(8).plot(kind='barh', ax=ax3, color='#2ecc71', edgecolor='black')
ax3.set_xlabel('Pageviews', fontsize=10)
ax3.set_title('Top 8 Referral Sources', fontsize=12, fontweight='bold')
ax3.invert_yaxis()

# 4. Session Duration Distribution
ax4 = fig.add_subplot(gs[1, 0])
session_durations_filtered = session_durations[session_durations <= 120]
ax4.hist(session_durations_filtered, bins=50, color='#f39c12', edgecolor='black', alpha=0.7)
ax4.set_xlabel('Duration (minutes)', fontsize=10)
ax4.set_ylabel('Count', fontsize=10)
ax4.set_title('Session Duration Distribution', fontsize=12, fontweight='bold')
ax4.axvline(avg_session_duration, color='red', linestyle='--', linewidth=2, label=f'Avg: {avg_session_duration:.1f}m')
ax4.legend()

# 5. Bounce Rate by Page
ax5 = fig.add_subplot(gs[1, 1])
page_bounce_rate.head(10).plot(kind='barh', ax=ax5, color='#c0392b', edgecolor='black')
ax5.set_xlabel('Bounce Rate (%)', fontsize=10)
ax5.set_title('Top 10 Pages by Bounce Rate', fontsize=12, fontweight='bold')
ax5.invert_yaxis()

# 6. Sessions by Hour
ax6 = fig.add_subplot(gs[1, 2])
sessions_by_hour = df_clean.groupby('hour')['session_id'].nunique()
sessions_by_hour.plot(kind='bar', ax=ax6, color='#9b59b6', edgecolor='black', alpha=0.8)
ax6.set_xlabel('Hour of Day', fontsize=10)
ax6.set_ylabel('Sessions', fontsize=10)
ax6.set_title('Sessions by Hour', fontsize=12, fontweight='bold')
ax6.tick_params(axis='x', rotation=45)

# 7. Sessions by Day
ax7 = fig.add_subplot(gs[2, 0])
sessions_by_day = df_clean.groupby('day_of_week')['session_id'].nunique()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sessions_by_day = sessions_by_day.reindex(day_order)
sessions_by_day.plot(kind='bar', ax=ax7, color='#1abc9c', edgecolor='black', alpha=0.8)
ax7.set_xlabel('Day', fontsize=10)
ax7.set_ylabel('Sessions', fontsize=10)
ax7.set_title('Sessions by Day of Week', fontsize=12, fontweight='bold')
ax7.tick_params(axis='x', rotation=45)

# 8. User Distribution Pie
ax8 = fig.add_subplot(gs[2, 1])
ax8.pie([new_users, returning_users], labels=['New', 'Returning'], autopct='%1.1f%%', 
        colors=['#e74c3c', '#3498db'], startangle=90)
ax8.set_title('User Type Distribution', fontsize=12, fontweight='bold')

# 9. Key Metrics Text Box
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
metrics_text = f"""KEY METRICS
Users: {total_users:,}
Sessions: {total_sessions:,}
Bounce: {bounce_rate:.1f}%
Avg Duration: {avg_session_duration:.1f}m
Return Rate: {return_rate:.1f}%"""
ax9.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center',
         fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))

plt.suptitle('WEBSITE TRAFFIC ANALYSIS - ALFIDO TECH', fontsize=16, fontweight='bold')
plt.savefig('dashboard.png', dpi=300, bbox_inches='tight')
print(f"✓ Dashboard saved: dashboard.png")
plt.show()

# ============================================================================
# EXPORT REPORTS
# ============================================================================
print("\n[STEP 6] Exporting reports...")

landing_report = pd.DataFrame({
    'Rank': range(1, len(landing_pages.head(20))+1),
    'Page': landing_pages.index[:20],
    'Sessions': landing_pages.values[:20],
    'Percentage': (landing_pages.values[:20] / total_sessions * 100).round(2)
})
landing_report.to_csv('landing_pages_report.csv', index=False)

exit_report = pd.DataFrame({
    'Rank': range(1, len(exit_pages.head(20))+1),
    'Page': exit_pages.index[:20],
    'Sessions': exit_pages.values[:20],
    'Percentage': (exit_pages.values[:20] / total_sessions * 100).round(2)
})
exit_report.to_csv('exit_pages_report.csv', index=False)

referral_report = pd.DataFrame({
    'Rank': range(1, len(referral_sources.head(20))+1),
    'Source': referral_sources.index[:20],
    'Pageviews': referral_sources.values[:20],
    'Percentage': (referral_sources.values[:20] / len(df_clean) * 100).round(2)
})
referral_report.to_csv('referral_sources_report.csv', index=False)

summary_report = pd.DataFrame({
    'Metric': [
        'Total Users', 'Total Sessions', 'Total Pageviews', 'Sessions per User',
        'Pages per Session', 'Bounce Rate (%)', 'New Users', 'Returning Users',
        'Return Rate (%)', 'Avg Session Duration (min)', 'Median Session Duration (min)'
    ],
    'Value': [
        f"{total_users:,}", f"{total_sessions:,}", f"{total_pageviews:,}",
        f"{total_sessions/total_users:.2f}", f"{total_pageviews/total_sessions:.2f}",
        f"{bounce_rate:.2f}", f"{new_users:,}", f"{returning_users:,}",
        f"{return_rate:.2f}", f"{avg_session_duration:.2f}", f"{median_session_duration:.2f}"
    ]
})
summary_report.to_csv('summary_metrics_report.csv', index=False)

print(f"✓ Reports exported:")
print(f"  - landing_pages_report.csv")
print(f"  - exit_pages_report.csv")
print(f"  - referral_sources_report.csv")
print(f"  - summary_metrics_report.csv")

# ============================================================================
# 5 OPTIMIZATION RECOMMENDATIONS
# ============================================================================
print("\n" + "="*100)
print("🎯 5 KEY OPTIMIZATION RECOMMENDATIONS FOR ALFIDO TECH")
print("="*100)

top_ref_2 = referral_sources.index[1] if len(referral_sources) > 1 else "N/A"
top_ref_2_count = referral_sources.iloc[1] if len(referral_sources) > 1 else 0

recommendations = f"""
1. 📍 REDUCE BOUNCE RATE ON HIGH-TRAFFIC PAGES
   ├─ Current Bounce Rate: {bounce_rate:.2f}%
   ├─ Top Bounce Page: {page_bounce_rate.index[0]} ({page_bounce_rate.iloc[0]:.1f}%)
   ├─ Actions:
   │  ✓ Add compelling CTAs (Call-to-Action) above the fold
   │  ✓ Optimize page load speed (target < 2 seconds)
   │  ✓ A/B test headlines, imagery, and copy
   │  ✓ Improve page layout and UX design
   │  ✓ Add trust signals (reviews, testimonials, security badges)
   ├─ Expected Impact: 15-20% reduction in bounce rate
   ├─ Timeline: 2-3 weeks
   └─ ROI: Very High (direct impact on conversions)

2. 🔄 OPTIMIZE USER FUNNEL & CHECKOUT FLOW
   ├─ Current State: Average session duration {avg_session_duration:.1f} minutes
   ├─ Identify drop-off points in conversion funnel
   ├─ Actions:
   │  ✓ Reduce checkout form fields to maximum 5
   │  ✓ Implement one-page checkout option
   │  ✓ Add security badges and trust signals
   │  ✓ Enable guest checkout (no account required)
   │  ✓ Show progress indicator for multi-step forms
   │  ✓ Offer multiple payment methods
   ├─ Expected Impact: 10-15% increase in conversion rate
   ├─ Timeline: 1-2 weeks
   └─ ROI: Very High (directly increases revenue)

3. 🎯 EXPAND & OPTIMIZE REFERRAL TRAFFIC SOURCES
   ├─ Current Top Source: {referral_sources.index[0]} ({referral_sources.iloc[0]:,} pageviews)
   ├─ Secondary Source: {top_ref_2} ({top_ref_2_count:,} pageviews)
   ├─ Actions:
   │  ✓ Create custom landing pages for top referrers
   │  ✓ Build strategic partnerships with high performers
   │  ✓ Implement referral incentive program
   │  ✓ Set up proper UTM parameter tracking
   │  ✓ Create content specifically for referrer audiences
   │  ✓ Monitor and optimize direct traffic
   ├─ Expected Impact: 25-30% increase in referral traffic
   ├─ Timeline: 3-4 weeks
   └─ ROI: High (low cost, high potential)

4. ⏱️ INCREASE SESSION ENGAGEMENT & TIME ON SITE
   ├─ Current State: {avg_session_duration:.2f} minutes per session
   ├─ Target: 5+ minutes (benchmark for better engagement)
   ├─ Actions:
   │  ✓ Implement content recommendation engine
   │  ✓ Add "Related Products/Articles" suggestions
   │  ✓ Use exit-intent popups with special offers
   │  ✓ Improve internal linking strategy
   │  ✓ Add video content and interactive elements
   │  ✓ Create engaging blog/resource sections
   │  ✓ Implement sticky headers with navigation
   ├─ Expected Impact: 30-40% increase in session duration
   ├─ Timeline: 2-3 weeks
   └─ ROI: Medium (improves brand awareness and repeat visits)

5. 🛠️ FIX TOP EXIT PAGES & IMPROVE USER RETENTION
   ├─ Current State: Highest exit page is {exit_pages.index[0]}
   ├─ Exit Rate: ~{(exit_pages.iloc[0]/total_sessions)*100:.1f}% of sessions end here
   ├─ Actions:
   │  ✓ Conduct full UX/UI audit of exit pages
   │  ✓ Fix any broken elements or slow loading
   │  ✓ Add clear navigation breadcrumbs
   │  ✓ Implement sticky navigation header
   │  ✓ Add contextual help or live chat support
   │  ✓ Improve CTA buttons (size, color, text, placement)
   │  ✓ Add exit-intent popups with retention offers
   │  ✓ Create "Back to Shop" or "Continue Shopping" options
   ├─ Expected Impact: 20-30% reduction in exits, 5% conversion lift
   ├─ Timeline: 2 weeks
   └─ ROI: High (prevents customer loss)

{'='*100}
⚡ QUICK WINS (Implement This Week):
   1. Add FAQ accordion section to FAQ page
   2. Implement email capture popup for exit intent
   3. Add live chat support widget
   4. Create mobile-optimized landing pages
   5. Add product reviews/testimonials section
   6. Implement related products widget
   7. Add progress indicators to forms
   8. Add trust badges and security seals

📊 TRAFFIC INSIGHTS:
   • Peak Hours: {sessions_by_hour.idxmax()}:00-{sessions_by_hour.idxmax()+1}:00 ({sessions_by_hour.max():,} sessions)
   • Busiest Day: {sessions_by_day.idxmax()} ({sessions_by_day.max():,} sessions)
   • Return Visitor Rate: {return_rate:.1f}% (Industry benchmark: 25-35%)
   • Pages per Session: {total_pageviews/total_sessions:.2f} (Industry benchmark: 2-3)

💰 EXPECTED OUTCOMES:
   ├─ Timeline: 6-8 weeks to implement all recommendations
   ├─ Expected Conversion Increase: 25-35%
   ├─ Expected Traffic Increase: 20-30%
   ├─ Expected ROI: 150-250% (varies by industry)
   └─ Cost-to-Implement: Low ($500-2000 in tools and design)

🔍 NEXT STEPS:
   1. Prioritize recommendations by implementation difficulty
   2. Set up A/B tests for major changes
   3. Monitor daily KPIs using analytics dashboard
   4. Measure impact every 2 weeks
   5. Iterate and optimize based on results
{'='*100}
"""

print(recommendations)

# Save recommendations to file
with open('ALFIDO_TECH_RECOMMENDATIONS.txt', 'w') as f:
    f.write(recommendations)

print(f"\n✓ Recommendations saved to: ALFIDO_TECH_RECOMMENDATIONS.txt")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*100)
print("✅ ANALYSIS COMPLETE!")
print("="*100)
print("\n📁 GENERATED FILES:")
print("  1. dashboard.png - Complete visualization dashboard")
print("  2. landing_pages_report.csv - Landing pages analysis")
print("  3. exit_pages_report.csv - Exit pages analysis")
print("  4. referral_sources_report.csv - Referral sources analysis")
print("  5. summary_metrics_report.csv - Key metrics summary")
print("  6. ALFIDO_TECH_RECOMMENDATIONS.txt - 5 optimization recommendations")
print("  7. website-traffic-analysis.csv - Sample data (created if not found)")
print("\n📊 All files saved to:")
print(f"  C:\\Users\\Meghraj Ananya\\OneDrive\\Documents\\Internspark task 3")
print("="*100)