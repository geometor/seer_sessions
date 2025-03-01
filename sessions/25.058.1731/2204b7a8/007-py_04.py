import numpy as np

def analyze_results(train_pairs):
    results = []
    for i, (input_grid, output_grid) in enumerate(train_pairs):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)

        input_colors = np.unique(input_grid)
        output_colors = np.unique(output_grid)
        shape = input_grid.shape

        # Calculate pixel changes
        changed_pixels = []
        for row in range(input_grid.shape[0]):
            for col in range(input_grid.shape[1]):
                if input_grid[row, col] != output_grid[row, col]:
                    changed_pixels.append(
                        {
                            "row": row,
                            "col": col,
                            "from": int(input_grid[row, col]),
                            "to": int(output_grid[row, col]),
                        }
                    )
        # Determine the accuracy of the transform
        transform_grid = transform(input_grid) # calling the function from the prompt
        correct = np.array_equal(transform_grid, output_grid)

        results.append(
            {
                "example": i + 1,
                "shape": shape,
                "input_colors": [int(c) for c in input_colors],
                "output_colors": [int(c) for c in output_colors],
                "changed_pixels": changed_pixels,
                "correct": correct
            }
        )
    return results

# Call this with the actual train_pairs data from ARC
# Placeholder for demonstration - replace with actual task data
train_pairs = [
  ([[3, 7, 3], [3, 7, 3], [4, 1, 4]], [[1, 6, 1], [1, 6, 1], [3, 4, 3]]),
  ([[8, 8, 8, 8, 8], [8, 5, 8, 5, 8], [8, 8, 3, 8, 8], [8, 5, 8, 5, 8], [8, 8, 8, 8, 8]], [[8, 8, 8, 8, 8], [8, 5, 8, 5, 8], [8, 8, 1, 8, 8], [8, 5, 8, 5, 8], [8, 8, 8, 8, 8]]),
  ([[8, 5, 1, 1, 5, 8], [5, 1, 1, 1, 1, 5], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [5, 1, 1, 1, 1, 5], [8, 5, 1, 1, 5, 8]], [[8, 5, 4, 4, 5, 8], [5, 4, 4, 4, 4, 5], [4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4], [5, 4, 4, 4, 4, 5], [8, 5, 4, 4, 5, 8]])
]

analysis = analyze_results(train_pairs)

for item in analysis:
    print(item)