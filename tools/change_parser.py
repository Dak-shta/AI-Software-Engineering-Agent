import re


def parse_code_change(response: str):
    file_match = re.search(
        r"FILE:\s*(.+)",
        response
    )

    if not file_match:
        raise ValueError(
            "Could not find FILE in generated response."
        )

    file_path = file_match.group(1).strip()

    # Extract everything between PROPOSED CODE and REASON.
    code_match = re.search(
        r"PROPOSED CODE:\s*(.*?)(?:\n\s*REASON:|\Z)",
        response,
        re.DOTALL
    )

    if not code_match:
        raise ValueError(
            "Could not find PROPOSED CODE in generated response."
        )

    code = code_match.group(1).strip()

    # Remove markdown code fences if present.
    code = re.sub(
        r"^```(?:python)?\s*",
        "",
        code
    )

    code = re.sub(
        r"\s*```$",
        "",
        code
    )

    return {
        "file": file_path,
        "code": code.strip()
    }