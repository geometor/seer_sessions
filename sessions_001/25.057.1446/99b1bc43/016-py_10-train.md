
## example 1
*input:*
```
0 1 0 1
0 0 0 1
1 0 1 0
0 0 0 1
4 4 4 4
0 2 0 2
0 0 0 2
2 0 0 2
2 2 2 0
```
*expected output:*
```
0 0 0 0
0 0 0 0
0 0 3 3
3 3 3 3
```
*transformed output:*
```
0 1 0 1
0 0 0 1
1 0 1 0
0 0 0 1
4 4 4 4
0 2 0 2
0 0 0 2
2 0 0 2
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
1 1 0 0
1 0 1 0
1 1 0 1
0 1 1 0
4 4 4 4
0 2 2 2
2 0 2 0
2 2 2 2
2 2 2 2
```
*expected output:*
```
3 0 3 3
0 0 0 0
0 0 3 0
3 0 0 3
```
*transformed output:*
```
1 1 0 0
1 0 1 0
1 1 0 1
0 1 1 0
4 4 4 4
0 2 2 2
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 1 0 0
1 0 1 1
1 1 1 0
1 1 1 0
4 4 4 4
0 0 0 0
0 2 0 2
2 2 0 2
0 2 0 0
```
*expected output:*
```
0 3 0 0
3 3 3 0
0 0 3 3
3 0 3 0
```
*transformed output:*
```
0 1 0 0
1 0 1 1
1 1 1 0
1 1 1 0
4 4 4 4
0 0 0 0
0 2 0 2
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**

## example 4
*input:*
```
1 0 1 1
0 0 0 1
1 1 0 0
0 0 1 1
4 4 4 4
0 2 2 2
0 2 2 2
2 0 2 2
2 2 2 2
```
*expected output:*
```
3 3 0 0
0 3 3 0
0 3 3 3
3 3 0 0
```
*transformed output:*
```
1 0 1
0 0 0
1 1 0
0 0 1
4 4 4
0 2 2
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**
