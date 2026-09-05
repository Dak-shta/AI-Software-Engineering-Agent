from agent.code_generator import generate_code_change
from agent.apply_change import apply_code_change


REPO = "sample_repo"


query = "Add an email attribute to the User class."

print("Generating code change...\n")

generated_response = generate_code_change(query)

print(generated_response)

print("\nApplying change...\n")

result = apply_code_change(
    REPO,
    generated_response
)

print(result)