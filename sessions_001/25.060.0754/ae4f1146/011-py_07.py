import numpy as np

def analyze_example(input_grid, expected_output_grid):
    """Analyzes an example and provides metrics."""
    input_array = np.array(input_grid)
    expected_output_array = np.array(expected_output_grid)

    # Check for size correctness
    if input_array.shape != (9, 9):
        print("Input is not 9 x 9, but", input_array.shape )
        input_size_ok = False
    else:
        input_size_ok = True

    if expected_output_array.shape != (3, 3):
      print("Output is not 3 x 3, but", expected_output_array.shape )
      output_size_ok = False
    else:
      output_size_ok = True

    # Find unique colors in input and output, excluding 0 (background)
    input_colors = np.unique(input_array[input_array != 0])
    output_colors = np.unique(expected_output_array[expected_output_array != 0])

    return {
        "input_size_correct": input_size_ok,
        "output_size_correct": output_size_ok,
        "input_colors": input_colors.tolist(),
        "output_colors": output_colors.tolist(),
    }

def analyze_results(examples, transform_function):
  results = []
  for i, example in enumerate(examples):
        input_grid = example["input"]
        expected_output = example["output"]
        actual_output = transform_function(input_grid)
        analysis = analyze_example(input_grid, expected_output)
        analysis["correct"] = actual_output == expected_output
        results.append(analysis)
  return results

#the examples and transform function are available, so now call the code

examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 1, 0], [0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 8, 0], [0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0], [0, 2, 0], [0, 0, 0]]},
    {'input': [[1, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[1, 0, 8], [0, 2, 0], [0, 0, 0]]}
    ]

from previous_code import transform # Access the global scope

results = analyze_results(examples, transform)
for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Size Correct: {res['input_size_correct']}")
    print(f"  Output Size Correct: {res['output_size_correct']}")
    print(f"  Input Colors (excluding background): {res['input_colors']}")
    print(f"  Output Colors (excluding background): {res['output_colors']}")
    print(f"  Transformation Correct: {res['correct']}")