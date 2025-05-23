# tool_code is not needed for this analysis, manual inspection is sufficient.

# Example 1:
# A = [[3,3,3],[3,0,0],[3,0,0]] -> A0(T), A1(F), A2(F), A2[2]=0
# B = [[1,1,1],[1,0,1],[1,0,1]] -> B0(T), B1(F), B2(F)
# B3= [1,1,1]
# Out = [[3,3,3],[3,0,0],[1,1,0]] -> Out0=A0, Out1=A1, Out2=mod(B0)

# Example 2:
# A = [[7,7,7],[7,0,7],[7,0,0]] -> A0(T), A1(F), A2(F), A2[2]=0
# B = [[8,8,8],[8,0,0],[8,8,8]] -> B0(T), B1(F), B2(T)
# B3= [8,8,8]
# Out = [[7,7,7],[8,8,0],[0,0,0]] -> Out0=A0, Out1=mod(B0), Out2=zeros

# Example 3:
# A = [[9,9,9],[9,0,0],[9,9,0]] -> A0(T), A1(F), A2(F), A2[2]=0
# B = [[5,5,5],[5,0,0],[5,0,5]] -> B0(T), B1(F), B2(F)
# B3= [5,5,5]
# Out = [[9,9,9],[5,5,5],[0,0,0]] -> Out0=A0, Out1=B0, Out2=zeros

# Example 4:
# A = [[8,8,8],[8,0,8],[8,8,8]] -> A0(T), A1(F), A2(T)
# B = [[6,6,6],[6,0,6],[6,6,6]] -> B0(T), B1(F), B2(T)
# B3= [0,0,0]
# Out = [[8,0,0],[6,0,0],[0,0,0]] -> Out0=mod(A1), Out1=mod(B1), Out2=zeros

# Example 5:
# A = [[4,4,4],[4,0,4],[4,4,4]] -> A0(T), A1(F), A2(T)
# B = [[6,6,6],[6,0,0],[6,0,0]] -> B0(T), B1(F), B2(F)
# B3= [6,6,6]
# Out = [[4,0,0],[6,6,6],[6,6,6]] -> Out0=mod(A1), Out1=B0, Out2=B3(==B0)

# Example 6:
# A = [[7,7,7],[7,0,7],[7,0,7]] -> A0(T), A1(F), A2(F), A2[2]=7
# B = [[8,8,8],[8,0,8],[8,0,0]] -> B0(T), B1(F), B2(F)
# B3= [8,8,8]
# Out = [[7,7,0],[8,8,8],[0,0,0]] -> Out0=mod(A0), Out1=B0, Out2=zeros