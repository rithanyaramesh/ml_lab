from queue import PriorityQueue
pq=PriorityQueue()
pq.put((0,'s'))
par={}
cost={'s':0}
graph={'s':[('a',2),('b',3)],
    'a':[('c',3)],
    'b':[('c',1),('d',3)],
    'c':[('e',3),('d',1)],
    'd':[('f',2)],
    'e':[('g',2)],
    'f':[('g',1)]
}
h={'s':6,'a':4,'b':4,'c':4,'d':3.5,'e':1,'f':1,'g':0}
while pq:
    curr=pq.get()
    curr_node=curr[1]
    curr_cost=curr[0]
    if curr_node == 'g':
        break
    for next in graph[curr_node]:
        next_node=next[0]
        new_cost=cost[curr_node]+next[1]
        if next_node not in cost or cost[next_node]>new_cost:
            cost[next_node]=new_cost
            par[next_node]=curr_node
            pq.put((new_cost+h[next_node],next_node))
path=[]
node='g'
while node != 's':
    path.append(node)
    node=par[node]
path.append('s')
path.reverse()
print(path)
print('Total cost=',cost['g'])
            
    


