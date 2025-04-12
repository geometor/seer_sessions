import numpy as np

def get_metrics(input_grid_list, expected_output_list):
    input_grid = np.array(input_grid_list)
    expected_output_grid = np.array(expected_output_list)
    
    in_h, in_w = input_grid.shape if input_grid.ndim == 2 else (0, 0)
    out_h, out_w = expected_output_grid.shape if expected_output_grid.ndim == 2 else (0, 0)
    
    if in_h == 0 or in_w == 0:
        non_empty_cols_in = []
    else:
        non_empty_cols_in = [c for c in range(in_w) if not np.all(input_grid[:, c] == 0)]
        
    num_non_empty_in = len(non_empty_cols_in)
    
    metrics = {
        "input_height": in_h,
        "input_width": in_w,
        "output_height": out_h,
        "output_width": out_w,
        "height_match": in_h == out_h,
        "non_empty_cols_count": num_non_empty_in,
        "output_width_match": num_non_empty_in == out_w,
        "original_non_empty_indices": non_empty_cols_in,
    }
    return metrics

# Example 1
input1 = [[0,0,0,0,0,0,8,0,0,0,0],[2,2,2,0,8,8,8,0,0,0,0],[0,0,2,0,0,0,0,0,6,6,6]]
output1 = [[0,0,0,0,0,0,0,0,0],[2,2,2,0,0,8,6,6,6],[0,0,2,8,8,8,0,0,0]]
# Example 2
input2 = [[0,0,0,3,3,0,0,1,0,2,2],[2,2,0,0,0,0,1,1,0,0,2],[0,2,0,0,0,0,0,0,0,0,0]]
output2 = [[0,0,0,0,0,0,0,0],[2,2,0,0,0,1,2,2],[0,2,3,3,1,1,0,2]]
# Example 3
input3 = [[0,1,1,0,0,0,0,0,2,2,0],[1,1,0,0,2,2,0,2,2,0,0],[0,0,0,0,0,2,0,0,0,0,0]]
output3 = [[0,1,1,2,2,0,2,2],[1,1,0,0,2,2,2,0],[0,0,0,0,0,0,0,0]]
# Example 4
input4 = [[0,2,0,0,0,0,0,0,0],[2,2,0,1,1,0,2,2,2],[0,0,0,0,1,0,0,0,0]]
output4 = [[0,2,1,1,0,0,0],[2,2,0,1,2,2,2],[0,0,0,0,0,0,0]]
