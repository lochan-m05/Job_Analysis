# -*- coding: utf-8 -*-
"""
Example usage of the Job Market Analyzer
"""

from job_analyzer import JobMarketAnalyzer
from report_generator import create_html_report
import json
from datetime import datetime

def analyze_role(job_title):
    """Analyze a specific job role"""
    print(f"🔍 Analyzing: {job_title}")
    print("-" * 40)
    
    # Initialize the analyzer
    analyzer = JobMarketAnalyzer()
    
    # Perform full analysis
    results = analyzer.analyze_job_role(job_title)
    
    # Display summary
    analyzer.display_summary()
    
    # Generate HTML report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"analysis_{job_title.replace(' ', '_')}_{timestamp}.html"
    
    html_content = create_html_report(results)
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📁 Report saved: {report_filename}")
    return results

def compare_roles():
    """Compare multiple job roles"""
    roles = ["Data Scientist", "Software Engineer", "Product Manager"]
    
    print("🔍 Comparing Job Roles")
    print("=" * 50)
    
    all_results = {}
    
    for role in roles:
        print(f"\n📊 Analyzing: {role}")
        analyzer = JobMarketAnalyzer()
        
        # Get basic info for comparison
        layoff_data = analyzer.get_layoff_data(role)
        hiring_data = analyzer.search_indeed_jobs(role)
        
        all_results[role] = {
            'layoff_impact': layoff_data.get('job_relevance', {}).get('impact_assessment', 'N/A'),
            'job_postings': hiring_data.get('job_postings_found', 0),
            'hiring_trend': hiring_data.get('trend_assessment', 'N/A')
        }
    
    # Display comparison
    print("\n📋 COMPARISON SUMMARY")
    print("=" * 50)
    for role, data in all_results.items():
        print(f"\n{role}:")
        print(f"  Layoff Impact: {data['layoff_impact']}")
        print(f"  Job Postings: {data['job_postings']}")
        print(f"  Hiring Trend: {data['hiring_trend']}")

if __name__ == "__main__":
    # Example 1: Single role analysis
    print("Example 1: Single Role Analysis")
    print("=" * 40)
    analyze_role("Data Scientist")
    
    print("\n\n")
    
    # Example 2: Multiple role comparison
    print("Example 2: Multiple Role Comparison")
    print("=" * 40)
    compare_roles()
