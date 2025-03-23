import matplotlib.pyplot as plt
import seaborn as sns
from classes import Belligerant
import polars as pl
from multiprocessing import Pool
import altair as alt
import pandas as pd

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