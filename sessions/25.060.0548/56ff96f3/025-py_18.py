import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = transform(input_grid.copy()) # Use a copy to avoid modifying the original

    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(output_grid)
    print("Predicted Output Grid:")
    print(predicted_output)


    orange_pixels = find_orange_pixels(input_grid)
    print("Orange Pixels (Input):", orange_pixels)

    min_row, min_col, max_row, max_col = create_bounding_rectangle(orange_pixels)
    print("Bounding Box (min_row, min_col, max_row, max_col):", min_row, min_col, max_row, max_col)
    
    correct = np.array_equal(predicted_output, output_grid)
    print("Correct:", correct)
    print("-" * 20)
    return correct

# Example Data (replace with your actual task data)
examples = [
  ( [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 7, 7, 7, 0, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]],
   [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 7, 7, 7, 0, 0, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]]),

  ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),

([[0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 7, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]],
   [[0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 7, 7, 0, 0, 0],
    [0, 0, 0, 7, 7, 0, 0, 0],
    [0, 0, 0, 7, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]])
]

results = [analyze_example(input_grid, output_grid) for input_grid, output_grid in examples]
num_correct = sum(results)
print(f"Total Correct: {num_correct} / {len(examples)}")
