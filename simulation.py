import numpy as np
from typing import Tuple, List

from classes import Belligerant, Coefficients
import data_analysis as da

def sanctions_policy_russia(t: int) -> float:
    return .14 * max(min(t / 4, 90),0) / 90 + .01

def sanctions_policy_ukraine(t: int) -> float:
    return 0.0

def foreign_aid_policy_russia(t: int) -> float:
    return 0.0

def foreign_aid_policy_ukraine(t: int) -> float:
    return .16

def conflict_intensity(t: int) -> float:
    return 1 if t > 360 else -1.5 * t / 360 + 2.5

def create_belligerants(coefficients: Coefficients, monte_carlo=False) -> Tuple[Belligerant, Belligerant]:
    russian_federation: Belligerant
    ukraine: Belligerant
    if not monte_carlo:
        russian_federation = Belligerant(
            name="Russian Federation",
            coefficients=coefficients,
            military_technology=1.0,
            industrial_technology=1.0,
            military_industrial_capacity=100,
            civilian_industrial_capacity=760,
            military_capability=175,
            military_technology_investment_percentage=0.25,
            industrial_technology_investment_percentage=0.25,
            military_industrial_investment_percentage=0.25,
            civilian_industrial_investment_percentage=0.25,
            attacking_intensity=.6,
            tax_revenue_percentage=0.11,
            sanctions_policy=sanctions_policy_russia,
            foreign_aid_policy=foreign_aid_policy_russia,
        )

        ukraine = Belligerant(
            name="Ukraine",
            coefficients=coefficients,
            military_technology=1.0,
            industrial_technology=1.0,
            military_industrial_capacity=100,
            civilian_industrial_capacity=100,
            military_capability=100,
            military_technology_investment_percentage=0.25,
            industrial_technology_investment_percentage=0.25,
            military_industrial_investment_percentage=0.25,
            civilian_industrial_investment_percentage=0.25,
            attacking_intensity=.4,
            tax_revenue_percentage=0.19,
            sanctions_policy=sanctions_policy_ukraine,
            foreign_aid_policy=foreign_aid_policy_ukraine,
        )
    else:
        russia_attacking_intensity = np.random.normal(.62,.02)
        russian_federation = Belligerant(
            name="Russian Federation",
            coefficients=coefficients,
            military_technology=1.0,
            industrial_technology=1.0,
            military_industrial_capacity=100,
            civilian_industrial_capacity=850,
            military_capability=175,
            military_technology_investment_percentage=0.25,
            industrial_technology_investment_percentage=0.25,
            military_industrial_investment_percentage=0.25,
            civilian_industrial_investment_percentage=0.25,
            attacking_intensity=russia_attacking_intensity,
            tax_revenue_percentage=np.random.normal(0.11, 0.01),
            sanctions_policy=sanctions_policy_russia,
            foreign_aid_policy=foreign_aid_policy_russia,
        )

        ukraine = Belligerant(
            name="Ukraine",
            coefficients=coefficients,
            military_technology=1.0,
            industrial_technology=1.0,
            military_industrial_capacity=100,
            civilian_industrial_capacity=100,
            military_capability=100,
            military_technology_investment_percentage=0.25,
            industrial_technology_investment_percentage=0.25,
            military_industrial_investment_percentage=0.25,
            civilian_industrial_investment_percentage=0.25,
            attacking_intensity=1-russia_attacking_intensity,
            tax_revenue_percentage=np.random.normal(0.19, 0.01),
            sanctions_policy=sanctions_policy_ukraine,
            foreign_aid_policy=foreign_aid_policy_ukraine,
        )

    return russian_federation, ukraine

def check_termination_conditions(belligerants: List[Belligerant], monte_carlo=False) -> Tuple[bool, str, str]:
    end: bool = False
    winner = "None"
    reason = "None"
    for belligerant in belligerants:
        if belligerant.economic_capital < 0.6 * belligerant.history.economic_capital[0]:
            if not monte_carlo:
                print(f"{belligerant.name} has lost the war due to economic collapse.")
            winner = belligerants[1].name if belligerant == belligerants[0] else belligerants[0].name
            reason = "Enemy Economic Collapse"
            end = True
        elif belligerant.military_capability <= 15:
            if not monte_carlo:
                print(f"{belligerant.name} has lost the war due to military collapse.")
            winner = belligerants[1].name if belligerant == belligerants[0] else belligerants[0].name
            reason = "Enemy Military Collapse"
            end = True
    if belligerants[0].military_capability > 4 * belligerants[1].military_capability:
        if not monte_carlo:
            print(f"{belligerants[0].name} has won the war militarily.")
        winner = belligerants[0].name
        reason = "Military Superiority"
        end = True
    elif belligerants[1].military_capability > 4 * belligerants[0].military_capability:
        if not monte_carlo:
            print(f"{belligerants[1].name} has won the war militarily.")
        winner = belligerants[1].name
        reason = "Military Superiority"
        end = True

    if end and not monte_carlo:
        print_endgame_stats(belligerants)
    return end, winner, reason

def print_endgame_stats(belligerants: List[Belligerant]) -> None:
    for belligerant in belligerants:
        print(f"{belligerant.name} has {belligerant.economic_capital} economic capital, {belligerant.military_capability} military capability, and {belligerant.civilian_industrial_capacity} civilian industrial capacity.")

def run_simulation(timesteps: int, coefficients: Coefficients, monte_carlo=False) -> Tuple[Belligerant, Belligerant, int, str, str]:
    russian_federation, ukraine = create_belligerants(coefficients, monte_carlo)
    baseline_russian_attacking_intensity = np.random.normal(.62,.02)
    for t in range(timesteps):
        coefficients.conflict_intensity = conflict_intensity(t)
        ru_military_capability: float = russian_federation.military_capability
        ua_military_capability: float = ukraine.military_capability

        if t < 270:
            russian_federation.attacking_intensity = 0.7
            ukraine.attacking_intensity = 0.25
        elif t < 540:
            russian_federation.attacking_intensity = 0.7 - (.7 - baseline_russian_attacking_intensity) / 270 * (t - 270)
            ukraine.attacking_intensity = 1 - russian_federation.attacking_intensity            

        russian_federation.update(t, ua_military_capability)
        ukraine.update(t, ru_military_capability)

        end, winner, reason = check_termination_conditions([russian_federation, ukraine], monte_carlo=monte_carlo)
        if end:
            return russian_federation, ukraine, t, winner, reason

    return russian_federation, ukraine, timesteps, "None", reason

if __name__ == "__main__":
    global_coefficients: Coefficients = Coefficients(
        production_efficiency=8,
        military_capability_weight=1.5e-4,
        sanctions_delay=30,
        foreign_aid_delay=30,
        elasticity_coefficient=3e-4,
        military_technology_investment_coefficient=1e-3,
        industrial_technology_investment_coefficient=3e-4,
        military_industrial_investment_coefficient=5e-1,
        civilian_industrial_investment_coefficient=1e-1,
        military_consumption_cost_coefficient=3e-4,
        military_demand_coefficient=3.5,
        military_attrition_coefficient=5e-5,
        industrial_attrition_coefficient=4e-7,
        spending_scaling_coefficient=5e-1,
        conflict_intensity=2.5,
        epsilon=1e-10,
    )

    timesteps: int = 3600
    russian_federation, ukraine, t, winner, reason = run_simulation(timesteps, global_coefficients, monte_carlo=False)
    da.plot_dashboard([russian_federation, ukraine])