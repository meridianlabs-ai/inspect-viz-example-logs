
from inspect_viz import Component, Data
from inspect_viz.plot import plot, legend
from inspect_viz.mark import bar_y, rule_x
from inspect_viz.table import column, table
from inspect_viz.transform import sql

def evals_bar_plot(
    evals: Data, 
    ci: float = 0.95, 
    score_field: str = "score_headline_value",
    stderr_field: str = "score_headline_stderr",
    score_domain: list[float] = [0,1.0]
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
    # compute z_alpha for confidency interval
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
            column(stderr_field, label="Stderr", align="center")
        ]
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
        0.999: 3.291
    }
    
    if ci in z_values:
        return z_values[ci]
    else:
        raise ValueError(f"Please use one of these confidence levels: {list(z_values.keys())}")
 
