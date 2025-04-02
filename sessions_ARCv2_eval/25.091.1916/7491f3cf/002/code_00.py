    # Expected Output P4 Analysis
    output_p4 = expected_output_np[rows_slice, p4_cols_slice]
    output_p4_colors = np.unique(output_p4)
    expected_p4_fg = None
    expected_p4_bg = None

    if len(output_p4_colors) == 2:
        color1, color2 = output_p4_colors
        # Assign expected FG and BG based on primary_fg_color
        if color1 == primary_fg_color:
            expected_p4_fg = int(color1) # Cast to int
            expected_p4_bg = int(color2) # Cast to int
        elif color2 == primary_fg_color:
            expected_p4_fg = int(color2) # Cast to int
            expected_p4_bg = int(color1) # Cast to int
        else:
             # Error case if primary_fg_color is not one of the two colors in output P4
             expected_p4_fg = f"Error: Primary FG {primary_fg_color} not in Output P4 colors {output_p4_colors}"
             expected_p4_bg = "Error"
    elif len(output_p4_colors) == 1:
         expected_p4_fg = "Error: Only one color in Output P4"
         expected_p4_bg = int(output_p4_colors[0]) # Cast to int
    else: # 0 or >2 colors
         expected_p4_fg = "Error: Unexpected color count in Output P4"
         expected_p4_bg = "Error"
