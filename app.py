# This file generated by Quarto; do not edit by hand.
# shiny_mode: core

from __future__ import annotations

from pathlib import Path
from shiny import App, Inputs, Outputs, Session, ui

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shiny import render, reactive, ui

# ========================================================================




def server(input: Inputs, output: Outputs, session: Session) -> None:
    ui.input_slider("start_capital", "Initial investment", 1e5, 1e7, value=2e6, pre="$")

    ui.input_slider("return_mean", "Average annual investment return", 0, 30, value=5, step=0.5, post="%")

    ui.input_slider("inflation_mean", "Average annual inflation", 0, 20, value=2.5, step=0.5, post="%")

    ui.input_slider("monthly_withdrawal", "Monthly withdrawals", 0, 50000, value=10000, pre="$")

    # ========================================================================

    ui.input_slider("start_capital2", "Initial investment", 1e5, 1e7, value=2e6, pre="$")

    ui.input_slider("return_mean2", "Average annual investment return", 0, 30, value=5, step=0.5, post="%")

    ui.input_slider("inflation_mean2", "Average annual inflation", 0, 20, value=2.5, step=0.5, post="%")

    ui.input_slider("monthly_withdrawal2", "Monthly withdrawals", 0, 50000, value=8000, step=500, pre="$")

    # ========================================================================

    @render.plot()
    def nav_1():
        nav_df = run_simulation(
            input.start_capital(),
            input.return_mean() / 100,
            # input.return_stdev() / 100,
            .07,
            input.inflation_mean() / 100,
            # input.inflation_stdev() / 100,
            .015,
            input.monthly_withdrawal(),
            30,
            100
        )

        return make_plot(nav_df)

    # ========================================================================

    @render.plot()
    def nav_2():
        nav_df = run_simulation(
            input.start_capital2(),
            input.return_mean2() / 100,
            # input.return_stdev2() / 100,
            .07,
            input.inflation_mean2() / 100,
            # input.inflation_stdev2() / 100,
            .015,
            input.monthly_withdrawal2(),
            30,
            100
        )

        return make_plot(nav_df)

    # ========================================================================

    def create_matrix(rows, cols, mean, stdev):
        x = np.random.randn(rows, cols)
        x = mean + x * stdev
        return x


    def run_simulation(
        start_capital,
        return_mean,
        return_stdev,
        inflation_mean,
        inflation_stdev,
        monthly_withdrawal,
        n_years,
        n_simulations
    ):
        # Convert annual values to monthly
        n_months = 12 * n_years
        monthly_return_mean = return_mean / 12
        monthly_return_stdev = return_stdev / math.sqrt(12)
        monthly_inflation_mean = inflation_mean / 12
        monthly_inflation_stdev = inflation_stdev / math.sqrt(12)

        # Simulate returns and inflation
        monthly_returns = create_matrix(
            n_months, n_simulations, monthly_return_mean, monthly_return_stdev
        )
        monthly_inflation = create_matrix(
            n_months, n_simulations, monthly_inflation_mean, monthly_inflation_stdev
        )

        # Simulate withdrawals
        nav = np.full((n_months + 1, n_simulations), float(start_capital))
        for j in range(n_months):
            nav[j + 1, :] = (
                nav[j, :] *
                (1 + monthly_returns[j, :] - monthly_inflation[j, :]) -
                monthly_withdrawal
            )

        # Set nav values below 0 to NaN (Not a Number, which is equivalent to NA in R)
        nav[nav < 0] = np.nan

        # convert to millions
        nav = nav / 1000000

        return pd.DataFrame(nav)


    def make_plot(nav_df):
        # # For the histogram, we will fill NaNs with -1
        nav_df_zeros = nav_df.ffill().fillna(0).iloc[-1, :]

        # Define the figure and axes
        fig = plt.figure()

        # Create the top plot for time series on the first row that spans all columns
        ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)

        # Create the bottom left plot for the percentage above zero
        ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=2)

        for column in nav_df.columns:
            ax1.plot(nav_df.index, nav_df[column], alpha=0.3)

        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.title.set_text("Projected value of capital over 30 years")
        ax1.set_xlabel("Months")
        ax1.set_ylabel("Millions")
        ax1.grid(True)

        # Calculate the percentage of columns that are above zero for each date and plot (bottom left plot)
        percent_above_zero = (nav_df > 0).sum(axis=1) / nav_df.shape[1] * 100
        ax2.plot(nav_df.index, percent_above_zero, color='purple')
        ax2.set_xlim(nav_df.index.min(), nav_df.index.max())
        ax2.set_ylim(0, 100)  # Percentage goes from 0 to 100
        ax2.title.set_text("Percent of scenarios still paying")
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.set_xlabel("Months")
        ax2.grid(True)

        plt.tight_layout()

        return fig

    # ========================================================================



    return None


_static_assets = ["index_files","index_files/libs/quarto-html/tippy.css","index_files/libs/quarto-html/quarto-syntax-highlighting-01c78b5cd655e4cd89133cf59d535862.css","index_files/libs/bootstrap/bootstrap-icons.css","index_files/libs/bootstrap/bootstrap-f8c43d7765872cd89234a313bf24df9c.min.css","index_files/libs/quarto-dashboard/datatables.min.css","index_files/libs/clipboard/clipboard.min.js","index_files/libs/quarto-html/quarto.js","index_files/libs/quarto-html/popper.min.js","index_files/libs/quarto-html/tippy.umd.min.js","index_files/libs/quarto-html/anchor.min.js","index_files/libs/bootstrap/bootstrap.min.js","index_files/libs/quarto-dashboard/quarto-dashboard.js","index_files/libs/quarto-dashboard/stickythead.js","index_files/libs/quarto-dashboard/datatables.min.js","index_files/libs/quarto-dashboard/pdfmake.min.js","index_files/libs/quarto-dashboard/vfs_fonts.js","index_files/libs/quarto-dashboard/web-components.js","index_files/libs/quarto-dashboard/components.js"]
_static_assets = {"/" + sa: Path(__file__).parent / sa for sa in _static_assets}

app = App(
    Path(__file__).parent / "index.html",
    server,
    static_assets=_static_assets,
)
