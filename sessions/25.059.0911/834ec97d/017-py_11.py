import numpy as np

def code_execution(input_grid, output_grid, predicted_output):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output = np.array(predicted_output)
    
    input_width = input_grid.shape[1]
    input_height = input_grid.shape[0]
    output_width = output_grid.shape[1]
    output_height = output_grid.shape[0]
    
    
    def find_pixel_location(grid, color_value):
      for r_idx, row in enumerate(grid):
          for c_idx, pixel in enumerate(row):
              if pixel == color_value:
                  return (c_idx, r_idx)  # (col, row)
      return None

    maroon_input_loc = find_pixel_location(input_grid, 9)
    maroon_output_loc = find_pixel_location(output_grid, 9)
    
    is_correct = np.array_equal(output_grid, predicted_output)

    print(f"  Input Dimensions: {input_width}x{input_height}")
    print(f"  Output Dimensions: {output_width}x{output_height}")
    print(f"  Maroon Pixel Input Location: {maroon_input_loc}")
    print(f"  Maroon Pixel Output Location: {maroon_output_loc}")
    print(f"  Correct Prediction: {is_correct}")

# Example Usage (replace with actual data from each example)
examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9]],
        "output": [[4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 4, 0, 4, 0, 4, 0, 4, 0], [4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 4, 0, 4, 0, 4, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9]],
        "predicted": [[4, 0, 4, 0, 4, 0, 4, 0, 4], [4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9]],
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9]],
      "output": [[4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 4, 0, 4, 0, 4, 0, 4, 0], [4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 9]],
      "predicted": [[4, 0, 4, 0, 4, 0, 4, 0, 4], [4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9]]

    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9]],
        "output": [[4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 9]],
        "predicted": [[4, 0, 4, 0, 4, 0, 4, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 9]]
    }
]

for i, example in enumerate(examples):
  print(f"Example {i+1}:")
  code_execution(example["input"], example["output"], example["predicted"])
  print("-" * 20)