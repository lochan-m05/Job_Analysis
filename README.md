# 🔍 Comprehensive Job Market Research Tool

A powerful Python tool that provides comprehensive job market analysis including layoff tracking, hiring trends, skills analysis, and interview preparation.

## 🌟 Features

- **📊 Real-time Layoff Tracking**: Uses [layoffs.fyi](https://layoffs.fyi/) to get current tech layoff data
- **📈 Hiring Trends Analysis**: Searches job boards like Indeed and LinkedIn for current opportunities
- **🎯 Skills Demand Analysis**: Identifies in-demand skills and market requirements for any role
- **💬 Interview Questions**: Provides common interview questions specific to the job role
- **📊 Market Outlook**: Assesses overall market sentiment and growth potential
- **📁 HTML Reports**: Generates beautiful, detailed HTML reports with all findings

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Tool**:
   ```bash
   python main.py
   ```

3. **Enter a Job Title** when prompted (e.g., "Data Scientist", "Software Engineer", "Product Manager")

4. **Wait for Analysis** (30-60 seconds) while the tool:
   - Scrapes layoff data from layoffs.fyi
   - Analyzes hiring trends across job boards
   - Identifies skill requirements
   - Gathers interview questions
   - Performs market analysis

5. **Review Results**:
   - Console summary with key metrics
   - Detailed HTML report with visualizations
   - Raw JSON data for further analysis

## 📊 Example Output

For a "Data Scientist" analysis, you'll get:

### Console Summary
```
📋 ANALYSIS SUMMARY: Data Scientist
============================================================
📊 Layoff Impact: Minimal impact - No directly relevant companies in recent layoffs
📈 Job Postings Found: 15
🎯 Skills Identified: 12
📊 Market Sentiment: Positive
============================================================
```

### HTML Report Sections
- **Layoff Analysis**: Current layoff statistics with impact assessment
- **Hiring Trends**: Job posting counts and networking opportunities
- **Skills Analysis**: Required skills categorized by type with salary insights
- **Interview Preparation**: Common questions and preparation tips
- **Market Analysis**: Overall sentiment and growth potential

## 🎯 Supported Analysis Types

The tool works for any job role:
- **Tech Roles**: Software Engineer, Data Scientist, DevOps Engineer, etc.
- **Business Roles**: Product Manager, Business Analyst, Marketing Manager, etc.
- **Creative Roles**: UX Designer, Content Writer, Graphic Designer, etc.
- **Finance Roles**: Financial Analyst, Investment Banking, Accounting, etc.

## 📁 File Structure

```
Job_Analysis/
├── main.py              # Main entry point
├── job_analyzer.py      # Core analysis functionality
├── report_generator.py  # HTML report generation
├── demo.py             # Demo script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Technical Details

### Data Sources
- **Layoffs**: [layoffs.fyi](https://layoffs.fyi/) - Real-time tech layoff tracker
- **Job Trends**: Google search across Indeed, LinkedIn, and job market sites
- **Skills**: Analysis of job descriptions and requirements
- **Interviews**: Research from interview preparation sites

### Key Algorithms
- **Relevance Assessment**: Matches layoffs to specific job roles
- **Trend Analysis**: Sentiment analysis of market content
- **Skills Extraction**: Pattern matching for technical and soft skills
- **Impact Scoring**: Quantitative assessment of market factors

## 🎨 Sample HTML Report

The generated HTML reports include:
- **Professional Styling**: Clean, modern design with color-coded metrics
- **Interactive Elements**: Clickable links to source data
- **Data Visualization**: Tables, grids, and highlighted key insights
- **Mobile Responsive**: Works on desktop and mobile devices

## 📈 Use Cases

- **Job Seekers**: Research market conditions before applying
- **Career Changers**: Understand skill requirements for new roles
- **Recruiters**: Get market insights for talent acquisition
- **HR Professionals**: Monitor industry trends and compensation
- **Students**: Research career paths and required skills

## 🛠️ Dependencies

- `requests` - Web scraping and HTTP requests
- `beautifulsoup4` - HTML parsing
- `pandas` - Data manipulation
- `urllib` - URL encoding

## 🚨 Legal & Ethical Usage

This tool is for research and educational purposes. It:
- Respects robots.txt and rate limits
- Uses publicly available data
- Does not store personal information
- Provides attribution to data sources

## 🤝 Contributing

Feel free to enhance the tool by:
- Adding new data sources
- Improving analysis algorithms
- Enhancing the HTML report design
- Adding new metrics and insights

## 📞 Support

If you encounter any issues:
1. Check your internet connection
2. Verify dependencies are installed
3. Try with different job titles
4. Check the console for error messages

---

**Happy Job Market Research! 🎯**
