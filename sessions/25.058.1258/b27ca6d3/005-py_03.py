import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    red_pixels = []
    horizontal_sequences = []
    vertical_sequences = []
    expected_green_pixels = []
    actual_green_pixels = []
    discrepancies = []

    # Find red pixels and sequences
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 2:
                red_pixels.append((r, c))
                # Check horizontal
                if c > 0 and c < input_grid.shape[1] - 1:
                    if input_grid[r, c - 1] == 0 and input_grid[r, c + 1] == 0:
                        horizontal_sequences.append((r, c - 1, r, c + 1))
                # Check vertical
                if r > 0 and r < input_grid.shape[0] - 1:
                    if input_grid[r - 1, c] == 0 and input_grid[r + 1, c] == 0:
                        vertical_sequences.append((r - 1, c, r + 1, c))

    # Find expected and actual green pixels
    for r in range(expected_output.shape[0]):
        for c in range(expected_output.shape[1]):
            if expected_output[r, c] == 3 and input_grid[r,c] == 0:
                expected_green_pixels.append((r, c))
            if actual_output[r,c] == 3 and input_grid[r,c] == 0:
                actual_green_pixels.append((r,c))
    #find discrepancies
    discrepancies = list(set(expected_green_pixels) - set(actual_green_pixels)) + list(set(actual_green_pixels) - set(expected_green_pixels))

    return {
        "red_pixels": red_pixels,
        "horizontal_sequences": horizontal_sequences,
        "vertical_sequences": vertical_sequences,
        "expected_green_pixels": expected_green_pixels,
        "actual_green_pixels": actual_green_pixels,
        "discrepancies": discrepancies
    }

#example data (replace with your actual data)
task_examples = [
    {
        "input": [[5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 2, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 2, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5]],
        "output": [[5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 2, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 2, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5]],
    },
   {
        "input": [[0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 2, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 2, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 2]],
        "output": [[0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 2, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 3, 5, 0, 5, 2, 5, 0, 5, 3], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 3, 5, 0, 5, 0, 5, 0, 5, 2]],
    },
{
        "input": [[5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 2, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 2, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5]],
        "output": [[5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 3, 5, 0, 5, 2, 5, 3, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 2, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5]],
    },
{
        "input": [[0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 2, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 2, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0]],
        "output": [[0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 3, 5, 0, 5, 2, 5, 3, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 2, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0], [0, 5, 0, 5, 0, 5, 0, 5, 0, 5], [5, 0, 5, 0, 5, 0, 5, 0, 5, 0]],
    },
]

previous_outputs = [transform(np.array(ex["input"])) for ex in task_examples]

results = []
for i, ex in enumerate(task_examples):
    analysis = analyze_example(ex["input"], ex["output"], previous_outputs[i].tolist())
    results.append(analysis)
    print(f"Example {i+1}:")
    print(f"  Red Pixels: {analysis['red_pixels']}")
    print(f"  Horizontal Sequences: {analysis['horizontal_sequences']}")
    print(f"  Vertical Sequences: {analysis['vertical_sequences']}")
    print(f"  Expected Green Pixels: {analysis['expected_green_pixels']}")
    print(f"  Actual Green Pixels: {analysis['actual_green_pixels']}")
    print(f"Discrepancies: {analysis['discrepancies']}")
