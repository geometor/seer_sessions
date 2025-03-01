import numpy as np

def describe_grid(grid):
    grid_np = np.array(grid)
    dims = grid_np.shape
    unique_colors = np.unique(grid_np)
    return f"Dimensions: {dims}, Unique Colors: {list(unique_colors)}"

def compare_grids(grid1, grid2):
    """Creates a diff map highlighting the differences between two grids."""
    # Ensure grids are NumPy arrays
    grid1_np = np.array(grid1)
    grid2_np = np.array(grid2)

    # Check if dimensions are compatible
    if grid1_np.shape != grid2_np.shape:
        return "Grids have different dimensions and cannot be compared directly."

    # Create a diff map where 1 indicates a difference and 0 indicates equality
    diff_map = (grid1_np != grid2_np).astype(int)

    return diff_map.tolist()

def reflect_diagonal(grid):
    """Reflects the grid along the main diagonal."""
    grid_np = np.array(grid)
    reflected_grid_np = grid_np.transpose()
    return reflected_grid_np.tolist()

task = "b9140dd3"
train_examples = [
    {
        "input": [
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
            [8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
            [8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
            [8, 8, 8, 8, 8, 8, 0, 0, 0, 0],
            [8, 8, 8, 8, 8, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 0, 0, 0, 0, 0, 8],
            [8, 8, 8, 0, 0, 0, 0, 0, 8, 8],
            [8, 8, 0, 0, 0, 0, 0, 8, 8, 8],
            [8, 0, 0, 0, 0, 0, 8, 8, 8, 8]
        ],
        "output": [
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 8, 8, 8, 8, 8],
            [8, 0, 0, 0, 0, 0, 8, 8, 8, 8],
            [8, 8, 0, 0, 0, 0, 0, 8, 8, 8],
            [8, 8, 8, 0, 0, 0, 0, 0, 8, 8],
            [8, 8, 8, 8, 0, 0, 0, 0, 0, 8]
        ]
    },
    {
        "input": [
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
            [8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
            [8, 8, 8, 8, 8, 8, 8, 0, 0, 0],
            [8, 8, 8, 8, 8, 8, 0, 0, 0, 0],
            [8, 8, 8, 8, 8, 0, 0, 0, 0, 8],
            [8, 8, 8, 8, 0, 0, 0, 0, 8, 8],
            [8, 8, 8, 0, 0, 0, 0, 8, 8, 8],
            [8, 8, 0, 0, 0, 0, 8, 8, 8, 8]
        ],
        "output": [
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 8, 8, 8, 8, 8, 8],
            [8, 0, 0, 0, 0, 8, 8, 8, 8, 8],
            [8, 8, 0, 0, 0, 0, 8, 8, 8, 8],
            [8, 8, 8, 0, 0, 0, 0, 8, 8, 8],
            [8, 8, 8, 8, 0, 0, 0, 0, 8, 8]
        ]
    },
     {
        "input":
        [
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
            [8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
            [8, 8, 8, 8, 8, 8, 8, 0, 0, 8],
            [8, 8, 8, 8, 8, 8, 0, 0, 8, 8],
            [8, 8, 8, 8, 8, 0, 0, 8, 8, 8],
            [8, 8, 8, 8, 0, 0, 8, 8, 8, 8]
        ],
        "output":
        [
           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
           [0, 8, 8, 8, 8, 8, 8, 8, 8, 8],
           [0, 0, 8, 8, 8, 8, 8, 8, 8, 8],
           [8, 0, 0, 8, 8, 8, 8, 8, 8, 8],
           [8, 8, 0, 0, 8, 8, 8, 8, 8, 8],
           [8, 8, 8, 0, 0, 8, 8, 8, 8, 8],
           [8, 8, 8, 8, 0, 0, 8, 8, 8, 8]
        ]
    }
]

results = []
for example in train_examples:
  input_grid = example['input']
  expected_output = example['output']
  predicted_output = reflect_diagonal(input_grid)
  results.append(
      {
          'input_description': describe_grid(input_grid),
          'expected_output_description': describe_grid(expected_output),
          'predicted_output_description': describe_grid(predicted_output),
          'diff_map_expected_vs_predicted': compare_grids(expected_output,predicted_output),
          'diff_map_input_vs_expected' : compare_grids(input_grid, expected_output)
      }
  )

for result in results:
  print(result)