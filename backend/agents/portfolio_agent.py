"""
Portfolio Management Agent
Specialized agent for portfolio management and investment optimization
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from crewai import Task

from .base_agent import BaseFinanceAgent
from tools.database_tools import CustomerDataTool, AssetAllocationTool, PortfolioDataTool, NewsDataTool
from config.agents_config import TASK_TEMPLATES


class PortfolioAgent(BaseFinanceAgent):
    """Agent specialized in portfolio management and investment optimization"""
    
    def __init__(self, tools: List[BaseTool] = None):
        # Add portfolio-specific tools
        portfolio_tools = [
            CustomerDataTool(),
            AssetAllocationTool(),
            PortfolioDataTool(),
            NewsDataTool()
        ]
        if tools:
            portfolio_tools.extend(tools)
        
        super().__init__("portfolio_manager", portfolio_tools)
    
    def analyze_portfolio_performance(self, customer_id: int, portfolio_type: str = "overall") -> str:
        """Analyze portfolio performance and provide detailed metrics"""
        task_description = TASK_TEMPLATES["portfolio_analysis"].format(
            customer_id=customer_id,
            portfolio_type=portfolio_type
        )
        
        expected_output = """
        A comprehensive portfolio performance analysis including:
        1. Portfolio Summary and Current Composition
        2. Performance Metrics (Total Return, Annualized Return, YTD)
        3. Risk Metrics (Volatility, Sharpe Ratio, Maximum Drawdown)
        4. Benchmark Comparison and Relative Performance
        5. Asset Allocation Analysis and Drift Assessment
        6. Individual Security Performance Review
        7. Sector and Geographic Exposure Analysis
        8. Risk-Adjusted Performance Evaluation
        9. Performance Attribution Analysis
        10. Recommendations for Improvement
        """
        
        return self.execute_task(task_description, expected_output)
    
    def recommend_rebalancing(self, customer_id: int) -> str:
        """Recommend portfolio rebalancing strategies"""
        task_description = f"""
        Recommend portfolio rebalancing for customer {customer_id}:
        
        1. Retrieve current portfolio and target allocation
        2. Calculate allocation drift and deviation percentages
        3. Identify overweight and underweight positions
        4. Analyze tax implications of rebalancing trades
        5. Consider transaction costs and minimum trade sizes
        6. Evaluate market timing considerations
        7. Recommend specific rebalancing trades
        8. Suggest rebalancing frequency and triggers
        9. Provide alternative rebalancing strategies
        """
        
        expected_output = """
        A portfolio rebalancing recommendation with:
        1. Current vs Target Allocation Analysis
        2. Allocation Drift Assessment
        3. Specific Rebalancing Trades Recommended
        4. Tax Impact Analysis and Optimization
        5. Transaction Cost Considerations
        6. Market Timing and Implementation Strategy
        7. Alternative Rebalancing Approaches
        8. Future Rebalancing Schedule and Triggers
        9. Expected Impact on Risk and Return
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_asset_allocation(self, customer_id: int) -> str:
        """Analyze and optimize asset allocation strategy"""
        task_description = f"""
        Analyze asset allocation strategy for customer {customer_id}:
        
        1. Retrieve customer risk profile and investment objectives
        2. Analyze current asset allocation across all accounts
        3. Compare current allocation to target and benchmarks
        4. Evaluate allocation effectiveness and risk-return profile
        5. Consider customer's age, timeline, and risk tolerance
        6. Analyze diversification across asset classes and regions
        7. Recommend optimal asset allocation adjustments
        8. Consider tax-efficient allocation across account types
        9. Provide strategic and tactical allocation recommendations
        """
        
        expected_output = """
        An asset allocation analysis including:
        1. Current Asset Allocation Breakdown
        2. Risk Profile and Investment Objective Review
        3. Allocation Effectiveness Analysis
        4. Diversification Assessment
        5. Age and Timeline Appropriateness
        6. Strategic Asset Allocation Recommendations
        7. Tactical Allocation Opportunities
        8. Tax-Efficient Account Allocation Strategy
        9. Implementation Plan and Timeline
        """
        
        return self.execute_task(task_description, expected_output)
    
    def identify_investment_opportunities(self, customer_id: int) -> str:
        """Identify investment opportunities based on market analysis"""
        task_description = f"""
        Identify investment opportunities for customer {customer_id}:
        
        1. Retrieve customer profile and current portfolio
        2. Analyze market conditions and trends using latest news
        3. Identify undervalued sectors and securities
        4. Evaluate emerging investment themes and opportunities
        5. Consider customer's risk tolerance and investment timeline
        6. Analyze correlation with existing holdings
        7. Recommend specific investment vehicles and strategies
        8. Provide timing and implementation considerations
        9. Include risk assessment and exit strategies
        """
        
        expected_output = """
        An investment opportunities report with:
        1. Market Environment Analysis
        2. Customer Portfolio Context
        3. Identified Investment Opportunities by Category
        4. Specific Investment Recommendations
        5. Risk-Return Analysis for Each Opportunity
        6. Portfolio Fit and Correlation Analysis
        7. Implementation Strategy and Timing
        8. Position Sizing Recommendations
        9. Risk Management and Exit Strategies
        """
        
        return self.execute_task(task_description, expected_output)
    
    def conduct_risk_assessment(self, customer_id: int) -> str:
        """Conduct comprehensive portfolio risk assessment"""
        task_description = f"""
        Conduct portfolio risk assessment for customer {customer_id}:
        
        1. Retrieve portfolio holdings and position sizes
        2. Calculate portfolio volatility and risk metrics
        3. Analyze concentration risk and position limits
        4. Evaluate correlation and diversification effectiveness
        5. Assess downside risk and maximum drawdown potential
        6. Analyze sector, geographic, and currency exposures
        7. Evaluate liquidity risk and redemption constraints
        8. Consider macro-economic and systematic risks
        9. Recommend risk mitigation strategies
        """
        
        expected_output = """
        A comprehensive risk assessment including:
        1. Portfolio Risk Profile Summary
        2. Volatility and Risk Metrics Analysis
        3. Concentration Risk Assessment
        4. Diversification and Correlation Analysis
        5. Downside Risk and Stress Testing
        6. Exposure Analysis (Sector, Geographic, Currency)
        7. Liquidity Risk Evaluation
        8. Systematic and Macro Risk Factors
        9. Risk Mitigation Recommendations
        10. Risk Monitoring and Control Framework
        """
        
        return self.execute_task(task_description, expected_output)
    
    def optimize_tax_efficiency(self, customer_id: int) -> str:
        """Optimize portfolio for tax efficiency"""
        task_description = f"""
        Optimize tax efficiency for customer {customer_id}'s portfolio:
        
        1. Retrieve portfolio holdings across all account types
        2. Analyze current tax efficiency and tax drag
        3. Identify tax-loss harvesting opportunities
        4. Evaluate asset location optimization strategies
        5. Consider municipal bonds and tax-advantaged investments
        6. Analyze timing of capital gains and losses
        7. Recommend tax-efficient fund selections
        8. Evaluate Roth conversion opportunities
        9. Create ongoing tax management strategy
        """
        
        expected_output = """
        A tax optimization strategy including:
        1. Current Tax Efficiency Analysis
        2. Tax-Loss Harvesting Opportunities
        3. Asset Location Optimization Plan
        4. Tax-Advantaged Investment Recommendations
        5. Capital Gains/Loss Management Strategy
        6. Tax-Efficient Fund Selection
        7. Roth Conversion Analysis
        8. Ongoing Tax Management Framework
        9. Expected Tax Savings Quantification
        """
        
        return self.execute_task(task_description, expected_output)
    
    def create_income_strategy(self, customer_id: int, income_goal: float) -> str:
        """Create income-generating investment strategy"""
        task_description = f"""
        Create income strategy for customer {customer_id} with target income: ${income_goal:,.2f}
        
        1. Retrieve customer profile and current income sources
        2. Analyze income needs and timeline requirements
        3. Evaluate dividend-paying stocks and REITs
        4. Consider bond ladders and fixed income strategies
        5. Analyze covered call and income enhancement strategies
        6. Evaluate tax implications of income strategies
        7. Balance income generation with growth potential
        8. Consider inflation protection and purchasing power
        9. Create sustainable income withdrawal strategy
        """
        
        expected_output = f"""
        An income generation strategy including:
        1. Income Needs Analysis and Gap Assessment
        2. Current Income Sources Evaluation
        3. Dividend and Distribution Strategy
        4. Fixed Income and Bond Allocation
        5. Income Enhancement Strategies
        6. Tax-Efficient Income Planning
        7. Growth vs Income Balance Optimization
        8. Inflation Protection Considerations
        9. Sustainable Withdrawal Rate Analysis
        10. Implementation Timeline and Monitoring
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_alternative_investments(self, customer_id: int) -> str:
        """Analyze alternative investment opportunities"""
        task_description = f"""
        Analyze alternative investments for customer {customer_id}:
        
        1. Retrieve customer sophistication and accreditation status
        2. Evaluate portfolio's need for alternative diversification
        3. Analyze real estate investment opportunities (REITs, direct)
        4. Consider private equity and hedge fund allocations
        5. Evaluate commodity and precious metals exposure
        6. Analyze cryptocurrency and digital asset allocation
        7. Consider structured products and derivatives
        8. Assess liquidity and complexity considerations
        9. Recommend appropriate alternative allocation
        """
        
        expected_output = """
        An alternative investments analysis with:
        1. Alternative Investment Suitability Assessment
        2. Portfolio Diversification Benefits Analysis
        3. Real Estate Investment Evaluation
        4. Private Markets and Hedge Fund Opportunities
        5. Commodity and Precious Metals Analysis
        6. Digital Assets and Cryptocurrency Evaluation
        7. Structured Products Consideration
        8. Risk and Liquidity Assessment
        9. Recommended Alternative Allocation
        10. Due Diligence and Selection Criteria
        """
        
        return self.execute_task(task_description, expected_output)
