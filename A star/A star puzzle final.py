from queue import PriorityQueue
pq=PriorityQueue()
i = ((2, 8, 3), (1, 6, 4), (7, 0, 5))
f = ((1, 2, 3), (8, 0, 4), (7, 6, 5))

cost = {i: 0}
par={}
def find_succ(initial):
    for i in range (0,3):
        for j in range (0,3):
            if initial[i][j] == 0:
                pos=(i,j)
                break
    l=[]
    for i in range (-1,2):
        for j in range (-1,2):
            if i == j :
                continue
            new_pos=(i+pos[0],j+pos[1])
            if new_pos[0] >= 0 and new_pos[0] <= 2 and new_pos[1] >= 0 and new_pos[1] <= 2:
                l.append(new_pos)
    ans=[]
    for new_pos in l:
        temp=[list(row) for row in initial]
        t=temp[pos[0]][pos[1]]
        temp[pos[0]][pos[1]]=temp[new_pos[0]][new_pos[1]]
        temp[new_pos[0]][new_pos[1]]=t
        ans.append(tuple(tuple(row) for row in temp))
    return ans
def h(node,f):
    ans=0
    for i in range (3):
        for j in range (3):
            if node[i][j] != f[i][j]:
                ans+=1
    return ans
pq.put((0,i))
while pq:
    curr=pq.get()
    curr_node=curr[1]
    curr_cost=curr[0]
    if curr_node == f:
        break
    succ=find_succ(curr_node)
    for next_node in succ:
        new_cost=cost[curr_node]+1
        if next_node not in cost or cost[next_node]>new_cost:
            cost[next_node]=new_cost
            par[next_node]=curr_node
            '''print('Added to PQ:')
            for row in next_node:
                print(row)
            print('h(n):',h(next_node,f),'g(n):',new_cost,'f(n):',new_cost+h(next_node,f))'''
            pq.put((new_cost+h(next_node,f),next_node))
path=[]
node=f
while node != i:
    path.append(node)
    node=par[node]
path.append(i)
path.reverse()
print('\n\nFinal Path:')
for state in path:
    print('G(n)=',cost[state])
    print('H(n)=',h(state,f))
    print('F(n)=',cost[state]+h(state,f))
    for row in state:
        print(row)
    print('     |')
    print('     |')