
Previous Code:
```python
import numpy as np

"""
Identifies all maximal contiguous rectangular blocks composed solely of white (0) pixels in the input grid.
Calculates the area for each maximal white rectangle.
Selects a single rectangle based on the following ordered criteria:
1. Maximum Area (largest height * width).
2. Maximum Height (tallest, to break ties in area).
3. Minimum Row index (top-most, to break ties in area and height).
4. Minimum Column index (left-most, to break ties in area, height, and row).
Copies the input grid to the output grid, then changes the color of all pixels within the bounds of the selected rectangle to magenta (6).
If no white rectangles are found, the output grid is identical to the input grid.
"""

def find_all_white_rectangles(grid):
    """
    Finds all possible rectangular blocks of white (0) pixels.
    This generates rectangles anchored at every white pixel and extending
    as far right and down as possible while remaining white. Includes
    sub-rectangles, which will be filtered later for maximality.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a
              rectangle {'r': row, 'c': col, 'h': height, 'w': width, 'area': area}.
    """
    rows, cols = grid.shape
    all_rects = []
    # Iterate through each cell as a potential top-left corner
    for r in range(rows):
        for c in range(cols):
            # If the cell is white, start searching for rectangles
            if grid[r, c] == 0:
                max_w = 0
                # Find the maximum width of consecutive white cells in the current row starting at (r, c)
                while c + max_w < cols and grid[r, c + max_w] == 0:
                    max_w += 1
                
                # Now, for each possible width (1 to max_w), find the max height
                for w in range(1, max_w + 1):
                    max_h = 1 # Start with height 1 (the current row)
                    # Check subsequent rows to see how far down this rectangle of width 'w' can extend
                    while r + max_h < rows:
                        is_solid_row = True
                        # Check if the entire segment grid[r + max_h, c : c + w] is white
                        for k in range(w):
                            if grid[r + max_h, c + k] != 0:
                                is_solid_row = False
                                break
                        if is_solid_row:
                            max_h += 1 # If the row is solid white, increment height
                        else:
                            break # Stop extending height if a non-white cell is found
                    
                    # Add the found rectangle (with height max_h and width w) to the list
                    area = max_h * w
                    all_rects.append({'r': r, 'c': c, 'h': max_h, 'w': w, 'area': area})
    return all_rects

def filter_maximal_rectangles(rectangles):
    """
    Filters a list of rectangles to keep only the maximal ones.
    A rectangle R1 is maximal if no other rectangle R2 in the list fully contains R1.

    Args:
        rectangles (list): A list of rectangle dictionaries.

    Returns:
        list: A list of maximal rectangle dictionaries.
    """
    if not rectangles:
        return []

    maximal_rects_candidates = []
    # Iterate through each rectangle and check if it's contained within any other
    for i, r1 in enumerate(rectangles):
        is_maximal = True
        for j, r2 in enumerate(rectangles):
            # Don't compare a rectangle with itself
            if i == j:
                continue
            
            # Check if r2 strictly contains r1 (same dimensions allowed, but different location is okay)
            # Check if r2 contains r1
            # r2 contains r1 if:
            # r2.r <= r1.r
            # r2.c <= r1.c
            # r2.r + r2.h >= r1.r + r1.h
            # r2.c + r2.w >= r1.c + r1.w
            # And r2 is not identical to r1 (either bigger or same size at diff location)
            if (r2['r'] <= r1['r'] and
                r2['c'] <= r1['c'] and
                r2['r'] + r2['h'] >= r1['r'] + r1['h'] and
                r2['c'] + r2['w'] >= r1['c'] + r1['w']):
                
                # If r2 is strictly larger than r1 in at least one dimension or area
                if r2['area'] > r1['area'] or r2['h'] > r1['h'] or r2['w'] > r1['w']:
                   is_maximal = False
                   break
                # Handle case where r1 and r2 are identical but found from different starts
                # If they are identical, we only want one copy eventually, but
                # don't mark as non-maximal yet based on an identical copy.
                # Let the duplicate removal handle this.

        if is_maximal:
            maximal_rects_candidates.append(r1)
            
    # Remove duplicates. Since identical rectangles might be generated starting
    # from different top-left corners but deemed maximal, we need to ensure uniqueness.
    unique_maximal_rects_set = set()
    for rect in maximal_rects_candidates:
        # Use a tuple representation for hashing in the set
        unique_maximal_rects_set.add( (rect['r'], rect['c'], rect['h'], rect['w'], rect['area']) )
        
    # Convert back to list of dictionaries
    final_maximal_rects = [{'r': r, 'c': c, 'h': h, 'w': w, 'area': area} for r, c, h, w, area in unique_maximal_rects_set]
    
    return final_maximal_rects

def select_rectangle(rectangles):
    """
    Selects a single rectangle from a list based on sorting criteria:
    1. Max Area (descending)
    2. Max Height (descending)
    3. Min Row (ascending)
    4. Min Col (ascending)

    Args:
        rectangles (list): A list of maximal rectangle dictionaries.

    Returns:
        dict or None: The selected rectangle dictionary, or None if the list is empty.
    """
    if not rectangles:
        return None

    # Sort using a lambda function with multiple keys.
    # Negative sign is used for descending order for numeric types.
    sorted_rects = sorted(rectangles, key=lambda r: (-r['area'], -r['h'], r['r'], r['c']))
    
    # The first element after sorting is the desired rectangle
    return sorted_rects[0]

def transform(input_grid):
    """
    Applies the transformation logic: find the specific maximal white rectangle
    based on area, height, and position, and fill it with magenta.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Step 1 & 2: Identify all possible white rectangles
    # Note: This function might generate many sub-rectangles.
    all_rects = find_all_white_rectangles(input_grid)
    
    # Step 3: Filter to get only the maximal ones
    maximal_rects = filter_maximal_rectangles(all_rects)
    
    # Step 4 & 5: Select the target rectangle based on the specified criteria
    selected_rect = select_rectangle(maximal_rects)

    # Step 6 & 7: If a rectangle was successfully selected, fill it
    if selected_rect:
        # Extract coordinates and dimensions
        r, c, h, w = selected_rect['r'], selected_rect['c'], selected_rect['h'], selected_rect['w']
        
        # Fill the selected rectangular area in the output grid with magenta (6)
        output_grid[r:r+h, c:c+w] = 6

    # Step 8: Return the modified grid (or the original copy if no rectangle was selected)
    return output_grid

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 0 0 0 0 0 0 0 1 0 0 1 0 0 1 0 1 0 1
0 1 0 0 0 0 0 1 1 1 1 0 0 1 1 0 0 0 0 0
```
Expected Output:
```
1 1 6 6 6 6 6 0 0 1 0 0 1 0 0 1 0 1 0 1
0 1 6 6 6 6 6 1 1 1 1 0 0 1 1 0 0 0 0 0
```
Transformed Output:
```
1 1 6 6 6 6 6 0 0 1 0 0 1 0 0 1 0 1 0 1
0 1 6 6 6 6 6 1 1 1 1 0 0 1 1 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
1 1 1 0 0 1 1 0 1 1 1 1 0 0 0 0 0 1 0 1
1 1 1 0 1 1 0 0 1 0 1 0 1 1 0 0 0 1 1 1
0 0 1 1 1 0 0 1 0 1 0 1 1 0 1 0 1 1 1 0
0 1 0 1 0 0 0 1 1 0 1 1 1 0 0 0 1 1 1 1
```
Expected Output:
```
1 1 1 0 0 1 1 0 1 1 1 1 0 0 6 6 6 1 0 1
1 1 1 0 1 1 0 0 1 0 1 0 1 1 6 6 6 1 1 1
0 0 1 1 1 0 0 1 0 1 0 1 1 0 1 0 1 1 1 0
0 1 0 1 0 0 0 1 1 0 1 1 1 0 0 0 1 1 1 1
```
Transformed Output:
```
1 1 1 0 0 1 1 0 1 1 1 1 0 0 6 6 6 1 0 1
1 1 1 0 1 1 0 0 1 0 1 0 1 1 6 6 6 1 1 1
0 0 1 1 1 0 0 1 0 1 0 1 1 0 1 0 1 1 1 0
0 1 0 1 0 0 0 1 1 0 1 1 1 0 0 0 1 1 1 1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0 0 0 0
1 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 0 0 0
1 0 1 1 0 0 1 0 1 0 1 0 1 0 0 0 1 0 0 0
0 0 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1
```
Expected Output:
```
0 0 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0 6 6 6
1 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 6 6 6
1 0 1 1 0 0 1 0 1 0 1 0 1 0 0 0 1 6 6 6
0 0 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1
```
Transformed Output:
```
0 0 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0 6 6 6
1 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 6 6 6
1 0 1 1 0 0 1 0 1 0 1 0 1 0 0 0 1 6 6 6
0 0 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 4:
Input:
```
5 1 1 1 1 1 5 0 0 0 0 0 0 0 0 0 0 1 1 0 1 0 0 1 0 0 0 0 1 0
0 1 0 1 0 0 0 1 1 1 1 0 1 1 1 0 0 0 0 1 1 1 0 1 0 1 1 1 1 1
1 1 0 0 0 1 0 1 0 1 1 1 0 1 1 0 0 0 0 1 0 0 1 1 0 0 1 0 0 0
```
Expected Output:
```
5 1 1 1 1 1 5 0 0 0 0 0 0 0 0 0 0 1 1 0 1 0 0 1 0 0 0 0 1 0
0 1 0 1 0 0 0 1 1 1 1 0 1 1 1 6 6 6 6 1 1 1 0 1 0 1 1 1 1 1
1 1 0 0 0 1 0 1 0 1 1 1 0 1 1 6 6 6 6 1 0 0 1 1 0 0 1 0 0 0
```
Transformed Output:
```
5 1 1 1 1 1 5 6 6 6 6 6 6 6 6 6 6 1 1 0 1 0 0 1 0 0 0 0 1 0
0 1 0 1 0 0 0 1 1 1 1 0 1 1 1 0 0 0 0 1 1 1 0 1 0 1 1 1 1 1
1 1 0 0 0 1 0 1 0 1 1 1 0 1 1 0 0 0 0 1 0 0 1 1 0 0 1 0 0 0
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 40.0
