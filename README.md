# Repositorio template para un workshop en RIIAA '120

Este repositorio de github contiene material para un workshop plantilla dentro de la [RIIAA '20](www.riiaa.org). Para utilizarlo en tu propio taller, sigue a la siguiente sección. Nunca has usado github o markdown o jupyter/colab?
Hay muchas guías en línea para usar estas tecnologías, algunas recomendaciones:
* Github: https://guides.github.com/activities/hello-world/.
* Markdown: https://guides.github.com/features/mastering-markdown/.
* Jupyer notebooks: https://jupyter.org/, https://nbviewer.jupyter.org/github/jupyter/notebook/tree/master/docs/source/examples/Notebook/, https://colab.research.google.com.

Mas dudas?, escríbele a los organizadores :) o pon un [github issue](https://help.github.com/en/articles/creating-an-issue).

## Cómo usarlo para mi propio taller?

1. Crea tu propio [github repo](https://help.github.com/en/articles/create-a-repo).
2. Clona este [repo](https://help.github.com/en/articles/cloning-a-repository).
3. Copia los archivos a tu repo, elimina los archivos que no sean necesario (hay algunos de ejemplo).
4. Edita y llena el repo con datos/código/notebooks y un README.md especifico para tu taller.

## Organización del repositorio

La estructura está inspirado en una versión lite de [cookie cutter data science project](https://drivendata.github.io/cookiecutter-data-science/):

* **data/**: folder de datos para tu taller. Es recomendable enfocarse en un dataset o dos durante el workshop (vs varios), asi los talleristas podrán profundizar en aspectos específico de los datos y después enfocar su atención a la parte algorítmica/teoria del taller.
* **code/**: funciones de utilidad para usar en los notebooks.
* **notebook/**: jupyter notebooks que se pueden lanzar en colab. Enumera los notebook en orden de uso.
* **media/**: imagenes para usar en tus notebooks y repo.
* **environment.yml**: archivos anaconda para replicar el software stack localmente.
* **README.md**: archivo markdown de entrada para la pagina y tu taller.

## Mejoras? sugerencias?
Manda un [pull request](https://help.github.com/en/articles/about-pull-requests), lo evaluaremos, empezaremos una discusion y si es buena idea lo incorporaremos.

## Instrucciones para estudiantes

**Las siguientes instrucciones se pueden copiar**.

La mayoría de las prácticas de los talleres se desarrollarán en Python 3.7+ usando la biblioteca [Tensorflow 2.0](https://www.tensorflow.org/), que adopta [Keras](https://www.tensorflow.org/versions/r2.0/api_docs/python/tf/keras) como interfaz de alto nivel para construir y entrenar redes neuronales.

Cosas para preparar
* Una laptop.
* Este repositorio de GitHub clonado y actualizado antes del taller.
* Un sentido aventurero en los datos.
* Un ambiente Python 3.7+ con Anaconda (ver opciones 1 y 2 abajo).

Los talleres serán impartidos usando *notebooks* de Jupyter, documentos con código ejecutable, texto, ecuaciones, visualizaciones, imágenes y demás material. Los *notebooks* se pueden crear y ejecutar en la nube vía Google Colab (opción 1) o de manera local en tu computadora a través de [Jupyter Notebooks](https://jupyter.org/) (opción 2).

### Opcion 1: Google Colab
[Colab](https://colab.research.google.com) es un servicio de Google para ejecutar *notebooks* en la nube. Provee ambientes de Python 2 y 3 con CPUs, GPUs y TPUs. ¡Y es gratis! Solo necesitas tener una cuenta de Google o crear una.

Recomendamos que elijas un ambiente con Python 3 y GPU. Para activarlo:
* Abre el menú `Entorno de ejecución`
* Elige la opción `Restablecer todos los entornos de ejecución...` .
* Vuelve a abrir `Entorno de ejecución`
* Elige `Cambiar tipo de entorno de ejecución`
* Selecciona Python 3 como `Tipo de ejecución` y GPU de la lista de `Acelerador por hardware`

La siguiente captura de pantalla ilustra este proceso.

![](media/escoge_acelerador.png)

En [Colab](https://colab.research.google.com) puedes crear un nuevo *notebook*, subir uno existente desde tu computadora o importarlo de Google Drive o GitHub.

### Opcion 2: Ambiente local
Para tener la versión de Python 3.7+ y todas las bibliotecas instaladas en cualquier plataforma, recomendamos que uses [**Anaconda**](https://www.anaconda.com/) y generes un ambiente con el archivo `environment.yml` de este repositorio usando una terminal y el comando:

```
conda env create -n riiaa19 -f environment_cpu.yml
```

Cambia el nombre `riia19` por tu nombre favorito para el ambiente. Si cuentas con un GPU Nvidia y deseas aprovecharlo cambia el archivo `environment_cpu.yml` a `environment_gpu.yml`.

Para activar el ambiente que creaste, en una terminal ingresa el comando

```
conda activate riiaa19
```

Una vez activado, puedes ejecutar la aplicación de Jupyter Notebook

```
jupyter notebook
```

Este comando abrirá una pestaña o ventana en tu navegador web, como se muestra en la siguiente captura de pantalla:

![](media/jupyter_notebook.png)

Al igual que en Google Colab, puedes crear un nuevo *notebook* seleccionando el botón `New` y posteriormente `Python 3`. De forma alternativa, puedes abrir uno existente seleccionando el archivo del *notebook* (con extensión `.ipynb`) dentro del directorio donde ejecutaste Jupyter Notebook. Con el botón `Upload` agregas archivos que se encuentran en otra parte de tu computadora a este directorio. Para cerrar Jupyter Notebook, presiona el botón `Quit` y posteriormente cierra la pestaña o ventana de tu navegador web.

Para desactivar el ambiente `riiaa19` de Anaconda simplemente haz

```
conda deactivate
```
