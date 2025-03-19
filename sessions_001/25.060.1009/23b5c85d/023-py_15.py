# Conceptual code_execution - this won't actually run
import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_dims = input_grid.shape
    output_dims = output_grid.shape

    input_orange_count = np.sum(input_grid == 7)
    output_orange_count = np.sum(output_grid == 7)
    orange_bbox = find_object_by_color(input_grid, 7)
    is_orange_rectangle = False
    if orange_bbox is not None:
      extracted = input_grid[orange_bbox[0][0]:orange_bbox[1][0]+1, orange_bbox[0][1]:orange_bbox[1][1]+1]
      is_orange_rectangle = np.array_equal(extracted, output_grid)
    else:
      is_orange_rectangle = False

    return {
        "input_dims": input_dims,
        "output_dims": output_dims,
        "input_orange_count": input_orange_count,
        "output_orange_count": output_orange_count,
        "orange_bbox": orange_bbox,
        "is_orange_rectangle": is_orange_rectangle
    }

#Assume this data is the result of running analyze_example on each pair
example_data = [
    {
        "input_dims": (7, 11),
        "output_dims": (3, 5),
        "input_orange_count": 15,
        "output_orange_count": 15,
        "orange_bbox": ((2, 3), (4, 7)),
        "is_orange_rectangle": True
    },
     {
        "input_dims": (13, 16),
        "output_dims": (3, 3),
        "input_orange_count": 9,
        "output_orange_count": 9,
        "orange_bbox": ((2, 2), (4, 4)),
        "is_orange_rectangle": True
    },
    {
        "input_dims": (7, 10),
        "output_dims": (3, 6),
        "input_orange_count": 18,
        "output_orange_count": 18,
         "orange_bbox": ((2, 3), (4, 8)),
        "is_orange_rectangle": True
    },
    {
        "input_dims": (14, 14),
        "output_dims": (0, 0),
        "input_orange_count": 0,
        "output_orange_count": 0,
        "orange_bbox": None,
        "is_orange_rectangle": False
    }
]
for i,data in enumerate(example_data):
    print (f'Example {i}:')
    print (data)
