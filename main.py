import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
from datetime import datetime
import re
import os
from collections import defaultdict
import asyncio
import aiohttp
from typing import List, Dict
import feedparser
import urllib.parse

class CareerResearchTool:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.results = defaultdict(dict)
        
    def parse_query(self, query: str) -> tuple:
        """Parse user input into career research components"""
        parts = query.split(',')
        degree = parts[0].strip() if len(parts) > 0 else ""
        experience = parts[1].strip() if len(parts) > 1 else ""
        skills = parts[2].strip() if len(parts) > 2 else ""
        job_market = parts[3].strip() if len(parts) > 3 else ""
        year = parts[4].strip() if len(parts) > 4 else "2025"
        
        return degree, experience, skills, job_market, year
    
    def build_search_queries(self, degree: str, experience: str, skills: str, job_market: str, year: str) -> Dict[str, str]:
        """Build interconnected search queries for career research"""
        base_query = f"{degree} {experience} {skills} {job_market} {year}"
        
        queries = {
            'career_opportunities': f'"{degree}" "{experience}" jobs career opportunities {year}',
            'skills_required': f'"{degree}" "{experience}" skills required technical skills {year}',
            'job_market': f'"{degree}" job market trends employment opportunities {year}',
            'salary_expectations': f'"{degree}" "{experience}" salary compensation pay scale {year}',
            'companies_hiring': f'companies hiring "{degree}" "{experience}" {year}',
            'future_scope': f'"{degree}" future scope career growth {year}'
        }
        
        return queries
    
    def search_google_news(self, query: str) -> List[Dict]:
        """Search Google News for career-related articles"""
        try:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://news.google.com/rss/search?q={encoded_query}"
            news_feed = feedparser.parse(search_url)
            
            articles = []
            for entry in news_feed.entries[:10]:
                article = {
                    'title': entry.title if hasattr(entry, 'title') else '',
                    'link': entry.link if hasattr(entry, 'link') else '',
                    'published': entry.published if hasattr(entry, 'published') else '',
                    'source': entry.source.title if hasattr(entry, 'source') else 'Unknown',
                    'summary': entry.summary if hasattr(entry, 'summary') else ''
                }
                articles.append(article)
            return articles
        except Exception as e:
            print(f"Error searching Google News: {e}")
            return []
    
    def search_indeed_insights(self, job_title: str) -> List[Dict]:
        """Get job market insights from Indeed and similar platforms"""
        try:
            query = f"{job_title} job market trends skills required"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            insights = []
            # Extract relevant job market information
            results = soup.find_all('div', class_='g')[:5]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                desc_elem = result.find('span', class_='aCOpRe')
                
                if title_elem and link_elem:
                    insight = {
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href'),
                        'description': desc_elem.get_text() if desc_elem else ''
                    }
                    insights.append(insight)
            
            return insights
        except Exception as e:
            print(f"Error fetching job insights: {e}")
            return []
    
    def search_linkedin_insights(self, degree: str, skills: str) -> List[Dict]:
        """Get career insights from LinkedIn learning and articles"""
        try:
            query = f"LinkedIn learning {degree} {skills} career path"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            insights = []
            results = soup.find_all('div', class_='g')[:5]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    insight = {
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href'),
                        'source': 'LinkedIn Insights'
                    }
                    insights.append(insight)
            
            return insights
        except Exception as e:
            print(f"Error fetching LinkedIn insights: {e}")
            return []
    
    def search_coursera_skills(self, degree: str, skills: str) -> List[Dict]:
        """Get relevant courses and skills from Coursera"""
        try:
            query = f"Coursera {degree} {skills} courses certification"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            courses = []
            results = soup.find_all('div', class_='g')[:5]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    course = {
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href'),
                        'platform': 'Coursera'
                    }
                    courses.append(course)
            
            return courses
        except Exception as e:
            print(f"Error fetching Coursera courses: {e}")
            return []
    
    def search_glassdoor_salaries(self, degree: str, experience: str) -> List[Dict]:
        """Get salary information from Glassdoor"""
        try:
            query = f"Glassdoor {degree} {experience} salary"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            salaries = []
            results = soup.find_all('div', class_='g')[:5]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    salary_info = {
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href'),
                        'source': 'Glassdoor'
                    }
                    salaries.append(salary_info)
            
            return salaries
        except Exception as e:
            print(f"Error fetching salary information: {e}")
            return []
    
    def search_reddit_career_advice(self, degree: str, experience: str) -> List[Dict]:
        """Search Reddit for career advice and discussions"""
        try:
            query = f"{degree} {experience} career advice reddit"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.reddit.com/search.json?q={encoded_query}&sort=relevance&limit=10"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = []
                for post in data['data']['children'][:8]:
                    post_data = post['data']
                    posts.append({
                        'title': post_data.get('title', ''),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'comments': post_data.get('num_comments', 0),
                        'subreddit': post_data.get('subreddit', ''),
                        'created': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d')
                    })
                return posts
            return []
        except Exception as e:
            print(f"Error searching Reddit: {e}")
            return []
    
    def search_quora_answers(self, degree: str, experience: str, skills: str) -> List[Dict]:
        """Get career-related answers from Quora"""
        try:
            query = f"Quora {degree} {experience} {skills} career"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            answers = []
            results = soup.find_all('div', class_='g')[:5]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    answer = {
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href'),
                        'platform': 'Quora'
                    }
                    answers.append(answer)
            
            return answers
        except Exception as e:
            print(f"Error fetching Quora answers: {e}")
            return []
    
    def analyze_skill_trends(self, skills: str) -> Dict:
        """Analyze current skill trends and demands"""
        try:
            query = f"most in demand skills {skills} 2024 2025"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract skill trends from search results
            skill_trends = {
                'high_demand_skills': [],
                'emerging_skills': [],
                'traditional_skills': []
            }
            
            # This is a simplified analysis - you can enhance this with more sophisticated parsing
            results = soup.find_all('div', class_='g')[:3]
            for result in results:
                text_content = result.get_text().lower()
                
                # Simple keyword-based categorization
                if any(word in text_content for word in ['ai', 'machine learning', 'data science', 'cloud']):
                    skill_trends['emerging_skills'].append("AI/ML Technologies")
                if any(word in text_content for word in ['python', 'java', 'javascript', 'sql']):
                    skill_trends['high_demand_skills'].append("Programming Languages")
                if any(word in text_content for word in ['communication', 'leadership', 'problem solving']):
                    skill_trends['traditional_skills'].append("Soft Skills")
            
            return skill_trends
        except Exception as e:
            print(f"Error analyzing skill trends: {e}")
            return {}
    
    def generate_career_report(self, degree: str, experience: str, skills: str, job_market: str, year: str) -> Dict:
        """Generate comprehensive career research report"""
        print(f"🔍 Researching career path: {degree} for {experience} with skills in {skills}")
        print(f"📊 Analyzing job market: {job_market} for year: {year}")
        
        # Build interconnected search queries
        queries = self.build_search_queries(degree, experience, skills, job_market, year)
        
        # Career opportunities
        print("💼 Searching career opportunities...")
        career_articles = self.search_google_news(queries['career_opportunities'])
        self.results['career_opportunities'] = career_articles
        
        # Required skills
        print("🔧 Analyzing required skills...")
        skills_articles = self.search_google_news(queries['skills_required'])
        self.results['required_skills'] = skills_articles
        
        # Job market trends
        print("📈 Researching job market trends...")
        job_market_insights = self.search_indeed_insights(f"{degree} {experience}")
        self.results['job_market_trends'] = job_market_insights
        
        # Salary information
        print("💰 Gathering salary information...")
        salary_info = self.search_glassdoor_salaries(degree, experience)
        self.results['salary_information'] = salary_info
        
        # Learning resources
        print("🎓 Finding learning resources...")
        courses = self.search_coursera_skills(degree, skills)
        self.results['learning_resources'] = courses
        
        # Community discussions
        print("💬 Searching community discussions...")
        reddit_posts = self.search_reddit_career_advice(degree, experience)
        self.results['community_discussions'] = reddit_posts
        
        # LinkedIn insights
        print("👔 Getting LinkedIn insights...")
        linkedin_insights = self.search_linkedin_insights(degree, skills)
        self.results['linkedin_insights'] = linkedin_insights
        
        # Quora answers
        print("🤔 Gathering Quora insights...")
        quora_answers = self.search_quora_answers(degree, experience, skills)
        self.results['quora_insights'] = quora_answers
        
        # Skill trends analysis
        print("📊 Analyzing skill trends...")
        skill_trends = self.analyze_skill_trends(skills)
        self.results['skill_trends'] = skill_trends
        
        # Generate summary
        self.results['summary'] = self._generate_career_summary(degree, experience, skills, job_market, year)
        
        return self.results
    
    def _generate_career_summary(self, degree: str, experience: str, skills: str, job_market: str, year: str) -> Dict:
        """Generate comprehensive career summary"""
        total_sources = sum(len(items) for key, items in self.results.items() 
                           if key not in ['summary', 'skill_trends'])
        
        # Calculate overall opportunity score
        opportunity_indicators = len(self.results.get('career_opportunities', [])) + \
                               len(self.results.get('job_market_trends', [])) + \
                               len(self.results.get('salary_information', []))
        
        if opportunity_indicators > 15:
            market_outlook = "Very Positive"
        elif opportunity_indicators > 8:
            market_outlook = "Positive"
        elif opportunity_indicators > 3:
            market_outlook = "Moderate"
        else:
            market_outlook = "Limited Data"
        
        return {
            'degree': degree,
            'experience_level': experience,
            'skills_focus': skills,
            'job_market': job_market,
            'target_year': year,
            'total_sources_found': total_sources,
            'market_outlook': market_outlook,
            'career_areas_covered': list(self.results.keys()),
            'report_generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'key_findings': self._extract_key_findings()
        }
    
    def _extract_key_findings(self) -> List[str]:
        """Extract key findings from the research"""
        findings = []
        
        # Analyze career opportunities
        career_articles = self.results.get('career_opportunities', [])
        if career_articles:
            findings.append(f"Found {len(career_articles)} recent career opportunity articles")
        
        # Analyze skills demand
        skill_trends = self.results.get('skill_trends', {})
        if skill_trends.get('high_demand_skills'):
            findings.append(f"High demand skills identified: {', '.join(skill_trends['high_demand_skills'])}")
        
        # Analyze learning resources
        courses = self.results.get('learning_resources', [])
        if courses:
            findings.append(f"Available learning resources: {len(courses)} courses/certifications")
        
        # Analyze community engagement
        discussions = self.results.get('community_discussions', [])
        if discussions:
            findings.append(f"Active community discussions: {len(discussions)} threads")
        
        return findings
    
    def display_career_report(self):
        """Display career research results in a formatted way"""
        summary = self.results['summary']
        
        print(f"\n{'='*70}")
        print(f"🎓 CAREER RESEARCH REPORT")
        print(f"{'='*70}")
        print(f"📚 Degree/Qualification: {summary['degree']}")
        print(f"👤 Experience Level: {summary['experience_level']}")
        print(f"🔧 Skills Focus: {summary['skills_focus']}")
        print(f"📈 Job Market: {summary['job_market']}")
        print(f"🎯 Target Year: {summary['target_year']}")
        print(f"📊 Market Outlook: {summary['market_outlook']}")
        print(f"📋 Total Sources Analyzed: {summary['total_sources_found']}")
        print(f"{'='*70}")
        
        # Display key findings
        print(f"\n🔍 KEY FINDINGS:")
        for i, finding in enumerate(summary['key_findings'], 1):
            print(f"   {i}. {finding}")
        
        # Display career opportunities
        if self.results.get('career_opportunities'):
            print(f"\n💼 RECENT CAREER OPPORTUNITIES:")
            for i, article in enumerate(self.results['career_opportunities'][:3], 1):
                print(f"   {i}. {article['title'][:80]}...")
                print(f"      📅 {article.get('published', 'Date not available')}")
        
        # Display required skills
        if self.results.get('required_skills'):
            print(f"\n🔧 IN-DEMAND SKILLS:")
            for i, article in enumerate(self.results['required_skills'][:3], 1):
                print(f"   {i}. {article['title'][:80]}...")
        
        # Display skill trends
        if self.results.get('skill_trends'):
            trends = self.results['skill_trends']
            print(f"\n📊 SKILL TRENDS ANALYSIS:")
            if trends.get('high_demand_skills'):
                print(f"   🚀 High Demand: {', '.join(trends['high_demand_skills'])}")
            if trends.get('emerging_skills'):
                print(f"   🔥 Emerging: {', '.join(trends['emerging_skills'])}")
            if trends.get('traditional_skills'):
                print(f"   💼 Foundational: {', '.join(trends['traditional_skills'])}")
        
        # Display learning resources
        if self.results.get('learning_resources'):
            print(f"\n🎓 LEARNING RESOURCES:")
            for i, course in enumerate(self.results['learning_resources'][:3], 1):
                print(f"   {i}. {course['title'][:80]}...")
    
    def save_career_report(self, filename: str = None):
        """Save career report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            degree = self.results['summary']['degree'].replace(' ', '_')
            filename = f"career_report_{degree}_{timestamp}"
        
        # Save as JSON
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Save as HTML report
        self._generate_career_html_report(filename)
        
        print(f"✅ Career report saved as {filename}.json and {filename}.html")

    def _generate_career_html_report(self, filename: str):
        """Generate HTML version of the career report"""
        summary = self.results['summary']
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Career Research Report - {summary['degree']}</title>
            <meta charset="UTF-8">
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; 
                    padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    overflow: hidden;
                }}
                .header {{ 
                    background: linear-gradient(135deg, #2c3e50, #3498db);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{ margin: 0; font-size: 2.5em; }}
                .summary {{ 
                    background: #f8f9fa; 
                    padding: 25px; 
                    border-bottom: 3px solid #e9ecef;
                }}
                .summary-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 15px;
                    margin-top: 15px;
                }}
                .summary-item {{
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .section {{ 
                    padding: 25px; 
                    border-bottom: 1px solid #e9ecef;
                }}
                .section:last-child {{ border-bottom: none; }}
                .article {{ 
                    border: 1px solid #ddd; 
                    padding: 20px; 
                    margin: 15px 0; 
                    border-radius: 8px;
                    background: white;
                    transition: transform 0.2s;
                }}
                .article:hover {{ 
                    transform: translateY(-2px); 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .market-positive {{ color: #27ae60; font-weight: bold; }}
                .market-moderate {{ color: #f39c12; font-weight: bold; }}
                .market-limited {{ color: #e74c3c; font-weight: bold; }}
                .source-badge {{
                    background: #3498db;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 12px;
                    font-size: 0.8em;
                    margin-right: 10px;
                }}
                a {{ color: #2980b9; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .skill-category {{
                    margin: 10px 0;
                    padding: 10px;
                    border-left: 4px solid #3498db;
                    background: #f8f9fa;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎓 Career Research Report</h1>
                    <h2>{summary['degree']} for {summary['experience_level']}</h2>
                    <h3>Skills: {summary['skills_focus']} | Market: {summary['job_market']} | Year: {summary['target_year']}</h3>
                </div>
                
                <div class="summary">
                    <h3>📊 Executive Summary</h3>
                    <div class="summary-grid">
                        <div class="summary-item">
                            <strong>Degree/Qualification:</strong><br>{summary['degree']}
                        </div>
                        <div class="summary-item">
                            <strong>Experience Level:</strong><br>{summary['experience_level']}
                        </div>
                        <div class="summary-item">
                            <strong>Skills Focus:</strong><br>{summary['skills_focus']}
                        </div>
                        <div class="summary-item">
                            <strong>Job Market:</strong><br>{summary['job_market']}
                        </div>
                        <div class="summary-item">
                            <strong>Target Year:</strong><br>{summary['target_year']}
                        </div>
                        <div class="summary-item">
                            <strong>Market Outlook:</strong><br>
                            <span class="market-{summary['market_outlook'].split()[0].lower()}">
                                {summary['market_outlook']}
                            </span>
                        </div>
                        <div class="summary-item">
                            <strong>Sources Analyzed:</strong><br>{summary['total_sources_found']}
                        </div>
                        <div class="summary-item">
                            <strong>Generated:</strong><br>{summary['report_generated']}
                        </div>
                    </div>
                </div>
        """
        
        # Add key findings
        if summary.get('key_findings'):
            html_content += """
            <div class="section">
                <h2>🔍 Key Findings</h2>
            """
            for finding in summary['key_findings']:
                html_content += f'<div class="article"><p>✅ {finding}</p></div>'
            html_content += "</div>"
        
        # Add skill trends
        if self.results.get('skill_trends'):
            trends = self.results['skill_trends']
            html_content += """
            <div class="section">
                <h2>📊 Skill Trends Analysis</h2>
            """
            if trends.get('high_demand_skills'):
                html_content += f"""
                <div class="skill-category">
                    <h3>🚀 High Demand Skills</h3>
                    <p>{', '.join(trends['high_demand_skills'])}</p>
                </div>
                """
            if trends.get('emerging_skills'):
                html_content += f"""
                <div class="skill-category">
                    <h3>🔥 Emerging Skills</h3>
                    <p>{', '.join(trends['emerging_skills'])}</p>
                </div>
                """
            if trends.get('traditional_skills'):
                html_content += f"""
                <div class="skill-category">
                    <h3>💼 Foundational Skills</h3>
                    <p>{', '.join(trends['traditional_skills'])}</p>
                </div>
                """
            html_content += "</div>"
        
        # Add all research sections
        research_sections = [
            ('career_opportunities', '💼 Career Opportunities'),
            ('required_skills', '🔧 Required Skills'),
            ('job_market_trends', '📈 Job Market Trends'),
            ('salary_information', '💰 Salary Information'),
            ('learning_resources', '🎓 Learning Resources'),
            ('community_discussions', '💬 Community Discussions'),
            ('linkedin_insights', '👔 LinkedIn Insights'),
            ('quora_insights', '🤔 Quora Insights')
        ]
        
        for section_key, section_name in research_sections:
            if self.results.get(section_key):
                html_content += f"""
                <div class="section">
                    <h2>{section_name} ({len(self.results[section_key])} results)</h2>
                """
                for item in self.results[section_key]:
                    title = item.get('title', item.get('name', 'No title'))
                    url = item.get('url', item.get('link', '#'))
                    description = item.get('description', item.get('summary', ''))
                    
                    html_content += f"""
                    <div class="article">
                        <h3><a href="{url}" target="_blank">{title}</a></h3>
                        {f'<p>{description}</p>' if description else ''}
                        <div>
                            <span class="source-badge">{section_name}</span>
                            {f"<strong>Published:</strong> {item.get('published', item.get('created', ''))}" if item.get('published') or item.get('created') else ''}
                            {f"<strong>Source:</strong> {item.get('source', item.get('platform', ''))}" if item.get('source') or item.get('platform') else ''}
                            {f"<strong>Score:</strong> 👍 {item.get('score', '')}" if item.get('score') else ''}
                            {f"<strong>Comments:</strong> 💬 {item.get('comments', '')}" if item.get('comments') else ''}
                        </div>
                    </div>
                    """
                html_content += "</div>"
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(f"{filename}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    """Main function to run the career research tool"""
    print("🎓 Career Path Research Tool")
    print("=" * 70)
    print("=" * 70)
    
    research_tool = CareerResearchTool()
    
    while True:
        try:
            user_input = input("\n🔍 Enter your career research query (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            if not user_input:
                continue
                
            degree, experience, skills, job_market, year = research_tool.parse_query(user_input)
            
            if not degree:
                print("❌ Please enter at least a degree/qualification")
                continue
            
            # Generate career report
            print(f"\n🚀 Starting career research for: {degree} - {experience} - {skills}")
            report = research_tool.generate_career_report(degree, experience, skills, job_market, year)
            
            # Display results
            research_tool.display_career_report()
            
            # Save report
            save_choice = input("\n💾 Save career report? (y/n): ").lower()
            if save_choice in ['y', 'yes']:
                research_tool.save_career_report()
                print("✅ Career report saved successfully!")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
 
    main()