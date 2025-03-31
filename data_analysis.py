import matplotlib.pyplot as plt
import seaborn as sns
from classes import Belligerant
import polars as pl
from multiprocessing import Pool
import altair as alt
import pandas as pd
import numpy as np

def history_to_dict(belligerant: Belligerant, max_length=0, monte_carlo=False) -> dict[str, list]:
    data: dict = {}
    if not monte_carlo:
        data = {
            "Time": [i / 365.0 for i in belligerant.history.time],
            "GDP (Billions, PPP$)": belligerant.history.economic_capital,
            "Military Capability": belligerant.history.military_capability,
            "Civilian Industrial Capacity": belligerant.history.civilian_industrial_capacity,
            "Military Industrial Capacity": belligerant.history.military_industrial_capacity,
            "Military Technology": belligerant.history.military_technology,
            "Industrial Technology": belligerant.history.industrial_technology,
            "Price Level": belligerant.history.price_level,
            "Budget (Billions, PPP$)": belligerant.history.budget,
            "Spending (Billions, PPP$)": belligerant.history.spending,
            "Belligerant": belligerant.name
        }
    else:
        data = {
            "Time": [i / 365.0 for i in range(max_length)],
            "GDP (Billions, PPP$)": (belligerant.history.economic_capital + [belligerant.history.economic_capital[-1]] * (max_length - len(belligerant.history.economic_capital)))[:max_length],
            "Military Capability": (belligerant.history.military_capability + [belligerant.history.military_capability[-1]] * (max_length - len(belligerant.history.military_capability)))[:max_length],
            "Civilian Industrial Capacity": (belligerant.history.civilian_industrial_capacity + [belligerant.history.civilian_industrial_capacity[-1]] * (max_length - len(belligerant.history.civilian_industrial_capacity)))[:max_length],
            "Military Industrial Capacity": (belligerant.history.military_industrial_capacity + [belligerant.history.military_industrial_capacity[-1]] * (max_length - len(belligerant.history.military_industrial_capacity)))[:max_length],
            "Military Technology": (belligerant.history.military_technology + [belligerant.history.military_technology[-1]] * (max_length - len(belligerant.history.military_technology)))[:max_length],
            "Industrial Technology": (belligerant.history.industrial_technology + [belligerant.history.industrial_technology[-1]] * (max_length - len(belligerant.history.industrial_technology)))[:max_length],
            "Price Level": (belligerant.history.price_level + [belligerant.history.price_level[-1]] * (max_length - len(belligerant.history.price_level)))[:max_length],
            "Budget (Billions, PPP$)": (belligerant.history.budget + [belligerant.history.budget[-1]] * (max_length - len(belligerant.history.budget)))[:max_length],
            "Spending (Billions, PPP$)": (belligerant.history.spending + [belligerant.history.spending[-1]] * (max_length - len(belligerant.history.spending)))[:max_length],
            "Belligerant": belligerant.name
        }

    return data

def process_belligerent(belligerant, max_length):
    return pl.DataFrame(history_to_dict(belligerant, max_length, monte_carlo=True), strict=False)

def monte_carlo_to_df(belligerant_runs: list[list[Belligerant]], max_length: int):
    combined_data = []
    for belligerants in belligerant_runs:
        with Pool(processes=12) as pool:
            combined_data = pool.starmap(process_belligerent, [(b, max_length) for belligerants_group in belligerant_runs for b in belligerants_group])

    return pl.concat(combined_data)

def plot_dashboard(belligerants: list[Belligerant]):
    combined_data = []
    for belligerant in belligerants:
        df = history_to_dict(belligerant)
        combined_data.append(df)

    data = pl.concat([pl.DataFrame(data, strict=False) for data in combined_data])

    sns.set_theme(style="darkgrid")
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))

    sns.lineplot(data=data, x="Time", y="GDP (Billions, PPP$)", hue="Belligerant", ax=axs[0, 0])
    sns.lineplot(data=data, x="Time", y="Budget (Billions, PPP$)", hue="Belligerant", ax=axs[1, 2])
    sns.lineplot(data=data, x="Time", y="Spending (Billions, PPP$)", hue="Belligerant", ax=axs[2, 2])
    sns.lineplot(data=data, x="Time", y="Military Capability", hue="Belligerant", ax=axs[0, 1])
    sns.lineplot(data=data, x="Time", y="Civilian Industrial Capacity", hue="Belligerant", ax=axs[1, 0])
    sns.lineplot(data=data, x="Time", y="Military Industrial Capacity", hue="Belligerant", ax=axs[1, 1])
    sns.lineplot(data=data, x="Time", y="Military Technology", hue="Belligerant", ax=axs[2, 0])
    sns.lineplot(data=data, x="Time", y="Industrial Technology", hue="Belligerant", ax=axs[2, 1])
    sns.lineplot(data=data, x="Time", y="Price Level", hue="Belligerant", ax=axs[0, 2])

    plt.tight_layout()
    plt.show()

def plot_dashboard_from_csv(data: dict):
    sns.set_theme(style="darkgrid")
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    time = [i / 365.0 for i in range(len(data['ukraine_gdp']))]

    sns.lineplot(x=time, y=data['ukraine_gdp'], label="Ukraine", ax=axs[0, 0])
    sns.lineplot(x=time, y=data['russia_gdp'], label="Russia", ax=axs[0, 0])
    axs[0, 0].fill_between(x=time, y1=data['ukraine_gdp_lower'], y2=data['ukraine_gdp_upper'], alpha=0.3)
    axs[0, 0].fill_between(x=time, y1=data['russia_gdp_lower'], y2=data['russia_gdp_upper'], alpha=0.3)
    axs[0, 0].set_xlabel("Time (Years)")
    axs[0, 0].set_ylabel("GDP (Billions, PPP$)")
    axs[0, 0].set_title("GDP Over Time")
    axs[0, 0].legend(loc="upper right")

    sns.lineplot(x=time, y=data['ukraine_military_capability'], label="Ukraine", ax=axs[0, 1])
    sns.lineplot(x=time, y=data['russia_military_capability'], label="Russia", ax=axs[0, 1])
    axs[0, 1].fill_between(x=time, y1=data['ukraine_military_capability_lower'], y2=data['ukraine_military_capability_upper'], alpha=0.3)
    axs[0, 1].fill_between(x=time, y1=data['russia_military_capability_lower'], y2=data['russia_military_capability_upper'], alpha=0.3)
    axs[0, 1].set_xlabel("Time (Years)")
    axs[0, 1].set_ylabel("Military Capability")
    axs[0, 1].set_title("Military Capability Over Time")
    axs[0, 1].legend(loc="lower right")

    sns.lineplot(x=time, y=data['ukraine_price_level'], label="Ukraine", ax=axs[0, 2])
    sns.lineplot(x=time, y=data['russia_price_level'], label="Russia", ax=axs[0, 2])
    axs[0, 2].fill_between(x=time, y1=data['ukraine_price_level_lower'], y2=data['ukraine_price_level_upper'], alpha=0.3)
    axs[0, 2].fill_between(x=time, y1=data['russia_price_level_lower'], y2=data['russia_price_level_upper'], alpha=0.3)
    axs[0, 2].set_xlabel("Time (Years)")
    axs[0, 2].set_ylabel("Price Level")
    axs[0, 2].set_title("Price Level Over Time")
    axs[0, 2].legend(loc="lower right")

    sns.lineplot(x=time, y=data['ukraine_civilian_industrial_capacity'], label="Ukraine", ax=axs[1, 0])
    sns.lineplot(x=time, y=data['russia_civilian_industrial_capacity'], label="Russia", ax=axs[1, 0])
    axs[1, 0].fill_between(x=time, y1=data['ukraine_civilian_industrial_capacity_lower'], y2=data['ukraine_civilian_industrial_capacity_upper'], alpha=0.3)
    axs[1, 0].fill_between(x=time, y1=data['russia_civilian_industrial_capacity_lower'], y2=data['russia_civilian_industrial_capacity_upper'], alpha=0.3)
    axs[1, 0].set_xlabel("Time (Years)")
    axs[1, 0].set_ylabel("Civilian Industrial Capacity")
    axs[1, 0].set_title("Civilian Industrial Capacity Over Time")
    axs[1, 0].legend(loc="right")

    sns.lineplot(x=time, y=data['ukraine_military_industrial_capacity'], label="Ukraine", ax=axs[1, 1])
    sns.lineplot(x=time, y=data['russia_military_industrial_capacity'], label="Russia", ax=axs[1, 1])
    axs[1, 1].fill_between(x=time, y1=data['ukraine_military_industrial_capacity_lower'], y2=data['ukraine_military_industrial_capacity_upper'], alpha=0.3)
    axs[1, 1].fill_between(x=time, y1=data['russia_military_industrial_capacity_lower'], y2=data['russia_military_industrial_capacity_upper'], alpha=0.3)
    axs[1, 1].set_xlabel("Time (Years)")
    axs[1, 1].set_ylabel("Military Industrial Capacity")
    axs[1, 1].set_title("Military Industrial Capacity Over Time")
    axs[1, 1].legend(loc="right")

    sns.lineplot(x=time, y=data['ukraine_budget'], label="Ukraine", ax=axs[1, 2])
    sns.lineplot(x=time, y=data['russia_budget'], label="Russia", ax=axs[1, 2])
    axs[1, 2].fill_between(x=time, y1=data['ukraine_budget_lower'], y2=data['ukraine_budget_upper'], alpha=0.3)
    axs[1, 2].fill_between(x=time, y1=data['russia_budget_lower'], y2=data['russia_budget_upper'], alpha=0.3)
    axs[1, 2].set_xlabel("Time (Years)")
    axs[1, 2].set_ylabel("Budget (Billions, PPP$)")
    axs[1, 2].set_title("Budget Over Time")
    axs[1, 2].legend(loc="upper right")

    sns.lineplot(x=time, y=data['ukraine_military_technology'], label="Ukraine", ax=axs[2, 0])
    sns.lineplot(x=time, y=data['russia_military_technology'], label="Russia", ax=axs[2, 0])
    axs[2, 0].fill_between(x=time, y1=data['ukraine_military_technology_lower'], y2=data['ukraine_military_technology_upper'], alpha=0.3)
    axs[2, 0].fill_between(x=time, y1=data['russia_military_technology_lower'], y2=data['russia_military_technology_upper'], alpha=0.3)
    axs[2, 0].set_xlabel("Time (Years)")
    axs[2, 0].set_ylabel("Military Technology")
    axs[2, 0].set_title("Military Technology Over Time")
    axs[2, 0].legend(loc="lower right")

    sns.lineplot(x=time, y=data['ukraine_industrial_technology'], label="Ukraine", ax=axs[2, 1])
    sns.lineplot(x=time, y=data['russia_industrial_technology'], label="Russia", ax=axs[2, 1])
    axs[2, 1].fill_between(x=time, y1=data['ukraine_industrial_technology_lower'], y2=data['ukraine_industrial_technology_upper'], alpha=0.3)
    axs[2, 1].fill_between(x=time, y1=data['russia_industrial_technology_lower'], y2=data['russia_industrial_technology_upper'], alpha=0.3)
    axs[2, 1].set_xlabel("Time (Years)")
    axs[2, 1].set_ylabel("Industrial Technology")
    axs[2, 1].set_title("Industrial Technology Over Time")
    axs[2, 1].legend(loc="lower right")

    sns.lineplot(x=time, y=data['ukraine_spending'], label="Ukraine", ax=axs[2, 2])
    sns.lineplot(x=time, y=data['russia_spending'], label="Russia", ax=axs[2, 2])
    axs[2, 2].fill_between(x=time, y1=data['ukraine_spending_lower'], y2=data['ukraine_spending_upper'], alpha=0.3)
    axs[2, 2].fill_between(x=time, y1=data['russia_spending_lower'], y2=data['russia_spending_upper'], alpha=0.3)
    axs[2, 2].set_xlabel("Time (Years)")
    axs[2, 2].set_ylabel("Spending (Billions, PPP$)")
    axs[2, 2].set_title("Spending Over Time")
    axs[2, 2].legend(loc="upper right")

    plt.tight_layout()
    plt.show()


def plot_monte_carlo_line(belligerants: list[list[Belligerant]], variable: str, max_length: int):
    df = monte_carlo_to_df(belligerants, max_length)

    mean_line = alt.Chart(df).mark_line().encode(
        x='Time',
        y=alt.Y(f'mean({variable}):Q', title=f'Mean {variable}'),
        color='Belligerant'
    )
        
    band = alt.Chart(df).mark_errorband(extent='ci').encode(
        x='Time',
        y='GDP (Billions, PPP$)',
        color='Belligerant',
    )

    (mean_line + band).properties(width=800, height=400).interactive().show()

def plot_monte_carlo_histograms(lengths: list, winners: list, reasons: list):
    sns.set_theme(style="darkgrid")
    fig, axs = plt.subplots(1, 3, figsize=(15, 8))

    lengths = [length / 365.0 for length in lengths]
    
    df = pd.DataFrame({"Length of Conflict": lengths, "Winner": winners})
    hist1 = sns.histplot(df, bins=100, ax=axs[0], multiple="stack", x="Length of Conflict", hue="Winner")
    hist1.set_xticks(range(0, 11))
    axs[0].set_title("Winner by Length of Conflict")
    axs[0].set_xlabel("Length of Conflict (Years)")
    axs[0].set_ylabel("Frequency")

    df = pd.DataFrame({"Length of Conflict": lengths, "Reason": reasons})
    hist2 = sns.histplot(df, bins=100, ax=axs[1], multiple="stack", x="Length of Conflict", hue="Reason")
    hist2.set_xticks(range(0, 11))
    axs[1].set_title("Victory Reason by Length of Conflict")
    axs[1].set_xlabel("Length of Conflict (Years)")
    axs[1].set_ylabel("Frequency")

    pruned_winners = [winner for winner in winners if winner != "None"]
    reasons = [reason for reason in reasons if reason != "None"]
    russian_federation = [reason for winner, reason in zip(pruned_winners, reasons) if winner == "Russian Federation"]
    ukraine = [reason for winner, reason in zip(pruned_winners, reasons) if winner == "Ukraine"]
    military_superiority_by_country = [russian_federation.count("Military Superiority"), ukraine.count("Military Superiority")]
    enemy_economic_collapse_by_country = [russian_federation.count("Enemy Economic Collapse"), ukraine.count("Enemy Economic Collapse")]
    enemy_military_collapse_by_country = [russian_federation.count("Enemy Military Collapse"), ukraine.count("Enemy Military Collapse")]

    df = pd.DataFrame({"Military Superiority": military_superiority_by_country,
                       "Enemy Economic Collapse": enemy_economic_collapse_by_country,
                       "Enemy Military Collapse": enemy_military_collapse_by_country},
                      index=["Russian Federation", "Ukraine"]) 
    df.plot(kind="bar", stacked=True, ax=axs[2])
    plt.title("Victory Reason")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

def calc_confidence_interval_time_series(data: np.ndarray, z_score=1.96):
    means = np.mean(data, axis=1)
    std_errs = np.std(data, axis=1, ddof=1) / np.sqrt(data.shape[1])
    intervals = std_errs * z_score
    lower_bounds = means - intervals
    upper_bounds = means + intervals
    return means, lower_bounds, upper_bounds

def calc_extend_means(data, max_length):
    values_at_index = [[] for _ in range(max_length)]

    for lst in data:
        for i, val in enumerate(lst):
            values_at_index[i].append(val)
    means = np.array([np.mean(vals) for vals in values_at_index])

    padded_data = []
    for lst in data:
        padded = lst + means[len(lst):].tolist()
        padded_data.append(padded)
        
    return padded_data

def combine_simulation_results(data: list[Belligerant], max_length: int, interpolate_means=False):
    if interpolate_means:
        gdp = np.stack(calc_extend_means([b.history.economic_capital for b in data], max_length), axis=1)
        military_capability = np.stack(calc_extend_means([b.history.military_capability for b in data], max_length), axis=1)
        civilian_industrial_capacity = np.stack(calc_extend_means([b.history.civilian_industrial_capacity for b in data], max_length), axis=1)
        military_industrial_capacity = np.stack(calc_extend_means([b.history.military_industrial_capacity for b in data], max_length), axis=1)
        military_technology = np.stack(calc_extend_means([b.history.military_technology for b in data], max_length), axis=1)
        industrial_technology = np.stack(calc_extend_means([b.history.industrial_technology for b in data], max_length), axis=1)
        price_level = np.stack(calc_extend_means([b.history.price_level for b in data], max_length), axis=1)
        budget = np.stack(calc_extend_means([b.history.budget for b in data], max_length), axis=1)
        spending = np.stack(calc_extend_means([b.history.spending for b in data], max_length), axis=1)
    else:
        gdp = np.stack([(b.history.economic_capital + [b.history.economic_capital[-1]] * (max_length - len(b.history.economic_capital)))[:max_length] for b in data], axis=1)
        military_capability = np.stack([(b.history.military_capability + [b.history.military_capability[-1]] * (max_length - len(b.history.military_capability)))[:max_length] for b in data], axis=1)
        civilian_industrial_capacity = np.stack([(b.history.civilian_industrial_capacity + [b.history.civilian_industrial_capacity[-1]] * (max_length - len(b.history.civilian_industrial_capacity)))[:max_length] for b in data], axis=1)
        military_industrial_capacity = np.stack([(b.history.military_industrial_capacity + [b.history.military_industrial_capacity[-1]] * (max_length - len(b.history.military_industrial_capacity)))[:max_length] for b in data], axis=1)
        military_technology = np.stack([(b.history.military_technology + [b.history.military_technology[-1]] * (max_length - len(b.history.military_technology)))[:max_length] for b in data], axis=1)
        industrial_technology = np.stack([(b.history.industrial_technology + [b.history.industrial_technology[-1]] * (max_length - len(b.history.industrial_technology)))[:max_length] for b in data], axis=1)
        price_level = np.stack([(b.history.price_level + [b.history.price_level[-1]] * (max_length - len(b.history.price_level)))[:max_length] for b in data], axis=1)
        budget = np.stack([(b.history.budget + [b.history.budget[-1]] * (max_length - len(b.history.budget)))[:max_length] for b in data], axis=1)
        spending = np.stack([(b.history.spending + [b.history.spending[-1]] * (max_length - len(b.history.spending)))[:max_length] for b in data], axis=1)

    return gdp, military_capability, civilian_industrial_capacity, military_industrial_capacity, military_technology, industrial_technology, price_level, budget, spending