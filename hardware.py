import psutil
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter
import os.path

root_tk = tkinter.Tk()
root_tk.configure(bg='#333333')
root_tk.geometry("700x500")
root_tk.title("Home")
root_tk.resizable(width=False, height=False)
root_tk.update_idletasks()

width = root_tk.winfo_width()
screen_width = root_tk.winfo_rootx() - root_tk.winfo_x()
win_width = width + 2 * screen_width

height = root_tk.winfo_height()
screen_height = root_tk.winfo_rooty() - root_tk.winfo_y()
win_height = height + 2 * screen_height

y = root_tk.winfo_screenheight() // 2 - win_height // 2
x = root_tk.winfo_screenwidth() // 2 - win_width // 2

CPU_data, RAM_data, DISK_data = [], [], []

if os.path.isfile('hardware.txt'):
    print('File exists!')
else:
    open('hardware.txt', 'x')
    

def hardwareUsage(frame):
    file = open('hardware.txt', 'a')
    RAM = round(((psutil.virtual_memory().used//1024//1024)/(psutil.virtual_memory().total//1024//1024))*100, 2)
    CPU = psutil.cpu_percent()
    DISK = psutil.disk_usage('C:').percent

    CPU_data.append(CPU)
    RAM_data.append(RAM)
    DISK_data.append(DISK)

    ax.clear()
    ax.set_ylim(0, 100)
    ax.set_title('Hardware usage (%)')
    ax.bar('CPU', [CPU_data[-1]], color='red')
    ax.bar('RAM',[RAM_data[-1]], color='purple')
    ax.bar('DISK',[DISK_data[-1]], color='blue')

    file.write(f"{datetime.datetime.now().time().strftime('%H:%M:%S')} - CPU: {str(CPU)}%   RAM: {str(RAM)}%   DISK: {str(DISK)}%\n")
    file.close()
    
fig = Figure(figsize=(5, 5), dpi=100, facecolor='#333333')

ax = fig.add_subplot(111)
ax.set_facecolor('#333333')

canvas = FigureCanvasTkAgg(fig, master=root_tk)
canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=tkinter.YES)

anim = FuncAnimation(fig, hardwareUsage, interval=1000)

root_tk.geometry("{}x{}+{}+{}".format(width, height, x, y))
root_tk.deiconify()
root_tk.mainloop()