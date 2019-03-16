/* TASK:
  Create a set of Prolog rules which implement Wumpus World on a 5 by 5 space. 
  There can be any number of pits, one gold, and one Wumpus. 
  The player may be assumed to begin in the bottom left-hand square (1,1). 
  The code should be able to print out all possible solution paths. */

:- dynamic is_in_cave/1,([
  wumpus_world_size/1,
  wumpus_location/2,
  wumpus_health/1,
  maximal_depth/1,
  gold/2,
  pit/2,
  agent_arrows/1,
  agent_score/1
  ]).


/* initialize(World, Percept): initializes the our agent and Wumpus world 
 and returns the percept from square 1,1. */  

initialize(World, [Stench,Breeze,Glitter,no,no]) :-
  writeln("initialization began"),
  clear_world(),
  initialize_world(World),
  initialize_agent,
  stench(1, 1, Stench),
  breeze(1, 1, Breeze),
  glitter(1, 1, Glitter),
  assert(wumpus_world_size(5)),
  assert(maximal_depth(16)),
  writeln("initialization done").


/* wumpus_location(X,Y): the Wumpus is in square X,Y
 wumpus_health(H): H is 'dead' or 'alive'
 gold(X,Y): there is gold in square X,Y
 pit(X,Y): there is a pit in square X,Y */

clear_world() :-
  retractall(wumpus_world_size(_)),
  retractall(wumpus_location(_,_)),
  retractall(wumpus_health(_)),
  retractall(maximal_depth(_)),
  retractall(gold(_,_)),
  retractall(pit(_,_)).

initialize_world(World) :-
  World = possible,
  assert(wumpus_location(1,3)),
  assert(wumpus_health(alive)),
  assert(gold(2,3)),
  assert(pit(3,1)),
  assert(pit(3,3)),
  assert(pit(4,4)),
  assert(pit(5,2)).

initialize_world(World) :-
  World = impossible,
  assert(wumpus_location(3,2)),
  assert(wumpus_health(alive)),
  assert(gold(2,3)),
  assert(pit(3,1)),
  assert(pit(2,2)),
  assert(pit(1,3)),
  assert(pit(5,5)).

initialize_world(World) :-
  World = without_pits,
  assert(wumpus_location(3,2)),
  assert(wumpus_health(alive)),
  assert(gold(2,3)).


/* initialize_agent: agent is initially alive, destitute (except for one
   arrow), in grid 1,1 and facing to the right (0 degrees). */

initialize_agent :-
  retractall(agent_arrows(_)),
  retractall(agent_score(_)),
  assert(agent_arrows(1)),
  assert(agent_score(0)).


/* decrement_score: subtracts one or given number from agent's score */

decrement_score(N) :-
  retract(agent_score(S)),
  S1 is S - N,
  assert(agent_score(S1)).

decrement_score :-
  decrement_score(1).


/* stench(X, Y, Stench): Stench = yes if wumpus (dead or alive) is in a square
 directly up, down, left, or right of the given location. */

stench(X, Y, yes) :-
  X1 is X + 1,  X0 is X - 1,
  Y1 is Y + 1,  Y0 is Y - 1,
  ( 
    wumpus_location(X1,Y);
    wumpus_location(X0,Y);
    wumpus_location(X,Y1);
    wumpus_location(X,Y0);
    wumpus_location(X,Y)
  ),
  !.

stench(_, _, no).


/* breeze(X, Y, Breeze): Breeze = yes if a pit is in a square directly up, down,
 left, or right of the current agent location. */

breeze(X, Y, yes) :-
  X1 is X + 1, X0 is X - 1,
  Y1 is Y + 1, Y0 is Y - 1,
  ( 
    pit(X1,Y);
    pit(X0,Y);
    pit(X,Y1);
    pit(X,Y0);
    pit(X,Y)
  ),
  !.

breeze(_, _, no).


/* glitter(X, Y, Glitter): Glitter = yes if there is gold in the given location. */

glitter(X, Y, yes):-
  gold(X, Y), !.

glitter(_, _, no).


/* wumpus(X, Y, Wumpus): Wumpus = yes if there is Wumpus in the given location. */

wumpus(X, Y, yes):-
  wumpus_location(X, Y), !.

wumpus(_, _, no).


/* kill_wumpus: kills wumpus and makes changes in KB */

kill_wumpus :-
  retract(wumpus_health(alive)),
  assert(wumpus_health(dead)).


/* Utility predicates for algorithm part */

neighbor(up, X, Y, Xnew, Ynew) :-
  Xnew is X, Ynew is Y + 1. % up

neighbor(right, X, Y, Xnew, Ynew) :-
  Xnew is X + 1, Ynew is Y. % right

neighbor(down, X, Y, Xnew, Ynew) :-
  Xnew is X, Ynew is Y - 1. % down

neighbor(left, X, Y, Xnew, Ynew) :-
  Xnew is X - 1, Ynew is Y.  % left

is_in_cave(X, Y) :-
  wumpus_world_size(N),
  1 =< X, X =< N,
  1 =< Y, Y =< N.

coordinates([H, M|_], X, Y) :-
  X = H,
  Y = M.  


/*Starting predicate*/

start() :-
  start(possible).

start(World) :-
  initialize(World, _),
  writeln("start to walk"),
  walk(1, 1, 1, []).


/* Algorithm predicates */

walk(X, Y, _, _) :-
  not(is_in_cave(X, Y)).

walk(_, _, Depth, _) :-
  maximal_depth(Max_depth),
  Depth = Max_depth.
  %writeln("max depth walk").

walk(X, Y, _, Visited) :-
  glitter(X, Y, yes),
  append(Visited, [[X, Y]], VisitedNew),
  writeln("We reached the goal " + VisitedNew).

walk(X, Y, _, _) :-
  wumpus(X, Y, yes).
  %writeln("wumpus walk" + X + Y).  

walk(X, Y, _, _) :-
  pit(X, Y).
  %writeln("pit walk" + X + Y). 

walk(X, Y, Depth, Visited) :-  
  maximal_depth(MaxDepth),
  Depth \== MaxDepth,

  append(Visited, [[X, Y]], VisitedNew),  %appending current cell to list of Visited
  DepthNew is Depth + 1, %increasing depth
  
  %Generating all neighbors
  neighbor(up, X, Y, X1, Y1),
  neighbor(right, X, Y, X2, Y2),
  neighbor(down, X, Y, X3, Y3),
  neighbor(left, X, Y, X4, Y4),
  Neighbors = [[X1,Y1], [X2,Y2], [X3,Y3], [X4,Y4]],

  %writeln([X,Y]+Depth+VisitedNew), %used for debugging

  forall(member(Z, Neighbors), ( 
        coordinates(Z, Xnew, Ynew),
        (
          member(Z, VisitedNew); % already visited
          walk(Xnew, Ynew, DepthNew, VisitedNew) % or visit now
        )
        )).