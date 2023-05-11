import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
#we set the map up as a (2n + 1) x (2n + 1) grid 
#to set walls differently

class Node:
    def __init__(self, x, y, prev, found = False):
        self.x = x
        self.y = y 
        self.prev = prev
        self.found = found
    
    def is_edge(self):
        x = self.x 
        y = self.y 

        if x <= 0 or x >= mazecoord(14) + 1:
            return True 
        if y <= 0 or y >= mazecoord(14) + 1:
            return True

        return False

    def get_prev(self):
        return self.prev

    def set_found(self):
        self.found = True

    def get_pos(self):
        return (self.x, self.y)

    def set_prev(self, prev):
        self.prev = prev
    
    def get_found(self):
        return self.found
    
def plot_maze(array):

    array[mazecoord(7)][mazecoord(7)] = 0.5
    plt.imshow(array,cmap='magma')
    #plt.imshow(new,cmap='gray')
    plt.title("Maze")
    plt.show(block = False)

def mazecoord(x):
    return 2*x + 1

def create_maze(filename):
    df = pd.read_csv(filename)

    n = 15
    size = (2*n + 1, 2*n + 1)
    maze = np.zeros(size)
    for index, row in df.iterrows():
        x = row['x']
        y = row['y']
        maze[mazecoord(y) - 1][mazecoord(x)] = row['top']
        maze[mazecoord(y)][mazecoord(x) + 1] = row['right']
        maze[mazecoord(y) + 1][mazecoord(x)] = row['bottom']
        maze[mazecoord(y)][mazecoord(x) - 1] = row['left']
    
    return maze

def maze_to_node(maze):
    n = 15
    output = [[]]
    index = 0

    for y in range(mazecoord(15)):
        for x in range(mazecoord(15)):
            output[index].append(Node(x, y, None))
        output.append([])
        index += 1
  
    return output

def BFS(maze):

    queue = []
    nodemaze = maze_to_node(maze)
    current = nodemaze[mazecoord(7)][mazecoord(7)]
    current.set_found()
    x, y = current.get_pos()
    update_queue(nodemaze, queue, x, y, current)
    prev = current

    i = 0
    while len(queue) > 0:
        
        current = queue.pop(0)
        prev = current
        x, y = current.get_pos()
        
        if maze[y][x] == 0 and not current.get_found():
            current.set_found()
            update_queue(nodemaze, queue, x, y, current)
            if current.is_edge():
                return current 
        
    return None 
        

def update_queue(maze, queue, x, y, prev):
    if not maze[y][x + 1].get_found():
        queue.append(maze[y][x + 1])
        maze[y][x+1].set_prev(prev)
    
    if not maze[y][x - 1].get_found():
        queue.append(maze[y][x-1])
        maze[y][x-1].set_prev(prev)

    if not maze[y + 1][x].get_found():
        queue.append(maze[y + 1][x])
        maze[y + 1][x].set_prev(prev)

    if not maze[y -1 ][x].get_found():
        queue.append(maze[y - 1][x])
        maze[y -1 ][x].set_prev(prev)

def visualise_path(maze, path):
    newmaze = copy.deepcopy(maze)
    for x,y in path:
        newmaze[y][x] = 0.5
        plot_maze(newmaze)
        plt.pause(0.01)
    plt.pause(3)

def main():
    filename = 'Maps/maze_1.csv'
    maze = create_maze(filename)
    #plot_maze(maze)
    out = BFS(maze)
    if out is None:
        print("False")
        exit()
    else:
        print("True")

    current = out

    path_found = []
    while current != None:
        path_found.append(current.get_pos())
        current = current.get_prev()

    path_found.reverse()
    visualise_path(maze, path_found)

if __name__ == '__main__':
    main()