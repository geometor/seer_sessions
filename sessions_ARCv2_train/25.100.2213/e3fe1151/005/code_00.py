import copy

"""
Transforms a 5x5 grid of digits based on the following rules:
1. Initialize the output grid as a copy of the input grid.
2. Identify three source values from the input grid: S1=input[0,4], S2=input[4,4], S3=input[4,1].
3. Iterate through each cell (r, c).
4. If the cell is outside the central cross (r!=2 and c!=2) AND its value is 7:
   a. Check if S2 == 7:
      i. If yes, check the quadrant: If UL (r<2, c<2), replace with S1. Otherwise (UR, LL, LR), replace with S3.
   b. Else (S2 != 7):
      i. Check the quadrant:
         - If LR (r>2, c>2), replace with S1.
         - If UL or UR (r<2), replace with S2.
         - If LL (r>2, c<2): Compare S1 and S2. If S1 < S2, replace with S2. Else replace with S1.
5. Cells in the central cross or cells outside the cross that are not 7 remain unchanged.
6. Return the modified output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the transformation rules to the input grid."""

    # 1. Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) # Assuming 5x5

    # 2. Identify source values from the input grid
    s1 = input_grid[0][4]
    s2 = input_grid[4][4]
    s3 = input_grid[4][1]

    # 3. Iterate through each cell (r, c)
    for r in range(rows):
        for c in range(cols):

            # 4. Check if the cell should be modified
            is_outside_cross = (r != 2 and c != 2)
            is_seven = (input_grid[r][c] == 7)

            if is_outside_cross and is_seven:
                # 6. Determine replacement value based on logic
                replacement_value = 7 # Default, should always be overwritten if logic is correct

                # 6a. Check the value of S2
                if s2 == 7:
                    # 6a.i. Determine quadrant and assign value
                    is_ul_quadrant = (r < 2 and c < 2)
                    if is_ul_quadrant:
                        replacement_value = s1
                    else: # UR, LL, or LR quadrants
                        replacement_value = s3
                else: # 6a.ii. S2 != 7
                    # Determine quadrant
                    is_lr_quadrant = (r > 2 and c > 2)
                    is_upper_quadrants = (r < 2) # UL or UR
                    is_ll_quadrant = (r > 2 and c < 2)

                    if is_lr_quadrant:
                        replacement_value = s1
                    elif is_upper_quadrants:
                        replacement_value = s2
                    elif is_ll_quadrant:
                        # Compare S1 and S2
                        if s1 < s2:
                            replacement_value = s2
                        else: # s1 >= s2
                            replacement_value = s1

                # 6b. Update the output grid
                output_grid[r][c] = replacement_value

            # 5. If conditions in step 4 are not met, the cell remains unchanged (already copied)

    # 7. Return the final output grid
    return output_grid