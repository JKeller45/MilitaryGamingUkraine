from simulation import run_simulation
from classes import Coefficients
import numpy as np
from data_analysis import plot_monte_carlo_histograms, plot_monte_carlo_line
from multiprocessing import Pool

def individual_simulation(timesteps: int):
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
        
    return run_simulation(timesteps, global_sampled_coefficients, monte_carlo=True)

def run_monte_carlo_simulation(num_simulations: int, plot_line: bool = False):
    timesteps = 3600
    winners = []
    reasons = []
    lengths = []
    russia_results = []
    ukraine_results = []

    with Pool(processes=12) as pool:
        results = pool.imap(individual_simulation, [timesteps] * num_simulations)
        
        for result in results:
            russia, ukraine, length, winner, reason = result
            russia_results.append(russia)
            ukraine_results.append(ukraine)
            winners.append(winner)
            reasons.append(reason)
            lengths.append(length)

    print(f"Ran {num_simulations} Simulations")
    print(f"Average length of conflict: {np.mean(lengths)}")
    print(f"Most wins: {max(set(winners), key=winners.count)}")
    print(f"Number of inconclusive simulations: {winners.count('None')}")

    plot_monte_carlo_histograms(lengths, winners, reasons)
    if plot_line:
        plot_monte_carlo_line([russia_results, ukraine_results], "GDP (Billions, PPP$)", max(lengths))

if __name__ == "__main__":
    run_monte_carlo_simulation(25000)