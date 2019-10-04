class Graph:
    def __init__(self,name,nodes=[]):
        self.name=name
        self.nodes={}
        for node in nodes:
            self.nodes[node.name]=node

    def __getitem__(self, item):
        if item not in self:
            raise KeyError("node is not in the graph")
        else:
            return self.nodes[item]

    def __str__(self):
        a =""
        for node in self.nodes.values():
            if len(a)==0:
                a += node.name
            else:
                a +=","+node.name
        return a


    def __len__(self):
        return len(self.nodes.keys())

    def __contains__(self, item):
        if isinstance(item,str):
            return item in self.nodes.keys()
        elif isinstance(item,node):
            return item.name in self.nodes.keys()

    def __add__(self, other):
        newnodes={}
        newnodes.update(self.nodes)
        newnodes.update(other.nodes)
        return Graph('combine_graph',newnodes.values())

    def update(self,node):
    # is new node exsist in the graph
        if node.name not in self:
            # enter new node to graph
            self.nodes[node.name] = node
        else:
            for value, key in node.neighbors.items():
                self.nodes[node.name].update(value, key)

    def remove_node(self,name):
        if name in self:
            self.nodes.pop(name)

    def is_edge(self,frm_name,to_name):
        if frm_name in self:
            return (to_name in self.nodes[frm_name].neighbors.keys())


    def add_edge(self, frm_name, to_name, weight):
        if frm_name in self and to_name in self:
            self[frm_name].update(to_name,weight)

    def remove_edge(self, frm_name, to_name):
        if frm_name in self and to_name in self.nodes[frm_name].neighbors:
            self.nodes[frm_name].neighbors.pop(to_name)

    def get_edge_weight(self, frm_name,to_name):
        if frm_name in self and to_name in self:
            if to_name in self.nodes[frm_name].neighbors:
                return self.nodes[frm_name].neighbors.get(to_name)
            else:
                return None

    def get_path_weight(self,path):
        totalweight = 0

        if all([self.get_edge_weight(path[i], path[i + 1]) for i in range(0,len(path)-1)]):
            if len(path) <= 1 or any([isempty == "" for isempty in path]):
                return (None)
            elif all([inpath in self for inpath in path]):
                for i in range(0,len(path)-1):
                    totalweight += self.get_edge_weight(path[i], path[i + 1])
                return (totalweight)
            else:
                return (None)
        else:
            return (None)


    # def all_paths(self):
    #took from lecture
    #     from itertools import chain, combinations, permutations
    #
    #     s = list(self.nodes.keys())
    #     nodes_sets = list(chain.from_iterable(combinations(s, r) for r in range(2, len(s) + 1)))
    #     paths = list(chain.from_iterable((permutations(nodes_set) for nodes_set in nodes_sets)))
    #     return paths


    def all_paths(self):
        #i wotre that sting
        pathlist2n = []
        allpath = []
        templist = []
        for node in self.nodes.values():
            for neighbor in node.neighbors.keys():
                pathlist2n.append((node.name, neighbor))
        pathlist2n
        allpath.extend(pathlist2n)

        n = 2
        while n < len(self.nodes):
            for path0 in allpath:
                for path1 in pathlist2n:
                    if path0[-1] == path1[0] and path1[1] not in path0:
                        x = ((*path0, path1[1]))
                        templist.append(x)
            allpath.extend(templist)
            n += 1
        allpath = list(set(allpath))
        return allpath


    def is_reachable(self,frm_name,to_name):
        if frm_name in self and to_name in self:
            for path in self.all_paths():
                if frm_name == path[0] and to_name == path[-1]:
                    if all([self.is_edge(path[i], path[i + 1]) for i in range(0, len(path) - 1)]):
                        return (True)


    def find_shortest_path(self,frm_name,to_name):
        minweight = None
        shortpath = None
        if frm_name in self and to_name in self:
            for path in self.all_paths():
                if frm_name == path[0] and to_name == path[-1]:
                    if all([self.is_edge(path[i], path[i + 1]) for i in range(0, len(path) - 1)]):
                        if minweight == None:
                            minweight = self.get_path_weight(path)
                            shortpath = path
                        elif minweight > self.get_path_weight(path):
                            minweight = self.get_path_weight(path)
                            shortpath = path
        return (shortpath)

class node:
    def __init__(self, name):
        self.name = name
        self.neighbors = dict()

    def __str__(self):
        return self.name

    def __len__(self):

        return len(self.neighbors.keys())

    def __contains__(self, item):
        return item in self.neighbors.keys()

    def __getitem__(self, item):
        if item in self.neighbors.keys():
            return self.neighbors[item]
        else:
            return None
    def __eq__(self, other):
        return self.name==other.name

    def __ne__(self, other):
        return self.name!=other.name

    def __lt__(self, other):
        return len(self)<len(other)

    def __le__(self, other):
        return len(self)<=len(other)

    def __gt__(self, other):
        return len(self)>len(other)

    def __ge__(self, other):
        return len(self)>=len(other)

    def is_neighbor(self,name):
        return name in self.neighbors.keys()

    def update(self,name,weight):
        if self.name==name:
            return print('same key name and self name is not allowed')
        else:
            if name in self.neighbors.keys() and weight>self.neighbors[name]:
                self.neighbors[name]=weight
            if name not in self.neighbors.keys():
                self.neighbors[name] = weight

    def revmove_neighbor(self,name):
        if name in self.neighbors.keys():
            self.neighbors.pop(name)

    def is_isolated(self):
        return len(self)==0


class NonDirectionalGraph:
    def __init__(self,name,nodes=[]):
        self.name=name
        self.nodes={}
        for node in nodes:
            self.nodes[node.name]=node
        #revrese update edges
        for node in self.nodes:
            for neighbor in self[node].neighbors:
                self[neighbor].update(node,self[node].neighbors[neighbor])

    def __getitem__(self, item):
        if item not in self:
            raise KeyError("node is not in the graph")
        else:
            return self.nodes[item]

    def __str__(self):
        a =""
        for node in self.nodes.values():
            if len(a)==0:
                a += node.name
            else:
                a +=","+node.name
        return a


    def __len__(self):
        return len(self.nodes.keys())

    def __contains__(self, item):
        if isinstance(item,str):
            return item in self.nodes.keys()
        elif isinstance(item,node):
            return item.name in self.nodes.keys()

    def __add__(self, other):
        newnodes={}
        newnodes.update(self.nodes)
        newnodes.update(other.nodes)
        return NonDirectionalGraph('combine_graph',newnodes.values())

    def update(self,node):
    # is new node exsist in the graph
        if node.name not in self:
            # enter new node to graph
            self.nodes[node.name] = node
        else:
            for value, key in node.neighbors.items():
                self.nodes[node.name].update(value, key)
   # revrese update edges
        for neighbor in self[node.name].neighbors:
            self[neighbor].update(node.name,node.neighbors[neighbor])


    def remove_node(self,name):
        if name in self:
            #get our revese edges
            for neighbor in self[name].neighbors:
                if neighbor in self.nodes:
                    self[neighbor].neighbors.pop(name)
            self.nodes.pop(name)


    def is_edge(self,frm_name,to_name):
        if frm_name in self:
            return (to_name in self.nodes[frm_name].neighbors.keys())


    def add_edge(self, frm_name, to_name, weight):
        if frm_name in self and to_name in self:
            self[frm_name].update(to_name,weight)
            #get our revese edges
            self[to_name].update(frm_name,weight)

    def remove_edge(self, frm_name, to_name):
        if frm_name in self and to_name in self.nodes[frm_name].neighbors:
            self.nodes[frm_name].neighbors.pop(to_name)
            #get our revese edges
            self.nodes[to_name].neighbors.pop(frm_name)


    def get_edge_weight(self, frm_name,to_name):
        if frm_name in self and to_name in self:
            if to_name in self.nodes[frm_name].neighbors:
                return self.nodes[frm_name].neighbors.get(to_name)
            else:
                return None

    def get_path_weight(self,path):
        totalweight = 0

        if all([self.get_edge_weight(path[i], path[i + 1]) for i in range(0,len(path)-1)]):
            if len(path) <= 1 or any([isempty == "" for isempty in path]):
                return (None)
            elif all([inpath in self for inpath in path]):
                for i in range(0,len(path)-1):
                    totalweight += self.get_edge_weight(path[i], path[i + 1])
                return (totalweight)
            else:
                return (None)
        else:
            return (None)


    # def all_paths2(self):
    #     #from lecture
    #     from itertools import chain, combinations, permutations
    #
    #     s = list(self.nodes.keys())
    #     nodes_sets = list(chain.from_iterable(combinations(s, r) for r in range(2, len(s) + 1)))
    #     paths = list(chain.from_iterable((permutations(nodes_set) for nodes_set in nodes_sets)))
    #     return paths

    def all_paths(self):
        #i wotre that sting
        pathlist2n = []
        allpath = []
        templist = []
        for node in self.nodes.values():
            for neighbor in node.neighbors.keys():
                pathlist2n.append((node.name, neighbor))
        pathlist2n
        allpath.extend(pathlist2n)

        n = 2
        while n < len(self.nodes):
            for path0 in allpath:
                for path1 in pathlist2n:
                    if path0[-1] == path1[0] and path1[1] not in path0:
                        x = ((*path0, path1[1]))
                        templist.append(x)
            allpath.extend(templist)
            n += 1
        allpath = list(set(allpath))
        return allpath

    def is_reachable(self,frm_name,to_name):
        if frm_name in self and to_name in self:
            for path in self.all_paths():
                if frm_name == path[0] and to_name == path[-1]:
                    if all([self.is_edge(path[i], path[i + 1]) for i in range(0, len(path) - 1)]):
                        return (True)





    def find_shortest_path(self,frm_name,to_name):
        minweight = None
        shortpath = None
        if frm_name in self and to_name in self:
            for path in self.all_paths():
                if frm_name == path[0] and to_name == path[-1]:
                    if all([self.is_edge(path[i], path[i + 1]) for i in range(0, len(path) - 1)]):
                        if minweight == None:
                            minweight = self.get_path_weight(path)
                            shortpath = path
                        elif minweight > self.get_path_weight(path):
                            minweight = self.get_path_weight(path)
                            shortpath = path
        return (shortpath)

    def suggest_friend(self,node_name):
        counter = 0
        bigcounter = 0
        for friend in self.nodes:
            if friend not in self.nodes[node_name].neighbors and friend != node_name:
                for nearfriend in self.nodes[friend].neighbors:
                    if nearfriend in self.nodes[node_name].neighbors:
                        counter += 1
                        # print(friend,nearfriend,counter)
                if bigcounter < counter:
                    bigcounter = counter
                    suggest = friend
                # print('BF',suggest,bigcounter,'now',friend,counter)
                counter = 0
        return (suggest)


