import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import control 
import numpy as np


naranja_fuerte_codigo_de_colores='#EEA006'
naranja_claro_codigo_de_colores='#FCEAC7'

def ajusta_el_retardo_segun_el_input_de_la_ventana(t_orig,y_orig,retardo):
   
    m=np.array([0])
    t=np.concatenate([m,t_orig+retardo])
    y=np.concatenate([m,y_orig])
    return t,y

def leer_datos_de_la_ventana():
    
    global G_inicial_sin_datos_externos,Gcreada,s,p1,p2,p3,k,deslizadera_tiempo,retardo

    s=control.tf('s')
    p1=p1_objeto.variable.get()
    p2=p2_objeto.variable.get()
    p3=p3_objeto.variable.get()
    k=k_objeto.variable.get()
    factor_de_amortiguamiento=factor_de_amortiguamiento_objeto.variable.get()
    frec_natural=frec_natural_objeto.variable.get()
    deslizadera_tiempo=deslizadera_tiempo_objeto.variable.get()
    retardo=retardo_objeto.variable.get()
    b=b_objeto.variable.get()
    polos_complejos_habilitados=polos_comp_sel.get()
    
    if polos_complejos_habilitados==1:
        frec_natural_objeto.deslizadera.configure(state='normal',bg=naranja_fuerte_codigo_de_colores)
        factor_de_amortiguamiento_objeto.deslizadera.configure(state='normal',bg=naranja_fuerte_codigo_de_colores)
        Gcreada=(k*(1+b*s))/((1+p1*s)*(1+p2*s)*(1+p3*s)*(1+((2*factor_de_amortiguamiento*s)/frec_natural))+((1*s**2)/frec_natural**2))
    
    else: 
        frec_natural_objeto.deslizadera.configure(state='disabled',bg='gray')
        factor_de_amortiguamiento_objeto.deslizadera.configure(state='disabled',bg='gray')
        Gcreada=(k*(1+b*s))/((1+p1*s)*(1+p2*s)*(1+p3*s))   
        
    G_inicial_sin_datos_externos= 8/(3+4*s+2*s**2)
    graficado()
    
def graficado():
    
    
    fig.clf()
    
    t_deslizadera_ajustada=np.linspace(0.0,deslizadera_tiempo, num=1000)
    t,y=control.step_response(Gcreada,T=(t_deslizadera_ajustada))   
    t_fin,y_fin=ajusta_el_retardo_segun_el_input_de_la_ventana(t,y,retardo)
    if usar_datos_experimentales==0:
        t_ini,y_ini=control.step_response(G_inicial_sin_datos_externos,T=(t_deslizadera_ajustada))     
        fig.add_subplot(111).plot(t_ini,y_ini)
    if usar_datos_experimentales==1:
        fig.add_subplot(111).plot(t_experimental,y_experimental)
        
    fig.add_subplot(111).plot(t_fin, y_fin)
    error=np.zeros(len(y))
    for i in range(len(y)):
        error[i]=np.absolute(y_fin[i]-y_ini[i])
        if np.around(y_ini[i],2)==np.around(k_objeto.variable.get(),2):
            np.delete(error,i)
    error_final=np.mean(error)
    error_por_pantalla.configure(text=round(error_final,3))
    canvas.draw()  

def recibir_datos_fichero():
    
    global t_experimental,y_experimental,usar_datos_experimentales
    
    ty_experimentalJuntas=np.loadtxt('datos.txt')
    t_experimental=ty_experimentalJuntas[:,0]
    y_experimental=ty_experimentalJuntas[:,1]
    usar_datos_experimentales=1
    leer_datos_de_la_ventana()
    
class Deslizadera:

    def __init__(self,master,texto,valor_inicial,valor_maximo,valor_minimo):
        
        self.dmin=valor_minimo
        self.dmax=valor_maximo
        self.master=master
        self.variable=tk.DoubleVar()
        self.variable.set(valor_inicial)
        self.deslizadera=tk.Scale(master,variable=self.variable,from_=self.dmin,to=self.dmax,orient=tk.HORIZONTAL,label=texto,resolution=0.001,length=400,bg=naranja_fuerte_codigo_de_colores,troughcolor='black')
        self.deslizadera.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
        self.deslizadera.bind("<ButtonRelease-1>",self.update)
        
    def update(self,event):
  
        if self.variable.get()==0:        
            self.dmax=self.dmax/2
            self.deslizadera.configure(to=self.dmax)
            
        if self.variable.get() >= (self.dmax-self.dmax/1000):            
            self.dmax=self.dmax*2
            self.deslizadera.configure(to=self.dmax)
        
        if self.dmax < 10:          
            self.deslizadera.configure(resolution=(self.dmax/1000))
            
        leer_datos_de_la_ventana()
                  
usar_datos_experimentales=0
ventana= tk.Tk()
ventana.wm_title("Calculo de parametros una f.d.t")
ventana.configure(bg=naranja_claro_codigo_de_colores)
frame_canvas=tk.Frame(ventana,bg=naranja_claro_codigo_de_colores)
frame_botones=tk.Frame(ventana,bg=naranja_claro_codigo_de_colores)
frame_deslizaderas=tk.Frame(ventana,bg=naranja_claro_codigo_de_colores)

frame_canvas.grid(row=1, column=1)
frame_botones.grid(row=0, column=0)

frame_deslizaderas.grid(row=1,column=0)

fig = Figure(figsize=(7, 7), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_canvas)  
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)

label_complejos=tk.Label(master=frame_botones,text='Polos complejos',bg=naranja_fuerte_codigo_de_colores,relief='solid')
label_complejos.grid(row=0,column=0)

polos_comp_sel=tk.IntVar()
polos_comp_sel.set(1)
boton_polos_complejos_no=ttk.Radiobutton(master=frame_botones,variable=polos_comp_sel,value=0,command=leer_datos_de_la_ventana)
boton_polos_complejos_si=ttk.Radiobutton(master=frame_botones,variable=polos_comp_sel,value=1,command=leer_datos_de_la_ventana)


label_complejos_no=tk.Label(master=frame_botones,text='No',bg=naranja_claro_codigo_de_colores)
label_complejos_si=tk.Label(master=frame_botones,text='Si',bg=naranja_claro_codigo_de_colores)
label_complejos_no.grid(row=0,column=3)
label_complejos_si.grid(row=0,column=1)
boton_polos_complejos_no.grid(row=0,column=4)
boton_polos_complejos_si.grid(row=0,column=2)

error_label=tk.Label(master=frame_botones,bg=naranja_fuerte_codigo_de_colores,text='Error medio entre puntos de las graficas',relief='solid')
error_por_pantalla=ttk.Label(master=frame_botones,text='0',relief='solid')
error_label.grid(row=2,column=0)
error_por_pantalla.grid(row=2,column=2)

boton_datos_fichero = tk.Button(frame_deslizaderas, text="Cargar datos Y(t) y t de un fichero",command=recibir_datos_fichero,bg=naranja_fuerte_codigo_de_colores)
boton_datos_fichero.pack(side=tk.BOTTOM)


deslizadera_tiempo_objeto=Deslizadera(frame_canvas,"Tiempo de visualizacion",40,100,0) 
retardo_objeto=Deslizadera(frame_deslizaderas,"retardo",0,5,0)  
factor_de_amortiguamiento_objeto=Deslizadera(frame_deslizaderas,"ξ",0,5,0)      
frec_natural_objeto=Deslizadera(frame_deslizaderas,"ωn",0.1,5,0.0001)      
b_objeto=Deslizadera(frame_deslizaderas,"B",0,5,0)        
p3_objeto=Deslizadera(frame_deslizaderas,"p3",0,10,0)  
p2_objeto=Deslizadera(frame_deslizaderas,"p2",0,10,0) 
p1_objeto=Deslizadera(frame_deslizaderas,"p1",1,10,0)      
k_objeto=Deslizadera(frame_deslizaderas,"k",1,30,0)




ventana.mainloop()