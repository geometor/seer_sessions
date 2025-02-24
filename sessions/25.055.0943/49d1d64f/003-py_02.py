import numpy as np

# Provided training examples (replace with actual data)
train_examples = [
    {
        "input": np.array([[1, 2], [3, 4]]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 2, 2, 0],
            [0, 1, 1, 2, 2, 0],
            [0, 3, 3, 4, 4, 0],
            [0, 3, 3, 4, 4, 0],
            [0, 0, 0, 0, 0, 0],
        ]),
    },
    {
        "input": np.array([[5, 6], [7, 8]]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 5, 5, 6, 6, 0],
            [0, 5, 5, 6, 6, 0],
            [0, 7, 7, 8, 8, 0],
            [0, 7, 7, 8, 8, 0],
            [0, 0, 0, 0, 0, 0],
        ]),
    },
        {
        "input": np.array([[9, 1], [2, 3]]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 9, 9, 1, 1, 0],
            [0, 9, 9, 1, 1, 0],
            [0, 2, 2, 3, 3, 0],
            [0, 2, 2, 3, 3, 0],
            [0, 0, 0, 0, 0, 0],
        ]),
    },
]

# Test example is not relevant to this task

results = []

for i, example in enumerate(train_examples):
    input_grid = example['input']
    output_grid = example['output']
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape

    # Calculate scaling factor - take floor
    scale_height = output_height // input_height
    scale_width = output_width // input_width
    
    # simple check here - are the scales the same?
    scale_factor = 0
    if scale_height == scale_width:
        scale_factor = scale_height
        
    # look more closely at what's going on at the border
    border_width_top = 0
    border_width_left = 0
    border_color_top = -1
    border_color_left = -1
    
    # only calculate if the scale is not zero
    if scale_factor > 0:

        # Find first row with non-zero elements in output - top border
        for row in range(output_height):
            if np.any(output_grid[row, :] != 0):
                border_width_top = row
                border_color_top = output_grid[row,np.where(output_grid[row,:] !=0)[0][0]]
                break; #exit on first non-zero

        # Find first col with non-zero elements in output - left border
        for col in range(output_width):
            if np.any(output_grid[:, col] != 0):
                border_width_left = col
                border_color_left = output_grid[np.where(output_grid[:,col] !=0)[0][0], col]
                break;

    results.append({
        'example': i + 1,
        'input_height': input_height,
        'input_width': input_width,
        'output_height': output_height,
        'output_width': output_width,
        'scale_factor': scale_factor,
        'border_width_top': border_width_top,
        'border_width_left': border_width_left,
        'border_color_top': border_color_top,
        'border_color_left': border_color_left
    })

for result in results:
    print(result)