import os

print("Hello World from Python!!")
print("Deployed after approval")

print(f"CIRCLE_PROJECT_ID: {os.getenv("CIRCLE_PROJECT_ID")}")

print("Duplicate pipeline deleted!")