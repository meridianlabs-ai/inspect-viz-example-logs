
from inspect_viz import Component, Data
from inspect_viz.plot import plot, legend
from inspect_viz.mark import bar_y, rule_x
from inspect_viz.table import column, table
from inspect_viz.transform import sql

def evals_bar_plot(evals: Data) -> Component:
    return plot(
        bar_y(evals, x="model", fx="task_name", y="score_headline_value", fill="model"),
        rule_x(
            evals,
            x="model",
            fx="task_name",
            y1=sql("score_headline_value - score_headline_stderr"),
            y2=sql("score_headline_value + score_headline_stderr"),
            stroke="black",
            marker="tick-x",
        ),
        legend=legend("color", location="bottom"),
        y_label="score",
        y_domain=[0,1.0],
        x_label=None,
        x_ticks=[],
        fx_label=None
    )


def evals_table(evals: Data) -> Component:
    return table(
        data=evals, 
        columns=[
            column("model", label="Model"), 
            column("task_name", label="Task"), 
            column("score_headline_metric", label="Metric"),
            column("score_headline_value", label="Value", align="center"),
            column("score_headline_stderr", label="Stderr", align="center")
        ]
    )