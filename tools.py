tools = {
    'calculate':{
        'function_name':'calculate',
        'example_usage': 'e.g. calculate: 5+2',
        'description':'Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary'
    },
    'get_planet_mass':{
        'function_name':'get_planet_mass',
        'example_usage': 'e.g. get_planet_mass: earth',
        'description': 'returns weight of the planet in kg'
    },
    'get_planet_distance': {
        'function_name': 'get_planet_distance',
        'example_usage': 'e.g. get_planet_distance: Earth, Mars',
        'description': 'Calculates the distance between two planets in kilometers based on their average distances from the Sun'
    }
}

# Function to get planet mass
def get_planet_mass(planet):
    planet_masses = {
        'Mercury': 3.301e23,  # Mercury mass in kg
        'Venus': 4.867e24,    # Venus mass in kg
        'Earth': 5.972e24,    # Earth mass in kg
        'Mars': 6.417e23,     # Mars mass in kg
        'Jupiter': 1.898e27,  # Jupiter mass in kg
        'Saturn': 5.683e26,   # Saturn mass in kg
        'Uranus': 8.681e25,   # Uranus mass in kg
        'Neptune': 1.024e26,  # Neptune mass in kg
        # Add other celestial objects if needed
    }
    return planet_masses.get(planet, 0)


def get_planet_distance(planet1, planet2):
    # Average distances of planets from the Sun in millions of kilometers
    planet_distances_km = {
        'Mercury': 57.9e6,   # in km
        'Venus': 108.2e6,
        'Earth': 149.6e6,
        'Mars': 227.9e6,
        'Jupiter': 778.5e6,
        'Saturn': 1433.5e6,
        'Uranus': 2872.5e6,
        'Neptune': 4495.1e6,
    }

    # Get distances of the two planets
    dist1 = planet_distances_km.get(planet1)
    dist2 = planet_distances_km.get(planet2)

    if dist1 is None or dist2 is None:
        return f"Error: One or both planets not found in the dataset."

    # Calculate and return the absolute difference
    distance_between = abs(dist1 - dist2)
    return distance_between

# Function to calculate an expression given as a string
def calculate(expression):
    return eval(expression)
