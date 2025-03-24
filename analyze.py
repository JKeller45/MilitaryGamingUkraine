import data_analysis as da
import polars as pl

file_name = 'ukraine_[0.25, 0.25, 0.25, 0.25]_russia_[0.25, 0.25, 0.25, 0.25]_aid_0.24_sanctions_0.14'
data = pl.read_csv(f"data/{file_name}.csv", glob=False)

da.plot_monte_carlo_histograms(data['lengths'], data['winners'], data['reasons'])
da.plot_dashboard_from_csv(data)