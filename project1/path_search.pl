%% =============== CS314 Prolog Project (Owner: Yanhao Chen) ================== %%
% Introduction:
% 	Train schedules can get very complex. Many countries with extenstive mass transit can 
%		have dizzying schedules with different service on weekends, expresses, specials, 
%		holiday trains, shuttles and any number of other variations. Monty Python's Flying Circus
%		based at least one sketch on the arcane and ever-changing English train system's schedule
%		where discovery of feasible solutions for generating a rail route solved a murder mystery:
%		    https://montypython.net/scripts/railway.php
%		.. too bad they weren't computer scientists.
%
%		One of the main powers of Prolog is that you do not need to understand the whole if you
%		understand the parts and how they relate. You can enumerate the qualities things have as facts, 
%		code how they relate as rules, thenyou can use that knowledge base to find solutions to very
%		complicated queries involving many rules with any number of requirements.
%		
%		In this project, you are going to find the path between two stations on a certain day with
% 	the train schedule info given below. You need to generate a weighted where each
%		note represents a station and each edges represents a path between the stations it joins.
%		Once you have the train station problem represented as a graph you can bring all your
%		graph searching algorithms to bear. There are three very useful algorithms for searching
%		graphs to find a minimal path; depth-first search, breadth-first search, and Dijkstra's algorithm.
%
%		The search algorithm will return a path with a cost that represents the length of the 
% 	path. Different search algorithms may return different paths with different costs 
% 	while the Dijkstra algorithm is guaranteed to return the path with the smallest cost.
% 
%What to implement:
%		Implementing all of Dijkstra's, BFS and DFS may be a bit difficult, so the TAs have
%		kindly implemented that for you (w00t)! All you have to do is build a library of smaller
%		helper rules that their code relies on.
%
%		The first segment below is a test library with some basic rules and routes. Feel free
%		to test yoru code them. Examples for the rules below are written presuming this test data.
%
%		The second segment below is a utility library. You do not have to implement any
%		of the rules in the utility library, however we strongly recommend you do.
%		You will find them very useful later and they serve as good practice to get started.
%
%		The third and forth segments below are the graph and helper libraries. 
%		You must implement all of the rules in both of them, except for the navigate rule.
%		The TAs also implemented that for you. You can use it to check your implementation
%		by giving it queries like:
%			navigate(sun, s1, s9, bfs, P, C).
%			navigate(mon, s9, s1, dfs, P, C).
%			navigate(tue, s2, s5, dijkstra, P, C).
%		The graph search algorithms are	implemented such that they rely on the rules in the
%		graph and helper libraries.
%
%		The last segment holds the TAs' implementations of the various graph search
%		algorithms. Do not modify them. You may however find looking over them useful
%		in order to see how the helper rules are used.
%
%Methodology and guidelines:
%		Holy moly! This might seem like a lot. Take it one bit at a time. You don't need to
%		understand the whole to make the parts work.
%
%		Take a look at the example data and the image links that depict the graphs directly
%		to get a feel for how the data is being represented. It may be very useful to spend
%		some time first completing the rules in the utility library. They can make coding up the
%		rules in the helper library much more simple and they will get you used to working with
%		the data.
%
%		Many of the rules in the utility library are fairly simple. They shouldn't present too
%		much of a challenge given the recent homework.
%
%		The graph rules are also astoundingly simple. They only represent interpreting the facts
%		and rules in the test section as a graph. No more, no less.
%
%		While the rules in the helper library may look very complex, most of what you need to
%		do is structural. Put the minimum of X in Y, make a list of Xs where Y, or change X if Y
%		are the essential themes. It can help to approach each rule as an individual element
%		and to only think about what is necessary to implement it given the rules you have so far.
%		The examples can be very useful in determining what has to change where for a rule to
%		work correctly.
% 
% What to submit: This prolog file: path_search.pl.
%
%
%% ============================================================================ %%

% =============== Test Graphs ================== %

day(mon).
day(tue).
day(wed).
day(thu).
day(fri).
day(sat).
day(sun).

% Train stations
station(s1).
station(s2).
station(s3).
station(s4).
station(s5).
station(s6).
station(s7).
station(s8).
station(s9).

% Routes. 
% A simple list of stations is provided, together with a weight indicates the distance between two stations.
% By default, routes are considered as two-way. For example, [s1, 2, s2] means the train can go both from 
% s1 to s2 and from s2 to s1.
route(ra, [s1, 2, s2, 2, s3, 1, s4]).
route(rb, [s7, 5, s6, 2, s2, 3, s5]).
route(rc, [s2, 4, s8, 3, s4, 1, s9]).
route(rd, [s1, 4, s7, 1, s9]).

% Some routes will be one-way on some specific days. For example, oneway_route(rd, [mon]). means route rd
% is one-way on monday, which means it only goes from s1 to s9 on monday. 
oneway_route(rd, [mon, tue]).

% Some routes will become a loop route on some specific days. For example, loop_route(rc, 1, [tue, wed, sun]). means
% for route rc, there will be paths from both s9 to s2 and s2 to s9 on tuesday, wenesday and sunday. The distance 
% between these two stations is 1.
loop_route(rc, 1, [wed, sun]).

% Trains.
% Trains will only run on some specific days.
train(ta, [tue, wed, thu, fri, sat, sun]).
train(tb, [mon, thu, fri]).
train(tc, [mon, tue, wed, thu, fri, sat, sun]).
train(td, [mon, tue, wed, thu, fri]).
train(te, [mon, sat, sun]).
train(tf, [mon, tue, sat, sun]).

% Multpile trains may provide services for runnning on the same route.
service(ta, ra).
service(tb, ra).
service(tc, rb).
service(td, rc).
service(te, rc).
service(tf, rd).


% =============== Utility rule library (optional) ================== %
% These predicators may be useful when you implement the bfs/dfs/dijkstra algorithms. You do not need to use all
% of them.


%Member rule:
% memberL(X, L) should be true if X is a memebr of L.
% memberL(b, [a, b, c]).
% true.
% memberL(e, [a, b, c]).
% false.

memberL(A, [A]).
memberL(A, [Car | Cdr]) :- A = Car; memberL(A, Cdr).	

%Reverse rule:
% reverseL(L1, L2) should be true when the elements of L2 are in reverse order compared to L1.
% reverseL([a, b, c], [c, b, a]).
% true.
% reverseL([a, b, c], X).
% X = [c, b, a].

reverseL(L1, L2) :- false. /* <-- YOUR CODE HERE (delete the false) */


%Length rule:
% lengthL(L, Length) should be true if Length represents the number of elements in L. 
% lengthL([a, b, c], 3).
% true.
% lengthL([[a, b], [c, d], [e, f]], X).
% X = 3.

lengthL([], X) :- X = 0.
lengthL([Car | Cdr], Length) :- lengthL(Cdr, I), Length is I + 1.

%Sublist rule:
% sublistL(L1, L2) should be true if L1 is a sublist of L2.
% sublistL([c, d, e], [a, b, c, d, e, f]).
% true.
% sublistL(X, [a, b, c]).
% X = []
% X = [a];
% X = [b];
% X = [c];
% X = [a, b];
% X = [b, c];
% X = [a, b, c].

sublistL(L1, L2) :- false. /* <-- YOUR CODE HERE (delete the false) */


%Nth rule:
% nth1L(N, L, X) should be true if X is the N-th element in L.
% nth1L(1, [a, b, c], a).
% true.
% nth1L(3, [a, b, c], c).
% true.

nth1L(N, [Car | Cdr], X) :- (N = 1, Car = X); (I is N - 1, nth1L(I, Cdr, X)).


%Exclude rule:
% excludeL(L1, L2, L3) should be true if L3 contains those elements in L1 but not in L2.
% excludeL([a, b, d, f], [a, c, d, e], [b, f]).
% true.
% excludeL([a, b, d, f], [a, c], X).
% X = [b, d, f].

excludeL_includes(_, []).
excludeL_includes([Car1|Cdr1], L2) :- ([Car2|Cdr2] = L2, Car1 = Car2, excludeL_includes(Cdr1, Cdr2)); excludeL_includes(Cdr1, L2).
excludeL_excludesOne([], X).
excludeL_excludesOne([Car|Cdr], X) :- \+(Car = X), excludeL_excludesOne(Cdr, X).
excludeL_excludesList(_, []).
excludeL_excludesList(L1, [Car|Cdr]) :- excludeL_excludesOne(L1, Car), excludeL_excludesList(L1, Cdr).

excludeL(L1, L2, L3) :- excludeL_includes(L1, L3), excludeL_excludesList(L2, L3). 


%Delete rule
% deleteL(X, L1, L2) should be true if L2 is the same as L1 except that X is not in L1.
% delete(a, [a, b, c, a], [b, c, a]).
% true.
% deleteL(c, [a, b, c, d], X).
% X = [a, b, d].

deleteL(X, [], []).
deleteL(X, [Car1|Cdr1], L2) :- (X = Car1, deleteL(0,Cdr1,L2) ); ([Car2|Cdr2] = L2, Car1 = Car2, deleteL(X,Cdr1,Cdr2)).


%Repeat rule
% repeatL(L1, N, L2) should be true if L2 is a length N list while each element of L2 is L1.
% repeatL([a, b, c], 2, [[a, b, c], [a, b, c]]).
% true.
% repeatL([a, b, c], 2, X).
% X = [[a, b, c], [a, b, c]].

repeatL(L1, 0, []).
repeatL(L1, N, [Car | Cdr]) :- L1 = Car, I is N - 1, repeatL(L1, I, Cdr).


% =============== Graph rule library (required) ================== %
% The represented graph for the above example on tuesday should be:
% https://drive.google.com/file/d/1V7sOPJ1xPI6GKY5nNTuM16GQlCw2ZxMO/view?usp=sharing
% The represented graph for the above example on sunday should be:
% https://drive.google.com/file/d/1SY-_2P2swjzx9CrJDrlrZWtc3y_njiYi/view?usp=sharing
% You can use node(X) and edge(tue, X, Y, C). to generate all edges to check the correctness.


%Node rule:
% Each node in the graph represents a station.
% node(s1).
% true.
% node(ta).
% false.

node(X) :- false. /* <-- YOUR CODE HERE (delete the false) */


%Edge rule:
% edge(D, X, Y, C). should be true if there is an path between station X and Y with cost C on the day D.
% Each edge represents the two connected stations on the given day.
% The distance between two stations will be positive and less than 9999.
% edge(sun, s9, s2, 1).
% true.
% edge(mon, s7, s1, _).
% false.

edge(D, X, Y, C) :- false.  /* <-- YOUR CODE HERE (delete the false) */


% =============== Helper rule library (required) ================== %

%Neighbors rule: already defined!
% neighbors(+Day, +Node, -NeighborNodes).
% When exploring a node in bfs/dfs/dijkstra, the very first thing to do is to get all the neighbor nodes
% of the current node. The neighbor nodes of a node may be different on different days.
%
% This predicator returns all the neighbor nodes of Node on certain Day.
%
% neighbors(sun, s1, [s2, s7]).
% true.
% neighbors(wed, s1, X).
% X = [s2]. % Only train tf services route rd which includes edge(_, s1, s7, _). train tf does not run on wednesday.

neighbors(Day, Node, Neighbors) :- findall(N, edge(Day, Node, N, _), Neighbors). //do not modify ... already defined!


%Generate cost list rule: 
% generate_cost_list(+CurNode, +CurCost, +NewNodes, -NewNodeCostsList).
% Generate a list that holds the total costs of moving from the current node to each of its neighbors,
%	 which is the cost to reach a neighbor node plus the cost of the path to the current node.
%
% Given a list of neighbor nodes NewNodes and the cost of reaching the current node, this predicator 
% generates a list costs to reach these NewNodes.
%
% generate_cost_list(sun, s1, 0, [s2, s7], [2, 4]).
% true.
% generate_cost_list(sun, s1, 0, [s2, s7], X).
% X = [2, 4].

generate_cost_list(CurNode, CurCost, NewNodes, NewNodeCostsList) :- false. /* <-- YOUR CODE HERE (delete the false) */


%Generate path list rule:
% generate_path_list(+CurPath, +NewNodes, -NewNodesPathsList).
% For each neighbor node, we need to get the cost of the path to each neighbor node
% from the current node.
%
% Given a list of neighbor nodes NewNodes and the path to reach the current node CurPath, this predicator
% generates a list of lists where each sublist represents a path to reach a node in NewNodes by extending
%	the path so far, listed in CurPath.
% For example, CurPath is [s1, s2] which means the current node is s2 and the path to s2 is s1->s2.
% For each of s3's neighbors [s3, s5, s8], we generate the path to s3 which is s1->s2->s3 and can be
% represented as [s1, s2, s3].
%
% generate_path_list([s1, s2], [s3, s5, s8], [[s1, s2, s3], [s1, s2, s5], [s1, s2, s8]]).
% true.
% generate_path_list([s1, s2], [s3, s5, s8], X).
% X = [[s1, s2, s3], [s1, s2, s5], [s1, s2, s8]].

generate_path_list(CurPath, NewNodes, NewNodesPathsList) :- false. /* <-- YOUR CODE HERE (delete the false) */


%Generate search node list rule
% generate_search_node_list(+Nodes, +Costs, +Paths, -SearchNodeLists).
%
% A search_node(Node, Cost, Path) describes an item stored in a Queue/Stack/Priority_Queue for analysis.
%	This predicator stitches together information from a number of different sources and reformats the information as a 
%	 list of search_nodes.
%
% generate_search_node_list([s8, s6], [6, 4], [[s1, s2], [s2, s6]], [search_node(s8, 6, [s1, s2]), search_node(s6, 4, [s2, s6])]).
% true.
% generate_search_node_list([s8, s6], [6, 4], [[s1, s2], [s2, s6]], X).
% X = [search_node(s8, 6, [s1, s2]), search_node(s6, 4, [s2, s6])].

generate_search_node_list(Nodes, Costs, Paths, SearchNodeLists) :- false. /* <-- YOUR CODE HERE (delete the false) */


%Get min from pq rule:
% get_min_from_pq(+PQ, -MinCostSearchNode).
% Dijkstra's algorithm uses a priority queue so that, of all nodes yet to be explored, those with the lowest cost
% will be processed first. In this project, you do not need to implement the real priority queue operations, but just
%	find the search_node with the lowest cost.
%
% This predicator returns the search node with the minimum cost from the "Priority Queue".
%
% get_min_from_pq([search_node(s6, 8, [s9, s2, s6]), search_node(s1, 2, [s9, s2, s1]), search_node(s8, 3, [s9, s2, s8])], search_node(s1, 2, [s9, s2, s1])).
% true.
% get_min_from_pq([search_node(s6, 8, [s9, s2, s6]), search_node(s1, 2, [s9, s2, s1]), search_node(s8, 3, [s9, s2, s8])], X).
% X = search_node(s1, 2, [s9, s2, s1]).

get_min_from_pq(PQ, MinCostSearchNode) :- false. /* <-- YOUR CODE HERE (delete the false) */


%Update pq rule:
% update_pq(+SearchNodesList, +PQ, -NewPQ).
% When Dijkstra's algorithm visits a node it see if the cost of reaching the neigboring nodes, plus the cost
%	of the path so far is less than the current stored cost. If so, it will update that cost.
%
% Given a list of search nodes, for each of the search node, this predicator only updates the cost and path
%	of the corresponding search node in the priority queue when the newly-calculated cost is lower than the old one.
%
% update_pq([search_node(s1, 0, [s1]), search_node(s3, 4, [s2])], [search_node(s1, 1, [s1, s2]), search_node(s3, 1, [s3])], X).
% X = [search_node(s1, 0, [s1]), search_node(s3, 1, [s3])].
% Only search_node(s3, _, _) is updated to the new cost and path since the orignal cost 4 is larger than 0.

update_pq(SearchNodesList, PQ, NewPQ) :- false. /* <-- YOUR CODE HERE (delete the false) */



%% DO NOT MODIFY ANYTHING BELOW THIS LINE %%

% =============== bfs/dfs/dijkstra ================== %

% Depth-first search (DFS) is an algorithm for searching tree/graph. The algorithm starts at the starting node
% and explores neighbor nodes as far as possible along each branch before backtracking.
% The pseudo-code of DFS is shown below.
% procedure DFS(G(V, E), Start, Goal)
% 	let S be a stack
%    S.push(search_node(Start, 0, [Start]))
%    while S is not empty do
%        search_node(node, cost, [path]) = S.pop()
%        if node is Goal then
%        	return cost, path
%        if node is visited then
%        	label v as visited
%        	for all edges edge(v, nv, c) in E do
%        		S.push(search_node(nv, cost + c, [nv, path]))
% We use a stack to store all the to-explore nodes so that deeper nodes will be explored first. We need 
% to report the path to the node and the cost of the path, so we combine the cost and path with the node
% and store them together as a "search_node". In the prolog program we provide, we also use a fact 
% search_node(node, cost, [path]). to represent the item we store in the stack.
% To make sure visited nodes are not explored again, we use Visited to store all explored nodes in the prolog
% program.
dfs(Day, Start, Goal, Path, Cost) :-
    depth_first_search(Day, Goal, [], [search_node(Start, 0, [Start])|_], Path, Cost), !.
depth_first_search(_, Goal, _, [search_node(Goal, Cost, Path)|_], Path, Cost).
depth_first_search(Day, Goal, Visited, [search_node(CurNode, CurCost, CurPath)|Stack], Path, Cost) :-
    neighbors(Day, CurNode, Neighbors), % get all neighbors of CurNode.
    excludeL(Neighbors, [CurNode|Visited], NewNodes), % exclude visited nodes from Neighbors, CurNode is included in the visited nodes.
    generate_cost_list(CurNode, CurCost, NewNodes, NewCosts),
    generate_path_list(CurPath, NewNodes, NewPaths),
    generate_search_node_list(NewNodes, NewCosts, NewPaths, NewSearchNodesList),
    append(NewSearchNodesList, Stack, NewStack), % insert new search nodes at the head of the original stack.
    depth_first_search(Day, Goal, [CurNode|Visited], NewStack, Path, Cost).

% Breadth-first search (BFS) is yet another algorithm for searching tree/graph. The algorithm starts at the starting node
% and explores all of the neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.
% The pseudo-code of BFS is shown below.
% procedure BFS(G(V, E), Start, Goal)
% 	 let Q be a Queue
% 	 Lable Start as visited
%    Q.push(search_node(Start, 0, [Start]))
%    while Q is not empty do
%        search_node(node, cost, [path]) = Q.dequeue()
%        if node is Goal then
%        	return cost, path
%        for all edges edge(v, nv, c) in E do
%        	if nv is not visited then
%        		label nv as visited
%        		Q.enqueue(search_node(nv, cost + c, [nv, path]))
% In stead of the stack used in DFS, we use a FIFO queue to store all the to-explore nodes so that nodes with smaller depth 
% will be explored first.
bfs(Day, Start, Goal, Path, Cost) :- 
    breadth_first_search(Day, Goal, [Start], [search_node(Start, 0, [Start])|_], Path, Cost), !.

breadth_first_search(_, Goal, _, [search_node(Goal, Cost, Path)|_], Path, Cost).
breadth_first_search(Day, Goal, Visited, [search_node(CurNode, CurCost, CurPath)|Queue], Path, Cost) :-
    neighbors(Day, CurNode, Neighbors), % get all neighbors of CurNo
    excludeL(Neighbors, Visited, NewNodes), % exclude visited nodes from Neighbors, CurNode is excluded in the visited nodes.
    append(Visited, NewNodes, NewVisited), % makr CurNode as visited.
    generate_cost_list(CurNode, CurCost, NewNodes, NewCosts),
    generate_path_list(CurPath, NewNodes, NewPaths),
    generate_search_node_list(NewNodes, NewCosts, NewPaths, NewSearchNodesList),
    append(Queue, NewSearchNodesList, NewQueue), % append new search nodes to the end of the original queue.
    breadth_first_search(Day, Goal, NewVisited, NewQueue, Path, Cost).


initial_pq(PQ) :-
    findall(N, node(N), Nodes),
    lengthL(Nodes, Length),
    repeatL(9999, Length, CostL),
    repeatL([], Length, PathL),
    generate_search_node_list(Nodes, CostL, PathL, PQ).

% Dijkstra Algorithm is an algorithm for finding the shortest path between nodes in a graph. Both BFS and DFS algorithm cannot
% guarantee the path returned is the one with smallest cost. In this project, you only need to implement a simply version
% of the algorithm that finds a shortest path between the Start and the Goal nodes. The pseudo code is shown below.
% procedure Dijkstra(G(V, E), Start, Goal)
% 	Let PQ be a Priority_Queue
% 	for each node n in V do
% 		if n is not Start then
% 			PQ.decrease_priority(search_node(node, +INF, []), +INF)
% 	PQ.add_with_priority(search_node(Start, 0, [Start]), 0)
% 	while PQ is not empty do
% 		search_node(node, cost, [path]) = PQ.extract_min()
% 		label node as visited
% 		if node is Goal then
% 			return cost, path
%       for all edges edge(v, nv, c) in E do
%       	if nv is not visited then
%        		PQ.decrease_priority(search_node(nv, cost + c, [nv, path]), cost + c)
% Dijkstra algorithm needs to maintain a priority queue while using the cost stored in a search node as the prioirty key.
% In the prolog program, we use an array to implement the priority queue data structure. (The most common data structure
% used to implement a priority queue is the heap, but here this will make things complicated.) There are two predicators 
% associated with the priority queue, get_min_from_pq(PQ, SearchNode) that SearchNode is the search node with minimum cost
% in the priority queue. update_pq(SearchNodesList, PQ, NewPQ). SearchNodeList is a list of search node. If the search node 
% in the list has a smaller cost than the one in the priority queue, we will decrease the cost of the search node in the 
% priority queue.
dijkstra(Day, Start, Goal, Path, Cost) :-
    initial_pq(PQ), % initialize the priority queue that contains all nodes with cost +INF and an empty path.
    update_pq([search_node(Start, 0, [Start])], PQ, NewPQ), % Start node has 0 cost and a path with itself.
    dijkstra(Day, Goal, [], NewPQ, Path, Cost), !.
dijkstra(_, Goal, _, PQ, Path, Cost) :- get_min_from_pq(PQ, search_node(Goal, Cost, Path)).
dijkstra(Day, Goal, Visited, PQ, Path, Cost) :- 
    get_min_from_pq(PQ, search_node(CurNode, CurCost, CurPath)), % get the search node with minimum cost from the pq.
    deleteL(search_node(CurNode, CurCost, CurPath), PQ, NewPQ1), % delete this search node from the pq.
    neighbors(Day, CurNode, Neighbors),
    excludeL(Neighbors, [CurNode|Visited], NewNodes),
    generate_cost_list(CurNode, CurCost, NewNodes, NewCosts),
    generate_path_list(CurPath, NewNodes, NewPaths),
    generate_search_node_list(NewNodes, NewCosts, NewPaths, NewSearchNodesList),
    update_pq(NewSearchNodesList, NewPQ1, NewPQ2), % this is like the "decrease_key" operations, only search node has larger cost will update its cost and path.
    dijkstra(Day, Goal, [CurNode|Visited], NewPQ2, Path, Cost).

% =============== main predicator ================== %

navigate(Day, Start, Goal, Method, Path, Cost) :- 
    node(Start), node(Goal), day(Day), % Invalid methods will fail at compile time.
    call(Method, Day, Start, Goal, Path, Cost).
    

       


















