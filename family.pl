% Dynamic predicates
:- dynamic sister/2.
:- dynamic brother/2.
:- dynamic siblings/2.
:- dynamic grandmother/2.
:- dynamic grandfather/2.
:- dynamic mother/2.
:- dynamic father/2.
:- dynamic daughter/2.
:- dynamic son/2.
:- dynamic male/1.
:- dynamic female/1.
:- dynamic parent/2.
:- dynamic child/2.
:- dynamic aunt/2.
:- dynamic uncle/2.
:- dynamic person/1.
:- dynamic genderless/1.
:- dynamic cousin/2.

% Daughter Rule
daughter(X, Y) :- female(X), parent(Y, X).

% Son Rule
son(X, Y) :- male(X), parent(Y, X).

% Child Rule
child(X, Y) :- parent(Y, X).
child(X, Y) :- father(Y, X).
child(X, Y) :- mother(Y, X).
child(X, Y) :- daughter(X, Y).
child(X, Y) :- son(X, Y).

% Father Rule
father(X, Y) :- male(X), parent(X, Y).

% Mother Rule
mother(X, Y) :- female(X), parent(X, Y).

% Grandfather Rule
grandfather(X, Y) :- male(X), father(X, Z), (parent(Z, Y); mother(Z, Y); father(Z, Y)).

% Grandmother Rule
grandmother(X, Y) :- female(X), mother(X, Z), (parent(Z, Y); mother(Z, Y); father(Z, Y)).

% Siblings Rule
siblings(X, Y) :- (sister(X, Y); brother(X, Y); sister(Y, X); brother(Y, X)), X \= Y.
siblings(X, Y) :- (parent(Z, X); father(Z, X); mother(Z, X)), (parent(Z, Y); father(Z, Y); mother(Z, Y)), X \= Y.

% Sister Rule
sister(X, Y) :-
    female(X),
    (father(Z, X); mother(Z, X); parent(Z, X)),
    (father(Z, Y); mother(Z, Y); parent(Z, Y)),
    X \= Y.

% Brother Rule
brother(X, Y) :-
    male(X),
    (father(Z, X); mother(Z, X); parent(Z, X)),
    (father(Z, Y); mother(Z, Y); parent(Z, Y)),
    X \= Y.

% Aunt Rule
aunt(X, Y) :-
    female(X),
    sister(X, Z),
    (parent(Z, Y); mother(Z, Y); father(Z, Y)).
aunt(X, Y) :-
    sister(X, Z),
    child(Y, Z).

% Uncle Rule
uncle(X, Y) :- 
    male(X),
    brother(X, Z),
    (parent(Z, Y); mother(Z, Y); father(Z, Y)).
uncle(X, Y) :-
    brother(X, Z),
    child(Y, Z).

% Either Uncle or Aunt Rule
aunt_or_uncle(X, Y) :-
    siblings(X, Z),
    (parent(Z, Y); father(Z, Y); mother(Z, Y)).

% Cousin Rule
cousin(X, Y) :- 
    (parent(PX, X); mother(PX, X); father(PX, X)), (parent(PY, Y); mother(PY, Y); father(PY, Y)),
    (siblings(PX, PY); brother(PX, PY); sister(PX, PY)),
    X \= Y.

% Grandchild Rule
grandchild(X, Y) :- child(X, Z), (grandfather(Y, Z); grandmother(Y, Z)).

% Relatives Rule
relatives(X, Y) :- uncle(X, Y).
relatives(X, Y) :- aunt(X, Y).
relatives(X, Y) :- cousin(X, Y).
relatives(X, Y) :- grandfather(X, Y).
relatives(X, Y) :- grandmother(X, Y).
relatives(X, Y) :- siblings(X, Y).
relatives(X, Y) :- daughter(X, Y).
relatives(X, Y) :- son(X, Y).
relatives(X, Y) :- child(X, Y).
relatives(X, Y) :- parent(X, Y).
relatives(X, Y) :- father(X, Y).
relatives(X, Y) :- mother(X, Y).
relatives(X, Y) :- sister(X, Y).
relatives(X, Y) :- brother(X, Y).
relatives(X, Y) :- aunt_or_uncle(X, Y).