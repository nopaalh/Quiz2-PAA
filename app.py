from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

WALL = "#"
FLOOR = "."
START = "P"
GOAL = "G"

def generalKruskalMap(width, height, loopProbability=0.3):
    maze = []
    sets = []
    edges = []
    
    for i in range(height):
        maze.append([])
        for j in range(width):
            isWall = not (i % 2 == 1 and j % 2 == 1)
            maze[i].append(WALL if isWall else FLOOR)
            
            if not isWall:
                sets.append([(i, j)])
                
            if i != height - 2 and not isWall:
                edges.append((i + 1, j))
                
            if j != width - 2 and not isWall:
                edges.append((i, j + 1))
                
    initialMap = [row[:] for row in maze]
    steps = []

    while edges:
        index = random.randint(0, len(edges) - 1)
        removed = edges.pop(index)
        
        iorj = removed[0] % 2
        
        if iorj:
            cell1 = (removed[0], removed[1] - 1)
            cell2 = (removed[0], removed[1] + 1)
        else:
            cell1 = (removed[0] - 1, removed[1])
            cell2 = (removed[0] + 1, removed[1])
            
        i1 = next((i for i, s in enumerate(sets) if cell1 in s), -1)
        i2 = next((i for i, s in enumerate(sets) if cell2 in s), -1)
        
        if i1 != i2:
            addSet = sets.pop(i2)
            if i2 < i1:
                i1 -= 1
            sets[i1].extend(addSet)
            maze[removed[0]][removed[1]] = FLOOR
            steps.append([removed[0], removed[1]])
        else:
            if random.random() < loopProbability:
                maze[removed[0]][removed[1]] = FLOOR
                steps.append([removed[0], removed[1]])
                
    return {
        "initialMap": initialMap,
        "steps": steps,
        "finalMap": maze,
        "start": [0, 1],
        "goal": [height - 1, width - 2]
    }

def getRandomMapData(width=21, height=15):
    return generalKruskalMap(width, height, 0.3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generateMap')
def apiGenerateMap():
    width = request.args.get('width', default=21, type=int)
    height = request.args.get('height', default=15, type=int)
    
    width = max(5, width)
    height = max(5, height)
    
    mapData = getRandomMapData(width, height)
    return jsonify(mapData)

if __name__ == '__main__':
    app.run(debug=True)
