import pandas as pd
import matplotlib.pyplot as plt
# uso esta funcion para pasar a entero el campo que esta en formato texto
def integer(texto):
    try : 
        return int(texto)
    except:
        #uso el retorno de 0 para salvar inconsistencia en los datos
        return 0     
#Para poder segmentar el lugar la funcion devuelve un valor para indiicar el lugar donde ocurrio      
def valor_lugar(lugar):
    if lugar == "Redes Sociales":
        return 1
    elif lugar == "Vivienda de la Víctima":
        return 2
    elif lugar == "Vivienda del Agresor":
        return 3
    else :
        return 0
# para poder segmentar si se hiso la denuncia la funcion devuelve un valor
def valor_judicial(judicial):
    if judicial == "NO":
        return 1
    elif judicial == "SI" :
        return 2
    else: 
        return 3   
df = pd.read_csv("llamados-atendidos-abuso-sexual-2023.csv")
df.dropna()
#paso a entero las edades de las victimas y los llamantes y los guardo en un vuevo campo del dataFrame
df["edad_del_llamante"]=df["llamante_edad"].apply(integer)
df["edad_de_la_victima"]=df["victima_edad"].apply(integer)
df_victimas_adolescentes = df[(df["edad_de_la_victima"]<25) & (df["edad_de_la_victima"]>12)]
df_victimas_en_la_ninies = df[(df["edad_de_la_victima"]<13) & (df["edad_de_la_victima"]>-1)]
plt.show()
#En caso de querer graficar la edad de una vicitma en especial usar estas lineas comentadas
#df_victima_adolescente_15 = df_victimas_adolescentes.query('edad_de_la_victima == 15')
#df_victima_adolescente_15.plot(kind="scatter", x="edad_del_llamante", y="edad_de_la_victima")
#print(df_victima_adolescente_15.head())
df_victimas_en_la_ninies.plot(kind="scatter", x="edad_del_llamante", y="edad_de_la_victima")
plt.title("Correlación de la edad del llamante \n y de las victimas de en la niñes")
plt.show()
df_victimas_adolescentes.plot(kind="scatter", x="edad_del_llamante", y="edad_de_la_victima")
plt.title("Correlación entre la edad del llamante \n y el de la victima adolescente")
plt.show()
df_victimas_en_la_ninies_segmento =df_victimas_en_la_ninies[["edad_del_llamante","edad_de_la_victima","llamado_region","llamante_vinculo","vs_grooming","vs_obligacion_sacarse_fotos_pornograficas","hecho_lugar","caso_judicializado"]]
df_victimas_en_la_ninies_segmento = df_victimas_en_la_ninies_segmento[df_victimas_en_la_ninies_segmento['vs_obligacion_sacarse_fotos_pornograficas'] == "SI"]

print(df_victimas_en_la_ninies_segmento.head())
#Creamos nuevo campo y damos valor a los datos para poder agruparlos
df_victimas_en_la_ninies_segmento["lugar"]= df_victimas_en_la_ninies_segmento["hecho_lugar"].apply(valor_lugar)
df_victimas_en_la_ninies_segmento["hecho_juzgado"]=df_victimas_en_la_ninies_segmento["caso_judicializado"].apply(valor_judicial)
print(df_victimas_en_la_ninies_segmento[["edad_de_la_victima","llamante_vinculo","hecho_lugar","lugar","hecho_juzgado","caso_judicializado"]])

print(df_victimas_en_la_ninies_segmento.describe())
eti=["Redes Sociales","Casa de la victima","Casa del agresor"]
#segmentamos por lugar del hecho
lugar_hecho = df_victimas_en_la_ninies_segmento["lugar"]
redes = 0 
victima = 0 
agresor = 0
for hecho in lugar_hecho :
    if hecho == 1 :
        redes+=1
    elif hecho == 2 :
        victima+=1
    else:
        agresor+=1
conteo_lugar_hecho =[redes, victima, agresor]
#uso el parametro explode=(0.1,0,0) para resaltar el lugar donde ocurre 
plt.pie(conteo_lugar_hecho,labels=eti, autopct="%0.1f %%", explode=(0.1,0,0))
plt.axis("equal")
plt.title("Lugar donde ocurrio el hecho")
plt.show()
# segmentamos para saver si el hecho fue denunciado. 
hecho_denunciado = df_victimas_en_la_ninies_segmento["hecho_juzgado"]
si = 0 
no = 0 
nc = 0
for hecho in hecho_denunciado :
    if hecho == 1 :
        no+=1
    elif hecho == 2 :
        si+=1
    else:
        nc+=1
conteo_hecho =[no,si,nc]
etiqueta =["NO","SI","N/NC"]
# uso explode=(0.1,0,0) para resaltar que el hecho no fue denunciado. 
plt.pie(conteo_lugar_hecho,labels=etiqueta, autopct="%0.1f %%", explode=(0.1,0,0))
plt.axis("equal")
plt.title("Hecho denunciado")
plt.show()

# comenzamos la misma segmentacion para adolescentes 
df_victimas_adolescentes_segmento =df_victimas_adolescentes[["edad_del_llamante","edad_de_la_victima","llamado_region","llamante_vinculo","vs_grooming","vs_obligacion_sacarse_fotos_pornograficas","hecho_lugar","caso_judicializado"]]
df_victimas_adolescentes_segmento = df_victimas_adolescentes_segmento[df_victimas_adolescentes_segmento['vs_obligacion_sacarse_fotos_pornograficas'] == "SI"]
df_victimas_adolescentes_segmento["lugar"]= df_victimas_adolescentes_segmento["hecho_lugar"].apply(valor_lugar)
df_victimas_adolescentes_segmento["hecho_juzgado"]= df_victimas_adolescentes_segmento["caso_judicializado"].apply(valor_judicial)

print(df_victimas_adolescentes_segmento.describe())
eti=["Redes Sociales","Casa de la victima","Casa del agresor"]
#segmentamos por lugar del hecho
lugar_hecho = df_victimas_adolescentes_segmento["lugar"]
redes = 0 
victima = 0 
agresor = 0
for hecho in lugar_hecho :
    if hecho == 1 :
        redes+=1
    elif hecho == 2 :
        victima+=1
    else:
        agresor+=1
conteo_lugar_hecho =[redes, victima, agresor]
#uso el parametro explode=(0.1,0,0) para resaltar el lugar donde ocurre 
#No se registro que el delito informado haya ocurrido en la casa del agresor pero se deja el código para su observacion.
plt.pie(conteo_lugar_hecho,labels=eti, autopct="%0.1f %%", explode=(0.1,0,0))
plt.axis("equal")
plt.title("Lugar donde ocurrio el hecho en perjuicio de adolescentes")
plt.show()
# segmentamos para saver si el hecho fue denunciado. 
hecho_denunciado = df_victimas_adolescentes_segmento["hecho_juzgado"]
si = 0 
no = 0 
nc = 0
for hecho in hecho_denunciado :
    if hecho == 1 :
        no+=1
    elif hecho == 2 :
        si+=1
    else:
        nc+=1
conteo_hecho =[no,si,nc]
etiqueta =["NO","SI","N/NC"]
# uso explode=(0.1,0,0) para resaltar que el hecho no fue denunciado. 
# Siempre se observo una respuesta por lo que N/NC esta en 0%
plt.pie(conteo_lugar_hecho,labels=etiqueta, autopct="%0.1f %%", explode=(0.1,0,0))
plt.axis("equal")
plt.title("Hecho denunciado cuando la victima es adolescente")
plt.show()

