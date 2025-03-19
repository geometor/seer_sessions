import numpy as np

def analyze_examples(examples):
    analysis = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        # Find red and green objects
        red_coords_input = np.argwhere(input_grid == 2)
        green_coords_input = np.argwhere(input_grid == 3)
        red_coords_output = np.argwhere(output_grid == 2)
        green_coords_output = np.argwhere(output_grid == 3)
        
        #Determine bounding box for input red
        red_bbox_input = {}
        if len(red_coords_input) > 0:
            min_row = np.min(red_coords_input[:, 0])
            max_row = np.max(red_coords_input[:, 0])
            min_col = np.min(red_coords_input[:, 1])
            max_col = np.max(red_coords_input[:, 1])
            red_bbox_input = {
                "min_row": int(min_row), "max_row": int(max_row),
                "min_col": int(min_col), "max_col": int(max_col),
                "height": int(max_row - min_row + 1),
                "width": int(max_col - min_col + 1)
            }
        #Determine bounding box for output red
        red_bbox_output = {}
        if len(red_coords_output) > 0:
            min_row = np.min(red_coords_output[:, 0])
            max_row = np.max(red_coords_output[:, 0])
            min_col = np.min(red_coords_output[:, 1])
            max_col = np.max(red_coords_output[:, 1])
            red_bbox_output = {
                "min_row": int(min_row), "max_row": int(max_row),
                "min_col": int(min_col), "max_col": int(max_col),
                "height": int(max_row - min_row + 1),
                "width": int(max_col - min_col + 1)
            }

        analysis.append({
            'example_index': i,
            'input_grid_shape': input_grid.shape,
            'output_grid_shape': output_grid.shape,
            'red_pixels_input': red_coords_input.tolist(),
            'green_pixels_input': green_coords_input.tolist(),
            'red_pixels_output': red_coords_output.tolist(),
            'green_pixels_output': green_coords_output.tolist(),
            'red_bbox_input': red_bbox_input,
            'red_bbox_output': red_bbox_output,
        })
    return analysis
# the task and train_examples will be filled in by the prompt
task = {}
train_examples = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 2, 0, 0],
            [0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 2, 2, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 2, 0, 3, 0],
            [0, 0, 0, 0, 2, 0, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0],
            [0, 3, 2, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0],
        ],
    },
]

analysis = analyze_examples(train_examples)
for item in analysis:
    print(item)
