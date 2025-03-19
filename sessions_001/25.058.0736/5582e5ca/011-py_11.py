import numpy as np

def analyze_examples(examples):
    color_mapping = {}
    for example in examples:
        input_grid = example['input']
        output_grid = example['output']
        
        # Check if input is a single color
        unique_input_colors = np.unique(input_grid)
        if len(unique_input_colors) == 1:
            input_color = unique_input_colors[0]
            
            #check if the output is a single color
            unique_output_colors = np.unique(output_grid)
            if len(unique_output_colors) == 1:
                output_color = unique_output_colors[0]
                color_mapping[input_color] = output_color
            else:
                print(f"Output grid is not single color {output_grid}")
        else:
            print(f"Input grid is not single color: {input_grid}")
    return color_mapping

examples = [
    {'input': np.array([[1, 1], [1, 1]]), 'output': np.array([[9, 9], [9, 9]])},
    {'input': np.array([[5, 5], [5, 5]]), 'output': np.array([[0, 0], [0, 0]])},
    {'input': np.array([[3, 3], [3, 3]]), 'output': np.array([[4, 4], [4, 4]])},
]

color_map = analyze_examples(examples)
print(color_map)