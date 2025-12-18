import random

class RetentionAgent:
    """
    Agent responsible for generating retention plans.
    Uses a Mock LLM to avoid API costs during development.
    """
    
    def generate_plan(self, employee_data: dict, risk_level: str) -> str:
        """
        Generate a personalized retention plan.
        """
        name = "Employee"
        dept = employee_data.get("Department", "Unknown Department")
        role = employee_data.get("JobRole", "Unknown Role")
        income = employee_data.get("MonthlyIncome", 0)
        
        # Simple dynamic prompt logic (Mocking the LLM)
        strategies = [
            "Schedule a one-on-one career development meeting.",
            "Offer a spot bonus or performance incentive.",
            "Propose a flexible work arrangement or remote days.",
            "Review current compensation package against market rates.",
            "Assign a senior mentor to guide career growth."
        ]
        
        # Business Logic: only authoritative advice for High Risk
        if risk_level in ["HIGH", "CRITICAL"]:
            focus = "Immediate Intervention Required"
            strategy = random.choice(strategies)
            salary_increase = int(income * 0.10)
        else:
            focus = "Maintenance & Growth"
            strategy = "Regular quarterly check-in."
            salary_increase = int(income * 0.03)

        # "Generative" Output
        response = f"""
        **Retention Plan for {role} in {dept}**
        
        **Risk Profile**: {risk_level}
        **Focus Area**: {focus}
        
        **Suggested Actions**:
        1. {strategy}
        2. Consider a salary adjustment. Current: ${income}. Proposed: ${income + salary_increase} (+{salary_increase}).
        
        **Communication Script**:
        "We value your contribution to the {dept} team. We see great potential in your future here..."
        """
        return response.strip()

# Singleton
agent = RetentionAgent()

def get_agent():
    return agent
