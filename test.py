from vpython import *

box1 = box(pos=vec(-5,0,0), size=vec(0.5,0.25,0.25), color=color.yellow, make_trail=True, trail_type="points", interval=10)

a = vec(1, 0, 0)
v = vec(0, 0, 0)
x = vec(-5, 0, 0)
dt = 0.01

t = 0
while t < 5:
    rate(100)
    x += v*dt + 0.5*a*dt**2
    v += a*dt
    box1.pos = x
    t += dt
