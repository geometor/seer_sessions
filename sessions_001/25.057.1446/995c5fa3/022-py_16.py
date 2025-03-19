# Conceptual Code - This would be implemented in the coder phase
import numpy as np

def analyze_results(results):
    analysis = []
    for input_grid, expected_output, result, actual_output in results:
        input_shape = input_grid.shape
        output_shape = expected_output.shape
        
        # Find the center of the non-zero region.
        non_zero_indices = np.argwhere(input_grid != 5)
        if non_zero_indices.size > 0:
            center_row = np.mean(non_zero_indices[:, 0])
            center_col = np.mean(non_zero_indices[:, 1])
        else:
          center_row = -1
          center_col = -1
        
        
        # Determine the 3x3 subgrid around center.
        h, w = input_grid.shape
        
        center_r = -1
        center_c = -1
        
        for r in range(h):
          for c in range(w):
            if input_grid[r,c] != 5:
              center_r = r
              center_c = c
              break
          if center_r != -1:
            break;
        
        subgrid = []
        if center_r > -1:
          start_row = max(0, center_r -1)
          end_row = min(h, center_r + 2)
          start_col = max(0, center_c - 1)
          end_col = min(w, center_c + 2)
          subgrid = input_grid[start_row:end_row, start_col:end_col]
        
        analysis.append({
            "input_shape": input_shape,
            "output_shape": output_shape,
            "match": result,
            "center_row": center_row,
            "center_col": center_col,
            "subgrid": subgrid,
            "output_colors": np.unique(expected_output).tolist(),
            "input_colors" : np.unique(input_grid).tolist()
        })
    return analysis

# Assume 'results' is the list from the provided code's output.
analysis = analyze_results(results)

for item in analysis:
    print(item)