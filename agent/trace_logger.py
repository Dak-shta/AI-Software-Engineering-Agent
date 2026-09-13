import json
from pathlib import Path
from datetime import datetime


class TraceLogger:

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.started_at = datetime.now().isoformat()
        self.steps = []

    def log_step(
        self,
        step_number,
        tool_name,
        arguments,
        observation,
        success
    ):
        self.steps.append({
            "step": step_number,
            "tool": tool_name,
            "arguments": arguments,
            "observation": observation,
            "success": success
        })

    def save(
        self,
        final_success,
        total_steps,
        tools_used
    ):
        trace = {
            "task_id": self.task_id,
            "started_at": self.started_at,
            "total_steps": total_steps,
            "tools_used": tools_used,
            "agent_completed": final_success,
            "steps": self.steps
        }

        output_dir = Path("evaluation/traces")
        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_dir /
            f"{self.task_id}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                trace,
                f,
                indent=2,
                default=str
            )

        return output_file