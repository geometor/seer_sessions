import numpy as np

def analyze_examples(examples):
    for i, (input_grid, output_grid) in enumerate(examples):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        print(f"--- Example {i+1} ---")
        print("Input Grid:\n", input_grid)
        print("Output Grid:\n", output_grid)

        rows, cols = input_grid.shape
        for row_index in range(rows):
            for col_index in range(cols):
                if input_grid[row_index, col_index] == 3: #green
                    
                    #Original and transformed value
                    original_value = input_grid[row_index, col_index]
                    transformed_value = output_grid[row_index, col_index]
                    
                    print(f"Green pixel at ({row_index}, {col_index}): Original={original_value}, Transformed={transformed_value}")

                    # Check above for red
                    if row_index > 0 and input_grid[row_index - 1, col_index] == 2:
                        print(f"  Red pixel directly above at ({row_index - 1}, {col_index})")
                    # Check below for red
                    if row_index < rows - 1 and input_grid[row_index + 1, col_index] == 2:
                        print(f"  Red pixel directly below at ({row_index + 1}, {col_index})")
                    # Check above row for any red
                    if row_index > 0:
                        if 2 in input_grid[row_index-1]:
                            print(f" Red pixel(s) exist in the row above")
                            #get all the indices
                            red_indices = np.where(input_grid[row_index-1] == 2)[0]
                            print(f"  Red pixel(s) found at column(s): {red_indices} in row above")
                    # Check below row for any red
                    if row_index < rows - 1:
                        if 2 in input_grid[row_index+1]:
                            print(f" Red pixel(s) exist in the row below")
                            #get all the indices
                            red_indices = np.where(input_grid[row_index+1] == 2)[0]
                            print(f"  Red pixel(s) found at column(s): {red_indices} in row below")

# Provided training examples (replace with actual data)
train = [
    ([
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 2, 5, 5, 5],
        [5, 5, 5, 3, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5]
    ], [
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 2, 5, 5, 5],
        [5, 5, 5, 8, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5]
    ]),
    ([
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 3, 5, 5, 5],
        [5, 5, 5, 2, 5, 5, 5]
    ], [
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 8, 5, 5, 5],
        [5, 5, 5, 2, 5, 5, 5]
    ]),
    ([
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 2, 5, 5, 5],
        [5, 5, 3, 3, 3, 5, 5],
        [5, 5, 5, 2, 5, 5, 5]
    ], [
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 2, 5, 5, 5],
        [5, 5, 8, 8, 8, 5, 5],
        [5, 5, 5, 2, 5, 5, 5]
    ]),
    ([
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 2, 3, 5, 5],
        [5, 5, 5, 3, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5]
    ], [
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 2, 3, 5, 5],
        [5, 5, 5, 3, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5]
    ]),
    ([
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5],
        [5, 2, 5, 3, 5, 2, 5],
        [5, 5, 5, 5, 5, 5, 5]
    ], [
        [5, 5, 5, 5, 5, 5, 5],
        [5, 5, 5, 5, 5, 5, 5],
        [5, 2, 5, 8, 5, 2, 5],
        [5, 5, 5, 5, 5, 5, 5]
    ]),
]

analyze_examples(train)