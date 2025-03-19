import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    correct = np.array_equal(output_grid, predicted_grid)
    input_bottom_right = input_grid[-2:, -2:]
    output_bottom_right = output_grid[-2:, -2:]
    predicted_bottom_right = predicted_grid[-2:,-2:]
    diff_input_output = np.array_equal(input_bottom_right,output_bottom_right)
    diff_output_predicted = np.array_equal(output_bottom_right, predicted_bottom_right)

    return {
        'correct': correct,
        'input_bottom_right': input_bottom_right.tolist(),
        'output_bottom_right': output_bottom_right.tolist(),
        'predicted_bottom_right': predicted_bottom_right.tolist(),
        'diff_input_output' : diff_input_output,
        'diff_output_predicted': diff_output_predicted
    }

# Example Usage (replace with your actual grids) - dummy grids for example
input_grids = [
  np.array([[1, 1, 1], [1, 1, 1], [1, 8, 1]]),
  np.array([[5, 5], [5, 5]]),
  np.array([[9, 9, 9, 9], [9, 9, 9, 9], [9, 9, 9, 9], [9, 7, 9, 9]]),
  np.array([[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 2]]),
  np.array([[0, 0, 0, 0, 8], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [5, 0, 0, 0, 0]]),
]
output_grids = [
  np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 8]]),
  np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 5, 5], [0, 0, 5, 5]]),
  np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 9, 9], [0, 0, 9, 7]]),
  np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 4, 4], [0, 0, 4, 2]]),
  np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 5, 0]]),
]

#use previous transform to generate
def transform(input_grid):
    # Initialize output grid as all zeros with size 4x4
    output_grid = np.zeros((4, 4), dtype=int)

    # Set the bottom-right 2x2 block to green
    output_grid[2:4, 2:4] = 3
   
    return output_grid
predicted_grids = [transform(input_grid) for input_grid in input_grids]

results = [analyze_example(inp, out, pred) for inp, out, pred in zip(input_grids, output_grids, predicted_grids)]

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Correct: {res['correct']}")
    print(f"  Input Bottom-Right 2x2:\n{np.array(res['input_bottom_right'])}")
    print(f"  Output Bottom-Right 2x2:\n{np.array(res['output_bottom_right'])}")
    print(f"  Predicted Bottom-Right 2x2:\n{np.array(res['predicted_bottom_right'])}")
    print(f"  Input == Output Bottom-Right 2x2: {res['diff_input_output']}")
    print(f"  Output == Predicted Bottom-Right 2x2: {res['diff_output_predicted']}")
    print("-" * 20)