"""
HTML Report Generator for Job Market Analysis
"""

def create_html_report(results):
    """Create detailed HTML report"""
    job_title = results['job_title']
    analysis_date = results['analysis_date']
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Market Analysis - {job_title}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
            }}
            .section {{
                background: white;
                padding: 25px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .metric-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .metric-card {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }}
            .positive {{ border-left-color: #28a745; }}
            .warning {{ border-left-color: #ffc107; }}
            .negative {{ border-left-color: #dc3545; }}
            .skills-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 15px 0;
            }}
            .skill-category {{
                background: #e9ecef;
                padding: 15px;
                border-radius: 8px;
            }}
            .question-list {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 15px 0;
            }}
            .source-link {{
                color: #667eea;
                text-decoration: none;
                font-weight: bold;
            }}
            .source-link:hover {{ text-decoration: underline; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }}
            th {{
                background: #f8f9fa;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔍 Job Market Analysis</h1>
            <h2>{job_title}</h2>
            <p>Analysis Date: {analysis_date}</p>
            <p>Layoff Data Source: <a href="https://layoffs.fyi/" style="color: #fff; text-decoration: underline;">layoffs.fyi</a></p>
        </div>
    """
    
    # Add layoff analysis section
    layoff_data = results.get('layoff_data', {})
    html += create_layoff_section(layoff_data, job_title)
    
    # Add hiring trends section
    hiring_trends = results.get('hiring_trends', {})
    html += create_hiring_trends_section(hiring_trends)
    
    # Add skills analysis section
    skills_data = results.get('skills_analysis', {})
    html += create_skills_section(skills_data)
    
    # Add interview questions section
    interview_data = results.get('interview_questions', {})
    html += create_interview_section(interview_data)
    
    # Add market analysis section
    market_analysis = results.get('market_analysis', {})
    html += create_market_analysis_section(market_analysis)
    
    html += """
    </body>
    </html>
    """
    
    return html

def create_layoff_section(layoff_data, job_title):
    """Create layoff analysis section"""
    if layoff_data.get('error'):
        return f"""
        <div class="section">
            <h2>📊 Layoff Analysis (layoffs.fyi)</h2>
            <p>⚠️ Could not fetch layoff data: {layoff_data['error']}</p>
            <p>Source: <a href="{layoff_data['source']}" class="source-link" target="_blank">layoffs.fyi</a></p>
        </div>
        """
    
    stats = layoff_data.get('statistics', {})
    recent_layoffs = layoff_data.get('recent_layoffs', [])
    relevance = layoff_data.get('job_relevance', {})
    
    html = f"""
    <div class="section">
        <h2>📊 Layoff Analysis</h2>
        <p>Real-time data from: <a href="{layoff_data['source']}" class="source-link" target="_blank">layoffs.fyi</a></p>
        
        <div class="metric-grid">
    """
    
    # Add statistics
    for year, data in stats.items():
        html += f"""
            <div class="metric-card warning">
                <h3>{year} Tech Layoffs</h3>
                <p><strong>{data['employees_laid_off']}</strong> employees laid off</p>
                <p><strong>{data['companies_affected']}</strong> companies affected</p>
            </div>
        """
    
    # Add impact assessment
    impact = relevance.get('impact_assessment', 'No assessment available')
    impact_class = 'positive' if 'minimal' in impact.lower() or 'low' in impact.lower() else 'warning'
    
    html += f"""
            <div class="metric-card {impact_class}">
                <h3>Impact on {job_title}</h3>
                <p>{impact}</p>
            </div>
        </div>
    """
    
    # Add recent layoffs table
    if recent_layoffs:
        html += """
        <h3>Recent Tech Company Layoffs</h3>
        <table>
            <tr>
                <th>Company</th>
                <th>Employees Laid Off</th>
                <th>Date</th>
            </tr>
        """
        
        for layoff in recent_layoffs[:10]:
            html += f"""
            <tr>
                <td>{layoff['company']}</td>
                <td>{layoff['employees_laid_off']}</td>
                <td>{layoff['date']}</td>
            </tr>
            """
        
        html += "</table>"
    
    html += "</div>"
    return html

def create_hiring_trends_section(hiring_trends):
    """Create hiring trends section"""
    html = """
    <div class="section">
        <h2>📈 Hiring Trends Analysis</h2>
    """
    
    # Indeed data
    indeed_data = hiring_trends.get('indeed', {})
    if indeed_data and not indeed_data.get('error'):
        job_count = indeed_data.get('job_postings_found', 0)
        trend_class = 'positive' if job_count > 10 else 'warning' if job_count > 5 else 'negative'
        
        html += f"""
        <div class="metric-grid">
            <div class="metric-card {trend_class}">
                <h3>Indeed Job Postings</h3>
                <p><strong>{job_count}</strong> relevant job postings found</p>
                <p>{indeed_data.get('trend_assessment', '')}</p>
            </div>
        """
    
    # LinkedIn data
    linkedin_data = hiring_trends.get('linkedin', {})
    if linkedin_data and not linkedin_data.get('error'):
        opportunities = linkedin_data.get('professional_opportunities', 0)
        networking = linkedin_data.get('networking_potential', '')
        
        html += f"""
            <div class="metric-card">
                <h3>LinkedIn Professional Network</h3>
                <p><strong>{opportunities}</strong> professional opportunities</p>
                <p>{networking}</p>
            </div>
        """
    
    # Market trends
    market_data = hiring_trends.get('market_trends', {})
    if market_data and not market_data.get('error'):
        articles_count = market_data.get('trend_articles_found', 0)
        trend_analysis = market_data.get('trend_analysis', '')
        
        trend_class = 'positive' if 'positive' in trend_analysis.lower() else 'warning'
        
        html += f"""
            <div class="metric-card {trend_class}">
                <h3>Market Trend Analysis</h3>
                <p><strong>{articles_count}</strong> market trend articles analyzed</p>
                <p>{trend_analysis}</p>
            </div>
        </div>
        """
    
    html += "</div>"
    return html

def create_skills_section(skills_data):
    """Create skills analysis section"""
    html = """
    <div class="section">
        <h2>🎯 Skills Analysis & Market Requirements</h2>
    """
    
    # Skills requirements
    requirements = skills_data.get('requirements', {})
    if requirements and not requirements.get('error'):
        extracted_skills = requirements.get('extracted_skills', {})
        categories = requirements.get('skill_categories', {})
        
        html += f"""
        <div class="metric-card">
            <h3>Skills Demand Analysis</h3>
            <p><strong>{extracted_skills.get('total_skills_identified', 0)}</strong> skills identified from job descriptions</p>
            <p>Technical skills: {len(extracted_skills.get('technical_skills', []))}</p>
            <p>Soft skills: {len(extracted_skills.get('soft_skills', []))}</p>
        </div>
        
        <h3>Required Skills by Category</h3>
        <div class="skills-grid">
        """
        
        for category, skills in categories.items():
            if skills:
                skills_list = ', '.join(skills[:10])  # Show first 10 skills
                html += f"""
                <div class="skill-category">
                    <h4>{category.title()}</h4>
                    <p>{skills_list}</p>
                </div>
                """
        
        html += "</div>"
    
    # Salary insights
    salary_data = skills_data.get('salary_insights', {})
    if salary_data and not salary_data.get('error'):
        salary_analysis = salary_data.get('salary_analysis', {})
        
        if 'min_salary' in salary_analysis:
            html += f"""
            <div class="metric-card positive">
                <h3>Salary Analysis</h3>
                <p>Salary range: ${salary_analysis['min_salary']:,} - ${salary_analysis['max_salary']:,}</p>
                <p>Average: ${salary_analysis['avg_salary']:,}</p>
                <p>Based on {salary_analysis['salary_count']} data points</p>
            </div>
            """
    
    # Trending skills
    trends = skills_data.get('trends', {})
    if trends and not trends.get('error'):
        trending_skills = trends.get('trending_skills', [])
        
        if trending_skills:
            html += """
            <h3>Trending/In-Demand Skills</h3>
            <div style="margin: 15px 0;">
            """
            
            for skill, count in trending_skills[:5]:
                html += f'<span style="display: inline-block; padding: 8px 15px; margin: 5px; background: #e7f3ff; color: #0066cc; border-radius: 20px; font-weight: bold;">{skill.title()} ({count})</span>'
            
            html += "</div>"
    
    html += "</div>"
    return html

def create_interview_section(interview_data):
    """Create interview questions section"""
    html = """
    <div class="section">
        <h2>💬 Interview Preparation</h2>
    """
    
    if interview_data.get('error'):
        html += f"<p>⚠️ Could not fetch interview data: {interview_data['error']}</p>"
    else:
        # Common questions
        questions = interview_data.get('common_questions', {})
        standard_questions = questions.get('standard_questions', [])
        
        if standard_questions:
            html += """
            <div class="question-list">
                <h3>Common Interview Questions</h3>
                <ul>
            """
            
            for question in standard_questions[:10]:
                html += f"<li>{question}</li>"
            
            html += "</ul></div>"
        
        # Preparation tips
        tips = interview_data.get('preparation_tips', [])
        if tips:
            html += """
            <h3>Interview Preparation Tips</h3>
            <ul>
            """
            
            for tip in tips:
                html += f"<li>{tip}</li>"
            
            html += "</ul>"
        
        # Interview sources
        sources = interview_data.get('source_links', [])
        if sources:
            html += """
            <h3>Additional Interview Resources</h3>
            <ul>
            """
            
            for source in sources[:5]:
                html += f'<li><a href="{source["link"]}" class="source-link" target="_blank">{source["title"]}</a></li>'
            
            html += "</ul>"
    
    html += "</div>"
    return html

def create_market_analysis_section(market_analysis):
    """Create market analysis section"""
    html = """
    <div class="section">
        <h2>📊 Market Analysis & Outlook</h2>
    """
    
    # Market outlook
    outlook = market_analysis.get('market_outlook', {})
    if outlook:
        sentiment = outlook.get('overall_sentiment', 'Neutral')
        sentiment_class = 'positive' if sentiment == 'Positive' else 'negative' if sentiment == 'Cautious' else 'warning'
        
        html += f"""
        <div class="metric-card {sentiment_class}">
            <h3>Market Outlook</h3>
            <p><strong>Overall Sentiment:</strong> {sentiment}</p>
            <p><strong>Recommendation:</strong> {outlook.get('recommendation', 'Monitor market conditions')}</p>
        </div>
        """
        
        factors = outlook.get('key_factors', [])
        if factors:
            html += """
            <h3>Key Market Factors</h3>
            <ul>
            """
            for factor in factors:
                html += f"<li>{factor}</li>"
            html += "</ul>"
    
    # Growth potential
    growth = market_analysis.get('growth_potential', {})
    if growth:
        html += f"""
        <div class="metric-card">
            <h3>Career Growth Potential</h3>
            <p><strong>Short-term:</strong> {growth.get('short_term', 'N/A')}</p>
            <p><strong>Long-term:</strong> {growth.get('long_term', 'N/A')}</p>
        </div>
        """
    
    html += "</div>"
    return html
