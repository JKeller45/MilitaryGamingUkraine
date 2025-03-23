from simulation import run_simulation
from classes import Coefficients
import numpy as np
from data_analysis import plot_monte_carlo_histograms, plot_monte_carlo_line, monte_carlo_to_df
from multiprocessing import Pool

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
    timesteps = 3600
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
        df = monte_carlo_to_df([russia_results, ukraine_results], max(lengths))
        df.write_parquet(f"data/ukraine_{investment_policies.get('ukraine')}_russia_{investment_policies.get('russia')}_aid_{international_interference.get('foreign_aid_ukraine')}_sanctions_{international_interference.get('sanctions_russia')}.parquet", 
                         compression="brotli", 
                         compression_level=8, 
                         row_group_size=600_000, 
                         data_page_size=300_000)
        del df

    if plot_histograms:
        plot_monte_carlo_histograms(lengths, winners, reasons)
    if plot_line:
        plot_monte_carlo_line([russia_results, ukraine_results], "GDP (Billions, PPP$)", max(lengths))

    del winners, reasons, lengths, russia_results, ukraine_results
        

if __name__ == "__main__":
    run_monte_carlo_simulation(10000, plot_histograms=True, export=True)