# Continuing from previous tool code block
output1_objects_expected = find_objects(output1_list, background_color)
output2_objects_expected = find_objects(output2_list, background_color)

if len(input1_objects) == 1 and len(output1_objects_expected) == 2:
    in1 = input1_objects[0]
    # Sort expected output objects by row, then col
    output1_objects_expected.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    out1_exp_B = output1_objects_expected[0] # Top-Right (4, 7)
    out1_exp_A = output1_objects_expected[1] # Bottom-Left (8, 1)

    shift1_exp_A = (out1_exp_A['top_left'][0] - in1['top_left'][0], out1_exp_A['top_left'][1] - in1['top_left'][1])
    shift1_exp_B = (out1_exp_B['top_left'][0] - in1['top_left'][0], out1_exp_B['top_left'][1] - in1['top_left'][1])

    print("\n--- Example 1 Expected Shifts ---")
    print(f"Input TopLeft={in1['top_left']}")
    print(f"Expected Output A TopLeft={out1_exp_A['top_left']}, Expected Shift A={shift1_exp_A}") # Should be bottom-left
    print(f"Expected Output B TopLeft={out1_exp_B['top_left']}, Expected Shift B={shift1_exp_B}") # Should be top-right
    print(f"Needs Swap? {1 in in1['colors'] and 2 in in1['colors']}")


if len(input2_objects) == 1 and len(output2_objects_expected) == 2:
    in2 = input2_objects[0]
    # Sort expected output objects by row, then col
    output2_objects_expected.sort(key=lambda o: (o['top_left'][0], o['top_left'][1]))
    out2_exp_B = output2_objects_expected[0] # Top-Right (4, 7)
    out2_exp_A = output2_objects_expected[1] # Bottom-Left (8, 1)

    shift2_exp_A = (out2_exp_A['top_left'][0] - in2['top_left'][0], out2_exp_A['top_left'][1] - in2['top_left'][1])
    shift2_exp_B = (out2_exp_B['top_left'][0] - in2['top_left'][0], out2_exp_B['top_left'][1] - in2['top_left'][1])

    print("\n--- Example 2 Expected Shifts ---")
    print(f"Input TopLeft={in2['top_left']}")
    print(f"Expected Output A TopLeft={out2_exp_A['top_left']}, Expected Shift A={shift2_exp_A}") # Should be bottom-left
    print(f"Expected Output B TopLeft={out2_exp_B['top_left']}, Expected Shift B={shift2_exp_B}") # Should be top-right
    print(f"Needs Swap? {1 in in2['colors'] and 2 in in2['colors']}")
