"""
Financial Advisor Agent
Specialized agent for personalized financial advice and investment recommendations
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from crewai import Task

from .base_agent import BaseFinanceAgent
from tools.database_tools import CustomerDataTool, AssetAllocationTool, PortfolioDataTool, ITRDataTool
from config.agents_config import TASK_TEMPLATES


class FinancialAdvisorAgent(BaseFinanceAgent):
    """Agent specialized in providing personalized financial advice"""
    
    def __init__(self, tools: List[BaseTool] = None):
        # Add financial advisor specific tools
        advisor_tools = [
            CustomerDataTool(),
            AssetAllocationTool(),
            PortfolioDataTool(),
            ITRDataTool()
        ]
        if tools:
            advisor_tools.extend(tools)
        
        super().__init__("financial_advisor", advisor_tools)
    
    def provide_financial_advice(self, customer_id: int, query: str) -> str:
        """Provide personalized financial advice"""
        task_description = TASK_TEMPLATES["provide_financial_advice"].format(
            customer_id=customer_id,
            query=query
        )
        
        expected_output = """
        A comprehensive financial advice report including:
        1. Customer Profile Summary
        2. Current Financial Situation Analysis
        3. Risk Assessment and Risk Tolerance Analysis
        4. Specific Recommendations for the Query
        5. Investment Strategy Suggestions
        6. Portfolio Optimization Recommendations
        7. Tax Planning Considerations
        8. Action Plan with Timeline
        9. Follow-up Recommendations
        
        Make the advice practical, actionable, and tailored to the customer's specific situation.
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_portfolio_performance(self, customer_id: int) -> str:
        """Analyze customer's portfolio performance"""
        task_description = f"""
        Analyze the portfolio performance for customer {customer_id}:
        
        1. Retrieve customer's portfolio data using portfolio_data_fetcher
        2. Retrieve asset allocation data using asset_allocation_fetcher
        3. Calculate portfolio performance metrics:
           - Total return and annualized return
           - Risk-adjusted returns (Sharpe ratio)
           - Asset allocation effectiveness
           - Diversification analysis
        4. Compare performance against relevant benchmarks
        5. Identify underperforming and outperforming assets
        6. Analyze risk exposure and concentration
        7. Provide rebalancing recommendations
        8. Suggest performance improvement strategies
        """
        
        expected_output = """
        A detailed portfolio performance analysis with:
        1. Portfolio Summary and Current Value
        2. Performance Metrics (YTD, 1Y, 3Y returns)
        3. Risk Metrics (Volatility, Sharpe Ratio, Maximum Drawdown)
        4. Asset Allocation Analysis
        5. Individual Asset Performance Review
        6. Benchmark Comparison
        7. Risk Assessment and Concentration Analysis
        8. Rebalancing Recommendations
        9. Performance Improvement Action Plan
        """
        
        return self.execute_task(task_description, expected_output)
    
    def create_investment_plan(self, customer_id: int, goal: str, timeline: str, amount: float) -> str:
        """Create a comprehensive investment plan"""
        task_description = f"""
        Create a comprehensive investment plan for customer {customer_id}:
        
        Investment Goal: {goal}
        Timeline: {timeline}
        Investment Amount: ${amount:,.2f}
        
        1. Retrieve customer profile and financial metrics
        2. Analyze risk tolerance and investment experience
        3. Consider current portfolio and asset allocation
        4. Design optimal asset allocation for the goal
        5. Recommend specific investment vehicles
        6. Create timeline and milestone-based plan
        7. Include risk management strategies
        8. Provide tax-efficient investment approaches
        9. Set up monitoring and review schedule
        """
        
        expected_output = f"""
        A comprehensive investment plan including:
        1. Investment Objective and Strategy Summary
        2. Recommended Asset Allocation
        3. Specific Investment Recommendations by Category
        4. Implementation Timeline and Phases
        5. Expected Returns and Risk Assessment
        6. Tax Optimization Strategies
        7. Monitoring and Review Schedule
        8. Contingency Plans and Risk Management
        9. Cost Analysis and Fee Considerations
        10. Success Metrics and Milestones
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_retirement_planning(self, customer_id: int) -> str:
        """Analyze retirement planning needs and provide recommendations"""
        task_description = f"""
        Analyze retirement planning for customer {customer_id}:
        
        1. Retrieve customer demographics and financial data
        2. Calculate retirement funding gap
        3. Analyze current retirement savings and accounts
        4. Project future income needs and inflation impact
        5. Evaluate Social Security and pension benefits
        6. Recommend retirement account strategies (401k, IRA, Roth)
        7. Suggest catch-up contribution strategies if applicable
        8. Provide tax-efficient withdrawal strategies
        9. Include healthcare and long-term care planning
        """
        
        expected_output = """
        A comprehensive retirement planning analysis with:
        1. Retirement Goal and Timeline Assessment
        2. Current Retirement Savings Evaluation
        3. Funding Gap Analysis
        4. Projected Retirement Income Needs
        5. Social Security and Pension Optimization
        6. Retirement Account Strategy Recommendations
        7. Investment Allocation for Retirement
        8. Tax-Efficient Distribution Planning
        9. Healthcare and Insurance Considerations
        10. Action Plan with Annual Contribution Targets
        """
        
        return self.execute_task(task_description, expected_output)
    
    def provide_tax_planning_advice(self, customer_id: int) -> str:
        """Provide tax planning advice based on customer's financial situation"""
        task_description = f"""
        Provide comprehensive tax planning advice for customer {customer_id}:
        
        1. Retrieve customer's ITR data and financial information
        2. Analyze current tax situation and effective tax rate
        3. Identify tax-saving opportunities and deductions
        4. Recommend tax-efficient investment strategies
        5. Suggest retirement account optimization for tax benefits
        6. Analyze capital gains and losses management
        7. Provide tax-loss harvesting strategies
        8. Consider timing of income and deductions
        9. Recommend estate planning tax strategies if applicable
        """
        
        expected_output = """
        A comprehensive tax planning report including:
        1. Current Tax Situation Analysis
        2. Tax Optimization Opportunities
        3. Investment Tax Strategies
        4. Retirement Account Tax Planning
        5. Capital Gains/Loss Management
        6. Tax-Loss Harvesting Recommendations
        7. Income and Deduction Timing Strategies
        8. Year-End Tax Planning Checklist
        9. Long-term Tax Efficiency Plan
        10. Estimated Tax Savings Potential
        """
        
        return self.execute_task(task_description, expected_output)
    
    def assess_insurance_needs(self, customer_id: int) -> str:
        """Assess insurance needs and provide recommendations"""
        task_description = f"""
        Assess insurance needs for customer {customer_id}:
        
        1. Retrieve customer profile and financial obligations
        2. Calculate life insurance needs based on income replacement
        3. Analyze disability insurance requirements
        4. Evaluate health insurance adequacy
        5. Consider property and casualty insurance needs
        6. Assess umbrella insurance requirements
        7. Review existing insurance coverage for gaps
        8. Recommend cost-effective insurance strategies
        9. Consider insurance as part of estate planning
        """
        
        expected_output = """
        An insurance needs analysis report with:
        1. Current Insurance Coverage Review
        2. Life Insurance Needs Calculation
        3. Disability Insurance Assessment
        4. Health Insurance Evaluation
        5. Property & Casualty Insurance Review
        6. Coverage Gap Analysis
        7. Cost-Benefit Analysis of Recommendations
        8. Insurance Shopping Strategy
        9. Annual Review and Update Schedule
        10. Integration with Overall Financial Plan
        """
        
        return self.execute_task(task_description, expected_output)
    
    def create_debt_management_plan(self, customer_id: int) -> str:
        """Create a debt management and payoff plan"""
        task_description = f"""
        Create a debt management plan for customer {customer_id}:
        
        1. Retrieve customer's financial data and debt information
        2. Catalog all debts (credit cards, loans, mortgages)
        3. Analyze interest rates and payment terms
        4. Calculate debt-to-income ratios
        5. Recommend debt payoff strategies (avalanche vs snowball)
        6. Suggest debt consolidation opportunities
        7. Analyze refinancing options for mortgages and loans
        8. Create payment prioritization strategy
        9. Include emergency fund considerations
        """
        
        expected_output = """
        A comprehensive debt management plan including:
        1. Current Debt Portfolio Analysis
        2. Debt-to-Income Ratio Assessment
        3. Interest Rate and Payment Term Analysis
        4. Recommended Payoff Strategy
        5. Debt Consolidation Opportunities
        6. Refinancing Analysis and Recommendations
        7. Payment Prioritization Schedule
        8. Emergency Fund Strategy
        9. Credit Score Improvement Plan
        10. Timeline and Milestones for Debt Freedom
        """
        
        return self.execute_task(task_description, expected_output)
