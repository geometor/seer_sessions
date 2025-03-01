import numpy as np

def analyze_examples(examples):
    analysis = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        output_grid = example["output"]

        red_pixels_input = np.where(input_grid == 2)
        red_pixels_input = list(zip(red_pixels_input[0], red_pixels_input[1]))
        
        yellow_pixels_output = np.where(output_grid == 4)
        yellow_pixels_output = list(zip(yellow_pixels_output[0], yellow_pixels_output[1]))
        
        red_pixels_by_row_input = {}
        for r, c in red_pixels_input:
            if r not in red_pixels_by_row_input:
                red_pixels_by_row_input[r] = []
            red_pixels_by_row_input[r].append(c)
        
        #sort by columns
        for row in red_pixels_by_row_input:
            red_pixels_by_row_input[row].sort()

        analysis.append({
            "example_index": i,
            "input_grid_shape": input_grid.shape,
            "output_grid_shape": output_grid.shape,
            "red_pixels_input": red_pixels_input,
            "yellow_pixels_output": yellow_pixels_output,
            "red_pixels_by_row_input":red_pixels_by_row_input,
        })

    return analysis

examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 0, 0, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 0, 0, 0, 4, 0],
                            [0, 0, 0, 0, 0, 4, 0]]),
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 0, 0, 2, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 0, 0, 4, 0, 4, 0],
                            [0, 0, 0, 0, 4, 0, 4, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 0, 0, 2, 0, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 0, 0, 4, 0, 0, 4, 0],
                            [0, 0, 0, 0, 4, 0, 0, 4, 0]]),
    },
        {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 0, 2, 0, 0, 0, 2, 0, 2],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 0, 4, 0, 0, 0, 4, 0, 2],
                            [0, 0, 0, 4, 0, 0, 0, 4, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    },
]
analysis = analyze_examples(examples)
print(analysis)