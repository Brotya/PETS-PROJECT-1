# maze_solver.py
from collections import deque

def solve_maze(maze):
    rows = len(maze)
    cols = len(maze[0])
    
    start = None
    end = None
    
    # Step 1: Scan the maze to find the Start (S) and End (E) coordinates
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
                
    if not start or not end:
        return "Maze must have an 'S' and an 'E'."

    # Step 2: Setup BFS
    # Queue stores tuples of: (current_row, current_col, path_taken_so_far)
    queue = deque([(start[0], start[1], [])]) 
    
    # Visited set keeps track of (row, col) so we don't go backwards
    visited = set()
    visited.add(start)
    
    # Directions: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Step 3: Run BFS loop
    while queue:
        r, c, path = queue.popleft()
        
        # If we reached the End, return the path taken + the end coordinate itself
        if (r, c) == end:
            return path + [(r, c)]
            
        # Check all 4 possible directions
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc
            
            # Ensure the next step is inside the maze bounds
            if 0 <= next_r < rows and 0 <= next_c < cols:
                # Ensure the next step is NOT a wall ('1') and NOT visited
                if maze[next_r][next_c] != '1' and (next_r, next_c) not in visited:
                    visited.add((next_r, next_c))
                    # Append new position to queue, and add current node to the path history
                    queue.append((next_r, next_c, path + [(r, c)]))
                    
    return None # Returns None if no escape route exists

def print_solved_maze(maze, path):
    """Helper function to print the maze with the escape route marked by '*'"""
    if not path:
        print("No solution found!")
        return
        
    # Create a deep copy of the maze so we don't overwrite the original
    solved_maze = [list(row) for row in maze]
    
    # Mark the path with '*' (skipping S and E for visual clarity)
    for r, c in path:
        if solved_maze[r][c] not in ['S', 'E']:
            solved_maze[r][c] = '*'
            
    print("\n--- Maze Solved! ---")
    for row in solved_maze:
        print(" ".join(row))


# ==========================================
# Testing the Maze Solver
# ==========================================
if __name__ == "__main__":
    # 0 = Path, 1 = Wall, S = Start, E = End
    my_maze = [
        ['S', '0', '1', '0', '0'],
        ['1', '0', '1', '0', '1'],
        ['0', '0', '0', '0', '0'],
        ['0', '1', '1', '1', '0'],
        ['0', '0', '0', '1', 'E']
    ]

    print("--- Original Maze ---")
    for row in my_maze:
        print(" ".join(row))

    # Run BFS algorithm
    shortest_path = solve_maze(my_maze)
    
    # Print the visually solved maze
    print_solved_maze(my_maze, shortest_path)
    
    # Print the exact coordinate steps
    print(f"\nExact Coordinate Path:\n{shortest_path}")