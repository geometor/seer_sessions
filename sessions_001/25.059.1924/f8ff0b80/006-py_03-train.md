
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 8 0 0
0 0 3 3 3 0 0 0 8 8 0 0
0 3 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
3
2
8
```
*transformed output:*
```
2
3
8
```
size: True
palette: True
color count: True
pixels off: 2
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 1 0
0 0 0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 7 0
0 0 0 2 0 0 0 0 7 7 7 0
0 0 0 0 0 0 0 0 0 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
1
7
2
```
*transformed output:*
```
1
7
2
```
size: True
palette: True
color count: True
pixels off: 0
PASSED

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 1 0 0 0
0 2 2 2 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
4
2
1
```
*transformed output:*
```
1
2
4
```
size: True
palette: True
color count: True
pixels off: 2
**FAILED!**
