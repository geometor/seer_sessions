import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns details about differences."""
    if grid1.shape != grid2.shape:
        return f"Shape mismatch: {grid1.shape} vs {grid2.shape}"
    else:
        diff = grid1 != grid2
        num_diffs = np.sum(diff)
        diff_indices = np.where(diff)
        diff_details = []
        for i in range(len(diff_indices[0])):
            row, col = diff_indices[0][i], diff_indices[1][i]
            diff_details.append(
                f"  Pixel ({row}, {col}): Expected {grid2[row, col]}, Got {grid1[row, col]}"
            )
        return {
            "num_diffs": num_diffs,
            "diff_details": diff_details,
            "shape": grid1.shape
                }

# Example usage with previous transform and example data
# (Assuming input_output_pairs is defined as in the initial notebook)

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    # 1. Locate Subgrid
    rows, cols = input_grid.shape
    subgrid_height = 10
    subgrid_width = 9
    start_row = 7
    start_col = 3  # 0-indexed, so column 4 is index 3
    end_row = start_row + subgrid_height
    end_col = start_col + subgrid_width

    output_grid = np.zeros((subgrid_height, subgrid_width), dtype=int)

    # 2. Color Reduction and 3. Column Patterning (combined for efficiency)
    for r in range(subgrid_height):
        for c in range(subgrid_width):
            original_value = input_grid[start_row + r, start_col + c]

            if (c+1) % 2 != 0: # Odd Columns
              if r == 0 or r == 1 or r==3 or r==4 or r==7 or r==8:
                output_grid[r,c] = 4
              else:
                output_grid[r,c] = 1
            else:
              output_grid[r,c] = 1


    return output_grid

input_output_pairs = [
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 4, 4, 4, 4, 4, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], [
        [4, 4, 1, 4, 4, 1, 4, 4, 1],
        [4, 4, 1, 4, 4, 1, 4, 4, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [4, 4, 1, 4, 4, 1, 4, 4, 1],
        [4, 4, 1, 4, 4, 1, 4, 4, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [4, 4, 1, 4, 4, 1, 4, 4, 1],
        [4, 4, 1, 4, 4, 1, 4, 4, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [4, 4, 1, 4, 4, 1, 4, 4, 1]
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 4, 4, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], [
        [4, 1, 1, 4, 1, 1, 1],
        [4, 1, 1, 4, 1, 4, 1],
        [4, 4, 4, 4, 1, 1, 1],
        [1, 1, 4, 1, 1, 4, 1],
        [1, 1, 4, 1, 1, 1, 4],
        [4, 4, 4, 4, 1, 4, 1],
        [1, 1, 4, 1, 1, 1, 1],
        [1, 1, 4, 1, 1, 4, 1],
        [1, 1, 4, 4, 1, 1, 1]
    ]),
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 4, 4, 1, 4, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 4, 1, 1, 1, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 4, 4, 4, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 4, 1, 1, 1, 1, 1, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 4, 4, 1, 4, 4, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], [
        [1, 1, 1, 4, 4, 1, 4, 4, 1],
        [1, 4, 1, 1, 1, 1, 1, 4, 1],
        [1, 1, 4, 4, 4, 4, 1, 1, 1],
        [1, 4, 1, 1, 1, 1, 1, 4, 1],
        [1, 1, 1, 4, 4, 1, 4, 4, 1]
    ]),
      ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 4, 4, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
     [
        [1, 1, 4, 1, 1, 4],
        [1, 1, 4, 4, 4, 4],
        [1, 1, 4, 1, 1, 4]
     ]),
          ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 4, 1, 1, 4, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 4, 1, 1, 1, 4, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 1, 4, 4, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
     [
        [1, 1, 4, 4, 1, 1, 4],
        [1, 1, 4, 1, 1, 1, 4],
        [4, 4, 4, 1, 4, 4, 4]
     ])
]

results = []
for i, (input_grid, expected_output) in enumerate(input_output_pairs):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_grid = transform(input_grid)
    comparison = compare_grids(transformed_grid, expected_output)
    results.append(
        {
            "example": i + 1,
            "comparison": comparison,
        }
    )

for result in results:
    print(f"Example {result['example']}:")
    if isinstance(result['comparison'], str):
        print(result['comparison'])
    else:
        print(f"  Shape: {result['comparison']['shape']}")
        print(f"  Number of differences: {result['comparison']['num_diffs']}")
        if result['comparison']['num_diffs'] > 0:
            print(f"  Details:")
            for detail in result['comparison']['diff_details']:
                print(detail)