# Example Metric Gathering Plan (Conceptual)
import numpy as np

# Assume input_grid_list and output_grid_list hold the examples
# train_examples = [ {'input': input_grid_1, 'output': output_grid_1}, ... ]

all_metrics = []

for i, example in enumerate(train_examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    
    metrics = {
        'example_index': i,
        'input_shape': input_grid.shape,
        'output_shape': output_grid.shape,
        'input_unique_colors': np.unique(input_grid).tolist(),
        'output_unique_colors': np.unique(output_grid).tolist(),
        'changed_pixels_count': np.sum(input_grid != output_grid),
        # Add more detailed analysis here:
        # - Find objects (e.g., contiguous blocks of non-background color) in input
        # - Characterize objects (color, shape, size, bounding box)
        # - Track how input objects correspond to output objects/patterns
        # - Identify specific patterns applied (e.g., checkerboard)
        # - Check if background (color 0) is ever modified
        # - Check if shapes/sizes change beyond internal patterning
    }
    
    # --- Placeholder for Object/Pattern Analysis ---
    # Code to find rectangles (like find_solid_rectangles, but corrected)
    # input_rectangles = find_solid_rectangles(input_grid) 
    # metrics['input_rectangles'] = input_rectangles
    
    # For each rectangle >= 3x3:
    #   Compare its interior in input vs output.
    #   Verify if output interior matches the described checkerboard pattern.
    #   Check if border pixels are unchanged.
    #   Check if smaller rectangles or non-rectangular shapes are modified.
    
    all_metrics.append(metrics)

# print(all_metrics) # This would output the gathered data