import numpy as np

def find_object(grid, color):
    coords = np.argwhere(grid == color)
    return coords

def analyze_example(input_grid, output_grid):
    azure_coords_in = find_object(input_grid, 8)
    yellow_coords_in = find_object(input_grid, 4)
    azure_coords_out = find_object(output_grid, 8)

    print("Input Grid:")
    print(input_grid)
    print("Output Grid:")
    print(output_grid)

    print("\nAzure Object Analysis:")
    print(f"  Initial Coordinates: {azure_coords_in}")
    print(f"  Initial Size: {len(azure_coords_in)} pixels")
    print(f"  Output Coordinates: {azure_coords_out}")
    print(f"  Output Size: {len(azure_coords_out)} pixels")

    print("\nYellow Object Analysis:")
    print(f"  Coordinates: {yellow_coords_in}")
    print(f"  Size: {len(yellow_coords_in)} pixels")

    print("\nGrid Boundaries:")
    print(f"  Height: {input_grid.shape[0]}, Width: {input_grid.shape[1]}")

# example_data is not available here, so it cannot execute
#for i, (input_grid, output_grid) in enumerate(example_data):
#    print(f"\n--- Example {i+1} ---")
#    analyze_example(input_grid, output_grid)

#Mock the data to validate that the analysis script works
mock_input = np.array([[0,0,0,0,0],[0,8,0,0,0],[0,0,0,0,4],[0,0,0,0,0]])
mock_output = np.array([[0,8,8,0,0],[8,8,8,0,4],[0,8,8,0,4],[0,0,0,0,0]])

analyze_example(mock_input, mock_output)