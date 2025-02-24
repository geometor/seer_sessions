import numpy as np

def analyze_examples(examples):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)

        # Find input non-zero pixels
        input_non_zero = np.argwhere(input_grid != 0)
        # Find output non-zero pixels
        output_non_zero = np.argwhere(expected_output != 0)
        # Find the color
        input_colors = [input_grid[x,y] for x,y in input_non_zero]
        output_colors = [expected_output[x,y] for x,y in output_non_zero]

        results.append({
            "example": i + 1,
            "input_non_zero": input_non_zero.tolist(),
            "output_non_zero": output_non_zero.tolist(),
            "input_colors": input_colors,
            "output_colors": output_colors
        })
    return results

examples = [
    ([[0, 0, 0, 0, 0],
      [0, 2, 0, 0, 0],
      [0, 0, 0, 0, 0]],
     [[3, 0, 6, 0, 0],
      [0, 0, 0, 0, 0],
      [8, 0, 7, 0, 0]]),

    ([[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 2]],
     [[0, 0, 0, 0, 0],
      [0, 0, 0, 3, 0],
      [0, 0, 0, 0, 0]]),

    ([[0, 0, 2, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 8, 0, 7, 0],
      [0, 0, 0, 0, 0]]),

    ([[0, 0, 0, 0, 0],
      [0, 0, 0, 2, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 3, 0, 6],
      [0, 0, 0, 0, 0],
      [0, 0, 8, 0, 7]])
]

analysis = analyze_examples(examples)

for result in analysis:
    print(f"Example {result['example']}:")
    print(f"  Input Non-zero Pixels: {result['input_non_zero']}, Colors: {result['input_colors']}")
    print(f"  Output Non-zero Pixels: {result['output_non_zero']}, Colors: {result['output_colors']}")
    print("-" * 40)