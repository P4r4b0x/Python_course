import random
import itertools
import numpy as np
from PIL import Image

def get_neighbors(N, tuple, periodic):
    sublist = [[], []]
    if periodic:
        for s in range(2):
            if tuple[s] == N - 1:
                sublist[s] = [tuple[s] - 1, tuple[s], 0]
            else:
                sublist[s] = [tuple[s] - 1, tuple[s], tuple[s] + 1]
    else:
        for s in range(2):
            sublist[s] = [tuple[s] + k for k in [-1, 0, 1] if tuple[s] + k not in [-1, N]]
    neighbors = list(itertools.product(*sublist))
    neighbors.remove(tuple)
    return neighbors


compute_more = 3


def CONWAY(startgrid, K, N, filename, periodic):
    if not periodic:
        N += 2 * compute_more
        for k in range(N - 2 * compute_more):
            for l in range(compute_more):
                startgrid[k].insert(0, 0)
                startgrid[k].append(0)
        for k in range(compute_more):
            startgrid.insert(0, [0 for i in range(N)])
            startgrid.append([0 for i in range(N)])

    neighborlist = [[get_neighbors(N, (i, j), periodic) for j in range(N)] for i in range(N)]
    frames = []
    frames.append(startgrid)
    for time in range(K - 1):
        #print(time)
        frames.append([])
        for i in range(N):
            frames[time + 1].append([])
            for j in range(N):
                alife = frames[time][i][j]
                newlife = 0
                neighbors = neighborlist[i][j]
                number = sum(frames[time][a][b] for (a, b) in neighbors)
                if (alife and number == 2) or number == 3:
                    newlife = 1
                frames[time + 1][i].append(newlife)
    if not periodic:
        N -= 2 * compute_more
        print(frames[0])
        for frame in frames:
            for k in range(compute_more):
                frame.pop(0)
                frame.pop(-1)
            for i in range(N):
                for k in range(compute_more):
                    frame[i].pop(0)
                    frame[i].pop(-1)
        print(frames[0])
    gif = []
    for time in range(K):
        #print(time)
        gif.append(Image.fromarray(np.asarray(dtype=np.dtype('uint8'),
                                              a=[[255 - 255 * frames[time][i][j] for j in range(N)] for i in range(N)]),
                                   mode='L'))
    gif[0].save(filename, format='GIF', append_images=gif[1:], save_all=True, duration=50, loop=0)

N = 300
startgrid = [[random.choices([1, 0], [0.5, 0.5])[0] for i in range(N)] for j in range(N)]
K = 200
filename = "conway.gif"
CONWAY(startgrid, K, N, filename, True)




