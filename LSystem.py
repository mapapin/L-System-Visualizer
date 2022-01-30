import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import json
import sys
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (40, 55, 71)
YELLOW = (248, 196, 113)

class LSystem():
    def __init__(self, axiom, rules):
        self.sequence = axiom
        self.rules = rules

    def updateSystem(self):
        newSequence = ""
        for i in range(len(self.sequence)):
            if self.sequence[i] in self.rules:
                newSequence += self.rules[self.sequence[i]]
            else: newSequence += self.sequence[i]
        self.sequence = newSequence
    
    def __str__(self):
        return self.sequence

class Visualizer():
    def __init__(self, width, height, x, y, angle, lineSize, maxDepth, axiom, rules):
        self.w = width
        self.h = height
        self.x = x
        self.y = y
        self.angle = math.pi / 2
        self.deltaAngle = angle
        self.lineSize = lineSize
        self.RUN = True
        self.stack = []
        self.maxDepth = maxDepth
        self.initSystem(axiom, rules)
        self.initPygame()
        self.winLoop()

    def initSystem(self, axiom, rules):
        self.Lsys = LSystem(axiom, rules)

    def initPygame(self):
        pygame.init()
        self.win = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('L-System Visualizer')
        self.win.fill(BACKGROUND)
        pygame.display.update()

    def drawSystem(self, depth):
        x = self.x
        y = self.y
        angle = self.angle
        sentence = self.Lsys.__str__()
        color = YELLOW
        for char in sentence:
            if (char != '+' and char != '-' and char != '[' and char != ']'):
                x2 = x - (self.lineSize / math.exp(depth / 5)) * math.cos(angle)
                y2 = y - (self.lineSize / math.exp(depth / 5)) * math.sin(angle)
                pygame.draw.line(self.win,
                                (color[0], color[1], color[2], 100),
                                (x, y), (x2, y2), width=1)
                x = x2
                y = y2
            elif (char == '+'):
                angle += self.deltaAngle
            elif (char == '-'):
                angle -= self.deltaAngle
            elif (char == '['):
                self.stack.append(
                    {'x': x, 'y': y, 'angle': angle})
            elif (char == ']'):
                save = self.stack.pop()
                x = save['x']
                y = save['y']
                angle = save['angle']
            color = ((color[0] + depth * 2) % 255, color[1], color[2])

    def winLoop(self):
        depth = 1
        while self.RUN:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.RUN = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if (depth < self.maxDepth):
                            self.win.fill(BACKGROUND)
                            self.drawSystem(depth)
                            self.Lsys.updateSystem()
                            depth += 1
                            pygame.display.update()
            except KeyboardInterrupt:
                self.RUN = False
        pygame.quit()
        exit()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Not enough arguments. try : python3 LSystem.py path/parameters.json')
        exit()
    try:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f'\n{e}\n')
        exit(1)
    vis = Visualizer(data['width'], data['height'], data['x'], data['y'],
                     math.radians(data['angle']), data['size'], data['maxDepth'],
                     data['axiom'], data['rules'])
