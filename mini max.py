print('Computer takes X and player takes O')
grid=[['_','_','_'],['_','_','_'],['_','_','_']]
end=0
def evaluate(grid):
    x_win = [True] * 8
    y_win = [True] * 8

    for k in range(3):
        if grid[0][k] == 'O':
            x_win[0] = False
        if grid[0][k] == 'X':
            y_win[0] = False
        if grid[k][0] == 'O':
            x_win[1] = False
        if grid[k][0] == 'X':
            y_win[1] = False
        if grid[k][2] == 'O':
            x_win[2] = False
        if grid[k][2] == 'X':
            y_win[2] = False
        if grid[2][k] == 'O':
            x_win[3] = False
        if grid[2][k] == 'X':
            y_win[3] = False
        if grid[1][k] == 'O':
            x_win[4] = False
        if grid[1][k] == 'X':
            y_win[4] = False
        if grid[k][1] == 'O':
            x_win[5] = False
        if grid[k][1] == 'X':
            y_win[5] = False

    if grid[1][1] == 'O' or grid[0][0] == 'O' or grid[2][2] == 'O':
        x_win[6] = False
    if grid[1][1] == 'X' or grid[0][0] == 'X' or grid[2][2] == 'X':
        y_win[6] = False
    if grid[1][1] == 'O' or grid[0][2] == 'O' or grid[2][0] == 'O':
        x_win[7] = False
    if grid[1][1] == 'X' or grid[0][2] == 'X' or grid[2][0] == 'X':
        y_win[7] = False

    xw = sum(x_win)
    yw = sum(y_win)

    return xw - yw
def find_succ(grid,turn):
    succ=[]
    if turn == 'X':
        for i in range(3):
            for j in range(3):
                if grid[i][j]=='_':
                    new_grid = [row[:] for row in grid]
                    new_grid[i][j]='X'
                    succ.append(new_grid)
    else:
        for i in range(3):
            for j in range(3):
                if grid[i][j]=='_':
                    new_grid = [row[:] for row in grid]
                    new_grid[i][j]='O'
                    succ.append(new_grid)
    return succ
def check_win(grid, turn):
    for row in grid:
        if all(cell == turn for cell in row):
            return True

    for col in range(3):
        if all(grid[row][col] == turn for row in range(3)):
            return True

    if all(grid[i][i] == turn for i in range(3)):
        return True

    if all(grid[i][2 - i] == turn for i in range(3)):
        return True

    return False
def check_tie(grid):
    for row in grid:
        if '_' in row:
            return False
    return True
while(1):
    succ=find_succ(grid,'X')
    if check_tie(grid)==True:
        print('Game is a tie!')
        break
    max_succ_val=float('-inf')
    for s in succ:
        super_succ=find_succ(s,'O')
        mini=float('inf')
        for ss in super_succ:
            mini=min(mini,evaluate(ss))
        if mini>max_succ_val:
            max_succ_val=mini
            max_succ=s
    grid=max_succ
    for row in grid:
        print(row)
    if check_win(grid,'X') == True:
        print('Computer Wins!')
        break
    if check_tie(grid)==True:
        print('Game is a tie!')
        break
    print('enter row and col no of ur choice:')
    x=int(input())
    y=int(input())
    grid[x][y]='O'
    if check_win(grid,'O') == True:
        print('Computer Loses!')
        break
