from inspect_viz import Component, Data, Param, Selection
from inspect_viz.input import select, slider
from inspect_viz.layout import hconcat, vconcat
from inspect_viz.mark import bar_y, cell, rule_x
from inspect_viz.plot import legend, plot
from inspect_viz.table import column, table
from inspect_viz.transform import avg, column, sql


def evals_bar_plot(
    evals: Data,
    ci: float = 0.95,
    score_field: str = "score_headline_value",
    stderr_field: str = "score_headline_stderr",
    score_domain: list[float] = [0, 1.0],
) -> Component:
    """Bar plot that summarizes evals scores by model and task.

    By default, scores used for plotting are the headline metric and stderr extracted by the `evals_df()` function from the `inspect_ai` package (which is the first score in the eval results). Specify alternative `score_field` and/or `stderr_field` options to override the default fields.

    Args:
       evals: Evals data table.
       ci: Confidence interval (defaults to 0.95)
       score_field: Name of field containing score value in data table.
       stderr_field: Name of field containing stderr in data table.
       score_domain: Domain (beginning and ending values) for y-axis.
    """
    # compute z_alpha for confidence interval
    z_alpha = _z_alpha(ci)

    # render plot
    return plot(
        # main bar plot
        bar_y(
            evals,
            # models (faceted by task) on x-axis
            x="model",
            fx="task_name",
            # headline metric score on y-axis
            y=score_field,
            # model as fill color
            fill="model",
        ),
        # confidence intervals
        rule_x(
            evals,
            # model (faceted by task) on x-axis
            x="model",
            fx="task_name",
            # line between confidence interval points w/ tick at end
            y1=sql(f"{score_field} - ({z_alpha} * {stderr_field})"),
            y2=sql(f"{score_field} + ({z_alpha} * {stderr_field})"),
            stroke="black",
            marker="tick-x",
        ),
        # model legend at bottom (remove some extraneous labels and margin)
        legend=legend("color", location="bottom"),
        x_label=None,
        x_ticks=[],
        fx_label=None,
        margin_bottom=10,
        # y axis w/ score domain
        y_label="score",
        y_domain=score_domain,
        y_inset_top=10,
    )


def evals_table(
    evals: Data,
    metric_field: str = "score_headline_metric",
    score_field: str = "score_headline_value",
    stderr_field: str = "score_headline_stderr",
) -> Component:
    """Table that summarizes eval scores by model and task.

    Args:
       evals: Evals data table.
       metric_field: Name of field containing score metric in data table.
       score_field: Name of field containing score value in data table.
       stderr_field: Name of field containing stderr in data table.
    """
    return table(
        data=evals,
        columns=[
            column("model", label="Model"),
            column("task_name", label="Task"),
            column(metric_field, label="Metric"),
            column(score_field, label="Value", align="center"),
            column(stderr_field, label="Stderr", align="center"),
        ],
    )


def _z_alpha(ci: float = 0.95):
    """
    Calculate z_alpha (critical value) for a given confidence level

    Args:
        ci: Confidence level (e.g., 0.95 for 95%)

    Returns:
        z_alpha: Critical value for the confidence interval
    """
    z_values = {
        0.80: 1.282,
        0.85: 1.440,
        0.90: 1.645,
        0.95: 1.960,
        0.975: 2.241,
        0.99: 2.576,
        0.995: 2.807,
        0.999: 3.291,
    }

    if ci in z_values:
        return z_values[ci]
    else:
        raise ValueError(
            f"Please use one of these confidence levels: {list(z_values.keys())}"
        )


def evals_heatmap_plot(
    evals: Data,
    row_field: str = "model",
    column_field: str = "id",
    score_field: str = "score",
    color_palette: str = "reds",
) -> Component:
    """
    Creates a heatmap plot of success rate of eval data.

    Args:
       evals: Evals data table.
       row_field: Name of field to use for rows.
       column_field: Name of field to use for columns.
       score_field: Name of field containing score value in data table.
       color_palette: Name of color palette to use.
    """

    heatmap = plot(
        cell(
            evals,
            x=column_field,
            y=row_field,
            fill=avg(score_field),
            tip=True,
        ),
        color_scheme=color_palette,
        color_scale="linear",
        color_domain=[0, 1],
        legend=legend("color", location="bottom"),
        x_tick_rotate=90,
        margin_left=100,
        margin_bottom=100,
        height=260,
        x_label=None,
        y_label=None,
    )

    return vconcat(
        hconcat(
            select(evals, label=column_field, column=column_field),
            select(evals, label=row_field, column=row_field),
        ),
        heatmap,
    )


def evals_pass_at_k_heatmap_plot(
    evals: Data,
    row_field: str = "model",
    column_field: str = "id",
    color_palette: str = "reds",
    min_k: int = 1,
    max_k: int = 5,
) -> Component:
    """
    Creates a heatmap plot of evals data. Assumes that pass@k values are already computed.

    Args:
       evals: Evals data table.
       row_field: Name of field to use for rows.
       column_field: Name of field to use for columns.
       color_palette: Name of color palette to use.
       min_k: Minimum value for k (pass@k).
       max_k: Maximum value for k (pass@k).
    """
    k = Param(1)

    k_slider = slider(
        min=min_k,
        max=max_k,
        step=1,
        value=1,
        label="k (pass@k)",
        target=k,
        width=250,
    )

    heatmap = plot(
        cell(
            evals,
            x=column_field,
            y=row_field,
            fill=column(k),
            tip=True,
        ),
        color_scheme=color_palette,
        color_scale="linear",
        color_domain=[0, 1],
        legend=legend("color", location="bottom"),
        x_tick_rotate=90,
        margin_left=100,
        margin_bottom=100,
        height=260,
        x_label=None,
        y_label=None,
    )

    return vconcat(
        hconcat(
            select(evals, label=column_field, column=column_field),
            select(evals, label=row_field, column=row_field),
            k_slider,
        ),
        heatmap,
    )
