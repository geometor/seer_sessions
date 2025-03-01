import numpy as np

def get_contiguous_regions(grid):
    """Identifies contiguous horizontal regions of the same color."""
    regions = []
    for row in grid:
        current_region = []
        for cell in row:
            if not current_region or cell == current_region[-1]:
                current_region.append(cell)
            else:
                regions.append(current_region[0])  # Add the dominant color
                current_region = [cell]
        if current_region:
            regions.append(current_region[0])
    return regions

def transform(input_grid):
    # Identify contiguous horizontal regions.
    regions = get_contiguous_regions(np.array(input_grid))

    # Determine the number of unique regions
    unique_regions = []
    for region in regions:
        if region not in unique_regions:
            unique_regions.append(region)

    # Create the output grid (1 x N).
    output_grid = np.zeros((1, len(unique_regions)), dtype=int)

    # Populate the output grid with the dominant colors.
    for i, color in enumerate(unique_regions):
        output_grid[0, i] = color

    return output_grid


task = {
  "train": [
    {
      "input": [
        [6, 6, 2, 2, 2, 6, 6, 6, 8],
        [6, 6, 2, 2, 2, 6, 6, 6, 8],
        [6, 6, 2, 2, 2, 6, 6, 6, 8],
        [8, 6, 6, 6, 6, 6, 8, 8, 8]
      ],
      "output": [[6, 2, 6, 8, 6, 8]]
    },
    {
      "input": [
        [7, 7, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7, 7],
        [7, 7, 7, 7, 7, 7, 7, 7, 7]
      ],
      "output": [[7, 7]]
    },
    {
      "input": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [[1, 1, 0, 0]]
    },
      {
      "input": [[3, 3, 3, 3, 3, 3, 3, 3, 3]],
      "output": [[3]]
    },
    {
      "input": [[4, 4, 4, 5, 5, 5, 5, 5, 5]],
      "output": [[4, 5]]
    }
  ],
  "test": [
    {
      "input": [
        [8, 8, 8, 8, 8, 3, 3, 8, 8],
        [8, 8, 8, 8, 8, 3, 3, 8, 8],
        [8, 8, 8, 8, 8, 3, 3, 8, 8]
      ],
      "output": [[8, 3, 8]]
    }
  ]
}

def assess_examples(task):
    for example_index, example in enumerate(task['train']):
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid)

        # Convert to strings for easy comparison
        predicted_output_str = str(predicted_output.flatten())
        expected_output_str = str(np.array(expected_output).flatten())
        
        print(f"Example {example_index + 1}:")
        print(f"  Input: {input_grid}")
        print(f"  Expected Output: {expected_output_str}")
        print(f"  Predicted Output: {predicted_output_str}")
        print(f"  Correct: {predicted_output_str == expected_output_str}")
        print("-" * 20)
assess_examples(task)
