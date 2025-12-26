#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Analyzer Module
Analyzes collected data using Google Gemini AI for intelligent insights
"""

import logging
import json
from typing import Dict, List, Any
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """
    Performs intelligent analysis on collected data using Gemini API
    """
    
    def __init__(self, api_key: str, model: str = 'gemini-pro'):
        """
        Initialize the DataAnalyzer with Gemini API
        
        Args:
            api_key: Google Gemini API key
            model: Model to use (default: gemini-pro)
        """
        self.api_key = api_key
        self.model_name = model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        logger.info(f'DataAnalyzer initialized with model: {model}')
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze scraped data and generate insights using Gemini
        
        Args:
            data: Dictionary containing scraped data
            
        Returns:
            Dictionary with analysis results and insights
        """
        logger.info('Starting data analysis with Gemini')
        
        try:
            # Prepare context from scraped data
            context = self._prepare_context(data)
            
            # Generate comprehensive analysis
            insights = {
                'timestamp': datetime.now().isoformat(),
                'query': data.get('query', 'Unknown'),
                'sources_analyzed': len(data.get('sources', [])),
                'analysis': {}
            }
            
            # Financial Analysis
            fin_analysis = self._analyze_financial(context)
            if fin_analysis:
                insights['analysis']['financial'] = fin_analysis
            
            # Historical/Background Analysis
            hist_analysis = self._analyze_history(context)
            if hist_analysis:
                insights['analysis']['history'] = hist_analysis
            
            # Industry/Market Analysis
            industry_analysis = self._analyze_industry(context)
            if industry_analysis:
                insights['analysis']['industry'] = industry_analysis
            
            # Strengths & Weaknesses Analysis
            swot_analysis = self._analyze_swot(context)
            if swot_analysis:
                insights['analysis']['swot'] = swot_analysis
            
            # Future Predictions
            predictions = self._analyze_predictions(context)
            if predictions:
                insights['analysis']['predictions'] = predictions
            
            logger.info('Data analysis completed successfully')
            return insights
        
        except Exception as e:
            logger.error(f'Error during analysis: {str(e)}')
            return self._error_insights(data, str(e))
    
    def _prepare_context(self, data: Dict) -> str:
        """
        Prepare context from scraped data for Gemini analysis
        """
        context = f"Analyze the following information:\n\n"
        context += f"Query: {data.get('query', 'Unknown')}\n"
        context += f"Sources: {', '.join(data.get('sources', []))}\n\n"
        
        for source, content in data.get('raw_content', {}).items():
            context += f"\n{source.upper()}:\n"
            if isinstance(content, dict):
                for key, val in content.items():
                    context += f"{key}: {val}\n"
            else:
                context += str(content)[:500] + "...\n"
        
        return context
    
    def _analyze_financial(self, context: str) -> Dict[str, Any]:
        """
        Analyze financial aspects using Gemini
        """
        try:
            prompt = f"""{context}\n\nBased on the above information, provide a detailed financial analysis including:
            - Revenue trends
            - Profitability metrics
            - Financial health indicators
            - Investment potential
            
            Format as JSON with keys: revenue, profitability, health, investment_rating"""
            
            response = self.model.generate_content(prompt)
            
            try:
                return json.loads(response.text)
            except:
                return {'summary': response.text}
        
        except Exception as e:
            logger.warning(f'Financial analysis failed: {str(e)}')
            return None
    
    def _analyze_history(self, context: str) -> Dict[str, str]:
        """
        Analyze historical background and milestones
        """
        try:
            prompt = f"""{context}\n\nProvide a historical analysis including:
            - Key milestones
            - Company evolution
            - Major achievements
            - Turning points
            
            Format as detailed narrative."""
            
            response = self.model.generate_content(prompt)
            return {'timeline': response.text}
        
        except Exception as e:
            logger.warning(f'History analysis failed: {str(e)}')
            return None
    
    def _analyze_industry(self, context: str) -> Dict[str, str]:
        """
        Analyze industry and market position
        """
        try:
            prompt = f"""{context}\n\nAnalyze the industry and market including:
            - Industry trends
            - Market position
            - Competitive landscape
            - Growth opportunities
            
            Format as structured analysis."""
            
            response = self.model.generate_content(prompt)
            return {'market_analysis': response.text}
        
        except Exception as e:
            logger.warning(f'Industry analysis failed: {str(e)}')
            return None
    
    def _analyze_swot(self, context: str) -> Dict[str, List[str]]:
        """
        Perform SWOT analysis
        """
        try:
            prompt = f"""{context}\n\nPerform a SWOT analysis providing:
            - Strengths (at least 3)
            - Weaknesses (at least 3)
            - Opportunities (at least 3)
            - Threats (at least 3)
            
            Format as JSON."""
            
            response = self.model.generate_content(prompt)
            
            try:
                return json.loads(response.text)
            except:
                return {'summary': response.text}
        
        except Exception as e:
            logger.warning(f'SWOT analysis failed: {str(e)}')
            return None
    
    def _analyze_predictions(self, context: str) -> Dict[str, str]:
        """
        Generate future predictions and recommendations
        """
        try:
            prompt = f"""{context}\n\nBased on the analysis, provide:
            - Future outlook (next 1-3 years)
            - Key growth drivers
            - Risk factors
            - Strategic recommendations
            
            Format as structured predictions."""
            
            response = self.model.generate_content(prompt)
            return {'outlook': response.text}
        
        except Exception as e:
            logger.warning(f'Predictions analysis failed: {str(e)}')
            return None
    
    def _error_insights(self, data: Dict, error: str) -> Dict[str, Any]:
        """
        Return default insights when analysis fails
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'query': data.get('query'),
            'error': error,
            'analysis': {
                'status': 'Analysis incomplete',
                'message': f'Analysis failed: {error}'
            }
        }
