def identificar(lista):
    resultado=[]
    repetidos=[]
    c=0
    for elemento in lista:
        if elemento not in resultado:
            resultado.append(elemento)
        elif c!=0 :
            resultado.remove(elemento)
            repetidos.append(elemento)
    return resultado,repetidos
lista=[7,5,7,9,6,3,4,3,8,9,4,2,3]
print(identificar(lista))


