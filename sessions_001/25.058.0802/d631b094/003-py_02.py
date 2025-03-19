import numpy as np

def describe_grid(grid, name="Grid"):
    print(f"{name}:")
    print(f"  Shape: {grid.shape}")
    print(f"  Unique Values: {np.unique(grid)}")
    # Count of each unique value
    for value in np.unique(grid):
        count = np.sum(grid == value)
        print(f"  Count of {value}: {count}")

def analyze_example(input_grid, output_grid, transform_func):
    print("--- Analyzing Example ---")
    describe_grid(input_grid, "Input Grid")
    describe_grid(output_grid, "Output Grid")
    
    transformed_grid = transform_func(input_grid)
    describe_grid(transformed_grid, "Transformed Grid")

    print(f"Output Matches Transformed: {np.array_equal(output_grid, transformed_grid)}")
    print("--- End Analysis ---")


# Example Grids (replace with actual grids from the task)
example_grids = [
    (np.array([[6, 1, 1, 1, 1, 6, 6],
               [6, 1, 6, 6, 6, 1, 6],
               [6, 1, 6, 6, 6, 6, 6],
               [6, 1, 1, 6, 6, 6, 6]]),
     np.array([[1, 1, 1, 1, 1, 1, 1, 1]])),
    
    (np.array([[6, 1, 1, 1, 6, 6, 1, 6],
               [6, 6, 1, 6, 6, 1, 6, 6],
               [6, 6, 1, 6, 1, 6, 6, 6],
               [6, 6, 1, 1, 6, 6, 6, 6]]),
     np.array([[1, 1, 1, 1, 1, 1, 1]])),
    
    (np.array([[6, 1, 6, 6, 6, 6, 6, 6],
               [6, 1, 1, 6, 6, 6, 1, 6],
               [6, 6, 1, 6, 6, 1, 6, 6],
               [6, 6, 6, 6, 1, 6, 6, 6]]),
     np.array([[1, 1, 1, 1, 1]])),
]


# Analyze each example
for input_grid, output_grid in example_grids:
    analyze_example(input_grid, output_grid, transform)
