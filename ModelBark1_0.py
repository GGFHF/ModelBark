'''
 Trabajo de Fin de Grado Álvaro Gutiérrez Climent 
 Un modelo matemático-computacional para estudiar la formación de cortezas de
 distinta tipología en especies leñosas.
 Director: Alvaro Soto de Viana Co-director: Juan Carlos Sanz Nuño
'''

# Importación de las librerias necesarias para el desarrollo del script.

import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Primera Parte: Creación de la clase Planta.


class Planta:
    '''
    Creación de las instancias de atributo en la clase Planta. También llamadas
    Variables de clase, estas se generan en el momento que se inicia la clase.
    '''
    def __init__(self):
        
        self.radio = [1]     # Condiciones iniciales del radio dentro del modelo.
        self.n = 0           # Número de felógenos.
        self.almacenamiento_xilema = [0]   # Almacenamiento parametro xilema.
        self.almacenamiento_floema = [0]   # Almacenamiento parametro floema.
        self.almacenamiento_felema = [0]   # Almacenamiento parametro felema.
        self.almacenamiento_floema_inactivo = [0] #Almacenamiento parametro floema inactivo
        self.almacenamiento_ecuacion = [1] # Almacenamiento parametro ecuación.
        self.lugar_primer_felogeno = 0     # Almacenamiento del lugar donde aparece el primer felógeno.


    '''
    Creación de las instancias de método en la clase Planta. Estas son las 
    funciones que modifican las instancias atributo. Dentro de un método se
    puede llamar a otro método.

    En primer lugar, se va a crear el método Dado. Genera un 0 o un 1 en función
    de una probabilidad T. Utiliza la función random_sample() de Numpy.
    '''

    def dado(self, T):
        sample = np.random.random_sample()
        dado = 0
        if (sample <= T):
            dado = 0
        if(sample > T):
            dado = 1
        return (int(dado))

    '''
     El método de División de Cambium Vascular importa al radio de las
     variables de clase, busca la posición del 1, y utilizando el método Dado,
     en función de una probabilidad, TCV: Tasa del Cambium Vascular, inserta
     en la variable de clase un 0 A la izquierda o derecha del 1 creando así
     el Xilema o Floema en cada iteración del modelo.
    '''

    def division_cambium_vascular(self, TCV):
        radio_imp = self.radio
        posicion_1 = radio_imp.index(1)
        dado = self.dado(float(TCV))
        if (dado == 0):
            radio_imp.insert(0, 0)
        if (dado == 1):
            radio_imp.insert(posicion_1+1, 0)
        self.radio = radio_imp

    '''
    El método de Creación del primer felógeno importa al radio, cambia el número
    de felógenos a 1, busca la posición del 1, crea 2 variables: la longitud
    del radio y la posición en la que se insertará el primer felógeno,
    (Longitud del radio - posición del 1 (Cambium Vascular)) * porcentaje dentro
    del floema, e insertará en la posición el Felógeno (2). También, se almacena
    en qué momento se crea el primer felógeno para la calibración de la 
    ecuación.
    '''

    def creacion_primer_felogeno(self, porcentaje):
        radio_imp = self.radio
        posicion_1 = radio_imp.index(1)
        longitud_radio = len(radio_imp)
        lugar_porcentaje = round((longitud_radio-posicion_1)*porcentaje)
        radio_imp.insert(longitud_radio-lugar_porcentaje, 2)
        self.radio = radio_imp
        self.lugar_primer_felogeno = len(radio_imp)
        self.n = 1

    '''
    El método de División del cambium Suberoso importa el radio y el número de
    felógenos de las variables de clase, busca la posición del 2, y utilizando
    el método dado con una probabilidad, TCS: Tasa de división del cambium
    suberoso, inserta a la derecha del 2 el número de felógenos + 2.
    '''

    def division_cambium_suberoso(self, TCS):
        radio_imp = self.radio
        n_imp = self.n
        posicion_2 = radio_imp.index(2)
        dado = self.dado(float(TCS))
        if (dado == 0):
            radio_imp.insert(posicion_2+1, (n_imp+2))
        self.radio = radio_imp

    '''
    El método de Creación de nuevo felógeno importa el radio de las variables
    de clase, busca tanto la posición del 1 como del 2, calcula donde se tiene
    que posicionar el nuevo felógeno (Posición del 2 -Posición del 1)*porcentaje
    cambia el antiguo 2 según el número de felógenos que haya creado n+2 e
    inserta el nuevo felógeno en la posición. Por último, actualiza el número de
    felógenos +1.
    '''

    def creacion_nuevo_felogeno(self, porcentaje):
        radio_imp = self.radio
        posicion_1 = radio_imp.index(1)
        posicion_2 = radio_imp.index(2)
        lugar_porcentaje = round((posicion_2-posicion_1)*porcentaje)
        radio_imp[posicion_2] = (self.n+2)
        radio_imp.insert(posicion_2-lugar_porcentaje, 2)
        self.n += 1
        self.radio = radio_imp

    '''
    El método Longitud devuelve la longitud del radio.
    '''

    def longitud(self):
        return(len(self.radio))

    '''
    El método Células del último felógeno devuelve el número de células que ha
    creado el último felógeno. Este método se utiliza para el calibrado de los
    parámetros de la ecuación.
    '''

    def celulas_ultimo_felogeno(self):
        radio_imp = self.radio
        n_imp = self.n
        return(int(radio_imp.count(n_imp+2)))

    '''
    El método número de células de xilema contabiliza el número de células de
    xilema que se encuentra en el radio. Para ello se busca la posición del
    cambium vascular (1).
    '''

    def numero_celulas_xilema(self):
        radio_imp = self.radio
        posicion_1 = radio_imp.index(1)
        return(posicion_1)

    '''
    El método número de células de floema contabiliza el número de células de
    floema que se encuentran en el radio. Si en el radio existe ya un felógeno,
    resta la posición del felógeno menos la posición del cambium vascular,
    y si en el radio no existe ningún felógeno calcula el número de 0's que hay
    en el vector y le resta la posición del cambium vascular.
    '''

    def numero_celulas_floema(self):
        radio_imp = self.radio
        if radio_imp.count(2) == 1:
            posicion_1 = radio_imp.index(1)
            posicion_2 = radio_imp.index(2)
            return(posicion_2-posicion_1-1)
        else:
            posicion_1 = radio_imp.index(1)
            return((radio_imp.count(0))-posicion_1)

    '''
    El método de numero de células de felema contabiliza el número de células
    de felema. Si no existe ningún felógeno, los contabiliza como 0, y si
    existe felógeno, calcula el numero de 0's y le resta la célula de cambium
    vascular y la de felógeno.
    '''

    def numero_celulas_felema(self):
        radio_imp = self.radio
        if radio_imp.count(2) == 0:
            return(0)
        else:
            numero_ceros = radio_imp.count(0)
            longitud_radio = len(radio_imp)
            return(longitud_radio-numero_ceros)

    '''
    El método de número de células de floema inactivo contabiliza el número de
    células de floema inactivo que se encuentran en el radio. Para ello se
    contabiliza el numero de 0's dentro del radio y se le resta el número de
    células de xilema y floema utilizando sus respectivos métodos.
    '''

    def numero_celulas_floema_inactivo(self):
        radio_imp = self.radio
        numero_ceros = radio_imp.count(0)
        celulas_xilema = self.numero_celulas_xilema()
        celulas_floema = self.numero_celulas_floema()
        return(numero_ceros-celulas_xilema-celulas_floema)

    '''
    El método de Parámetros unifica todos los parámetros de la ecuación, y los
    junta en una sola lista que más adelante será utilizada como input de la
    ecuación del modelo.
    '''

    def parametros(self):
        xilema = self.numero_celulas_xilema()
        floema = self.numero_celulas_floema()
        felema = self.numero_celulas_felema()
        floema_inactivo = self.numero_celulas_floema_inactivo()
        return([xilema, floema, felema, floema_inactivo])

    '''
    El método de Ecuación toma de entrada los valores de los parámetros de la
    función directamente desde la aplicación, y los parámetros a través del
    método parámetros.
    '''

    def ecuacion(self, A, B, C, D):
        parametros_radio = self.parametros()
        xilema_A = A * parametros_radio[0]
        floema_B = B * parametros_radio[1]
        felema_C = C * parametros_radio[2]
        floema_inactivo_D = D * parametros_radio[3]
        return((1+(felema_C)+(floema_inactivo_D))/(xilema_A + floema_B))

    '''
    El método de almacenamiento de parámetros para graficación almacena los
    parámetros de la ecuación, así como el resultado de la graficación en
    variables de clase, para que luego sea más fácil llegar a ellos.
    '''

    def almacenamiento_parametros_graficacion(self, A, B, C, D):
        self.almacenamiento_xilema.append(self.numero_celulas_xilema())
        self.almacenamiento_floema.append(self.numero_celulas_floema())
        self.almacenamiento_felema.append(self.numero_celulas_felema())
        self.almacenamiento_floema_inactivo.append(self.numero_celulas_floema_inactivo())
        self.almacenamiento_ecuacion.append(self.ecuacion(A, B, C, D))
    
    '''
    El método resultado unifica todos los resultados en un solo vector para
    optimizar la salida de los datos. Se crea una lista con la siguiente
    configuración: [Parámetro A, Parámetro B, Parámetro C, Parámetro D, 
                    Numero de felógenos, Lugar de creación del primer felógeno,
                    [radio]]
    '''
    
    def resultado(self, A, B, C, D):
        salida = self.parametros()
        salida.append(self.n)
        salida.append(self.lugar_primer_felogeno)
        salida.append(self.radio)
        return(salida)
    
    '''
    El método de graficación crea dos gráficas con la biblioteca MatplotLib.
    La primera representa como cambian las células de: xilema, floema, felema
    y floema inactivo en función del tiempo.
    Y la segunda cómo evoluciona la ecuación del modelo en función del tiempo.
    '''
    
    def graficacion(self, K):
        
        # Gráfica 1:
            
        plt.plot(self.almacenamiento_xilema, label = 'Xilema')
        plt.plot(self.almacenamiento_floema, label = 'Floema')
        plt.plot(self.almacenamiento_felema, label = 'Felema')
        plt.plot(self.almacenamiento_floema_inactivo, label = 'Floema Inactivo')
        plt.legend()
        plt.title("Representación de los parametros del modelo en el tiempo")
        plt.savefig('Figuras/grafica_parametros.jpg')
        plt.close()

        # Gráfica 2:

        plt.plot(self.almacenamiento_ecuacion, label='Ecuación')
        plt.axhline(y = K, color = 'r', linestyle = ':', label = 'K')
        plt.legend()
        plt.title("Representación de la función F(t) en el tiempo")
        plt.savefig('Figuras/grafica_ecuacion.jpg')
        plt.close()


# Segunda Parte: Creación de la función que se utilizará posteriormente el botón de la aplicación.

'''
En este apartado se establece el orden en el que se organizan los métodos para
la simulación dentro del modelo.
'''

def generacion_simulacion_planta(Nom, TCV, TCS, A, B, C, D, K, longitud_maxima):
    
    '''
    En primer lugar se crea el objeto Planta. Se realiza una primera división
    del cambium vascular. Y se guardan los parámetros para graficar mas
    adelante al terminar la simulacion.
    '''
    
    Nom = Planta()
    Nom.division_cambium_vascular(TCV)
    Nom.almacenamiento_parametros_graficacion(A, B, C, D)
    
    '''
    Una vez las condiciones iniciales se han establecido, se empieza a comprobar
    si la ecuación del modelo se cumple o no. Se comprueba con un bucle
    while. Siempre y cuando la ecuación este por encima del umbral de tensión
    K, se divide el cambium vascular. Este bucle tiene 2 maneras de romperse,
    o que se deje de cumplir la ecuación o que la longitud del radio sea
    máxima. 
    
    Si la longitud del radio es máxima inmediatamente se generan los 
    resultados con el método correspondiente.
    
    Y en el caso de que se rompa el bucle, pero la longitud del radio no sea
    la máxima, ya que la ecuación no se cumple, se crea el primer felógeno.
    '''
    
    while Nom.ecuacion(A, B, C, D) >= K:
        Nom.division_cambium_vascular(TCV)
        Nom.almacenamiento_parametros_graficacion(A, B, C, D)
        if Nom.longitud() >= longitud_maxima:
            break
    if Nom.longitud() >= longitud_maxima:
        Nom.graficacion(K)
        return(Nom.resultado(A, B, C, D))
    else:
        Nom.creacion_primer_felogeno(0.3)
        
        '''
        Una vez creado el primer felógeno se establece un esquema de dos bucles
        while anidados.
        En primer lugar, el primer bucle while establece la norma de que solo
        se realice el otro bloque siempre y cuando la longitud del radio sea
        menor a la longitud máxima de este.
        
        En cuanto al segundo while establece una doble condición para romper
        el bucle, si el valor de la ecuación es mayor que el valor del umbral
        K, y que la longitud del radio sea menor a la máxima.
        
        En el momento en el que se incumple ese bucle, se crea un nuevo felógeno
        siempre y cuando la longitud del radio sea menor que la longitud máxima
        y se vuelve a iniciar el primer bucle while.
        '''
        
        while Nom.longitud() <= longitud_maxima:
            while Nom.ecuacion(A, B, C, D) >= K and Nom.longitud() <= longitud_maxima:
                Nom.division_cambium_vascular(TCV)
                Nom.division_cambium_suberoso(TCS)
                Nom.almacenamiento_parametros_graficacion(A, B, C, D)
            if Nom.longitud() <= longitud_maxima:
                Nom.creacion_nuevo_felogeno(0.3)
                Nom.division_cambium_vascular(TCV)
            else:
                break
        
        '''
        Por último, se utiliza el método graficación para exportar las gráficas
        con los parámetros y la función devuelve la lista creada con los
        parámetros establecidos en el método resultado.
        '''
        
        Nom.graficacion(K)
        return(Nom.resultado(A, B, C, D))
    
#Tercera Parte: Configuración de la interfaz de usuario y aplicación.

'''
En este apartado, se configura la interfaz de usuario, así como la estética
de la aplicación. Para esta interfaz se utiliza principalmente la librería
dedicada a este tipo de funciones llamada Tkinter.

En primer lugar, se crea la ventana principal. Tamaño de la ventana, color del
fondo, geometría y el título de esta.
'''

menu_principal = tk.Tk()
menu_principal.configure(bg='white')
menu_principal.geometry('1360x250')
menu_principal.title('Universidad Politécnica de Madrid - Departamento de Sistemas y Recursos Naturales')

'''
A continuación se configura todo el texto que se encuentra dentro del menú
principal.
'''

tk.Label(menu_principal, text = "    Un modelo matemático-computacional para " + 
         "estudiar la formación de cortezas de distinta tipología en especies leñosas",
         bg='white',font = ('Bahnschrift SemiBold Condensed',18)).place(x=70,y=0)
tk.Label(menu_principal, text = "Autor: Álvaro Gutiérrez Climent   " + 
         "Director: Alvaro Soto de Viana   Director: Juan Carlos Sanz Nuño",
         bg='white').place(x=400,y=45)
tk.Label(menu_principal,text='L',bg='white').place(x=1025,y=100)
tk.Label(menu_principal,text='K',bg='white').place(x=900,y=100)
tk.Label(menu_principal,text='D',bg='white').place(x=780,y=100)
tk.Label(menu_principal,text='C',bg='white').place(x=660,y=100)
tk.Label(menu_principal,text='B',bg='white').place(x=530,y=100)
tk.Label(menu_principal,text='A',bg='white').place(x=410,y=100)
tk.Label(menu_principal,text='TCS',bg='white').place(x=276,y=100)
tk.Label(menu_principal,text='Nombre del Radio',bg='white').place(x=115,y=100)
tk.Label(menu_principal,text='Combinaciones',bg='white').place(x=860,y=160)
tk.Label(menu_principal,text='Iteraciones',bg='white').place(x=1000,y=160)
tk.Label(menu_principal,text='Nombre Archivo Entrada',bg='white').place(x=400,y=160)
tk.Label(menu_principal,text='Nombre Archivo Salida',bg='white').place(x=650,y=160)


# Configuración de los WIDGETS  de entrada

Nombre = tk.Entry(menu_principal,bg='pale green',width=12)
TCS = tk.Entry(menu_principal,bg='pale green',width=12)
A = tk.Entry(menu_principal,bg='pale green',width=12)
B = tk.Entry(menu_principal,bg='pale green',width=12)
C = tk.Entry(menu_principal,bg='pale green',width=12)
D = tk.Entry(menu_principal,bg='pale green',width=12)
K = tk.Entry(menu_principal,bg='pale green',width=12)
L = tk.Entry(menu_principal,bg='pale green',width=12)
numero_combinaciones = tk.Entry(menu_principal,bg='pale green',width=12)
numero_iteraciones_combinaciones = tk.Entry(menu_principal,bg='pale green',width=12)
nombre_entrada = tk.Entry(menu_principal,bg='pale green',width=27)
nombre_salida = tk.Entry(menu_principal,bg='pale green',width=27)

Nombre.place(x=123,y=125)
TCS.place(x=246,y=125)
A.place(x=369,y=125)
B.place(x=492,y=125)
C.place(x=615,y=125)
D.place(x=738,y=125)
K.place(x=861,y=125)
L.place(x=984,y=125)
numero_combinaciones.place(x=861,y=185)
numero_iteraciones_combinaciones.place(x=984,y=185)
nombre_entrada.place(x=369,y=185)
nombre_salida.place(x=615,y=185)

# Cofiguración de los parámetros por defecto

TCS.insert(0,0.054)
A.insert(0,0.016)
B.insert(0,0.008)
C.insert(0,0.3)
D.insert(0,0.002)
K.insert(0,1)
L.insert(0,1000)

'''
Configuración de la función del botón Ejecutar de la interfaz de usuario.
'''

def BotonEjecutar():
    
    # Entrada de los datos de los espacios de entrada
    
    Nombre_get = Nombre.get()
    TCS_get = TCS.get()
    A_get = A.get()
    B_get = B.get()
    C_get = C.get()
    D_get = D.get()
    K_get = K.get()
    L_get = L.get()
    Comprobador = bool()
    
    # Creación del mensaje de error si no introduces bien los parámetros.
    try:
        TCS_get = float(TCS_get)
        A_get = float(A_get)
        B_get = float(B_get)
        C_get = float(C_get)
        D_get = float(D_get)
        K_get = float(K_get)
        L_get = int(L_get)
        Comprobador = True
    except:
        
        error = tk.Toplevel()
        error.configure(bg='white')
        error.geometry('330x50')
        tk.Label(error,text = "Error al introducir los datos dentro de la ecuación",
                  bg = "white").place(x=10,y=15)
        error.mainloop()
        
    # Si no existe ningún fallo dentro de la introducción de los datos    
        
    if Comprobador == True:
        
        #Recoger los parámetros de los botones y ejecutar la función
        
        Text = [Nombre_get,TCS_get,A_get,B_get,C_get,D_get,K_get,L_get]
        Ejecutable = generacion_simulacion_planta(Text[0],0.9,Text[1],Text[2],Text[3],Text[4],Text[5],Text[6],Text[7])
        
        #Creación del mapa de calor
        
        lista = Ejecutable[6]
        res = [(max(Ejecutable[6])+1) if item == 1 else item for item in lista]
        Mapadecalor = np.array(res)
        Mapadecalor = np.expand_dims(Mapadecalor,axis=0)
        plt.figure(figsize= (14,1.8))
        plt.imshow(Mapadecalor, aspect='auto',cmap='YlOrBr')
        plt.axis('on')
        plt.title("Representación del Radio")
        plt.savefig('Figuras/grafica_mapadecalor.jpg')
        plt.close()
        
        # Configuración de la ventana emergente Titulo 
        
        Solu = tk.Toplevel()
        Solu.configure(bg='white')
        Solu.geometry('1360x800')
        Solu.title('Universidad Politécnica de Madrid - Departamento de Sistemas y Recursos Naturales')
        
        
        tk.Label(Solu, text = "    Un modelo matemático-computacional para estudiar"+
                 " la formación de cortezas de distinta tipología en especies leñosas",
          bg='white',font = ('Bahnschrift SemiBold Condensed',18)).place(x=70,y=0)
        tk.Label(Solu, text = "Autor: Álvaro Gutiérrez Climent   Director: Alvaro Soto de Viana "+
                 "  Director: Juan Carlos Sanz Nuño",bg = 'white').place(x=400,y=50)
        
        #Configuración del Mapa de calor
        
        MapaImag = Image.open("Figuras/grafica_mapadecalor.jpg")
        MapaImagph = ImageTk.PhotoImage(MapaImag)
        tk.Label(Solu,image=MapaImagph,bg='white').place(x=400,y=100)
        
        #Configuración del texto de las estadísticas
        
        tk.Label(Solu, text = "Estadísticas del radio", bg = "white",font=('*font',12,'bold')).place(x=100,y=90)
        tk.Label(Solu,text = f"Nombre de la simulación: {Text[0]}", bg = "white").place(x=60,y=120)
        tk.Label(Solu,text = "Parámetros de entrada de la simulación:", bg = "white").place(x=60,y=150)
        tk.Label(Solu,text = "Tasa de división del cambium vascular: 0.9", bg = "white").place(x=70,y=175)
        tk.Label(Solu,text = f"Tasa de división del cambium suberoso: {Text[1]}", bg = "white").place(x=70,y=200)
        tk.Label(Solu,text = f"Valor del parámetro A: {Text[2]}", bg = "white").place(x=70,y=225)
        tk.Label(Solu,text = f"Valor del parámetro B: {Text[3]}", bg = "white").place(x=70,y=250)
        tk.Label(Solu,text = f"Valor del parámetro C: {Text[4]}", bg = "white").place(x=70,y=275)
        tk.Label(Solu,text = f"Valor del parámetro D: {Text[5]}", bg = "white").place(x=70,y=300)
        tk.Label(Solu,text = f"Valor del parámetro K: {Text[6]}", bg = "white").place(x=70,y=325)
        tk.Label(Solu,text = f"Longitud del Radio: {Text[7]}", bg = "white").place(x=70,y=350)
        tk.Label(Solu,text = "Parametros de salida de la simulación:", bg = "white").place(x=60,y=380)
        tk.Label(Solu,text = f"Células totales de xilema: {Ejecutable[0]}", bg = "white").place(x=70,y=405)
        tk.Label(Solu,text = f"Células totales de floema: {Ejecutable[1]}", bg = "white").place(x=70,y=430)
        tk.Label(Solu,text = f"Células totales de felema: {Ejecutable[2]}", bg = "white").place(x=70,y=455)
        tk.Label(Solu,text = f"Células totales de floema inactivo: {Ejecutable[3]}", bg = "white").place(x=70,y=480)
        tk.Label(Solu,text = f"Número de felógenos creados: {Ejecutable[4]}", bg = "white").place(x=70,y=505)
        tk.Label(Solu,text = f"Momento en el que se crea el primer felógeno: {Ejecutable[5]}", bg = "white").place(x=70,y=530)
        tk.Label(Solu,text = "Vector del radio", bg = "white",font=('*font',10,'bold')).place(x=600,y=550)
        
        #Configuración del texto del radio
        
        TextodelRadio = tk.Text(Solu,height = 10, width=135, wrap = 'word')
        TextodelRadio.insert('end', Ejecutable[6])
        TextodelRadio.place(x=70,y=580)
        
        
        #Configuración del grafico de los parámetros
        
        ParaImag = Image.open("Figuras/grafica_parametros.jpg")
        ParaImagph = ImageTk.PhotoImage(ParaImag)
        tk.Label(Solu,image=ParaImagph,bg='white').place(x=470,y=250)
        
        #Configuración del gráfico de la ecuación
        
        EcImag = Image.open("Figuras/grafica_ecuacion.jpg")
        EcImagph = ImageTk.PhotoImage(EcImag)
        tk.Label(Solu,image=EcImagph,bg='white').place(x=915,y=250)
        
        #Activar la ventana
        
        Solu.mainloop()
        
        

'''
Configuración de la función de ejecución múltiple dentro de la interfaz de usuario.
'''
def boton_ejecutar_multiple():
    
    #Leer los parámetros de entrada dentro de la interfaz
    
    numero_combinaciones_get = numero_combinaciones.get()
    numero_iteraciones_combinacion_get = numero_iteraciones_combinaciones.get()
    nombre_entrada_get = nombre_entrada.get()
    nombre_salida_get = nombre_salida.get()

    # Creación del mensaje de error si no introduces bien los parámetros.
    try:
        numero_combinaciones_get = int(numero_combinaciones_get)
        numero_iteraciones_combinacion_get = int(numero_iteraciones_combinacion_get)
        nombre_entrada_get = str(nombre_entrada_get)
        nombre_salida_get = str(nombre_salida_get)
        Comprobador = True
        
    except:
        
        error = tk.Toplevel()
        error.configure(bg='white')
        error.geometry('200x50')
        tk.Label(error,text = "Error al introducir los datos", bg = "white").place(x=10,y=15)
        error.mainloop()
    
    if Comprobador == True:
        
        # Si todos los parámetros de entrada están bien introducidos introducir los
        # datos dentro de la función.
        
        nombre_archivo_entrada = f'{nombre_entrada_get}.csv'
        
        nombre_archivo_salida = f'{nombre_salida_get}.csv'
        
        InputConditions = pd.read_csv(nombre_archivo_entrada, header = None)
        
        # Creación de la función para generar todas las simulaciones.
        
        def generacion_multiple(numero_combinaciones_generacion,numero_iteraciones_combinacion_generacion):
            R=[]
            Col=[]
            for i in range(0,numero_combinaciones_generacion):
                print(f'Running iteration n: {i+1}')
                for j in range(0,numero_iteraciones_combinacion_generacion):
                    R.append(generacion_simulacion_planta("R", 
                              0.9, 
                              InputConditions.iloc[i,0],
                              InputConditions.iloc[i,1],
                              InputConditions.iloc[i,2],
                              InputConditions.iloc[i,3],
                              InputConditions.iloc[i,4],
                              InputConditions.iloc[i,5],
                              1000))
             
            for k in range(0,numero_combinaciones_generacion):
                for l in range(0,numero_iteraciones_combinacion_generacion):
                    Col.append([str(f"C{k}"),InputConditions.iloc[k,0],
                              InputConditions.iloc[k,1],
                              InputConditions.iloc[k,2],
                              InputConditions.iloc[k,3],
                              InputConditions.iloc[k,4],
                              InputConditions.iloc[k,5],])
                             
            Nombres=["Nx","Nph","Nf","Nphi","Nfel","TPFel","radio"]
            Nombres2=["Comb","TCS","A","B","C","D","K"]
            Resultados2 = pd.DataFrame(Col,columns=Nombres2)
            Resultados = pd.DataFrame(R,columns=Nombres)
            Resultados3 = pd.concat([Resultados2,Resultados],axis=1)
            Resultados3['Nf/Nfel']=Resultados3['Nf']/Resultados3['Nfel']
            Resultados3=Resultados3[["Comb","TCS","A","B","C","D","K","Nx","Nph","Nf","Nphi","Nfel","TPFel",'Nf/Nfel',"radio"]]
            Resultados3.to_csv(nombre_archivo_salida,index=False)
            
        # Se llama a la función creada con los parámetros que coge de la interfaz
        # de usuario.
            
        generacion_multiple(numero_combinaciones_get,numero_iteraciones_combinacion_get)
        

# Configuración de los botones

Ejecutar = tk.Button(menu_principal,text='Ejecutar',width=13,command=BotonEjecutar).place(x=1107,y=118)
ejecutar_multiple = tk.Button(menu_principal,text='Ejecutar Múltiple',width=13,command=boton_ejecutar_multiple).place(x=1107,y=180)

#Activación del menu principal

menu_principal.mainloop()