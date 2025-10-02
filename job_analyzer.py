#!/usr/bin/env python3
"""
Comprehensive Job Market Research Tool
Features: Hiring trends, Skills analysis, Layoff tracking, Interview questions
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd
from datetime import datetime, timedelta
import re
from collections import Counter, defaultdict
import urllib.parse
import os

class JobMarketAnalyzer:
    """Comprehensive job market research and analysis tool"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.results = {}
        
    def analyze_job_role(self, job_title):
        """Main analysis function for a job role"""
        print(f"🔍 Comprehensive Job Market Analysis: {job_title}")
        print("=" * 60)
        
        # 1. Get layoff data from layoffs.fyi
        print("📊 1. Analyzing layoff trends...")
        layoff_data = self.get_layoff_data(job_title)
        
        # 2. Research hiring trends
        print("📈 2. Researching hiring trends...")
        hiring_trends = self.get_hiring_trends(job_title)
        
        # 3. Analyze skill requirements
        print("🎯 3. Analyzing skill requirements...")
        skills_data = self.analyze_skills_demand(job_title)
        
        # 4. Get interview questions
        print("💬 4. Gathering interview questions...")
        interview_data = self.get_interview_questions(job_title)
        
        # 5. Market analysis
        print("📊 5. Performing market analysis...")
        market_analysis = self.perform_market_analysis(job_title)
        
        # Compile results
        self.results = {
            'job_title': job_title,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'layoff_data': layoff_data,
            'hiring_trends': hiring_trends,
            'skills_analysis': skills_data,
            'interview_questions': interview_data,
            'market_analysis': market_analysis
        }
        
        return self.results
    
    def get_layoff_data(self, job_title):
        """Scrape layoff data from layoffs.fyi"""
        try:
            url = "https://layoffs.fyi/"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            layoff_stats = {}
            
            # Extract main statistics based on the provided website content
            stats_text = soup.get_text()
            
            # Look for 2025 stats (current year)
            year_pattern = r'(\d{1,3},?\d{3})\s+tech employees laid off.*?(\d{1,3})\s+tech companies.*?In 2025'
            year_match = re.search(year_pattern, stats_text)
            if year_match:
                layoff_stats['2025'] = {
                    'employees_laid_off': year_match.group(1).replace(',', ''),
                    'companies_affected': year_match.group(2)
                }
            
            # Look for 2024 stats  
            year_2024_pattern = r'(\d{1,3},?\d{3})\s+tech employees laid off.*?(\d{1,3})\s+tech companies.*?In 2024'
            year_2024_match = re.search(year_2024_pattern, stats_text)
            if year_2024_match:
                layoff_stats['2024'] = {
                    'employees_laid_off': year_2024_match.group(1).replace(',', ''),
                    'companies_affected': year_2024_match.group(2)
                }
            
            # Get recent company layoffs from tables
            recent_layoffs = []
            tables = soup.find_all('table')
            if tables:
                for table in tables[:1]:  # First table usually has recent data
                    rows = table.find_all('tr')[1:11]  # Top 10 recent
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) >= 3:
                            company = cells[0].get_text(strip=True)
                            laid_off = cells[1].get_text(strip=True)
                            date = cells[2].get_text(strip=True) if len(cells) > 2 else 'N/A'
                            recent_layoffs.append({
                                'company': company,
                                'employees_laid_off': laid_off,
                                'date': date
                            })
            
            return {
                'statistics': layoff_stats,
                'recent_layoffs': recent_layoffs,
                'job_relevance': self.assess_layoff_relevance(job_title, recent_layoffs),
                'source': 'https://layoffs.fyi/'
            }
            
        except Exception as e:
            print(f"⚠️ Error fetching layoff data: {e}")
            return {'error': str(e), 'source': 'https://layoffs.fyi/'}
    
    def assess_layoff_relevance(self, job_title, layoffs):
        """Assess how layoffs affect the specific job role"""
        job_keywords = job_title.lower().split()
        relevant_layoffs = []
        
        for layoff in layoffs:
            company = layoff['company'].lower()
            # Simple relevance check
            if any(keyword in company for keyword in job_keywords):
                relevant_layoffs.append(layoff)
        
        return {
            'relevant_layoffs': relevant_layoffs,
            'impact_assessment': self.get_impact_assessment(len(relevant_layoffs), len(layoffs))
        }
    
    def get_impact_assessment(self, relevant_count, total_count):
        """Assess the impact level"""
        if total_count == 0:
            return "No recent layoff data available"
        
        percentage = (relevant_count / total_count) * 100
        
        if percentage > 20:
            return "High impact - Many relevant companies affected"
        elif percentage > 10:
            return "Moderate impact - Some relevant companies affected"
        elif percentage > 0:
            return "Low impact - Few relevant companies affected"
        else:
            return "Minimal impact - No directly relevant companies in recent layoffs"
    
    def get_hiring_trends(self, job_title):
        """Research hiring trends from multiple sources"""
        trends = {}
        
        # Search Indeed for job postings
        indeed_data = self.search_indeed_jobs(job_title)
        trends['indeed'] = indeed_data
        
        # Search LinkedIn Jobs
        linkedin_data = self.search_linkedin_jobs(job_title)
        trends['linkedin'] = linkedin_data
        
        # General job market search
        market_data = self.search_job_market_trends(job_title)
        trends['market_trends'] = market_data
        
        return trends
    
    def search_indeed_jobs(self, job_title):
        """Search Indeed for job data"""
        try:
            query = f"{job_title} jobs"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q=site:indeed.com+{encoded_query}"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            jobs_data = []
            results = soup.find_all('div', class_='g')[:10]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                desc_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                
                if title_elem and link_elem:
                    jobs_data.append({
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href', ''),
                        'description': desc_elem.get_text() if desc_elem else ''
                    })
            
            return {
                'job_postings_found': len(jobs_data),
                'sample_jobs': jobs_data[:5],
                'trend_assessment': self.assess_hiring_trend(len(jobs_data))
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def search_linkedin_jobs(self, job_title):
        """Search LinkedIn for job data"""
        try:
            query = f"{job_title} jobs hiring"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q=site:linkedin.com+{encoded_query}"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            linkedin_data = []
            results = soup.find_all('div', class_='g')[:8]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                
                if title_elem and link_elem:
                    linkedin_data.append({
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href', '')
                    })
            
            return {
                'professional_opportunities': len(linkedin_data),
                'sample_opportunities': linkedin_data[:3],
                'networking_potential': self.assess_networking_potential(len(linkedin_data))
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def search_job_market_trends(self, job_title):
        """Search for general job market trends"""
        try:
            query = f"{job_title} job market trends 2024 2025 hiring"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            trend_articles = []
            results = soup.find_all('div', class_='g')[:10]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                desc_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                
                if title_elem and link_elem:
                    trend_articles.append({
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href', ''),
                        'snippet': desc_elem.get_text() if desc_elem else ''
                    })
            
            return {
                'trend_articles_found': len(trend_articles),
                'market_insights': trend_articles[:5],
                'trend_analysis': self.analyze_trend_content(trend_articles)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_skills_demand(self, job_title):
        """Analyze skills demand for the job role"""
        skills_data = {}
        
        # Search for skill requirements
        skills_search = self.search_skills_requirements(job_title)
        skills_data['requirements'] = skills_search
        
        # Get salary data
        salary_data = self.get_salary_data(job_title)
        skills_data['salary_insights'] = salary_data
        
        # Analyze skill trends
        skill_trends = self.analyze_skill_trends(job_title)
        skills_data['trends'] = skill_trends
        
        return skills_data
    
    def search_skills_requirements(self, job_title):
        """Search for skills requirements"""
        try:
            query = f"{job_title} skills required qualifications"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            skills_content = []
            results = soup.find_all('div', class_='g')[:10]
            
            for result in results:
                title_elem = result.find('h3')
                desc_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                
                if title_elem and desc_elem:
                    skills_content.append({
                        'title': title_elem.get_text(),
                        'content': desc_elem.get_text()
                    })
            
            # Extract common skills
            extracted_skills = self.extract_skills_from_content(skills_content)
            
            return {
                'skills_sources': len(skills_content),
                'extracted_skills': extracted_skills,
                'skill_categories': self.categorize_skills(extracted_skills)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def extract_skills_from_content(self, content_list):
        """Extract skills from job descriptions"""
        # Common technical skills
        tech_skills = [
            'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'angular', 'vue',
            'node.js', 'django', 'flask', 'spring', 'mongodb', 'postgresql', 'mysql',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'jenkins', 'terraform',
            'machine learning', 'data science', 'artificial intelligence', 'deep learning',
            'tableau', 'power bi', 'excel', 'r', 'scala', 'spark', 'hadoop'
        ]
        
        # Soft skills
        soft_skills = [
            'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
            'project management', 'agile', 'scrum', 'critical thinking', 'creativity'
        ]
        
        all_content = ' '.join([item['content'].lower() for item in content_list])
        
        found_tech_skills = [skill for skill in tech_skills if skill in all_content]
        found_soft_skills = [skill for skill in soft_skills if skill in all_content]
        
        return {
            'technical_skills': found_tech_skills,
            'soft_skills': found_soft_skills,
            'total_skills_identified': len(found_tech_skills) + len(found_soft_skills)
        }
    
    def categorize_skills(self, skills_data):
        """Categorize skills by type"""
        categories = {
            'programming': [],
            'databases': [],
            'cloud': [],
            'analytics': [],
            'soft_skills': skills_data.get('soft_skills', [])
        }
        
        tech_skills = skills_data.get('technical_skills', [])
        
        for skill in tech_skills:
            if skill in ['python', 'java', 'javascript', 'html', 'css', 'react', 'angular', 'vue', 'node.js']:
                categories['programming'].append(skill)
            elif skill in ['sql', 'mongodb', 'postgresql', 'mysql']:
                categories['databases'].append(skill)
            elif skill in ['aws', 'azure', 'gcp', 'docker', 'kubernetes']:
                categories['cloud'].append(skill)
            elif skill in ['tableau', 'power bi', 'excel', 'r', 'machine learning', 'data science']:
                categories['analytics'].append(skill)
        
        return categories
    
    def get_salary_data(self, job_title):
        """Get salary information"""
        try:
            query = f"{job_title} salary 2024 2025"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            salary_info = []
            results = soup.find_all('div', class_='g')[:8]
            
            for result in results:
                title_elem = result.find('h3')
                desc_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                
                if title_elem and desc_elem:
                    content = desc_elem.get_text()
                    # Look for salary figures
                    salary_pattern = r'\$[\d,]+(?:k|,000)?'
                    salaries = re.findall(salary_pattern, content)
                    
                    if salaries:
                        salary_info.append({
                            'source': title_elem.get_text(),
                            'salaries_mentioned': salaries,
                            'content': content[:200] + '...'
                        })
            
            return {
                'salary_sources': len(salary_info),
                'salary_data': salary_info[:5],
                'salary_analysis': self.analyze_salary_ranges(salary_info)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_salary_ranges(self, salary_info):
        """Analyze salary ranges from collected data"""
        all_salaries = []
        for info in salary_info:
            for salary in info.get('salaries_mentioned', []):
                # Convert salary strings to numbers
                salary_clean = salary.replace('$', '').replace(',', '').replace('k', '000')
                try:
                    all_salaries.append(int(salary_clean))
                except:
                    continue
        
        if all_salaries:
            return {
                'min_salary': min(all_salaries),
                'max_salary': max(all_salaries),
                'avg_salary': sum(all_salaries) // len(all_salaries),
                'salary_count': len(all_salaries)
            }
        
        return {'analysis': 'No salary data found'}
    
    def analyze_skill_trends(self, job_title):
        """Analyze trending skills for the role"""
        try:
            query = f"{job_title} trending skills 2024 2025 in demand"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            trend_content = []
            results = soup.find_all('div', class_='g')[:8]
            
            for result in results:
                desc_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                if desc_elem:
                    trend_content.append(desc_elem.get_text())
            
            # Analyze trends
            all_content = ' '.join(trend_content).lower()
            
            emerging_keywords = ['ai', 'machine learning', 'cloud', 'automation', 'blockchain', 'cybersecurity']
            trend_analysis = {}
            
            for keyword in emerging_keywords:
                count = all_content.count(keyword)
                if count > 0:
                    trend_analysis[keyword] = count
            
            return {
                'trending_skills': sorted(trend_analysis.items(), key=lambda x: x[1], reverse=True),
                'trend_summary': self.generate_trend_summary(trend_analysis)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_trend_summary(self, trends):
        """Generate a summary of skill trends"""
        if not trends:
            return "No clear trending skills identified"
        
        top_trend = max(trends.items(), key=lambda x: x[1])
        return f"Most mentioned emerging skill: {top_trend[0]} (mentioned {top_trend[1]} times)"
    
    def get_interview_questions(self, job_title):
        """Get common interview questions for the role"""
        try:
            query = f"{job_title} interview questions common asked"
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.google.com/search?q={encoded_query}"
            
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            interview_sources = []
            results = soup.find_all('div', class_='g')[:10]
            
            for result in results:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                desc_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                
                if title_elem and link_elem:
                    interview_sources.append({
                        'title': title_elem.get_text(),
                        'link': link_elem.get('href', ''),
                        'preview': desc_elem.get_text() if desc_elem else ''
                    })
            
            # Extract potential questions from content
            questions = self.extract_interview_questions(interview_sources)
            
            return {
                'interview_sources': len(interview_sources),
                'source_links': interview_sources[:5],
                'common_questions': questions,
                'preparation_tips': self.generate_interview_tips(job_title)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def extract_interview_questions(self, sources):
        """Extract interview questions from source content"""
        # Common question patterns
        common_questions = [
            "Tell me about yourself",
            "Why do you want this position?",
            "What are your strengths and weaknesses?",
            "Describe a challenging project you worked on",
            "Where do you see yourself in 5 years?",
            "Why are you leaving your current job?",
            "What interests you about our company?",
            "Describe your experience with [relevant technology]",
            "How do you handle tight deadlines?",
            "Give an example of when you solved a complex problem"
        ]
        
        # Look for question indicators in content
        all_content = ' '.join([source['preview'].lower() for source in sources])
        question_indicators = ['interview questions', 'commonly asked', 'prepare for', 'expect to be asked']
        
        relevance_score = sum(1 for indicator in question_indicators if indicator in all_content)
        
        return {
            'standard_questions': common_questions,
            'source_relevance': f"{relevance_score}/4 question indicators found",
            'recommendation': "Review role-specific technical questions based on job requirements"
        }
    
    def generate_interview_tips(self, job_title):
        """Generate interview preparation tips"""
        return [
            f"Research the company's recent projects and initiatives",
            f"Prepare specific examples demonstrating {job_title} skills",
            "Practice explaining technical concepts in simple terms",
            "Prepare questions about team structure and growth opportunities",
            "Review your portfolio/projects and be ready to discuss them",
            "Stay updated on industry trends and challenges"
        ]
    
    def perform_market_analysis(self, job_title):
        """Perform comprehensive market analysis"""
        analysis = {}
        
        # Market outlook
        outlook = self.assess_market_outlook(job_title)
        analysis['market_outlook'] = outlook
        
        # Competition analysis
        competition = self.analyze_competition_level(job_title)
        analysis['competition'] = competition
        
        # Growth potential
        growth = self.assess_growth_potential(job_title)
        analysis['growth_potential'] = growth
        
        return analysis
    
    def assess_market_outlook(self, job_title):
        """Assess overall market outlook"""
        # Based on collected data
        outlook_factors = []
        
        if hasattr(self, 'results'):
            # Check layoff impact
            layoff_data = self.results.get('layoff_data', {})
            layoff_relevance = layoff_data.get('job_relevance', {})
            impact = layoff_relevance.get('impact_assessment', '')
            
            if 'minimal' in impact.lower() or 'low' in impact.lower():
                outlook_factors.append("Positive - Low layoff impact")
            elif 'high' in impact.lower():
                outlook_factors.append("Caution - High layoff impact")
            
            # Check hiring trends
            hiring_data = self.results.get('hiring_trends', {})
            indeed_data = hiring_data.get('indeed', {})
            job_count = indeed_data.get('job_postings_found', 0)
            
            if job_count > 15:
                outlook_factors.append("Positive - Strong job posting activity")
            elif job_count < 5:
                outlook_factors.append("Caution - Limited job postings")
        
        overall_sentiment = "Neutral"
        if len([f for f in outlook_factors if "Positive" in f]) > len([f for f in outlook_factors if "Caution" in f]):
            overall_sentiment = "Positive"
        elif len([f for f in outlook_factors if "Caution" in f]) > len([f for f in outlook_factors if "Positive" in f]):
            overall_sentiment = "Cautious"
        
        return {
            'overall_sentiment': overall_sentiment,
            'key_factors': outlook_factors,
            'recommendation': self.get_market_recommendation(overall_sentiment)
        }
    
    def get_market_recommendation(self, sentiment):
        """Get market recommendation based on sentiment"""
        if sentiment == "Positive":
            return "Good time to pursue opportunities in this field"
        elif sentiment == "Cautious":
            return "Consider timing and focus on skill development"
        else:
            return "Monitor market conditions and prepare for opportunities"
    
    def analyze_competition_level(self, job_title):
        """Analyze competition level for the role"""
        return {
            'assessment': 'Moderate',
            'factors': [
                'Skills demand vs supply',
                'Number of qualified candidates',
                'Barrier to entry'
            ],
            'advice': 'Focus on developing unique skill combinations'
        }
    
    def assess_growth_potential(self, job_title):
        """Assess career growth potential"""
        return {
            'short_term': 'Stable demand expected',
            'long_term': 'Growth dependent on industry evolution',
            'key_growth_drivers': [
                'Technology advancement',
                'Digital transformation',
                'Market expansion'
            ]
        }
    
    def assess_hiring_trend(self, job_count):
        """Assess hiring trend based on job count"""
        if job_count > 20:
            return "Strong hiring activity"
        elif job_count > 10:
            return "Moderate hiring activity"
        elif job_count > 5:
            return "Limited hiring activity"
        else:
            return "Minimal hiring activity"
    
    def assess_networking_potential(self, opportunity_count):
        """Assess networking potential"""
        if opportunity_count > 10:
            return "High networking potential"
        elif opportunity_count > 5:
            return "Moderate networking potential"
        else:
            return "Limited networking opportunities"
    
    def analyze_trend_content(self, articles):
        """Analyze content from trend articles"""
        if not articles:
            return "No trend data available"
        
        positive_indicators = ['growth', 'increasing', 'demand', 'expanding', 'opportunity']
        negative_indicators = ['decline', 'decreasing', 'layoffs', 'reduction', 'challenging']
        
        all_content = ' '.join([article['snippet'].lower() for article in articles])
        
        positive_count = sum(1 for indicator in positive_indicators if indicator in all_content)
        negative_count = sum(1 for indicator in negative_indicators if indicator in all_content)
        
        if positive_count > negative_count:
            return f"Positive trend indicators (found {positive_count} positive vs {negative_count} negative signals)"
        elif negative_count > positive_count:
            return f"Negative trend indicators (found {negative_count} negative vs {positive_count} positive signals)"
        else:
            return f"Mixed trend indicators (balanced positive/negative signals)"
    
    def display_summary(self):
        """Display a quick summary in console"""
        if not self.results:
            print("❌ No analysis results available")
            return
        
        job_title = self.results['job_title']
        print(f"\n📋 ANALYSIS SUMMARY: {job_title}")
        print("=" * 60)
        
        # Layoff impact
        layoff_data = self.results.get('layoff_data', {})
        if layoff_data and not layoff_data.get('error'):
            impact = layoff_data.get('job_relevance', {}).get('impact_assessment', 'N/A')
            print(f"📊 Layoff Impact: {impact}")
        
        # Hiring trends
        hiring_trends = self.results.get('hiring_trends', {})
        indeed_data = hiring_trends.get('indeed', {})
        if indeed_data and not indeed_data.get('error'):
            job_count = indeed_data.get('job_postings_found', 0)
            print(f"📈 Job Postings Found: {job_count}")
        
        # Skills summary
        skills_data = self.results.get('skills_analysis', {})
        requirements = skills_data.get('requirements', {})
        if requirements and not requirements.get('error'):
            total_skills = requirements.get('extracted_skills', {}).get('total_skills_identified', 0)
            print(f"🎯 Skills Identified: {total_skills}")
        
        # Market outlook
        market_analysis = self.results.get('market_analysis', {})
        outlook = market_analysis.get('market_outlook', {})
        if outlook:
            sentiment = outlook.get('overall_sentiment', 'N/A')
            print(f"📊 Market Sentiment: {sentiment}")
        
        print("=" * 60)
