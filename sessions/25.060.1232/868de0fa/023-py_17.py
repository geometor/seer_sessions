# Example Usage (and how we would get metrics)
import numpy as np

# Assume 'train' is a list of dictionaries, each with 'input' and 'output' grids
# Replace with the actual 'train' data from the ARC task

train = [
    {
        "input": np.array([[0,0,0],[0,1,0],[0,1,1]]),
        "output": np.array([[0,0,0],[0,7,0],[0,7,7]])
    },
    {
        "input": np.array([[0,0,0,0],[1,1,1,0],[0,0,1,0],[0,0,0,0]]),
        "output": np.array([[0,0,0,0],[2,2,2,0],[0,0,1,0],[0,0,0,0]])
    },
    {
        "input": np.array([[0,0,0,0,0],[0,1,1,1,0],[0,0,0,1,0],[0,0,0,1,0],[0,0,0,0,0]]),
        "output": np.array([[0,0,0,0,0],[0,7,7,7,0],[0,0,0,7,0],[0,0,0,7,0],[0,0,0,0,0]])
    },
        {
        "input": np.array([[0,0,0,0,0],[0,1,0,1,0],[0,0,0,0,0]]),
        "output": np.array([[0,0,0,0,0],[0,1,0,1,0],[0,0,0,0,0]])
    },
]

for i, example in enumerate(train):
    input_grid = example['input']
    expected_output_grid = example['output']
    predicted_output_grid = transform(input_grid.copy())  # Use a copy to avoid modifying the original

    print(f"--- Example {i+1} ---")
    print("Input:\n", input_grid)
    print("Expected Output:\n", expected_output_grid)
    print("Predicted Output:\n", predicted_output_grid)

    # Check for correctness
    if np.array_equal(expected_output_grid, predicted_output_grid):
        print("Result: Correct")
    else:
        print("Result: Incorrect")

    blue_regions = find_connected_regions(input_grid, 1)
    print(f"Number of blue regions: {len(blue_regions)}")

    for j, region in enumerate(blue_regions):
        print(f"  Region {j+1}:")
        print(f"    Coordinates: {region}")
        print(f"    L-shaped (current logic): {is_l_shaped(region, input_grid)}")
        # Add more detailed analysis here - bounding box dimensions, etc.

        # Analyze bounding box
        min_row = min(r for r, _ in region)
        max_row = max(r for r, _ in region)
        min_col = min(c for _, c in region)
        max_col = max(c for _, c in region)
        print(f"    Bounding Box: ({min_row}, {min_col}) to ({max_row}, {max_col})")
        rows = max_row - min_row + 1
        cols = max_col - min_col + 1
        print(f"    width: {cols}  height: {rows}")
        print(f"    area: {rows * cols}")
        print(f"    pixel count: {len(region)}")