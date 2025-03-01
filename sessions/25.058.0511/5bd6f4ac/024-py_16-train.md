
## example 1
*input:*
```
3 0 0 7 0 0 9 7 0
8 4 0 6 6 0 4 8 4
1 7 0 0 0 0 4 0 0
1 1 0 9 1 0 7 0 0
0 0 0 0 7 7 0 0 0
8 0 0 1 7 0 8 4 0
0 7 0 9 9 2 1 0 0
0 0 0 0 0 0 5 0 0
0 0 0 2 4 0 8 0 0
```
*expected output:*
```
9 7 0
4 8 4
4 0 0
```
*transformed output:*
```
0 0 0
0 0 0
0 0 8
```
size: True
palette: True
color count: False
pixels off: 7
**FAILED!**

## example 2
*input:*
```
9 0 0 0 0 0 0 6 0
0 4 0 7 0 5 0 8 1
0 2 0 0 7 1 4 4 5
0 6 0 0 4 0 0 0 0
8 3 0 4 2 0 0 9 7
0 0 2 3 0 2 0 6 7
4 0 4 0 3 4 7 0 7
7 1 0 0 0 0 3 0 0
3 2 0 0 4 0 0 0 0
```
*expected output:*
```
0 6 0
0 8 1
4 4 5
```
*transformed output:*
```
0 0 0
0 0 0
0 0 4
```
size: True
palette: True
color count: False
pixels off: 6
**FAILED!**

## example 3
*input:*
```
2 5 0 0 6 0 0 0 0
2 5 5 7 0 0 6 0 1
0 3 0 0 0 1 9 4 0
0 7 0 6 0 0 0 0 0
0 9 0 0 0 1 0 0 8
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 1 0 0 0 0 4
0 5 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0
6 0 1
9 4 0
```
*transformed output:*
```
0 0 0
0 0 0
0 0 5
```
size: True
palette: False
color count: False
pixels off: 5
**FAILED!**

## example 4
*input:*
```
0 5 0 0 8 0 0 0 4
0 0 0 0 0 0 3 0 0
0 0 0 0 2 1 0 0 3
0 1 0 0 0 0 3 0 0
1 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0
0 0 9 4 0 0 0 0 0
3 0 7 0 0 2 0 0 6
```
*expected output:*
```
0 0 4
3 0 0
0 0 3
```
*transformed output:*
```
0 0 0
0 0 0
0 0 6
```
size: True
palette: False
color count: False
pixels off: 3
**FAILED!**
