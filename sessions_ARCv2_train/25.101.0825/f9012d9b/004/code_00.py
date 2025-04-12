import numpy as np
from typing import List, Tuple, Optional, Dict

def grid_to_tuple(grid: np.ndarray) -> tuple:
    """Converts a numpy array (grid) to a hashable tuple of tuples."""
    if not isinstance(grid, np.ndarray): return tuple()
    if grid.ndim == 1: grid = grid.reshape(1, -1)
    elif grid.ndim == 0: grid = grid.reshape(1, 1)
    return tuple(map(tuple, grid))

def find_color_bbox(grid: np.ndarray, color: int) -> Optional[Tuple[int, int, int, int]]:
    """Returns (min_row, min_col, height, width) or None."""
    rows, cols = np.where(grid == color)
    if rows.size == 0: return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return min_row, min_col, height, width

def analyze_example(example_name: str, input_grid_list, output_grid_list):
    print(f"--- {example_name} Analysis ---")
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)
    target_pattern_tuple = grid_to_tuple(output_grid)

    white_bbox = find_color_bbox(input_grid, 0)
    if white_bbox is None:
        print("  ERROR: No white pixels found")
        return {}
    
    white_r, white_c, h, w = white_bbox
    grid_h, grid_w = input_grid.shape
    
    pattern_first_occurrence: Dict[tuple, Tuple[int, int]] = {}
    
    for r in range(grid_h - h + 1):
        for c in range(grid_w - w + 1):
            subgrid = input_grid[r:r+h, c:c+w]
            if np.any(subgrid == 0): # Skip patterns containing white
                continue
            
            pattern_key = grid_to_tuple(subgrid)
            if pattern_key not in pattern_first_occurrence:
                 pattern_first_occurrence[pattern_key] = (r, c)

    analysis = {
        "Input Shape": input_grid.shape,
        "Output Shape": output_grid.shape,
        "White Block H": h, "White Block W": w,
        "White Block Top-Left (Wr, Wc)": (white_r, white_c),
        "k (Unique patterns without white)": 0,
        "Sorted Candidates": [],
        "Actual Target": target_pattern_tuple,
        "Target Index in Sorted List": -1,
        "Wr % k": "N/A",
        "Wc % k": "N/A",
        "(Wr + Wc) % k": "N/A",
    }

    if not pattern_first_occurrence:
        print("  No non-white patterns of size HxW found.")
        return analysis # Return partial analysis

    candidate_patterns = list(pattern_first_occurrence.keys())
    k = len(candidate_patterns)
    analysis["k (Unique patterns without white)"] = k
    
    if k > 0:
        sorted_candidates = sorted(candidate_patterns)
        analysis["Sorted Candidates"] = sorted_candidates
        
        try:
            target_index = sorted_candidates.index(target_pattern_tuple)
            analysis["Target Index in Sorted List"] = target_index
        except ValueError:
            analysis["Target Index in Sorted List"] = "Not Found"
            
        analysis["Wr % k"] = white_r % k
        analysis["Wc % k"] = white_c % k
        analysis["(Wr + Wc) % k"] = (white_r + white_c) % k
        
    # Print analysis results clearly
    for key, value in analysis.items():
         # Avoid printing very long lists for brevity
         if key == "Sorted Candidates" and k > 5: 
              print(f"  {key}: [List of {k} patterns...]") 
         else:
              print(f"  {key}: {value}")
              
    print(f"  Hypothesis Check: Target Index == Wc % k ? {analysis['Target Index in Sorted List'] == analysis['Wc % k']}")
    print("-" * 20)
    
    return analysis

# Example 1 Data
train1_in = [[8, 6, 0, 6], [6, 8, 6, 8], [8, 6, 8, 6], [6, 8, 6, 8]]
train1_out = [[8]]

# Example 2 Data
train2_in = [[2, 1, 2, 1, 2], [1, 1, 1, 1, 1], [2, 1, 2, 1, 2], [0, 0, 1, 1, 1], [0, 0, 2, 1, 2]]
train2_out = [[1, 1], [2, 1]]

# Example 3 Data
train3_in = [[2, 2, 5, 2, 2, 5, 2], [2, 2, 5, 2, 2, 5, 2], [5, 5, 5, 5, 5, 5, 5], [2, 2, 5, 2, 2, 5, 2], [2, 2, 5, 2, 2, 5, 2], [5, 5, 5, 5, 5, 0, 0], [2, 2, 5, 2, 2, 0, 0]]
train3_out = [[5, 5], [5, 2]]

analysis1 = analyze_example("Example 1", train1_in, train1_out)
analysis2 = analyze_example("Example 2", train2_in, train2_out)
analysis3 = analyze_example("Example 3", train3_in, train3_out)
