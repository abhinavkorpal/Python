#!/bin/py

unsearched = deque([starting_node])

def breath_first_search(unsearched):
    node = unsearched.popleft()
    for m in gen_moves(node):
        if is_goal(m):
           return m
        unsearched.append(m)
