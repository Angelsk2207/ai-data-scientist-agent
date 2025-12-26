#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Generator Module
Generates professional Markdown reports from analyzed data
"""

import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates professional Markdown reports from analysis results
    """
    
    def __init__(self):
        """
        Initialize the Report Generator
        """
        self.template_version = '1.0'
        logger.info('ReportGenerator initialized')
    
    def generate(self, query: str, insights: Dict[str, Any]) -> str:
        """
        Generate a comprehensive Markdown report
        
        Args:
            query: Search query (company or person name)
            insights: Dictionary with analysis results from DataAnalyzer
            
        Returns:
            Formatted Markdown report as string
        """
        logger.info(f'Generating report for: {query}')
        
        try:
            report = self._build_header(query, insights)
            report += self._build_executive_summary(insights)
            report += self._build_financial_section(insights)
            report += self._build_history_section(insights)
            report += self._build_industry_section(insights)
            report += self._build_swot_section(insights)
            report += self._build_predictions_section(insights)
            report += self._build_footer()
            
            logger.info('Report generated successfully')
            return report
        
        except Exception as e:
            logger.error(f'Error generating report: {str(e)}')
            return self._error_report(query, str(e))
    
    def _build_header(self, query: str, insights: Dict) -> str:
        """
        Build the report header
        """
        timestamp = insights.get('timestamp', datetime.now().isoformat())
        sources = insights.get('sources_analyzed', 0)
        
        header = f"""# Research Report: {query}

**Generated:** {timestamp}
**Sources Analyzed:** {sources}
**Report Version:** {self.template_version}

---\n\n"""
        return header
    
    def _build_executive_summary(self, insights: Dict) -> str:
        """
        Build executive summary section
        """
        summary = "## Executive Summary\n\n"
        
        if 'error' in insights:
            summary += f"*Note: Analysis encountered an issue: {insights.get('error')}*\n\n"
        else:
            analysis = insights.get('analysis', {})
            sources = insights.get('sources_analyzed', 0)
            
            summary += f"This report provides a comprehensive analysis of the subject based on {sources} sources. "
            summary += "The analysis includes financial metrics, historical background, industry positioning, "
            summary += "SWOT analysis, and future predictions.\n\n"
        
        return summary
    
    def _build_financial_section(self, insights: Dict) -> str:
        """
        Build financial analysis section
        """
        analysis = insights.get('analysis', {})
        financial = analysis.get('financial', {})
        
        if not financial:
            return ""
        
        section = "## Financial Analysis\n\n"
        
        if isinstance(financial, dict):
            for key, value in financial.items():
                if key != 'summary':
                    section += f"**{key.replace('_', ' ').title()}:** {value}\n\n"
        else:
            section += f"{financial}\n\n"
        
        return section
    
    def _build_history_section(self, insights: Dict) -> str:
        """
        Build history and background section
        """
        analysis = insights.get('analysis', {})
        history = analysis.get('history', {})
        
        if not history:
            return ""
        
        section = "## History & Background\n\n"
        
        if isinstance(history, dict):
            timeline = history.get('timeline', '')
            if timeline:
                section += f"{timeline}\n\n"
        else:
            section += f"{history}\n\n"
        
        return section
    
    def _build_industry_section(self, insights: Dict) -> str:
        """
        Build industry and market analysis section
        """
        analysis = insights.get('analysis', {})
        industry = analysis.get('industry', {})
        
        if not industry:
            return ""
        
        section = "## Industry & Market Analysis\n\n"
        
        if isinstance(industry, dict):
            market_analysis = industry.get('market_analysis', '')
            if market_analysis:
                section += f"{market_analysis}\n\n"
        else:
            section += f"{industry}\n\n"
        
        return section
    
    def _build_swot_section(self, insights: Dict) -> str:
        """
        Build SWOT analysis section
        """
        analysis = insights.get('analysis', {})
        swot = analysis.get('swot', {})
        
        if not swot:
            return ""
        
        section = "## SWOT Analysis\n\n"
        
        if isinstance(swot, dict):
            for category in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                items = swot.get(category, [])
                section += f"### {category.capitalize()}\n"
                if isinstance(items, list):
                    for item in items:
                        section += f"- {item}\n"
                else:
                    section += f"{items}\n"
                section += "\n"
        else:
            section += f"{swot}\n\n"
        
        return section
    
    def _build_predictions_section(self, insights: Dict) -> str:
        """
        Build future predictions section
        """
        analysis = insights.get('analysis', {})
        predictions = analysis.get('predictions', {})
        
        if not predictions:
            return ""
        
        section = "## Future Outlook & Recommendations\n\n"
        
        if isinstance(predictions, dict):
            outlook = predictions.get('outlook', '')
            if outlook:
                section += f"{outlook}\n\n"
        else:
            section += f"{predictions}\n\n"
        
        return section
    
    def _build_footer(self) -> str:
        """
        Build report footer
        """
        footer = f"""---

*Report generated by AI Data Scientist Agent v{self.template_version}*
*Using Google Gemini API for intelligent analysis*
*For more information, visit: https://github.com/Angelsk2207/ai-data-scientist-agent*
"""
        return footer
    
    def _error_report(self, query: str, error: str) -> str:
        """
        Generate error report
        """
        return f"""# Error Report: {query}

**Status:** Analysis Failed
**Error:** {error}
**Generated:** {datetime.now().isoformat()}

The analysis could not be completed due to the error mentioned above.
Please try again or contact support.
"""}
