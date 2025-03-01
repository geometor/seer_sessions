import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a report."""
    if grid1.shape != grid2.shape:
        return {
            "shapes_match": False,
            "grid1_shape": grid1.shape,
            "grid2_shape": grid2.shape,
            "differences": [],
            "percentage_match":0
        }
    else:
        differences = []
        height, width = grid1.shape
        total_pixels = height * width
        mismatched_pixels = 0

        for y in range(height):
            for x in range(width):
                if grid1[y, x] != grid2[y, x]:
                    differences.append(((x, y), grid1[y, x], grid2[y, x]))
                    mismatched_pixels +=1
        percentage_match = ((total_pixels - mismatched_pixels) / total_pixels)*100

        return {
            "shapes_match": True,
            "grid1_shape": grid1.shape,
            "grid2_shape": grid2.shape,
            "differences": differences,
            "percentage_match": percentage_match
        }

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = 2 * input_height + 1
    output_width = 2 * input_width + 1

    # Initialize output_grid as calculated dimensions filled with 0s
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the input grid in the top-left corner
    output_grid[:input_height, :input_width] = input_grid

    # Place the mirrored input grid in the top-right corner
    output_grid[:input_height, input_width + 1:] = input_grid

    # Place the mirrored input grid in the bottom-left corner
    output_grid[input_height + 1:, :input_width] = input_grid
    
    # Place the mirrored input grid in the bottom-right corner
    output_grid[input_height + 1:, input_width + 1:] = input_grid
    

    return output_grid

# Example Data (replace with actual data from the task)

example_data = [
    (np.array([[6, 1, 1],
               [6, 1, 1]]),
     np.array([[6, 1, 1, 0, 6, 1, 1],
               [6, 1, 1, 0, 6, 1, 1],
               [0, 0, 0, 0, 0, 0, 0],
               [6, 1, 1, 0, 6, 1, 1],
               [6, 1, 1, 0, 6, 1, 1]])),
    (np.array([[2, 2, 2, 2, 8],
               [2, 2, 2, 8, 8],
               [2, 2, 8, 8, 8],
               [2, 8, 8, 8, 8]]),
     np.array([[2, 2, 2, 2, 8, 0, 2, 2, 2, 2, 8],
               [2, 2, 2, 8, 8, 0, 2, 2, 2, 8, 8],
               [2, 2, 8, 8, 8, 0, 2, 2, 8, 8, 8],
               [2, 8, 8, 8, 8, 0, 2, 8, 8, 8, 8],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 2, 8, 0, 2, 2, 2, 2, 8],
               [2, 2, 2, 8, 8, 0, 2, 2, 2, 8, 8],
               [2, 2, 8, 8, 8, 0, 2, 2, 8, 8, 8],
               [2, 8, 8, 8, 8, 0, 2, 8, 8, 8, 8]])),
    (np.array([[5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5]]),
     np.array([[5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5]]))
]

results = []
for i, (input_grid, expected_output) in enumerate(example_data):
    transformed_grid = transform(input_grid)
    comparison = compare_grids(transformed_grid, expected_output)
    results.append({
        "example": i + 1,
        "comparison": comparison
    })

for result in results:
    print(f"Example {result['example']}:")
    print(f"  Shapes Match: {result['comparison']['shapes_match']}")
    if not result['comparison']['shapes_match']:
        print(f"  Grid 1 Shape: {result['comparison']['grid1_shape']}")
        print(f"  Grid 2 Shape: {result['comparison']['grid2_shape']}")
    else:
        print(f"  Percentage Match: {result['comparison']['percentage_match']:.2f}%")
    if result['comparison']['differences']:
         print(f" Total Differences: {len(result['comparison']['differences'])}")
    print("-" * 20)