import tkinter as tk
from tkinter.colorchooser import askcolor

def set_color():
    global brush_color
    color = askcolor()[1]
    if color:
        brush_color = color
    
def paint(event):
    global last_x , last_y
    if last_x and last_y:
       canvas.create_line(last_x,last_y, event.x, event.y, fill = brush_color,
       width = brush_size, capstyle= tk.ROUND, smooth = True)
    last_x , last_y = event.x, event.y
    
def reset_position(event):
    global last_x , last_y
    last_x, last_y = None, None
       
    
    
def clear_canvas():
    canvas.delete('all')

window = tk.Tk()
window.title('Mini Çizim Programı')

brush_color = 'black'
brush_size = 8

last_x, last_y = None, None


canvas = tk.Canvas(window,bg='white', width=2000,height=700)
canvas.pack()

canvas.bind('<B1-Motion>', paint)
canvas.bind('<ButtonRelease-1>', reset_position)


color_button = tk.Button(window, text= 'Renk seç', command = set_color)
color_button.pack(side= tk.LEFT)

clear_button = tk.Button(window, text='Temizle', command = clear_canvas)
clear_button.pack(side = tk.LEFT)

window.mainloop()

    