def dias(fecha1,fecha2):
    años1=int(fecha1[6:10])
    años2=int(fecha2[6:10])
    meses1=int(fecha1[3:5])
    meses2=int(fecha2[3:5])
    dias1=int(fecha1[0:2])
    dias2=int(fecha2[0:2])
    if años1==años2 and meses1==meses2 and dias1==dias2:
        t_dias=0
    elif años1==años2 and meses1==meses2:
        t_dias=abs(dias1-dias2)
    elif años1==años2:
        dm1=abs((30*(meses1-1)+dias1))
        dm2=abs((30*(meses2-1)+dias2))
        t_dias=abs(dm1-dm2)
    else:
        dm1=abs((30*(meses1-1)+dias1))
        dm2=abs((30*(meses2-1)+dias2))
        t_dias1=abs(dm1-dm2)
        t_años=abs(años1-años2)
        da=365*t_años
        t_dias=da+t_dias1
    return t_dias

print(dias("15/12/1999","16/12/1997"))