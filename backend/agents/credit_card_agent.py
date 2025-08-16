"""
Credit Card Agent
Specialized agent for credit analysis and credit card recommendations
"""

from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from crewai import Task

from .base_agent import BaseFinanceAgent
from tools.database_tools import CustomerDataTool, CreditDataTool
from config.agents_config import TASK_TEMPLATES


class CreditCardAgent(BaseFinanceAgent):
    """Agent specialized in credit analysis and credit card recommendations"""
    
    def __init__(self, tools: List[BaseTool] = None):
        # Add credit-specific tools
        credit_tools = [
            CustomerDataTool(),
            CreditDataTool()
        ]
        if tools:
            credit_tools.extend(tools)
        
        super().__init__("credit_card_specialist", credit_tools)
    
    def analyze_credit_profile(self, customer_id: int) -> str:
        """Analyze customer's credit profile"""
        task_description = TASK_TEMPLATES["analyze_credit_profile"].format(
            customer_id=customer_id
        )
        
        expected_output = """
        A comprehensive credit profile analysis including:
        1. Credit Score Analysis and Interpretation
        2. Credit History Summary
        3. Credit Utilization Assessment
        4. Payment History Evaluation
        5. Credit Mix Analysis
        6. Recent Credit Inquiries Review
        7. Credit Strengths and Weaknesses
        8. Credit Improvement Recommendations
        9. Timeline for Credit Score Improvement
        10. Action Plan with Specific Steps
        """
        
        return self.execute_task(task_description, expected_output)
    
    def recommend_credit_cards(self, customer_id: int, purpose: str = "general") -> str:
        """Recommend credit cards based on customer profile"""
        task_description = f"""
        Recommend optimal credit cards for customer {customer_id} with purpose: {purpose}
        
        1. Retrieve customer's credit profile and financial data
        2. Analyze current credit cards and utilization
        3. Assess creditworthiness and approval probability
        4. Match customer needs with appropriate card categories
        5. Compare rewards, fees, and benefits
        6. Consider customer's spending patterns and preferences
        7. Evaluate balance transfer and promotional offers
        8. Rank recommendations by suitability and value
        9. Provide application strategy and timing
        """
        
        expected_output = """
        A credit card recommendation report with:
        1. Customer Credit Profile Summary
        2. Top 3-5 Credit Card Recommendations
        3. Detailed Comparison of Features and Benefits
        4. Approval Probability Assessment for Each Card
        5. Expected Value and Rewards Potential
        6. Fee Analysis and Break-even Calculations
        7. Application Strategy and Timeline
        8. Alternative Options and Backup Choices
        9. Post-approval Credit Management Tips
        """
        
        return self.execute_task(task_description, expected_output)
    
    def optimize_credit_utilization(self, customer_id: int) -> str:
        """Provide credit utilization optimization strategies"""
        task_description = f"""
        Optimize credit utilization for customer {customer_id}:
        
        1. Retrieve current credit cards and balances
        2. Calculate overall and per-card utilization ratios
        3. Analyze impact on credit score
        4. Identify high-utilization cards for priority paydown
        5. Recommend balance redistribution strategies
        6. Suggest credit limit increase requests
        7. Evaluate balance transfer opportunities
        8. Create payment timeline for optimization
        9. Monitor progress and adjustment strategies
        """
        
        expected_output = """
        A credit utilization optimization plan including:
        1. Current Utilization Analysis
        2. Impact Assessment on Credit Score
        3. Priority Paydown Strategy
        4. Balance Redistribution Plan
        5. Credit Limit Increase Recommendations
        6. Balance Transfer Analysis
        7. Payment Schedule and Timeline
        8. Monitoring and Tracking Plan
        9. Expected Credit Score Improvement
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_rewards_optimization(self, customer_id: int) -> str:
        """Analyze and optimize credit card rewards"""
        task_description = f"""
        Analyze and optimize credit card rewards for customer {customer_id}:
        
        1. Retrieve customer's spending patterns and categories
        2. Analyze current credit cards and reward structures
        3. Calculate current rewards earning rate
        4. Identify spending categories with highest volume
        5. Match optimal cards to spending patterns
        6. Compare different rewards programs (cash back, points, miles)
        7. Calculate potential rewards improvement
        8. Recommend card usage strategy
        9. Suggest timing for redemptions and maximization
        """
        
        expected_output = """
        A rewards optimization analysis with:
        1. Current Rewards Earning Summary
        2. Spending Pattern Analysis by Category
        3. Card-to-Spending Optimization Matrix
        4. Rewards Program Comparison
        5. Potential Additional Rewards Calculation
        6. Optimal Card Usage Strategy
        7. Redemption Strategy and Timing
        8. Annual Rewards Value Projection
        9. Implementation Plan and Tracking
        """
        
        return self.execute_task(task_description, expected_output)
    
    def create_credit_improvement_plan(self, customer_id: int) -> str:
        """Create a comprehensive credit improvement plan"""
        task_description = f"""
        Create a credit improvement plan for customer {customer_id}:
        
        1. Analyze current credit score and factors affecting it
        2. Identify specific areas for improvement
        3. Create timeline-based improvement strategy
        4. Recommend payment strategies and schedules
        5. Suggest credit mix optimization
        6. Plan for negative item removal or disputes
        7. Recommend authorized user strategies if applicable
        8. Set up credit monitoring and tracking
        9. Provide milestone-based progress tracking
        """
        
        expected_output = """
        A comprehensive credit improvement plan with:
        1. Current Credit Analysis and Baseline
        2. Improvement Goals and Targets
        3. Month-by-Month Action Plan
        4. Payment Strategy and Schedule
        5. Credit Mix Optimization Plan
        6. Dispute and Negative Item Strategy
        7. Credit Monitoring Setup
        8. Progress Milestones and Checkpoints
        9. Expected Timeline for Improvement
        10. Long-term Credit Health Maintenance
        """
        
        return self.execute_task(task_description, expected_output)
    
    def analyze_debt_consolidation(self, customer_id: int) -> str:
        """Analyze debt consolidation options"""
        task_description = f"""
        Analyze debt consolidation options for customer {customer_id}:
        
        1. Retrieve all current debts and interest rates
        2. Calculate total debt burden and monthly payments
        3. Evaluate balance transfer credit card options
        4. Analyze personal loan consolidation opportunities
        5. Compare home equity loan/HELOC options if applicable
        6. Calculate potential interest savings
        7. Assess impact on credit score and profile
        8. Recommend optimal consolidation strategy
        9. Create implementation timeline and steps
        """
        
        expected_output = """
        A debt consolidation analysis including:
        1. Current Debt Portfolio Summary
        2. Consolidation Options Comparison
        3. Interest Savings Calculation
        4. Credit Score Impact Analysis
        5. Qualification Assessment for Each Option
        6. Recommended Consolidation Strategy
        7. Implementation Timeline and Steps
        8. Risk Assessment and Considerations
        9. Post-consolidation Management Plan
        10. Long-term Debt Payoff Strategy
        """
        
        return self.execute_task(task_description, expected_output)
    
    def business_credit_analysis(self, customer_id: int) -> str:
        """Analyze business credit needs and recommendations"""
        task_description = f"""
        Analyze business credit needs for customer {customer_id}:
        
        1. Assess business credit requirements and goals
        2. Analyze personal vs business credit separation
        3. Recommend business credit card options
        4. Evaluate business loan and line of credit needs
        5. Suggest business credit building strategies
        6. Compare business rewards and cash flow benefits
        7. Analyze expense management and tracking needs
        8. Recommend business credit monitoring
        9. Create business credit establishment timeline
        """
        
        expected_output = """
        A business credit analysis report with:
        1. Business Credit Needs Assessment
        2. Personal vs Business Credit Separation Plan
        3. Business Credit Card Recommendations
        4. Business Loan and Financing Options
        5. Credit Building Strategy for Business
        6. Cash Flow and Expense Management Plan
        7. Business Credit Monitoring Setup
        8. Implementation Timeline and Milestones
        9. Expected Benefits and ROI Analysis
        """
        
        return self.execute_task(task_description, expected_output)
