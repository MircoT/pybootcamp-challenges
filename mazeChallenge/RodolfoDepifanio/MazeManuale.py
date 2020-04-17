import tkinter as tk
import mazeClient
import json

def Navigatore(event): # chiamata da tastiera
    if event.keysym == 'Escape':
        root.destroy()
        mazeClient.send_command(command.EXIT)
    else:
        temp = event.keysym
        if temp == 'Up':
            action = command.MOVE_RIGHT
        elif temp == 'Right':
            action = command.MOVE_UP
        elif temp == 'Left':
            action = command.MOVE_DOWN
        elif temp == 'Down':
            action = command.MOVE_LEFT
        else:
            action = command.GET_STATE
            temp = 'Non valido'
        print(temp)
        res = json.loads(mazeClient.send_command(action))
        Mappa_Colori = Assegnatrice_Colori(res,n)
        for i in range(n):
            for j in range(n):
                c.itemconfig(rect[i,j],fill=Mappa_Colori[i][j])

def Conversione_Colori(val):
    if val == 32:
        val = 'white'
    elif val == 66:
        val = 'blue'
    elif val == 71:
        val = 'green'
    else:
        val = 'red'
    return val

def Assegnatrice_Colori(res,n): # Funzioni per la definizione della mappa di colori
    x = [res['userX'],res['userY']]
    Colori = [['black','black','black'],['black','black','black'],['black','black','black']] #[['black']*n]*n
    Colori[1][1] = Conversione_Colori(res['userVal'])
    for i in res['Neighbors']:
        x_s = [i['x'],i['y']]
        temp = [-x[0]+x_s[0]+1,-x[1]+x_s[1]+1]
        # print({'x':temp,'c':i['val']})
        Colori[temp[0]][temp[1]] = Conversione_Colori(i['val'])
    return Colori
  
command = mazeClient.Commands
res = json.loads(mazeClient.send_command(command.GET_STATE))
Mappa_Colori = Assegnatrice_Colori(res,3)
# Parte grafica ==> inizializzo
root = tk.Tk()
root.title("Maze Manuale") 
root.geometry('300x300')
D = 300
n = 3
d = D/n
rect = {}
c = tk.Canvas(root,height = D,width=D)
for i in range(n):
    for j in range(n):
        rect[i,j] = c.create_rectangle(i*d,j*d,(i+1)*d,(j+1)*d,fill=Mappa_Colori[i][j])
k = 0.2
c.create_oval(d*(n//2+k),d*(n//2+k),(n//2+1-k)*d,(n//2+1-k)*d,fill='grey') 
c.pack()
root.bind('<KeyRelease>', Navigatore)
root.mainloop()
