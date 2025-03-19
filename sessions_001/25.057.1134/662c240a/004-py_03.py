import numpy as np

def analyze_example_v2(input_grid, output_grid):
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)

    # Find non-zero pixels
    non_zero_indices = np.argwhere(input_array != 0)

    if non_zero_indices.size == 0:  # Handle cases with no non-zero pixels
        bounding_box_dims = (0, 0)
        extracted_block = np.array([])

    else:
      # Find min and max row/col to define the bounding box
      min_row, min_col = np.min(non_zero_indices, axis=0)
      max_row, max_col = np.max(non_zero_indices, axis=0)

      # Extract the block
      extracted_block = input_array[min_row:max_row+1, min_col:max_col+1]
      bounding_box_dims = extracted_block.shape

    output_dims = output_array.shape
    match = np.array_equal(extracted_block, output_array)


    print(f"Input: {input_array.shape}")
    print(input_array)
    print(f"Output: {output_array.shape}")
    print(output_array)
    print(f"Extracted Block dims: {bounding_box_dims}")
    print(extracted_block)
    print(f"output matches extracted block: {match}")
    print("---")


examples = [
    ([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1]], [[0, 0, 1], [0, 1, 1]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 7, 7], [0, 0, 0, 0, 0, 7, 7, 7]], [[0, 0, 0, 7], [0, 0, 7, 7], [0, 7, 7, 7]]),
    ([[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 4, 4, 0]], [[0, 0, 4], [0, 4, 4]]),
    ([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0], [0, 0, 5, 5, 0, 0]], [[0, 5], [5, 5]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 6, 6, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0]], [[0, 0, 6], [0, 6, 6], [6, 6, 6]])
]

for input_grid, output_grid in examples:
    analyze_example_v2(input_grid, output_grid)
