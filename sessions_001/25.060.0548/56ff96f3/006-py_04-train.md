
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
1 1 1 1 1 1 1 0 0 0
1 1 1 1 1 1 1 0 0 0
1 1 1 1 1 1 1 0 0 0
1 1 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0 0
2 2 2 2 2 2 2 2 0 0
2 2 2 2 2 2 2 2 0 0
2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 40
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7
0 0 3 0 7 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0
0 3 3 0 0 0 0 0
0 3 3 0 7 7 7 7
0 3 3 0 7 7 7 7
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```
*transformed output:*
```
3 3 0 0 0 0 0 0
3 3 0 0 0 0 0 0
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 25
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 0 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 0 0 0 0
4 4 4 4 4 4 0 0 0 0
4 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 25
**FAILED!**

## example 4
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
7 7 0 0 0 0 0 0 0 0 0
7 7 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 0 0 0
7 7 7 7 7 7 7 7 0 0 0
7 7 7 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
size: True
palette: True
color count: False
pixels off: 19
**FAILED!**
