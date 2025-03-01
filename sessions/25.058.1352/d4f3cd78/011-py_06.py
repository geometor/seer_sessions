import numpy as np
from skimage.measure import label, regionprops

def analyze_results(input_grid, output_grid, expected_output):
    """Analyzes the results of the transformation, providing detailed metrics."""

    # Find gray objects in the input grid
    gray_objects = label(input_grid == 5, connectivity=1)
    num_gray_objects = np.max(gray_objects)

    print(f"Number of gray objects in input: {num_gray_objects}")

    for i in range(1, num_gray_objects + 1):
        object_coords = np.argwhere(gray_objects == i)
        if len(object_coords) > 0:  # Check if the object exists
              min_row, min_col = np.min(object_coords, axis=0)
              max_row, max_col = np.max(object_coords, axis=0)
              print(f"Gray object {i}: Bounding box - TopLeft: ({min_row}, {min_col}), BottomRight: ({max_row}, {max_col})")

    # Check azure line placement (assuming it should always be present)
    center_x = output_grid.shape[1] // 2
    azure_line_present = np.any(output_grid[:, center_x] == 8)
    print(f"Azure line present at center: {azure_line_present}")

    # Analyze filled pixels
    incorrectly_filled = []
    correctly_filled = []

    diff = output_grid - expected_output
    for y in range (diff.shape[0]):
      for x in range (diff.shape[1]):
        if diff[y,x] != 0:
          incorrectly_filled.append( (y,x,output_grid[y,x], expected_output[y,x]))
    #for y in range(output_grid.shape[0]):
    #   for x in range(output_grid.shape[1]):
    #       if output_grid[y, x] == 8 and input_grid[y,x] == 5:
    #         correctly_filled.append((y,x))
    #      if output_grid[y, x] == 8 and input_grid[y, x] != 5:  # Assuming only gray should be filled
    #           if not( expected_output[y,x] == 8 ):
    #             incorrectly_filled.append((y, x))
    
    print(f"changed pixels: {incorrectly_filled}")
    #print(f"Pixels correctly filled with azure: {correctly_filled}")
    #print(f"Pixels incorrectly filled with azure: {incorrectly_filled}")

# Example Usage (replace with actual grids for each example)
input_grid_ex0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0]])
output_grid_ex0 = transform(input_grid_ex0)
expected_output_ex0 = np.array([[0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0]])

input_grid_ex1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0]])
output_grid_ex1 = transform(input_grid_ex1)
expected_output_ex1 = np.array([[0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0]])

input_grid_ex2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 5, 0],
                           [0, 0, 0, 0, 5, 0, 0, 5, 0]])
output_grid_ex2 = transform(input_grid_ex2)
expected_output_ex2 = np.array([[0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                                [0, 0, 0, 0, 8, 0, 0, 5, 0],
                                [0, 0, 0, 0, 8, 0, 0, 5, 0],
                                [0, 0, 0, 0, 8, 0, 0, 5, 0]])

input_grid_ex3 = np.array([[5, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 0, 0, 5, 0, 0, 0, 0],
                           [5, 0, 0, 0, 5, 0, 0, 0, 0],
                           [5, 0, 0, 0, 5, 0, 0, 0, 0],
                           [5, 0, 0, 0, 5, 0, 0, 0, 5]])
output_grid_ex3 = transform(input_grid_ex3)
expected_output_ex3 = np.array([[8, 0, 0, 0, 8, 0, 0, 0, 0],
                                [8, 0, 0, 0, 8, 0, 0, 0, 0],
                                [8, 0, 0, 0, 8, 0, 0, 0, 0],
                                [8, 0, 0, 0, 8, 0, 0, 0, 0],
                                [8, 0, 0, 0, 8, 0, 0, 0, 0],
                                [8, 0, 0, 0, 8, 0, 0, 0, 5]])
analyze_results(input_grid_ex0, output_grid_ex0, expected_output_ex0)
analyze_results(input_grid_ex1, output_grid_ex1, expected_output_ex1)
analyze_results(input_grid_ex2, output_grid_ex2, expected_output_ex2)
analyze_results(input_grid_ex3, output_grid_ex3, expected_output_ex3)
