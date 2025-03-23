from dataclasses import dataclass, fields

class Belligerant:
    def __init__(
        self,
        name: str,
        coefficients: 'Coefficients',
        military_technology: float,
        industrial_technology: float,
        military_industrial_capacity: float,
        civilian_industrial_capacity: float,
        military_capability: float,
        military_technology_investment_percentage: float,
        industrial_technology_investment_percentage: float,
        military_industrial_investment_percentage: float,
        civilian_industrial_investment_percentage: float,
        tax_revenue_percentage: float,
        attacking_intensity: float,
        sanctions_policy,
        foreign_aid_policy,
    ) -> None:
        self.name: str = name
        self.coefficients: Coefficients = coefficients

        # stocks
        self.military_technology: float = military_technology
        self.industrial_technology: float = industrial_technology
        self.military_industrial_capacity: float = military_industrial_capacity
        self.civilian_industrial_capacity: float = civilian_industrial_capacity
        self.military_capability: float = military_capability
        self.economic_capital: float = 0.0

        # independent variables
        self.military_technology_investment_percentage: float = military_technology_investment_percentage
        self.industrial_technology_investment_percentage: float = industrial_technology_investment_percentage
        self.military_industrial_investment_percentage: float = military_industrial_investment_percentage
        self.civilian_industrial_investment_percentage: float = civilian_industrial_investment_percentage
        self.tax_revenue_percentage: float = tax_revenue_percentage
        self.sanctions_policy = sanctions_policy
        self.foreign_aid_policy = foreign_aid_policy
        self.attacking_intensity: float = attacking_intensity

        self.current_budget: float = 0.0
        self.current_spending: float = 0.0

        self.adversary_military_capability: float = 0.0

        self.history: History = History(
            [0.0],
            [self.coefficients.production_efficiency * self.industrial_technology * self.civilian_industrial_capacity],
            [industrial_technology],
            [military_technology],
            [civilian_industrial_capacity],
            [military_industrial_capacity],
            [military_capability],
            [self.price_level()],
            [self.budget(0, self.economic_capital_equation(0))],
            [self.spending(0, self.economic_capital_equation(0))]
        )

    def update(self, t: int, M_neg: float) -> None:
        self.adversary_military_capability = M_neg

        # Update the stocks
        self.economic_capital = self.economic_capital_equation(t)
        self.current_budget = self.budget(t, self.economic_capital)
        self.current_spending = self.spending(t, self.economic_capital)
        self.economic_capital += min(self.current_budget, 0)
        self.industrial_technology += self.industrial_technology_growth()
        self.military_technology += self.military_technology_growth()
        self.civilian_industrial_capacity += self.civilian_industrial_capacity_growth(M_neg)
        self.military_industrial_capacity += self.military_industrial_capacity_growth(M_neg)
        self.military_capability += self.military_capability_growth(M_neg)

        # Update the history
        self.update_history(t)

    def update_history(self, t: int) -> None:
        self.history.time.append(t)
        self.history.economic_capital.append(self.economic_capital)
        self.history.industrial_technology.append(self.industrial_technology)
        self.history.military_technology.append(self.military_technology)
        self.history.civilian_industrial_capacity.append(self.civilian_industrial_capacity)
        self.history.military_industrial_capacity.append(self.military_industrial_capacity)
        self.history.military_capability.append(self.military_capability)
        self.history.price_level.append(self.price_level())
        self.history.budget.append(self.current_budget)
        self.history.spending.append(self.current_spending)

    def economic_capital_equation(self, t: int) -> float:
        return (
            self.coefficients.production_efficiency *
            self.industrial_technology *
            self.civilian_industrial_capacity *
            self.sanctions_effect(t)
        )
    
    def budget(self, t: int, capital: float) -> float:
        return ((capital *
                self.tax_revenue_percentage *
                0.35 /
                365 +
                self.foreign_aid(t)) /
                self.price_level() -
                self.coefficients.military_consumption_cost_coefficient *
                self.military_capability)
    
    def spending(self, t: int, capital: float) -> float:
        return (
            max(self.budget(t, capital), 0) *
            (self.military_industrial_investment_percentage +
             self.civilian_industrial_investment_percentage +
             self.military_technology_investment_percentage +
             self.industrial_technology_investment_percentage)
        )
    
    def sanctions_effect(self, t: int) -> float:
        return 1 - self.sanctions_function(t - self.coefficients.sanctions_delay, self.sanctions_policy)
    
    def foreign_aid(self, t: int) -> float:
        return self.foreign_aid_function(t - self.coefficients.foreign_aid_delay, self.foreign_aid_policy)
    
    def industrial_technology_growth(self) -> float:
        return (
            self.coefficients.industrial_technology_investment_coefficient *
            self.industrial_technology_investment_percentage *
            max(self.current_budget, 0)
        )
    
    def military_technology_growth(self) -> float:
        return (
            self.coefficients.military_technology_investment_coefficient *
            self.military_technology_investment_percentage *
            max(self.current_budget, 0)
        )
    
    def civilian_industrial_capacity_growth(self, M_neg) -> float:
        return (
            self.coefficients.civilian_industrial_investment_coefficient *
            self.civilian_industrial_investment_percentage *
            max(self.current_budget, 0) -
            self.industrial_attrition(M_neg) *
            self.civilian_industrial_capacity
        )
    
    def military_industrial_capacity_growth(self, M_neg) -> float:
        return (
            self.coefficients.military_industrial_investment_coefficient *
            self.military_industrial_investment_percentage *
            max(self.current_budget, 0) -
            self.industrial_attrition(M_neg) *
            self.military_industrial_capacity
        )
    
    def military_capability_growth(self, M_neg: float) -> float:
        return (
            self.coefficients.military_capability_weight *
            self.military_technology *
            self.coefficients.production_efficiency *
            self.industrial_technology *
            self.military_industrial_capacity -
            self.military_attrition(M_neg)
        )
    
    def military_attrition(self, M_neg: float) -> float:
        return (
            self.attacking_intensity *
            self.coefficients.conflict_intensity *
            self.coefficients.military_attrition_coefficient *
            M_neg ** 1.5
        )
    
    def industrial_attrition(self, M_neg) -> float:
        return (
            self.coefficients.industrial_attrition_coefficient *
            M_neg ** 1.1
        )
    
    def price_level(self) -> float:
        return 1 * (
            1 + self.coefficients.elasticity_coefficient *
            max(
                0,
                self.coefficients.military_demand_coefficient *
                self.military_capability -
                self.coefficients.production_efficiency *
                self.industrial_technology *
                self.military_industrial_capacity
            )
        )
    
    def sanctions_function(self, t: int, max_sanctions: float) -> float:
        return max(0, min(max_sanctions, .001 + ((max_sanctions - .001) * t / 180)))

    def foreign_aid_function(self, t: int, max_foreign_aid: float) -> float:
        return max_foreign_aid

@dataclass(slots=True)
class Coefficients:
    production_efficiency: float
    military_capability_weight: float
    sanctions_delay: float
    foreign_aid_delay: float
    elasticity_coefficient: float
    military_technology_investment_coefficient: float
    industrial_technology_investment_coefficient: float
    military_industrial_investment_coefficient: float
    civilian_industrial_investment_coefficient: float
    military_consumption_cost_coefficient: float
    military_demand_coefficient: float
    military_attrition_coefficient: float
    industrial_attrition_coefficient: float
    spending_scaling_coefficient: float
    conflict_intensity: float
    epsilon: float

    def get_by_index(self, index: int) -> float:
        return list(getattr(self, field.name) for field in fields(self))[index]
    
    def set_by_index(self, index: int, value: float) -> None:
        setattr(self, fields(self)[index].name, value)

@dataclass(slots=True)
class History:
    time: list[float]
    economic_capital: list[float]
    industrial_technology: list[float]
    military_technology: list[float]
    civilian_industrial_capacity: list[float]
    military_industrial_capacity: list[float]
    military_capability: list[float]
    price_level: list[float]
    budget: list[float]
    spending: list[float]
