
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 7 7
0 0 0 0 0 0 0 0 7 7
```
*expected output:*
```
3 3 7
3 7 7
3 7 7
```
*transformed output:*
```
3 3 3
3 7 7
7 7 7
```
size: True
palette: True
color count: True
pixels off: 2
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 4 4
0 0 0 6 6 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
6 6 6
4 6 6
4 4 6
```
*transformed output:*
```
4 4 4
6 6 6
6 6 6
```
size: True
palette: True
color count: True
pixels off: 6
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
```
*expected output:*
```
1 1 1
1 3 1
3 3 3
```
*transformed output:*
```
3 3 3
3 1 1
1 1 1
```
size: True
palette: True
color count: True
pixels off: 8
**FAILED!**
