import numpy as np

train_pairs = [
    {
        "input": np.array([[9, 4, 2], [9, 9, 2], [4, 9, 4]]),
        "output": np.array([[8, 3, 6], [8, 8, 6], [3, 8, 3]]),
    },
    {
        "input": np.array([[2, 9, 9], [4, 9, 2], [9, 4, 2]]),
        "output": np.array([[6, 8, 8], [3, 8, 6], [8, 3, 6]]),
    },
    {
        "input": np.array([[4, 9, 4], [4, 2, 9], [9, 4, 2]]),
        "output": np.array([[3, 8, 3], [3, 6, 8], [8, 3, 6]]),
    },
    {
        "input": np.array([[4, 4, 9], [9, 2, 4], [2, 9, 4]]),
        "output": np.array([[3, 3, 8], [8, 6, 3], [6, 8, 3]]),
    },
]

def extract_color_mapping(train_pairs):
    """Extracts the color mapping from input-output pairs."""
    color_mapping = {}
    for pair in train_pairs:
        input_grid = pair["input"]
        output_grid = pair["output"]
        for i in range(input_grid.shape[0]):
            for j in range(input_grid.shape[1]):
                input_color = input_grid[i, j]
                output_color = output_grid[i, j]
                if input_color not in color_mapping:
                    color_mapping[input_color] = output_color
                elif color_mapping[input_color] != output_color:
                    print(
                        f"Warning: Inconsistent mapping for color {input_color}. "
                        f"Existing: {color_mapping[input_color]}, New: {output_color}"
                    )
    return color_mapping

color_map = extract_color_mapping(train_pairs)

print(color_map)

def verify_color_mapping_complete(train_pairs, color_map):
   
    all_input_colors = set()
    for pair in train_pairs:
      all_input_colors.update(pair['input'].flatten())
    
    print(f"unique input colors: {all_input_colors}")
    
    missing_keys = all_input_colors - color_map.keys()
    print(f"missing keys: {missing_keys}")    
    
    
verify_color_mapping_complete(train_pairs, color_map)