from monte_carlo_simulation import run_monte_carlo_simulation
import gc
from time import sleep

def run_full_simulation_space(num_simulations: int):
    international_interference_scenarios: list = []
    investment_policies_scenarios: list = []

    for military_tech_percentage in [.15, .25, .35]:
        for industrial_tech_percentage in [.15, .25, .35]:
            for military_industrial_percentage in [.15, .25, .35]:
                for civilian_industrial_percentage in [.15, .25, .35]:
                    if military_tech_percentage + industrial_tech_percentage + military_industrial_percentage + civilian_industrial_percentage == 1:
                        investment_policies_scenarios.append({
                            'russia': [military_tech_percentage, industrial_tech_percentage, military_industrial_percentage, civilian_industrial_percentage],
                            'ukraine': [military_tech_percentage, industrial_tech_percentage, military_industrial_percentage, civilian_industrial_percentage]
                        })

    for sanctions_russia in [.07, .14, .21]:
        for foreign_aid_ukraine in [.12, .24, .36]:
            international_interference_scenarios.append({
                'sanctions_russia': sanctions_russia,
                'foreign_aid_ukraine': foreign_aid_ukraine,
                'foreign_aid_russia': 0,
                'sanctions_ukraine': 0,
            })

    for investment in investment_policies_scenarios:
        for interference in international_interference_scenarios:
            run_monte_carlo_simulation(num_simulations, interference, investment, export=True)
            gc.collect()
            sleep(3)

if __name__ == "__main__":
    run_full_simulation_space(10000)