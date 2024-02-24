import Main
import math
from tkinter.ttk import *
from tkinter import *

model = 'models/teapot.obj'
model_2 = 'models/cube.obj'

renderer = Main.gl(1920,1080, 55, 1000, 0.1)
teapot_1 = Main.object(model,-4.5,-1,0,0,45,180, 1, 1, 1, '#0000ff')
teapot_2 = Main.object(model,4.5,-1,0,0,315,180, 1, 1, 1, '#ff0000')
cube = Main.object(model_2,0,0,0,0,35,0, 1, 1, 1, None)

hwstr = str(renderer.width) + 'x' + str(renderer.height)
ar = int(renderer.height)/int(renderer.width)
renderer.camera_absolute(_camera_x = 0, _camera_y = 0, _camera_z = 10, _camera_angle_x = 0, _camera_angle_y = 0, _camera_angle_z = 0)


#init the window and viewport
master = Tk()
master.geometry(hwstr)
master.title("Cube demo")

frame = Frame(master, width = renderer.width, height=renderer.height, bg="black")
frame.focus_set()
frame.pack(anchor=SW, side=LEFT)
viewport = Canvas(frame, width=renderer.width, height=renderer.height)
viewport.pack(side=TOP)

renderer.view_style(False, 1, 0, 1, '', 0.2)

def loop():
    viewport.create_rectangle(0,0,renderer.width,renderer.height, fill=renderer.background_colour)
    triangles = renderer.new_frame()

    renderer.move_camera(_camera_angle_z = 0, _camera_angle_y=2)
    for tri in triangles:
        viewport.create_polygon([tri[0], tri[1], tri[2], tri[3], tri[4], tri[5]],outline=tri[-2], fill=tri[-1])
    master.after(5,loop)

master.after(1,loop)
master.mainloop()
