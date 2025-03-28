# Continuing from previous tool code block
output1_objects_expected = find_objects(output1_list, background_color)
output2_objects_expected = find_objects(output2_list, background_color)

if len(input1_objects) == 1 and len(output1_objects_expected) == 2:
    in1 = input1_objects[0]
    # Sort expected output objects by row, then col
    output1_objects_expected.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    out1_exp_TR = output1_objects_expected[0] # Top-Right (Object B)
    out1_exp_BL = output1_objects_expected[1] # Bottom-Left (Object A)

    shift1_exp_A = (out1_exp_BL['top_left'][0] - in1['top_left'][0], out1_exp_BL['top_left'][1] - in1['top_left'][1]) # Shift for Bottom-Left
    shift1_exp_B = (out1_exp_TR['top_left'][0] - in1['top_left'][0], out1_exp_TR['top_left'][1] - in1['top_left'][1]) # Shift for Top-Right

    print("\n--- Example 1 Expected Shifts (Corrected Assignment) ---")
    print(f"Input TopLeft={in1['top_left']}")
    print(f"Expected Output A (BL) TopLeft={out1_exp_BL['top_left']}, Expected Shift A={shift1_exp_A}")
    print(f"Expected Output B (TR) TopLeft={out1_exp_TR['top_left']}, Expected Shift B={shift1_exp_B}")
    print(f"Needs Swap? {1 in in1['colors'] and 2 in in1['colors']}")


if len(input2_objects) == 1 and len(output2_objects_expected) == 2:
    in2 = input2_objects[0]
    # Sort expected output objects by row, then col
    output2_objects_expected.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    out2_exp_TR = output2_objects_expected[0] # Top-Right (Object B)
    out2_exp_BL = output2_objects_expected[1] # Bottom-Left (Object A)

    shift2_exp_A = (out2_exp_BL['top_left'][0] - in2['top_left'][0], out2_exp_BL['top_left'][1] - in2['top_left'][1]) # Shift for Bottom-Left
    shift2_exp_B = (out2_exp_TR['top_left'][0] - in2['top_left'][0], out2_exp_TR['top_left'][1] - in2['top_left'][1]) # Shift for Top-Right

    print("\n--- Example 2 Expected Shifts (Corrected Assignment) ---")
    print(f"Input TopLeft={in2['top_left']}")
    print(f"Expected Output A (BL) TopLeft={out2_exp_BL['top_left']}, Expected Shift A={shift2_exp_A}")
    print(f"Expected Output B (TR) TopLeft={out2_exp_TR['top_left']}, Expected Shift B={shift2_exp_B}")
    print(f"Needs Swap? {1 in in2['colors'] and 2 in in2['colors']}")
