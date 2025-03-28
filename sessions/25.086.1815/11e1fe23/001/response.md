```python
import numpy as np

"""
Identifies the three non-white pixels in the input grid. Calculates the pair with the maximum Euclidean distance. Finds the midpoint (M) between this pair and colors it gray (5) in the output grid. Then, for each of the three original pixels (P1, P2, P3), finds the point (N) that is 1/3 of the way along the vector from M to P. Colors N with the color of the corresponding P in the output grid. The original three pixels are also preserved in the output.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the geometric relationship of three points.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = input_grid.copy()
    
    # Find the coordinates and colors of the three non-white pixels
    points = []
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                points.append({'r': r, 'c': c, 'color': input_grid[r, c]})

    if len(points) != 3:
        # Should not happen based on task description, but good practice
        return output_grid 

    p1, p2, p3 = points

    # Calculate squared Euclidean distances between pairs
    def dist_sq(p_i, p_j):
        return (p_i['r'] - p_j['r'])**2 + (p_i['c'] - p_j['c'])**2

    d12_sq = dist_sq(p1, p2)
    d13_sq = dist_sq(p1, p3)
    d23_sq = dist_sq(p2, p3)

    # Identify the pair of points with the maximum distance (P_a, P_b) and the third point (P_c)
    max_dist = max(d12_sq, d13_sq, d23_sq)
    
    if d12_sq == max_dist:
        p_a, p_b, p_c = p1, p2, p3
    elif d13_sq == max_dist:
        p_a, p_b, p_c = p1, p3, p2
    else: # d23_sq == max_dist
        p_a, p_b, p_c = p2, p3, p1

    # Calculate the midpoint M of the segment connecting P_a and P_b
    # Use integer division // as coordinates must be integers
    m_r = (p_a['r'] + p_b['r']) // 2
    m_c = (p_a['c'] + p_b['c']) // 2

    # Place a gray (5) pixel at coordinates M in the output grid
    if 0 <= m_r < rows and 0 <= m_c < cols:
         output_grid[m_r, m_c] = 5
    # else: # Handle cases where midpoint might be outside - shouldn't happen per assumptions
    #     print(f"Warning: Midpoint ({m_r}, {m_c}) outside grid bounds.")


    # Calculate the coordinates for the three other new points N_a, N_b, N_c
    # N = M + (P - M) / 3
    def calculate_n_point(p_point, m_r_coord, m_c_coord):
        n_r = m_r_coord + (p_point['r'] - m_r_coord) // 3
        n_c = m_c_coord + (p_point['c'] - m_c_coord) // 3
        return n_r, n_c

    n_a_r, n_a_c = calculate_n_point(p_a, m_r, m_c)
    n_b_r, n_b_c = calculate_n_point(p_b, m_r, m_c)
    n_c_r, n_c_c = calculate_n_point(p_c, m_r, m_c)

    # Place pixels with the colors of P_a, P_b, P_c at N_a, N_b, N_c respectively
    if 0 <= n_a_r < rows and 0 <= n_a_c < cols:
        output_grid[n_a_r, n_a_c] = p_a['color']
    # else:
    #     print(f"Warning: N_a ({n_a_r}, {n_a_c}) outside grid bounds.")
        
    if 0 <= n_b_r < rows and 0 <= n_b_c < cols:
        output_grid[n_b_r, n_b_c] = p_b['color']
    # else:
    #     print(f"Warning: N_b ({n_b_r}, {n_b_c}) outside grid bounds.")
        
    if 0 <= n_c_r < rows and 0 <= n_c_c < cols:
        output_grid[n_c_r, n_c_c] = p_c['color']
    # else:
    #     print(f"Warning: N_c ({n_c_r}, {n_c_c}) outside grid bounds.")

    return output_grid
```