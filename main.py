#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Data Scientist Agent
Automated research and analysis tool using Gemini API

Author: Angel Sakura
Version: 1.0.0
"""

import os
import sys
import logging
from dotenv import load_dotenv
from data_scraper import DataScraper
from data_analyzer import DataAnalyzer
from report_generator import ReportGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def validate_api_key():
    """Validate that Gemini API key is configured"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error('GOOGLE_API_KEY not found. Set it as environment variable.')
        sys.exit(1)
    return api_key


def main():
    """
    Main function to orchestrate the AI agent workflow
    
    Flow:
    1. Collect data from multiple sources (web scraping, APIs)
    2. Analyze data using Gemini AI
    3. Generate structured markdown report
    4. Save report to file
    """
    try:
        # Validate prerequisites
        api_key = validate_api_key()
        logger.info('API key validated successfully')
        
        # Get input from user
        print('\n' + '='*60)
        print('AI DATA SCIENTIST AGENT - v1.0.0')
        print('='*60)
        
        search_query = input('\n[INPUT] Enter company or person name to research: ').strip()

        if not search_query:
            logger.warning('Empty search query provided')
            print('Error: Please provide a valid search query')
            sys.exit(1)

        logger.info(f'Starting research on: {search_query}')
        print(f'\n[PROCESS] Starting research on: {search_query}')
        print('='*60)

        # Step 1: Scrape data
        print('\n[Step 1/3] Collecting data from multiple sources...')
        logger.info('Initializing DataScraper')
        scraper = DataScraper(api_key=api_key)
        data = scraper.scrape(search_query)
        logger.info(f'Data collected: {len(data.get("sources", []))} sources')
        print(f'  ✓ Collected data from {len(data.get("sources", []))} sources')

        # Step 2: Analyze data
        print('\n[Step 2/3] Analyzing data with Gemini AI...')
        logger.info('Initializing DataAnalyzer')
        analyzer = DataAnalyzer(api_key=api_key)
        insights = analyzer.analyze(data)
        logger.info('Data analysis completed')
        print('  ✓ Analysis completed')

        # Step 3: Generate report
        print('\n[Step 3/3] Generating structured report...')
        logger.info('Initializing ReportGenerator')
        generator = ReportGenerator()
        report = generator.generate(search_query, insights)
        logger.info('Report generated')
        print('  ✓ Report generated')

        # Display results
        print('\n' + '='*60)
        print('RESEARCH COMPLETE')
        print('='*60)
        print(f'\n{report}')

        # Save report
        report_filename = f"report_{search_query.replace(' ', '_').lower()}.md"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f'Report saved to: {report_filename}')
        print(f'\n[OUTPUT] Report saved to: {report_filename}')
        print('='*60 + '\n')
        
        return 0
    
    except KeyboardInterrupt:
        logger.info('Process interrupted by user')
        print('\n\n[CANCELLED] Process interrupted by user')
        return 130
    
    except Exception as e:
        logger.error(f'Error during execution: {str(e)}')
        print(f'\n[ERROR] {str(e)}')
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
