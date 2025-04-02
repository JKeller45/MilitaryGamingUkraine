from monte_carlo_simulation import run_monte_carlo_simulation
import gc
import numpy as np

def run_full_simulation_space(num_simulations: int):
    international_interference_scenarios: list = []
    investment_policies_scenarios: list = []

    num_sims = 150

    # for military_tech_percentage in [.15, .25, .35]:
    #     for industrial_tech_percentage in [.15, .25, .35]:
    #         for military_industrial_percentage in [.15, .25, .35]:
    #             for civilian_industrial_percentage in [.15, .25, .35]:
    for _ in range(num_sims):
        rand_ints = [round(np.random.uniform(.05, 1), 2) for _ in range(3)]
        rand_ints = sorted(rand_ints)

        military_tech_percentage = rand_ints[0]
        industrial_tech_percentage = rand_ints[1] - rand_ints[0]
        military_industrial_percentage = rand_ints[2] - rand_ints[1]
        civilian_industrial_percentage = 1 - rand_ints[2]

        ukr = [military_tech_percentage, industrial_tech_percentage, military_industrial_percentage, civilian_industrial_percentage]

        rand_ints = [round(np.random.uniform(.05, 1), 2) for _ in range(3)]
        rand_ints = sorted(rand_ints)

        military_tech_percentage = rand_ints[0]
        industrial_tech_percentage = rand_ints[1] - rand_ints[0]
        military_industrial_percentage = rand_ints[2] - rand_ints[1]
        civilian_industrial_percentage = 1 - rand_ints[2]

        russia = [military_tech_percentage, industrial_tech_percentage, military_industrial_percentage, civilian_industrial_percentage]

        if sum(ukr) == 1 and sum(russia) == 1:
            investment_policies_scenarios.append({
                'russia': russia,
                'ukraine': ukr
            })

    # for sanctions_russia in [.07, .14, .21]:
    #     for foreign_aid_ukraine in [.12, .24, .36]:
            international_interference_scenarios.append({
                'sanctions_russia': round(np.random.uniform(0, .25), 2),
                'foreign_aid_ukraine':  round(np.random.uniform(0, .5), 2),
                'foreign_aid_russia': 0,
                'sanctions_ukraine': 0,
            })

    # print(investment_policies_scenarios)
    # print(international_interference_scenarios)
    for investment in investment_policies_scenarios:
        for interference in international_interference_scenarios:
            run_monte_carlo_simulation(num_simulations, interference, investment, export=True)
            gc.collect()

if __name__ == "__main__":
    run_full_simulation_space(12000)