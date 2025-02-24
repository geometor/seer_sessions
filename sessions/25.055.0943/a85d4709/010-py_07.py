import numpy as np
from skimage.measure import label, regionprops

def get_object_properties(grid):
    """Identifies objects and extracts their properties."""
    labeled_grid = label(grid, connectivity=1)  # Use 4-connectivity
    objects = []
    for region in regionprops(labeled_grid):
        # skimage regionprops identifies background, so we ignore that.
        if region.label == 0: continue # added

        min_row, min_col, max_row, max_col = region.bbox
        objects.append({
            "label": region.label, # added
            "color": grid[min_row, min_col],  # All pixels in region have same color
            "bbox": (min_row, min_col, max_row, max_col),
            "size": (max_row - min_row, max_col - min_col),
            "area": region.area,
            "centroid": region.centroid,
            "is_square": region.extent == 1
        })
    return objects

def analyze_example_objects(input_grid, output_grid):
    """Analyzes input/output, focusing on object properties and changes."""
    input_objects = get_object_properties(input_grid)
    output_objects = get_object_properties(output_grid)

    # Basic analysis - can be expanded with more sophisticated logic
    print(f"Input Objects: {input_objects}")
    print(f"Output Objects: {output_objects}")
    return input_objects, output_objects
# the first example
input_grid = np.array(task["train"][0]["input"])
output_grid = np.array(task["train"][0]["output"])

analyze_example_objects(input_grid,output_grid)
