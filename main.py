from agent.code_generator import generate_code_change


query = "Add an email attribute to the User class."

result = generate_code_change(query)

print("\nProposed Code Change:")
print(result)