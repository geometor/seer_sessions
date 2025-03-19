import numpy as np

def get_bounding_box(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return (min_row, min_col), (max_row, max_col)

def analyze_example(input_grid, output_grid, color=2):
    bbox = get_bounding_box(input_grid, color)
    input_shape_size = input_grid.shape
    output_shape_size = output_grid.shape

    if bbox:
      (min_row, min_col), (max_row, max_col) = bbox
      bbox_height = max_row - min_row + 1
      bbox_width = max_col - min_col + 1
    else:
       bbox_height = 0
       bbox_width = 0
    
    print(f"  Input shape: {input_shape_size}")
    print(f"  Output shape: {output_shape_size}")
    print(f"  Red BBox Height: {bbox_height}, Width: {bbox_width}")
    

examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 3, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 0, 0],
              [0, 0, 0, 2, 2, 0, 0],
              [0, 0, 0, 2, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]])),
  
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 3, 2, 2, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 3, 2, 2, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 3, 2, 2, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0],
             [0, 2, 2, 2, 0],
             [0, 2, 2, 2, 0],
             [0, 2, 2, 2, 0],
             [0, 0, 0, 0, 0]])),

    (np.array([[3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3],
              [3, 3, 3, 3, 3, 3, 3, 3]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]))
]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
    print("-" * 20)