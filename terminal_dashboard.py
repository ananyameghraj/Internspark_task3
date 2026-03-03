import pandas as pd
import os
from datetime import datetime
import time

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(100)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.ENDC}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'-'*100}{Colors.ENDC}")

def print_metric(label, value, color=Colors.GREEN):
    print(f"{label:40s} {color}{value}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

def print_table(df, title=""):
    if not df.empty:
        print(f"\n{Colors.BOLD}{Colors.CYAN}{title}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'-'*100}{Colors.ENDC}")
        print(df.to_string(index=False))
        print()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def main_dashboard():
    clear_screen()
    
    # Load all data
    print_header("🎯 WEBSITE TRAFFIC ANALYSIS DASHBOARD - ALFIDO TECH")
    
    print(f"{Colors.BOLD}Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.BOLD}Location: {os.getcwd()}{Colors.ENDC}\n")
    
    # ============================================================================
    # SECTION 1: SUMMARY METRICS
    # ============================================================================
    print_section("📊 SUMMARY METRICS")
    
    if os.path.exists('summary_metrics_report.csv'):
        df_summary = pd.read_csv('summary_metrics_report.csv')
        
        for idx, row in df_summary.iterrows():
            metric = row['Metric']
            value = row['Value']
            
            # Color code based on metric type
            if 'Users' in metric or 'Sessions' in metric or 'Pageviews' in metric:
                color = Colors.GREEN
            elif 'Bounce' in metric:
                color = Colors.RED
            elif 'Duration' in metric or 'Return' in metric:
                color = Colors.CYAN
            else:
                color = Colors.YELLOW
            
            print_metric(f"  • {metric}:", value, color)
    else:
        print_warning("summary_metrics_report.csv not found")
    
    # ============================================================================
    # SECTION 2: TOP LANDING PAGES
    # ============================================================================
    print_section("📍 TOP LANDING PAGES")
    
    if os.path.exists('landing_pages_report.csv'):
        df_landing = pd.read_csv('landing_pages_report.csv').head(10)
        
        for idx, row in df_landing.iterrows():
            rank = row['Rank']
            page = row['Page'][:50]
            sessions = row['Sessions']
            pct = row['Percentage']
            
            # Create bar
            bar_length = int(pct / 2)
            bar = '█' * bar_length
            
            print(f"  {int(rank):2d}. {page:45s} │ {bar:40s} {pct:5.1f}% ({sessions:,d})")
    else:
        print_warning("landing_pages_report.csv not found")
    
    # ============================================================================
    # SECTION 3: TOP EXIT PAGES
    # ============================================================================
    print_section("📤 TOP EXIT PAGES")
    
    if os.path.exists('exit_pages_report.csv'):
        df_exit = pd.read_csv('exit_pages_report.csv').head(10)
        
        for idx, row in df_exit.iterrows():
            rank = row['Rank']
            page = row['Page'][:50]
            sessions = row['Sessions']
            pct = row['Percentage']
            
            # Create bar
            bar_length = int(pct / 2)
            bar = '▓' * bar_length
            
            print(f"  {int(rank):2d}. {page:45s} │ {bar:40s} {pct:5.1f}% ({sessions:,d})")
    else:
        print_warning("exit_pages_report.csv not found")
    
    # ============================================================================
    # SECTION 4: TOP REFERRAL SOURCES
    # ============================================================================
    print_section("🌐 TOP REFERRAL SOURCES")
    
    if os.path.exists('referral_sources_report.csv'):
        df_referral = pd.read_csv('referral_sources_report.csv').head(10)
        
        for idx, row in df_referral.iterrows():
            rank = row['Rank']
            source = row['Source'][:40]
            pageviews = row['Pageviews']
            pct = row['Percentage']
            
            # Create bar
            bar_length = int(pct / 2)
            bar = '▒' * bar_length
            
            print(f"  {int(rank):2d}. {source:35s} │ {bar:40s} {pct:5.1f}% ({pageviews:,d})")
    else:
        print_warning("referral_sources_report.csv not found")
    
    # ============================================================================
    # SECTION 5: KEY INSIGHTS
    # ============================================================================
    print_section("💡 KEY INSIGHTS & ANALYSIS")
    
    if os.path.exists('summary_metrics_report.csv'):
        df_summary = pd.read_csv('summary_metrics_report.csv')
        metrics_dict = dict(zip(df_summary['Metric'], df_summary['Value']))
        
        # Extract values
        try:
            bounce_rate = float(metrics_dict.get('Bounce Rate (%)', '0').replace('%', ''))
            return_rate = float(metrics_dict.get('Return Rate (%)', '0').replace('%', ''))
            avg_duration = float(metrics_dict.get('Avg Session Duration (min)', '0').split()[0])
            
            print(f"\n  {Colors.YELLOW}🔴 BOUNCE RATE ANALYSIS:{Colors.ENDC}")
            if bounce_rate > 50:
                print(f"     ⚠️  High bounce rate ({bounce_rate:.1f}%) - Action needed!")
                print(f"     → Optimize landing pages with better CTAs")
                print(f"     → Reduce page load time")
            elif bounce_rate > 40:
                print(f"     📊 Moderate bounce rate ({bounce_rate:.1f}%) - Room for improvement")
            else:
                print(f"     ✓ Good bounce rate ({bounce_rate:.1f}%)")
            
            print(f"\n  {Colors.CYAN}👥 RETURN VISITOR ANALYSIS:{Colors.ENDC}")
            if return_rate < 20:
                print(f"     ⚠️  Low return rate ({return_rate:.1f}%) - Need engagement boost")
                print(f"     → Improve content quality")
                print(f"     → Implement email marketing")
            elif return_rate < 30:
                print(f"     📊 Fair return rate ({return_rate:.1f}%) - Standard for most sites")
            else:
                print(f"     ✓ Strong return rate ({return_rate:.1f}%) - Good engagement")
            
            print(f"\n  {Colors.GREEN}⏱️  SESSION DURATION ANALYSIS:{Colors.ENDC}")
            if avg_duration < 2:
                print(f"     ⚠️  Very low session duration ({avg_duration:.1f} min) - High friction")
                print(f"     → Improve page speed")
                print(f"     → Simplify navigation")
            elif avg_duration < 3:
                print(f"     📊 Low session duration ({avg_duration:.1f} min) - Users leaving quickly")
            else:
                print(f"     ✓ Good session duration ({avg_duration:.1f} min) - Users engaged")
        
        except:
            print("  Unable to extract metrics")
    
    # ============================================================================
    # SECTION 6: 5 RECOMMENDATIONS
    # ============================================================================
    print_section("🎯 5 KEY OPTIMIZATION RECOMMENDATIONS")
    
    recommendations = [
        {
            "num": "1",
            "icon": "📍",
            "title": "REDUCE BOUNCE RATE",
            "details": [
                "• Add compelling CTAs above the fold",
                "• Optimize page load speed (target < 2 seconds)",
                "• A/B test headlines and imagery",
                "• Add trust signals (reviews, badges)"
            ],
            "impact": "15-20% reduction in bounce rate",
            "timeline": "2-3 weeks",
            "roi": "Very High"
        },
        {
            "num": "2",
            "icon": "🔄",
            "title": "OPTIMIZE CHECKOUT FLOW",
            "details": [
                "• Reduce form fields to max 5",
                "• Implement one-page checkout",
                "• Add security badges",
                "• Enable guest checkout"
            ],
            "impact": "10-15% conversion increase",
            "timeline": "1-2 weeks",
            "roi": "Very High"
        },
        {
            "num": "3",
            "icon": "🎯",
            "title": "EXPAND REFERRAL SOURCES",
            "details": [
                "• Create custom landing pages",
                "• Build strategic partnerships",
                "• Set up UTM tracking",
                "• Implement referral programs"
            ],
            "impact": "25-30% traffic increase",
            "timeline": "3-4 weeks",
            "roi": "High"
        },
        {
            "num": "4",
            "icon": "⏱️",
            "title": "INCREASE ENGAGEMENT",
            "details": [
                "• Add recommendations engine",
                "• Improve internal linking",
                "• Use exit-intent popups",
                "• Add video content"
            ],
            "impact": "30-40% longer sessions",
            "timeline": "2-3 weeks",
            "roi": "Medium"
        },
        {
            "num": "5",
            "icon": "🛠️",
            "title": "FIX EXIT PAGES",
            "details": [
                "• Conduct UX audit",
                "• Fix broken elements",
                "• Add live chat support",
                "• Improve CTAs"
            ],
            "impact": "20% exit reduction",
            "timeline": "2 weeks",
            "roi": "High"
        }
    ]
    
    for rec in recommendations:
        print(f"\n  {Colors.BOLD}{Colors.YELLOW}{rec['icon']} #{rec['num']} {rec['title']}{Colors.ENDC}")
        print(f"  {Colors.BLUE}{'-'*95}{Colors.ENDC}")
        for detail in rec['details']:
            print(f"    {detail}")
        print(f"\n    {Colors.GREEN}Expected Impact:{Colors.ENDC} {rec['impact']}")
        print(f"    {Colors.CYAN}Timeline:{Colors.ENDC} {rec['timeline']}")
        print(f"    {Colors.YELLOW}ROI:{Colors.ENDC} {rec['roi']}")
    
    # ============================================================================
    # SECTION 7: QUICK WINS
    # ============================================================================
    print_section("⚡ QUICK WINS (Implement This Week)")
    
    quick_wins = [
        "Add FAQ accordion section",
        "Implement email capture popup",
        "Add live chat widget",
        "Create mobile-optimized pages",
        "Add product reviews",
        "Implement related products",
        "Add progress indicators",
        "Add trust badges"
    ]
    
    for idx, win in enumerate(quick_wins, 1):
        print(f"  {idx}. ✓ {win}")
    
    # ============================================================================
    # SECTION 8: EXPECTED OUTCOMES
    # ============================================================================
    print_section("💰 EXPECTED OUTCOMES (6-8 Weeks)")
    
    outcomes = [
        ("Conversion Increase", "25-35%", Colors.GREEN),
        ("Traffic Increase", "20-30%", Colors.GREEN),
        ("Expected ROI", "150-250%", Colors.YELLOW),
        ("Implementation Cost", "$500-2000", Colors.CYAN)
    ]
    
    for outcome, value, color in outcomes:
        print(f"  • {outcome:30s}: {color}{value}{Colors.ENDC}")
    
    # ============================================================================
    # SECTION 9: ACTION ITEMS
    # ============================================================================
    print_section("🔍 NEXT STEPS & ACTION ITEMS")
    
    steps = [
        "1. Review this dashboard analysis",
        "2. Prioritize recommendations by effort & impact",
        "3. Set up A/B tests for major changes",
        "4. Implement quick wins immediately",
        "5. Monitor KPIs daily",
        "6. Measure impact every 2 weeks",
        "7. Iterate and optimize based on results"
    ]
    
    for step in steps:
        print(f"  {Colors.BOLD}{Colors.CYAN}{step}{Colors.ENDC}")
    
    # ============================================================================
    # FOOTER
    # ============================================================================
    print_header("✅ ANALYSIS COMPLETE!")
    
    print(f"\n{Colors.GREEN}📁 Generated Files:{Colors.ENDC}")
    files = [
        'dashboard.png',
        'landing_pages_report.csv',
        'exit_pages_report.csv',
        'referral_sources_report.csv',
        'summary_metrics_report.csv',
        'ALFIDO_TECH_RECOMMENDATIONS.txt',
        'website-traffic-analysis.csv'
    ]
    
    for f in files:
        if os.path.exists(f):
            size = os.path.getsize(f) / 1024  # Size in KB
            print(f"  ✓ {f:40s} ({size:.1f} KB)")
        else:
            print(f"  ✗ {f:40s} (Not found)")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.GREEN}All analysis complete! Review files and start implementation.{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*100}{Colors.ENDC}\n")

if __name__ == "__main__":
    main_dashboard()