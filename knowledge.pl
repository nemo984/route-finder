cost(mrt_blue, N, Cost) :-
    ( N = 1, Cost = 16
    ; N = 2, Cost = 16
    ; N = 3, Cost = 19
    ; N = 4, Cost = 21
    ; N = 5, Cost = 23
    ; N = 6, Cost = 25
    ; N = 7, Cost = 28
    ; N = 8, Cost = 30
    ; N = 9, Cost = 32
    ; N = 10, Cost = 35
    ; N = 11, Cost = 37
    ; N = 12, Cost = 39
    ; N >= 13, Cost = 42
    ).

cost(mrt_purple, N, Cost) :-
    ( N = 1, Cost = 14
    ; N = 2, Cost = 17
    ; N = 3, Cost = 20
    ; N = 4, Cost = 23
    ; N = 5, Cost = 25
    ; N = 6, Cost = 27
    ; N = 7, Cost = 30
    ; N = 8, Cost = 33
    ; N = 9, Cost = 36
    ; N = 10, Cost = 38
    ; N = 11, Cost = 40
    ; N >= 12, Cost = 42
    ).

cost(bts, N, Cost) :-
    ( N = 1, Cost = 16
    ; N = 2, Cost = 16
    ; N = 3, Cost = 23
    ; N = 4, Cost = 26
    ; N = 5, Cost = 30
    ; N = 6, Cost = 33
    ; N = 7, Cost = 37
    ; N = 8, Cost = 40
    ; N >= 9, Cost = 44
    ).

all_paths(Start, End, Path) :-
    all_paths(Start, End, [], Path).

all_paths(Start, End, Visited, [Start|Visited]) :-
  % Base case: if the start node is the same as the end node, the path is just the start node.
  Start == End.

% Recursive case: if the start node is not the same as the end node, find a route from the start node to an adjacent node and continue the search from there.
all_paths(Start, End, Visited, AllPaths) :-
  % Find a route from the start node to an adjacent node.
  route(Start, Adjacent, _),
  % Make sure the adjacent node has not already been visited.
  \+ member(Adjacent, Visited),
  % Continue the search from the adjacent node.
  all_paths(Adjacent, End, [Start|Visited], AllPaths).

shortest_path(Start, End, SPath, Time, Cost, Stops) :-
  findall(Path, all_paths(Start, End, [], Path), Paths), % generate all paths
  shortest_list(Paths, MinPath), % find the path with minimum length
  reverse(MinPath, ShortestPath),
  delete(ShortestPath, sena_ruam, SPath),
  list_length(SPath, Length),
  Stops is Length - 1,
  compute_time(ShortestPath, Time),
  compute_cost(ShortestPath, Cost).

shortest_path(Start, End) :-
  findall(Path, all_paths(Start, End, [], Path), Paths), % generate all paths
  shortest_list(Paths, MinPath), % find the path with minimum length
  reverse(MinPath, SPath),
  compute_time(SPath, Time),
  compute_cost(SPath, Cost),
  format('Shortest path: ~w (total time: ~d minutes, cost: ~d baht)', [SPath, Time, Cost]).

shortest_list(L,S) :- aggregate(min(C,E),(member(E,L),length(E,C)),min(_,S)).

compute_cost(Path, Cost) :-
  head(Path, First),
  station(First, Type),
  compute_cost(Path, Type, 0, Cost).

compute_cost([], Type, Acc, Cost) :-
  cost(Type, Acc, TypeCost),
  Cost is TypeCost.

compute_cost([A|Rest], Type, Acc, Cost) :-
  station(A, CurrentType),
  ( CurrentType == Type ->
    NewAcc is Acc + 1,
    compute_cost(Rest, CurrentType, NewAcc, NewCost),
    Cost is NewCost
  ; cost(Type, Acc, TypeCost),
    compute_cost(Rest, CurrentType, 1, RestCost),
    Cost is TypeCost + RestCost
  ).

head([H|_], H).

compute_time([_], 0).
compute_time([A, B|Rest], Time) :-
  route(A, B, Time1),
  compute_time([B|Rest], Time2),
  Time is Time1 + Time2.

list_length([], 0 ).
list_length([_|Xs] , L ) :- list_length(Xs,N), L is N+1.

