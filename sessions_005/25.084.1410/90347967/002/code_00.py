import numpy as np
from scipy.ndimage import label

def analyze_grid_edges(grid_list):
    grid = np.array(grid_list)
    height, width = grid.shape
    
    if np.count_nonzero(grid) == 0:
        return {"num_edges_touched": 0, "num_objects": 0} # Handle empty grid case
        
    # Find coordinates of non-white pixels
    non_white_coords = np.argwhere(grid > 0)
    r_min = non_white_coords[:, 0].min()
    r_max = non_white_coords[:, 0].max()
    c_min = non_white_coords[:, 1].min()
    c_max = non_white_coords[:, 1].max()
    
    touches_top = (r_min == 0)
    touches_bottom = (r_max == height - 1)
    touches_left = (c_min == 0)
    touches_right = (c_max == width - 1)
    
    num_edges_touched = sum([touches_top, touches_bottom, touches_left, touches_right])
    
    # Define connectivity (8-connectivity)
    structure = np.array([[1,1,1],
                          [1,1,1],
                          [1,1,1]])
    # Label connected components (non-zero pixels)
    labeled_array, num_features = label(grid > 0, structure=structure)

    return {
        "height": height,
        "width": width,
        "num_objects": num_features,
        "num_edges_touched": num_edges_touched
    }

# Example Inputs (as lists of lists)
ex1_in = [[6, 0, 0], [2, 5, 0], [2, 1, 0]]
ex2_in = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 2, 5, 0, 0, 0, 0], [0, 0, 3, 3, 0, 0, 0, 0, 0], [0, 1, 4, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
ex3_in = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 5, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

results = {
    "example1": analyze_grid_edges(ex1_in),
    "example2": analyze_grid_edges(ex2_in),
    "example3": analyze_grid_edges(ex3_in),
}

print(results)
# Output from tool execution:
# {'example1': {'height': 3, 'width': 3, 'num_objects': 1, 'num_edges_touched': np.int64(3)}, 
#  'example2': {'height': 7, 'width': 9, 'num_objects': 1, 'num_edges_touched': np.int64(0)}, 
#  'example3': {'height': 9, 'width': 9, 'num_objects': 1, 'num_edges_touched': np.int64(1)}}
