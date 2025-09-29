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
import feedparser  # For RSS/XML feeds

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
    
    def search_google_news(self, query: str) -> List[Dict]:
        """Search Google News for relevant articles using feedparser"""
        try:
            search_url = f"https://news.google.com/rss/search?q={query}"
            news_feed = feedparser.parse(search_url)
            
            articles = []
            for entry in news_feed.entries[:15]:  # Get top 15 results
                article = {
                    'title': entry.title if hasattr(entry, 'title') else '',
                    'link': entry.link if hasattr(entry, 'link') else '',
                    'published': entry.published if hasattr(entry, 'published') else '',
                    'source': entry.source.title if hasattr(entry, 'source') else 'Unknown'
                }
                articles.append(article)
            return articles
        except Exception as e:
            print(f"Error searching Google News: {e}")
            return []
    
    def get_wikipedia_info(self, company: str) -> Dict:
        """Get basic information from Wikipedia"""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company.replace(' ', '_')}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'description': data.get('extract', 'No description available'),
                    'image_url': data.get('thumbnail', {}).get('source', ''),
                    'full_url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                }
            else:
                return {'description': f'No Wikipedia page found for {company}'}
        except Exception as e:
            print(f"Error fetching Wikipedia info: {e}")
            return {'description': f'Error fetching Wikipedia info: {e}'}
    
    def search_reddit(self, query: str) -> List[Dict]:
        """Search Reddit for discussions"""
        try:
            url = f"https://www.reddit.com/search.json?q={query}&sort=relevance&limit=10"
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
                        'subreddit': post_data.get('subreddit', '')
                    })
                return posts
            return []
        except Exception as e:
            print(f"Error searching Reddit: {e}")
            return []
    
    def search_github(self, query: str) -> List[Dict]:
        """Search GitHub for relevant repositories and discussions"""
        try:
            url = f"https://api.github.com/search/repositories?q={query}&sort=updated&per_page=10"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                repos = []
                for repo in data['items'][:5]:
                    repos.append({
                        'name': repo.get('name', ''),
                        'full_name': repo.get('full_name', ''),
                        'description': repo.get('description', ''),
                        'url': repo.get('html_url', ''),
                        'stars': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                        'updated': repo.get('updated_at', '')
                    })
                return repos
            return []
        except Exception as e:
            print(f"Error searching GitHub: {e}")
            return []
    
    def search_news_api(self, query: str) -> List[Dict]:
        """Search news using NewsAPI (you'll need to add your API key)"""
        try:
            # You need to get a free API key from https://newsapi.org/
            api_key = "nigga"  # Replace with your actual API key
            if api_key == "nigga":
                return []  # Skip if no API key
                
            url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={api_key}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('articles', [])[:10]:
                    articles.append({
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'publishedAt': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'description': article.get('description', '')
                    })
                return articles
            return []
        except Exception as e:
            print(f"Error with NewsAPI: {e}")
            return []
    
    def search_bing_news(self, query: str) -> List[Dict]:
        """Search Bing News as an alternative"""
        try:
            # Using a simple web search approach
            search_url = f"https://www.bing.com/news/search?q={query}"
            response = requests.get(search_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            # Look for news cards (this selector might need updating)
            news_cards = soup.find_all('div', class_='news-card') or soup.find_all('div', attrs={'class': re.compile('news')})
            
            for card in news_cards[:10]:
                title_elem = card.find('a', class_='title') or card.find('h2') or card.find('a')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    if link and not link.startswith('http'):
                        link = 'https://www.bing.com' + link
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'source': 'Bing News'
                    })
            return articles
        except Exception as e:
            print(f"Error searching Bing News: {e}")
            return []
    
    def analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        if not text:
            return "Neutral"
            
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'growth', 'profit', 
                         'amazing', 'outstanding', 'beneficial', 'progress', 'achievement']
        negative_words = ['bad', 'poor', 'negative', 'loss', 'layoff', 'cut', 'decline', 
                         'problem', 'issue', 'challenge', 'difficulty', 'crisis']
        
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
        
        search_query = f"{company} {topic} {year}".strip()
        
        # Wikipedia information
        print("📚 Getting Wikipedia information...")
        wiki_info = self.get_wikipedia_info(company)
        self.results['wikipedia'] = wiki_info
        
        # News articles from multiple sources
        print("📰 Searching Google News...")
        news_articles = self.search_google_news(search_query)
        self.results['google_news'] = news_articles
        
        print("🔍 Searching Bing News...")
        bing_news = self.search_bing_news(search_query)
        self.results['bing_news'] = bing_news
        
        # Additional news sources (if API key available)
        news_api_articles = self.search_news_api(search_query)
        if news_api_articles:
            self.results['news_api'] = news_api_articles
        
        # Reddit discussions
        print("💬 Searching Reddit...")
        reddit_posts = self.search_reddit(search_query)
        self.results['reddit'] = reddit_posts
        
        # GitHub repositories
        print("💻 Searching GitHub...")
        github_repos = self.search_github(search_query)
        self.results['github'] = github_repos
        
        # Generate summary
        self.results['summary'] = self._generate_summary(company, topic, year)
        
        return self.results
    
    def _generate_summary(self, company: str, topic: str, year: str) -> Dict:
        """Generate summary of findings"""
        total_articles = 0
        all_text = ""
        
        for source in ['google_news', 'bing_news', 'news_api', 'reddit', 'github']:
            items = self.results.get(source, [])
            total_articles += len(items)
            
            # Collect text for sentiment analysis
            for item in items:
                all_text += item.get('title', '') + " "
                all_text += item.get('description', '') + " "
        
        sentiment = self.analyze_sentiment(all_text)
        
        return {
            'company': company,
            'topic': topic,
            'year': year,
            'total_sources_found': total_articles,
            'sentiment_analysis': sentiment,
            'report_generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data_sources': list(self.results.keys())
        }
    
    def display_results(self):
        """Display results in a formatted way"""
        summary = self.results['summary']
        
        print(f"\n{'='*60}")
        print(f"📊 RESEARCH REPORT SUMMARY")
        print(f"{'='*60}")
        print(f"🏢 Company: {summary['company']}")
        print(f"📝 Topic: {summary['topic']}")
        print(f"📅 Year: {summary['year']}")
        print(f"📈 Total Sources Found: {summary['total_sources_found']}")
        print(f"😊 Sentiment: {summary['sentiment_analysis']}")
        print(f"🕒 Generated: {summary['report_generated']}")
        print(f"{'='*60}")
        
        # Display Wikipedia summary
        if self.results['wikipedia'] and self.results['wikipedia'].get('description'):
            print(f"\n📚 Wikipedia Summary:")
            print(f"   {self.results['wikipedia']['description'][:300]}...")
        
        # Display news highlights
        news_sources = ['google_news', 'bing_news', 'news_api']
        for source in news_sources:
            if self.results.get(source):
                print(f"\n📰 {source.replace('_', ' ').title()} ({len(self.results[source])} articles):")
                for i, article in enumerate(self.results[source][:3], 1):
                    print(f"   {i}. {article['title'][:80]}...")
        
        # Display Reddit highlights
        if self.results.get('reddit'):
            print(f"\n💬 Reddit Discussions ({len(self.results['reddit'])} posts):")
            for i, post in enumerate(self.results['reddit'][:3], 1):
                print(f"   {i}. {post['title'][:80]}...")
                print(f"      👍 Score: {post['score']} | 💬 Comments: {post['comments']}")
    
    def save_report(self, filename: str = None):
        """Save report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            company = self.results['summary']['company'].replace(' ', '_')
            filename = f"{company}_research_report_{timestamp}"
        
        # Save as JSON
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Save as HTML report
        self._generate_html_report(filename)
        
        print(f"✅ Report saved as {filename}.json and {filename}.html")
    
    def _generate_html_report(self, filename: str):
        """Generate HTML version of the report"""
        summary = self.results['summary']
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Research Report - {summary['company']}</title>
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
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
                .sentiment-positive {{ color: #27ae60; font-weight: bold; }}
                .sentiment-negative {{ color: #e74c3c; font-weight: bold; }}
                .sentiment-neutral {{ color: #f39c12; font-weight: bold; }}
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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 Research Report</h1>
                    <h2>{summary['company']} - {summary['topic']} - {summary['year']}</h2>
                </div>
                
                <div class="summary">
                    <h3>📊 Executive Summary</h3>
                    <div class="summary-grid">
                        <div class="summary-item">
                            <strong>Company:</strong><br>{summary['company']}
                        </div>
                        <div class="summary-item">
                            <strong>Topic:</strong><br>{summary['topic']}
                        </div>
                        <div class="summary-item">
                            <strong>Year:</strong><br>{summary['year']}
                        </div>
                        <div class="summary-item">
                            <strong>Sources Found:</strong><br>{summary['total_sources_found']}
                        </div>
                        <div class="summary-item">
                            <strong>Sentiment:</strong><br>
                            <span class="sentiment-{summary['sentiment_analysis'].lower()}">
                                {summary['sentiment_analysis']}
                            </span>
                        </div>
                        <div class="summary-item">
                            <strong>Generated:</strong><br>{summary['report_generated']}
                        </div>
                    </div>
                </div>
        """
        
        # Add Wikipedia info
        if self.results['wikipedia'] and self.results['wikipedia'].get('description'):
            html_content += f"""
            <div class="section">
                <h2>📚 Wikipedia Summary</h2>
                <div class="article">
                    <p>{self.results['wikipedia'].get('description', 'No description available')}</p>
                    {f'<p><a href="{self.results["wikipedia"].get("full_url", "#")}">Read more on Wikipedia</a></p>' if self.results['wikipedia'].get('full_url') else ''}
                </div>
            </div>
            """
        
        # Add news articles from all sources
        news_sources = [
            ('google_news', 'Google News'),
            ('bing_news', 'Bing News'), 
            ('news_api', 'News API'),
            ('reddit', 'Reddit Discussions'),
            ('github', 'GitHub Repositories')
        ]
        
        for source_key, source_name in news_sources:
            if self.results.get(source_key):
                html_content += f"""
                <div class="section">
                    <h2>📰 {source_name} ({len(self.results[source_key])} results)</h2>
                """
                for item in self.results[source_key]:
                    title = item.get('title', item.get('name', 'No title'))
                    url = item.get('url', item.get('link', '#'))
                    description = item.get('description', '')
                    
                    html_content += f"""
                    <div class="article">
                        <h3><a href="{url}" target="_blank">{title}</a></h3>
                        {f'<p>{description}</p>' if description else ''}
                        <div>
                            <span class="source-badge">{source_name}</span>
                            {f"<strong>Published:</strong> {item.get('published', item.get('publishedAt', item.get('updated', '')))}" if item.get('published') or item.get('publishedAt') or item.get('updated') else ''}
                            {f"<strong>Source:</strong> {item.get('source', '')}" if item.get('source') else ''}
                            {f"<strong>Stars:</strong> ⭐ {item.get('stars', '')}" if item.get('stars') else ''}
                            {f"<strong>Score:</strong> 👍 {item.get('score', '')}" if item.get('score') else ''}
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
    """Main function to run the research tool"""
    print("🌐 Universal Company & Topic Research Tool")
    print("=" * 60)
    print("Enter your search query in format: company,topic,year")
    print("Example: dell,layoff,2025")
    print("Example: microsoft,ai,2024")
    print("Example: tesla,autopilot,2023")
    print("=" * 60)
    
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
            print(f"\n🚀 Starting research for: {company} - {topic} - {year}")
            report = research_tool.generate_report(company, topic, year)
            
            # Display results
            research_tool.display_results()
            
            # Save report
            save_choice = input("\n💾 Save report? (y/n): ").lower()
            if save_choice in ['y', 'yes']:
                research_tool.save_report()
                print("✅ Report saved successfully!")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Install required packages first:
    # pip install requests beautifulsoup4 pandas feedparser
    
    main()