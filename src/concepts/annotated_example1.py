# Annotated as a Post-it note attached to a variable. The variable still works exactly the same, 
# but the "Post-it" contains extra instructions or information for other tools to read.
# We can use like email = Annotated[str, "This is an email address"]
# This helps in tools that can read these annotations to provide better support, like validation or documentation generation.
# We can attach validation rules like (must be a positive number) without cluttering the main type definition.

from typing import Annotated

# Define an annotated type for distance with extra metadata
Distance = Annotated[float, "units: meters"]

def calculate_speed(distance: Distance, time: float):
    return distance / time


speed = calculate_speed(100.0, 9.58)

print(f"Calculated Speed: {speed} m/s")
print(f"Extra Info: {Distance.__metadata__}")