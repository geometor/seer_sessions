import numpy as np
from scipy.ndimage import label, find_objects

def analyze_example(input_grid, expected_output):
    """
    Analyzes a single example, extracting object properties and comparing input and output.
    """

    def get_object_properties(grid):
        labeled_grid, num_objects = label(grid)
        object_properties = []
        for i in range(1, num_objects + 1):  # Iterate through object labels (starting from 1)
            object_pixels = (labeled_grid == i)
            object_color = grid[object_pixels][0]  # Pick the color of the object
            coords = np.where(object_pixels)
            min_y, min_x = np.min(coords, axis=1)
            max_y, max_x = np.max(coords, axis=1)
            size = np.sum(object_pixels)
            centroid_y = (min_y + max_y) / 2
            centroid_x = (min_x + max_x) / 2

            object_properties.append({
                'color': object_color,
                'bounding_box': ((min_y, min_x), (max_y, max_x)),
                'size': size,
                'centroid': (centroid_y, centroid_x),
                'label': i
            })
        return object_properties

    input_props = get_object_properties(input_grid)
    output_props = get_object_properties(expected_output)

    print(f"Input Objects ({len(input_props)}):")
    for obj in input_props:
        print(obj)
    print(f"Output Objects ({len(output_props)}):")
    for obj in output_props:
        print(obj)
    return input_props, output_props

task_data = task.get("train")

all_input_props = []
all_output_props = []

for i, example in enumerate(task_data):
    input_grid = example.get('input')
    output_grid = example.get('output')
    print(f"Example {i+1}:")
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)
    input_props, output_props = analyze_example(input_np, output_np)
    all_input_props.append(input_props)
    all_output_props.append(output_props)
