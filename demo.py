# -*- coding: utf-8 -*-
"""
Demo script for Job Market Analyzer
"""

from job_analyzer import JobMarketAnalyzer
from report_generator import create_html_report
import json
from datetime import datetime

def run_demo():
    """Run a demo analysis"""
    print("🔍 Job Market Analyzer Demo")
    print("=" * 40)
    
    # Demo with "Data Scientist" role
    job_title = "Data Scientist"
    print(f"📊 Analyzing: {job_title}")
    
    try:
        analyzer = JobMarketAnalyzer()
        
        # Just test the layoff data function to show it works
        print("📊 Testing layoff data retrieval...")
        layoff_data = analyzer.get_layoff_data(job_title)
        
        if layoff_data.get('error'):
            print(f"⚠️ Layoff data error: {layoff_data['error']}")
        else:
            print(f"✅ Layoff data retrieved successfully!")
            print(f"   Source: {layoff_data['source']}")
            if layoff_data.get('statistics'):
                for year, stats in layoff_data['statistics'].items():
                    print(f"   {year}: {stats['employees_laid_off']} employees laid off from {stats['companies_affected']} companies")
        
        print("\n🎯 Tool is ready to use!")
        print("   Run 'python main.py' to perform full analysis")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

if __name__ == "__main__":
    run_demo()
