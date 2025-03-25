import data_analysis as da
import polars as pl

file_name = input("Enter the csv file name (excluding the .csv extension): ")
data = pl.read_csv(f"data/{file_name}.csv", glob=False)

da.plot_monte_carlo_histograms(data['lengths'], data['winners'], data['reasons'])
da.plot_dashboard_from_csv(data)