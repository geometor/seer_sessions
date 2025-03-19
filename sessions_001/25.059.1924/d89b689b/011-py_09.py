import numpy as np
from skimage.measure import label, regionprops

def get_object_properties(grid):
    """
    Identifies objects in the grid and returns their properties.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its properties (color, bounding box, area).
    """

    labeled_grid = label(grid, connectivity=1)
    objects = []
    for region in regionprops(labeled_grid):
        #Bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        
        objects.append({
            'color': grid[min_row, min_col],
            'bbox': (min_row, min_col, max_row, max_col),
            'area': region.area,
            'centroid': region.centroid,
        })
    return objects

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output example."""

    input_objects = get_object_properties(input_grid)
    output_objects = get_object_properties(output_grid)

    print("Input Objects:")
    for obj in input_objects:
        print(obj)
    print("\nOutput Objects:")
    for obj in output_objects:
        print(obj)
    print("-" * 20)
    
# Example usage with the provided grids.  I've added the example grids here
# for ease of execution.  This is something I can't normally do.

example_grids = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 5, 0, 0, 0, 0, 0, 0, 0, 8, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 5, 9, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 5, 9, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),
     (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
      np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])),
      (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
       np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
]
# Assuming 'train_input_0', 'train_output_0', etc. are defined elsewhere
for i, example in enumerate(example_grids):
  print(f"Example: {i}")
  analyze_example(example[0],example[1])
