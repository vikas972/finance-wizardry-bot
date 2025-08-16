"""
Data Analyst Agent
Specialized agent for financial data analysis and extraction
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from crewai import Task

from .base_agent import BaseFinanceAgent
from tools.database_tools import get_database_tools
from config.agents_config import TASK_TEMPLATES


class DataAnalystAgent(BaseFinanceAgent):
    """Agent specialized in financial data analysis and extraction"""
    
    def __init__(self, tools: List[BaseTool] = None):
        # Add all database tools for comprehensive data access
        data_tools = get_database_tools()
        if tools:
            data_tools.extend(tools)
        
        super().__init__("data_analyst", data_tools)
    
    def extract_customer_insights(self, customer_id: int) -> str:
        """Extract comprehensive customer insights from all data sources"""
        task_description = TASK_TEMPLATES["fetch_customer_data"].format(
            customer_id=customer_id,
            data_type="comprehensive"
        )
        
        expected_output = """
        A comprehensive customer data analysis including:
        1. Customer Profile and Demographics Summary
        2. Financial Health Score and Key Metrics
        3. Investment Behavior and Patterns Analysis
        4. Credit Profile and Risk Assessment
        5. Asset Allocation and Portfolio Analysis
        6. Income and Tax Situation Overview
        7. Goal Achievement Progress Tracking
        8. Risk Tolerance and Investment Preferences
        9. Engagement and Activity Patterns
        10. Personalization Opportunities and Recommendations
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_market_trends(self) -> str:
        """Analyze market trends from news and data"""
        task_description = """
        Analyze current market trends and patterns:
        
        1. Retrieve latest financial news and market data
        2. Identify emerging trends and patterns
        3. Analyze sector rotation and performance
        4. Track economic indicators and their impact
        5. Monitor sentiment and investor behavior
        6. Identify correlation patterns and relationships
        7. Analyze volatility patterns and risk factors
        8. Track institutional and retail investor flows
        9. Provide data-driven market outlook
        """
        
        expected_output = """
        A comprehensive market trends analysis with:
        1. Current Market Environment Overview
        2. Emerging Trends and Patterns Identification
        3. Sector Performance and Rotation Analysis
        4. Economic Indicators Impact Assessment
        5. Market Sentiment and Behavior Analysis
        6. Correlation and Relationship Patterns
        7. Volatility and Risk Factor Analysis
        8. Investment Flow and Positioning Trends
        9. Data-Driven Market Outlook and Implications
        """
        
        return self.execute_task(task_description, expected_output)
    
    def create_performance_dashboard(self, customer_id: int) -> str:
        """Create comprehensive performance dashboard data"""
        task_description = f"""
        Create performance dashboard data for customer {customer_id}:
        
        1. Retrieve all customer financial data and metrics
        2. Calculate key performance indicators (KPIs)
        3. Analyze portfolio performance vs benchmarks
        4. Track goal achievement and milestones
        5. Monitor risk metrics and exposure analysis
        6. Calculate returns across different time periods
        7. Analyze cash flow and investment patterns
        8. Track credit score and financial health changes
        9. Provide actionable insights and alerts
        """
        
        expected_output = """
        A performance dashboard dataset including:
        1. Key Performance Indicators (KPIs) Summary
        2. Portfolio Performance Metrics and Charts
        3. Benchmark Comparison and Relative Performance
        4. Goal Tracking and Achievement Status
        5. Risk Metrics and Exposure Analysis
        6. Historical Performance Trends
        7. Cash Flow and Investment Activity
        8. Credit and Financial Health Metrics
        9. Alerts and Action Items
        10. Personalized Insights and Recommendations
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_customer_segmentation(self) -> str:
        """Analyze customer segmentation and patterns"""
        task_description = """
        Analyze customer segmentation and behavioral patterns:
        
        1. Retrieve data for all customers using customer_data_fetcher with 'all'
        2. Analyze demographics and financial characteristics
        3. Identify customer segments and personas
        4. Analyze investment behavior and preferences
        5. Track engagement and usage patterns
        6. Identify high-value and at-risk customers
        7. Analyze product adoption and cross-selling opportunities
        8. Provide segment-specific insights and strategies
        9. Recommend personalization and targeting approaches
        """
        
        expected_output = """
        A customer segmentation analysis including:
        1. Customer Demographics and Characteristics Overview
        2. Financial Behavior Segmentation
        3. Investment Preference Clusters
        4. Engagement and Activity Segments
        5. Value Tier and Profitability Analysis
        6. Risk and Credit Profile Segments
        7. Product Adoption and Cross-sell Analysis
        8. Segment-Specific Insights and Strategies
        9. Personalization and Targeting Recommendations
        """
        
        return self.execute_task(task_description, expected_output)
    
    def conduct_risk_analytics(self, customer_id: Optional[int] = None) -> str:
        """Conduct comprehensive risk analytics"""
        if customer_id:
            task_description = f"""
            Conduct risk analytics for customer {customer_id}:
            
            1. Retrieve customer portfolio and financial data
            2. Calculate portfolio risk metrics and volatility
            3. Analyze concentration and diversification risks
            4. Assess credit and default risk factors
            5. Evaluate market and systematic risk exposure
            6. Analyze liquidity and operational risks
            7. Track risk-adjusted performance metrics
            8. Identify risk mitigation opportunities
            9. Provide risk monitoring and alerting framework
            """
        else:
            task_description = """
            Conduct portfolio-wide risk analytics:
            
            1. Retrieve data for all customers and portfolios
            2. Analyze aggregate risk exposure and concentration
            3. Identify systemic and correlated risks
            4. Track market risk and stress testing scenarios
            5. Analyze credit and counterparty risk exposure
            6. Monitor liquidity and operational risk factors
            7. Provide risk dashboard and alerting framework
            8. Recommend risk management policies and limits
            """
        
        expected_output = """
        A comprehensive risk analytics report with:
        1. Risk Profile Summary and Key Metrics
        2. Portfolio Risk Analysis and Volatility Assessment
        3. Concentration and Diversification Risk Evaluation
        4. Credit and Default Risk Assessment
        5. Market and Systematic Risk Exposure
        6. Liquidity and Operational Risk Analysis
        7. Stress Testing and Scenario Analysis
        8. Risk-Adjusted Performance Metrics
        9. Risk Mitigation Recommendations
        10. Risk Monitoring and Alerting Framework
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_fee_optimization(self, customer_id: int) -> str:
        """Analyze fee structure and optimization opportunities"""
        task_description = f"""
        Analyze fee optimization for customer {customer_id}:
        
        1. Retrieve portfolio holdings and investment products
        2. Calculate total fees and expense ratios
        3. Analyze fee structure across different account types
        4. Identify high-fee products and alternatives
        5. Calculate fee impact on long-term returns
        6. Evaluate fee-efficient investment alternatives
        7. Analyze trading costs and transaction fees
        8. Recommend fee optimization strategies
        9. Quantify potential savings from fee reduction
        """
        
        expected_output = """
        A fee optimization analysis including:
        1. Current Fee Structure Analysis
        2. Total Cost of Ownership Calculation
        3. Fee Impact on Investment Returns
        4. High-Fee Products Identification
        5. Fee-Efficient Alternatives Evaluation
        6. Trading and Transaction Cost Analysis
        7. Fee Optimization Recommendations
        8. Potential Savings Quantification
        9. Implementation Strategy and Timeline
        """
        
        return self.execute_task(task_description, expected_output)
    
    def create_predictive_analytics(self, customer_id: int) -> str:
        """Create predictive analytics and forecasting"""
        task_description = f"""
        Create predictive analytics for customer {customer_id}:
        
        1. Retrieve historical performance and behavior data
        2. Analyze patterns and trends in investment behavior
        3. Predict future portfolio performance scenarios
        4. Forecast goal achievement probability
        5. Predict risk tolerance changes over time
        6. Analyze life event impact on financial planning
        7. Forecast cash flow needs and timing
        8. Predict product adoption and engagement likelihood
        9. Provide confidence intervals and scenario planning
        """
        
        expected_output = """
        A predictive analytics report including:
        1. Historical Pattern and Trend Analysis
        2. Portfolio Performance Forecasting
        3. Goal Achievement Probability Analysis
        4. Risk Tolerance Evolution Prediction
        5. Life Event Impact Modeling
        6. Cash Flow Forecasting and Planning
        7. Product Adoption Likelihood Scoring
        8. Scenario Planning and Stress Testing
        9. Confidence Intervals and Uncertainty Analysis
        10. Actionable Insights and Recommendations
        """
        
        return self.execute_task(task_description, expected_output)
    
    def generate_regulatory_reports(self, customer_id: Optional[int] = None) -> str:
        """Generate regulatory and compliance reports"""
        task_description = f"""
        Generate regulatory compliance reports:
        
        Customer Focus: {'Customer ' + str(customer_id) if customer_id else 'All Customers'}
        
        1. Retrieve relevant financial data and transactions
        2. Ensure data accuracy and completeness
        3. Apply regulatory reporting requirements
        4. Generate required disclosures and statements
        5. Validate compliance with financial regulations
        6. Check for reporting anomalies and exceptions
        7. Format reports according to regulatory standards
        8. Provide audit trail and documentation
        9. Recommend compliance improvements
        """
        
        expected_output = """
        A regulatory compliance report package with:
        1. Data Quality and Completeness Validation
        2. Regulatory Compliance Status Summary
        3. Required Financial Disclosures
        4. Transaction and Activity Reports
        5. Risk and Suitability Documentation
        6. Exception and Anomaly Reports
        7. Audit Trail and Supporting Documentation
        8. Compliance Gap Analysis
        9. Improvement Recommendations
        10. Regulatory Update and Impact Assessment
        """
        
        return self.execute_task(task_description, expected_output)
