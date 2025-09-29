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

class UniversalResearchTool:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.results = defaultdict(dict)
        
    def parse_query(self, query: str) -> tuple:
        """Parse user input into components"""
        parts = query.split(',')
        company = parts[0].strip() if len(parts) > 0 else ""
        topic = parts[1].strip() if len(parts) > 1 else ""
        year = parts[2].strip() if len(parts) > 2 else ""
        
        return company, topic, year
    
    async def fetch_url(self, session, url, source_name):
        """Fetch URL asynchronously"""
        try:
            async with session.get(url, headers=self.headers, timeout=10) as response:
                if response.status == 200:
                    return await response.text(), source_name
                return None, source_name
        except:
            return None, source_name
    
    def search_google_news(self, query: str) -> List[Dict]:
        """Search Google News for relevant articles"""
        try:
            search_url = f"https://news.google.com/rss/search?q={query}"
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'xml')
            
            articles = []
            for item in soup.find_all('item')[:10]:
                article = {
                    'title': item.title.text if item.title else '',
                    'link': item.link.text if item.link else '',
                    'pubDate': item.pubDate.text if item.pubDate else '',
                    'source': item.source.text if item.source else ''
                }
                articles.append(article)
            return articles
        except Exception as e:
            print(f"Error searching Google News: {e}")
            return []
    
    def get_wikipedia_info(self, company: str) -> Dict:
        """Get basic information from Wikipedia"""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return {
                    'description': data.get('extract', ''),
                    'image_url': data.get('thumbnail', {}).get('source', ''),
                    'full_url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                }
        except Exception as e:
            print(f"Error fetching Wikipedia info: {e}")
        return {}
    
    def search_reddit(self, query: str) -> List[Dict]:
        """Search Reddit for discussions"""
        try:
            url = f"https://www.reddit.com/search.json?q={query}&sort=relevance&t=year"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                posts = []
                for post in data['data']['children'][:5]:
                    post_data = post['data']
                    posts.append({
                        'title': post_data.get('title', ''),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'comments': post_data.get('num_comments', 0),
                        'subreddit': post_data.get('subreddit', '')
                    })
                return posts
        except Exception as e:
            print(f"Error searching Reddit: {e}")
        return []
    
    def get_company_news(self, company: str, topic: str = "", year: str = "") -> List[Dict]:
        """Get company-specific news"""
        query = f"{company} {topic} {year}".strip()
        return self.search_google_news(query)
    
    def search_github_discussions(self, query: str) -> List[Dict]:
        """Search GitHub issues and discussions"""
        try:
            url = f"https://api.github.com/search/issues?q={query}+in:title,body"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                discussions = []
                for item in data['items'][:5]:
                    discussions.append({
                        'title': item.get('title', ''),
                        'url': item.get('html_url', ''),
                        'repository': item.get('repository_url', '').split('/')[-1],
                        'state': item.get('state', ''),
                        'comments': item.get('comments', 0)
                    })
                return discussions
        except Exception as e:
            print(f"Error searching GitHub: {e}")
        return []
    
    def search_stack_overflow(self, query: str) -> List[Dict]:
        """Search Stack Overflow for relevant discussions"""
        try:
            url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={query}&site=stackoverflow"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                questions = []
                for item in data['items'][:5]:
                    questions.append({
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'answer_count': item.get('answer_count', 0),
                        'score': item.get('score', 0),
                        'view_count': item.get('view_count', 0)
                    })
                return questions
        except Exception as e:
            print(f"Error searching Stack Overflow: {e}")
        return []
    
    def analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'growth', 'profit']
        negative_words = ['bad', 'poor', 'negative', 'loss', 'layoff', 'cut', 'decline']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"
    
    def generate_report(self, company: str, topic: str, year: str) -> Dict:
        """Generate comprehensive research report"""
        print(f"🔍 Researching {company} - {topic} - {year}...")
        
        # Wikipedia information
        print("📚 Getting Wikipedia information...")
        wiki_info = self.get_wikipedia_info(company)
        self.results['wikipedia'] = wiki_info
        
        # News articles
        print("📰 Searching news sources...")
        news_articles = self.get_company_news(company, topic, year)
        self.results['news'] = news_articles
        
        # Reddit discussions
        print("💬 Searching Reddit...")
        reddit_posts = self.search_reddit(f"{company} {topic} {year}")
        self.results['reddit'] = reddit_posts
        
        # GitHub discussions
        print("💻 Searching GitHub...")
        github_discussions = self.search_github_discussions(f"{company} {topic}")
        self.results['github'] = github_discussions
        
        # Stack Overflow
        print("🔧 Searching Stack Overflow...")
        stack_overflow = self.search_stack_overflow(f"{company} {topic}")
        self.results['stack_overflow'] = stack_overflow
        
        # Generate summary
        self.results['summary'] = self._generate_summary(company, topic, year)
        
        return self.results
    
    def _generate_summary(self, company: str, topic: str, year: str) -> Dict:
        """Generate summary of findings"""
        total_sources = sum(len(items) for key, items in self.results.items() 
                           if key not in ['wikipedia', 'summary'])
        
        # Analyze sentiment from titles
        all_text = ""
        for source in ['news', 'reddit']:
            for item in self.results.get(source, []):
                all_text += item.get('title', '') + " "
        
        sentiment = self.analyze_sentiment(all_text)
        
        return {
            'company': company,
            'topic': topic,
            'year': year,
            'total_sources_found': total_sources,
            'sentiment_analysis': sentiment,
            'report_generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data_sources': list(self.results.keys())
        }
    
    def save_report(self, filename: str = None):
        """Save report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"research_report_{timestamp}"
        
        # Save as JSON
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Save as HTML report
        self._generate_html_report(filename)
        
        print(f"✅ Report saved as {filename}.json and {filename}.html")
    
    def _generate_html_report(self, filename: str):
        """Generate HTML version of the report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Research Report - {self.results['summary']['company']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #f4f4f4; padding: 20px; border-radius: 10px; }}
                .section {{ margin: 30px 0; }}
                .article {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .sentiment-positive {{ color: green; }}
                .sentiment-negative {{ color: red; }}
                .sentiment-neutral {{ color: orange; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Research Report: {self.results['summary']['company']}</h1>
                <p><strong>Topic:</strong> {self.results['summary']['topic']}</p>
                <p><strong>Year:</strong> {self.results['summary']['year']}</p>
                <p><strong>Generated:</strong> {self.results['summary']['report_generated']}</p>
                <p><strong>Sentiment:</strong> <span class="sentiment-{self.results['summary']['sentiment_analysis'].lower()}">{self.results['summary']['sentiment_analysis']}</span></p>
            </div>
        """
        
        # Add Wikipedia info
        if self.results['wikipedia']:
            html_content += f"""
            <div class="section">
                <h2>📚 Wikipedia Summary</h2>
                <p>{self.results['wikipedia'].get('description', 'No description available')}</p>
            </div>
            """
        
        # Add news articles
        if self.results['news']:
            html_content += "<div class='section'><h2>📰 News Articles</h2>"
            for article in self.results['news']:
                html_content += f"""
                <div class="article">
                    <h3><a href="{article.get('link', '#')}">{article.get('title', 'No title')}</a></h3>
                    <p><strong>Source:</strong> {article.get('source', 'Unknown')}</p>
                    <p><strong>Published:</strong> {article.get('pubDate', 'Unknown')}</p>
                </div>
                """
            html_content += "</div>"
        
        # Add Reddit posts
        if self.results['reddit']:
            html_content += "<div class='section'><h2>💬 Reddit Discussions</h2>"
            for post in self.results['reddit']:
                html_content += f"""
                <div class="article">
                    <h3><a href="{post.get('url', '#')}">{post.get('title', 'No title')}</a></h3>
                    <p><strong>Subreddit:</strong> {post.get('subreddit', 'Unknown')}</p>
                    <p><strong>Score:</strong> {post.get('score', 0)} | <strong>Comments:</strong> {post.get('comments', 0)}</p>
                </div>
                """
            html_content += "</div>"
        
        html_content += """
        </body>
        </html>
        """
        
        with open(f"{filename}.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

def main():
    """Main function to run the research tool"""
    print("🌐 Universal Company & Topic Research Tool")
    print("=" * 50)
    print("Enter your search query in format: company,topic,year")
    print("Example: dell,layoff,2025")
    print("Example: microsoft,ai,2024")
    print("Example: tesla,autopilot,2023")
    print("=" * 50)
    
    research_tool = UniversalResearchTool()
    
    while True:
        try:
            user_input = input("\n🔍 Enter your search query (or 'quit' to exit): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            if not user_input:
                continue
                
            company, topic, year = research_tool.parse_query(user_input)
            
            if not company:
                print("❌ Please enter at least a company name")
                continue
            
            # Generate report
            report = research_tool.generate_report(company, topic, year)
            
            # Display summary
            summary = report['summary']
            print(f"\n📊 Report Summary:")
            print(f"   Company: {summary['company']}")
            print(f"   Topic: {summary['topic']}")
            print(f"   Year: {summary['year']}")
            print(f"   Sources Found: {summary['total_sources_found']}")
            print(f"   Sentiment: {summary['sentiment_analysis']}")
            
            # Save report
            save_choice = input("\n💾 Save report? (y/n): ").lower()
            if save_choice in ['y', 'yes']:
                research_tool.save_report()
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Install required packages first:
    # pip install requests beautifulsoup4 pandas aiohttp
    main()