from simulation import run_simulation
from classes import Coefficients
import numpy as np
from data_analysis import plot_monte_carlo_histograms, plot_monte_carlo_line, combine_simulation_results, calc_confidence_interval_time_series
from multiprocessing import Pool
from json import dumps

def individual_simulation(args: tuple[int, dict[str, float], dict[str, list]]):
    timesteps, international_interference, investment_policies = args
    global_sampled_coefficients: Coefficients = Coefficients(
            production_efficiency=8,
            military_capability_weight=np.random.uniform(5e-5, 1e-3),
            sanctions_delay=int(np.random.normal(60, 10)),
            foreign_aid_delay=int(np.random.normal(60, 10)),
            elasticity_coefficient=np.random.uniform(1e-4, 8e-4),
            military_technology_investment_coefficient=np.random.uniform(5e-4, 5e-3),
            industrial_technology_investment_coefficient=np.random.uniform(1e-4, 1e-3),
            military_industrial_investment_coefficient=np.random.uniform(1e-1, 1e0),
            civilian_industrial_investment_coefficient=np.random.uniform(1e-2, 5e-1),
            military_consumption_cost_coefficient=np.random.uniform(1e-4, 1e-3),
            military_demand_coefficient=np.random.uniform(1, 10),
            military_attrition_coefficient=np.random.uniform(1e-6, 5e-4),
            industrial_attrition_coefficient=np.random.uniform(8e-8, 1e-6),
            spending_scaling_coefficient=np.random.uniform(1e-1, 1e0),
            conflict_intensity=2.5,
            epsilon=1e-10,
        )
        
    return run_simulation(timesteps, global_sampled_coefficients, international_interference, investment_policies, monte_carlo=True)

def run_monte_carlo_simulation(num_simulations: int, international_interference: dict[str, float] = None, investment_policies: dict[str, list] = None, plot_line: bool = False, plot_histograms: bool = False, export: bool = False):
    timesteps = 3650
    winners = []
    reasons = []
    lengths = []
    russia_results = []
    ukraine_results = []

    if not international_interference:
        international_interference: dict[str, float] = {}
        international_interference['foreign_aid_russia'] = 0
        international_interference['sanctions_ukraine'] = 0
        international_interference['foreign_aid_ukraine'] = .24
        international_interference['sanctions_russia'] = .14

    if not investment_policies:
        investment_policies: dict[str, list] = {}
        investment_policies['ukraine'] = [.25, .25, .25, .25]
        investment_policies['russia'] = [.25, .25, .25, .25]

    with Pool(processes=12) as pool:
        results = pool.imap(individual_simulation, [(timesteps, international_interference, investment_policies)] * num_simulations)
        
        for result in results:
            russia, ukraine, length, winner, reason = result
            russia_results.append(russia)
            ukraine_results.append(ukraine)
            winners.append(winner)
            reasons.append(reason)
            lengths.append(length)

    print("-----------------")
    print(f"Ran {num_simulations} Simulations")
    print(f"Average length of conflict: {np.mean(lengths) / 365.0} years")
    print(f"Standard deviation of conflict length: {np.std(lengths) / 365.0} years")
    print(f"Most wins: {max(set(winners), key=winners.count)}")
    print(f"Number of inconclusive simulations: {winners.count('None')}")

    if export:
        results_dict = {
            "winners": winners,
            "lengths": lengths,
            "reasons": reasons,
        }
        for name, x in [("russia", russia_results), ("ukraine", ukraine_results)]:
            gdp, military_capability, civilian_industrial_capacity, military_industrial_capacity, military_technology, industrial_technology, price_level, budget, spending = combine_simulation_results(x, max(lengths))
            results_dict[f"{name}_gdp"] = list(calc_confidence_interval_time_series(gdp))
            results_dict[f"{name}_military_capability"] = list(calc_confidence_interval_time_series(military_capability))
            results_dict[f"{name}_civilian_industrial_capacity"] = list(calc_confidence_interval_time_series(civilian_industrial_capacity))
            results_dict[f"{name}_military_industrial_capacity"] = list(calc_confidence_interval_time_series(military_industrial_capacity))
            results_dict[f"{name}_military_technology"] = list(calc_confidence_interval_time_series(military_technology))
            results_dict[f"{name}_industrial_technology"] = list(calc_confidence_interval_time_series(industrial_technology))
            results_dict[f"{name}_price_level"] = list(calc_confidence_interval_time_series(price_level))
            results_dict[f"{name}_budget"] = list(calc_confidence_interval_time_series(budget))
            results_dict[f"{name}_spending"] = list(calc_confidence_interval_time_series(spending))

        with open(f"data/ukraine_{investment_policies.get('ukraine')}_russia_{investment_policies.get('russia')}_aid_{international_interference.get('foreign_aid_ukraine')}_sanctions_{international_interference.get('sanctions_russia')}.json", "w") as file:
            file.write(dumps(results_dict, indent=4))
        del results_dict

    if plot_histograms:
        plot_monte_carlo_histograms(lengths, winners, reasons)
    if plot_line:
        plot_monte_carlo_line([russia_results, ukraine_results], "GDP (Billions, PPP$)", max(lengths))

    del winners, reasons, lengths, russia_results, ukraine_results
        

if __name__ == "__main__":
    run_monte_carlo_simulation(10000, plot_histograms=False, export=True)