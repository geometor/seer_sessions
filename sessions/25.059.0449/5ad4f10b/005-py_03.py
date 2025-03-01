import numpy as np

def get_azure_bounding_box(grid):
    # Find coordinates of all azure pixels
    azure_coords = np.argwhere(grid == 8)
    
    if azure_coords.size == 0:  # Handle the case with no azure pixels
        #default
        min_row, min_col = 0,0
        max_row, max_col = 2,2
        return min_row, min_col, max_row, max_col

    # Find minimum and maximum row and column
    min_row = np.min(azure_coords[:, 0])
    max_row = np.max(azure_coords[:, 0])
    min_col = np.min(azure_coords[:, 1])
    max_col = np.max(azure_coords[:, 1])

    return min_row, min_col, max_row, max_col

def analyze_transform(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    
    min_row, min_col, max_row, max_col = get_azure_bounding_box(input_grid)
    
    print(f"Bounding Box: ({min_row}, {min_col}) to ({max_row}, {max_col})")
    print(f"Bounding Box Dimensions: {max_row - min_row + 1} x {max_col - min_col + 1}")

    # Extract the subgrid within the bounding box
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]
    print("Subgrid within Bounding Box:\n", subgrid)
    print("Expected Output Grid:\n", output_grid)


# Example Usage (Iterate through your training examples)
task_id = "6f8cd795"
train = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 8, 0], [0, 8, 0, 0, 5, 0, 0, 0, 8, 0], [0, 8, 0, 5, 5, 0, 0, 8, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 8, 8], [8, 5, 8], [8, 8, 8]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0], [0, 8, 0], [0, 0, 0]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 8, 5, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 8, 8], [8, 5, 8], [8, 8, 8]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 0, 0, 0, 0, 8, 0, 0], [0, 0, 8, 0, 5, 5, 0, 8, 0, 0], [0, 0, 8, 0, 0, 0, 0, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 8, 8], [8, 5, 8], [8, 8, 8]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 8, 0], [0, 8, 0, 0, 5, 0, 0, 0, 8, 0], [0, 8, 0, 5, 5, 0, 0, 8, 0, 0], [0, 8, 0, 0, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[8, 8, 8], [8, 5, 8], [8, 8, 8]],
    }
]

for example in train:
    print(f"Example Pair:")
    analyze_transform(example["input"], example["output"])
    print("-" * 20)
