# «informesmultiformato»

Programa para generar descripciones de archivos, pensado para un formato muy específico. Solo usando parámetros, primero los momentos temporales separados por signos de suma, luego un doble guión bajo, después los nombres de los sitios separados por signos de suma, para cada sitio entre paréntesis un subtitulo opcional, y al final si hay etiquetas una coma con la inicial de las etiquetas. Ejemplo:
> python3 app.py 2023-10-12_10.58.51+2023-10-26_23.06.06+2023-11-03_17.25.13__Dloow.com+Tsubit.com(Anuncio y cierre de Tsubit)+Fantemti.up.railway.app+Devox.me,r.mp4 2023-10-12_10.58.51+2023-10-26_23.06.06+2023-11-03_17.25.13__Dloow.com+Tsubit.com(Anuncio y cierre de Tsubit)+Fantemti.up.railway.app+Devox.me,r.txt

Los archivos de texto pueden tener contenido y eso se agrega a la descripción, de lo contrario solo sale lo del nombre de archivo. 
