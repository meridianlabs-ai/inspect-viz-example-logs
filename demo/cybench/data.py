
from pathlib import Path
from inspect_ai.analysis.beta import (
   evals_df, messages_df, 
   EvalModel, MessageColumns, SampleSummary, 
   prepare, log_viewer, model_info
)

CYBENCH_LOGS_DIR=(Path(__file__).parent.parent.parent / "logs/cybench").as_posix()


# read, prepare, and save evals
df = evals_df(CYBENCH_LOGS_DIR)

df = prepare(df, [
    model_info(),
    log_viewer("eval", url_mappings={
      CYBENCH_LOGS_DIR: "https://samples.meridianlabs.ai/"  
    })
])

df.to_parquet("cybench.parquet")


# read, prepare, and save messages
df = messages_df(CYBENCH_LOGS_DIR, columns=EvalModel + SampleSummary + MessageColumns)

df = df[[
    "eval_id",
    "sample_id",
    "message_id",
    "model",
    "id",
    "order",
    "tool_call_function",
    "limit",
    "log"
]]

df = prepare(df, [
    model_info(),
    log_viewer("message", url_mappings={
      CYBENCH_LOGS_DIR: "https://samples.meridianlabs.ai/"  
    })
])

df.to_parquet("cybench_tools.parquet")

