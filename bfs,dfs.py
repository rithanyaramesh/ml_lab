graph={}

g = {
    '1': ['5', '2'],
    '2': ['1','5','3'],
    '3': ['4', '2'],
    '4': ['5','3','6'],
    '5': ['4', '1','2'],
    '6': ['4']
}

def dfs(src,dst,vis,graph,parent,org_par):
    if src==dst :
        vis.append(src)
        path=[]
        node =dst
        while node != org_par :
            path.append(node)
            node=parent[node]
        path.append(org_par)
        path.reverse()
        return path
    if src not in vis:
        vis.append(src)
        for node in graph[src] :
            if node not in vis :
                parent[node]=src
                result=dfs(node,dst,vis,graph,parent,org_par)
                if result != None:
                    return result
        return None
    
def bfs(src,dst,vis,graph):
    parent={}
    queue=[]
    queue.append(src)
    vis.append(src)
    while queue:
        curr=queue.pop(0)
        if curr == dst:
            break
        for adj in graph[curr]:
            if adj not in vis:
                vis.append(adj)
                queue.append(adj)
                parent[adj]=curr
    path=[]
    node =dst
    while node != src :
        path.append(node)
        node=parent[node]
    path.append(src)
    path.reverse()
    return path
    
vis=[]
print('The search algorithms are executed in the deafult graph:')
print('BFS path:',bfs('1','6',vis,g))
print('DFS path:',dfs('1','6',[],g,{},'1'))
print('Give the user input graph here:')
print('Enter the no. of nodes:')
n=int(input())
for i in range (0,n):
    print('Enter the number of adj nodes for node ',i)
    adj_count=int(input())
    adj_list=[]
    print('Enter the nodes:')
    for j in range(0,adj_count):
        adj_list.append(int(input()))
    graph[i]=adj_list
print('Enter source node and destination node:')
src=int(input())
dst=int(input())
print('Enter 1 for dfs and 2 for bfs:')
choice=int(input())
if choice == 1:
    path = dfs(src,dst,vis,graph,{},src)
else :
    path = bfs(src,dst,vis,graph)
print('The path from src to dst is :',path)

        
    

