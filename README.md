# Práctica de Ray Tracing

O siguiente comando instalará os paquetes necesarios de acordo co ficheiro de configuración [requirements.txt](requirements.txt).

```bash
pip install -r requirements.txt
```

E este comando executará o código en [raytracing.py](raytracing.py), xerando a imaxe [scene.png](images/scene.png).

```bash
python raytracing.py
```

## Primeira parte (ata 4 puntos sobre 10)

Engadirlle a este [motor](https://gist.github.com/rossant/6046463) a posibilidade de traballar cun número arbitrario de fontes de luz, cada unha delas coas súas propias características (posición, cor).

Modificade a escena predeterminada a renderizar para que inclúa novas luces con distintas cores, mostrando a nova feature incorporada.

## Segunda parte (ata +3 puntos sobre o anterior)

Engadir ao motor unha nova primitiva gráfica coa que traballar: triángulo.

O código orixinal deste raytracer unicamente emprega esferas ou planos para construír unha escena e iluminala. Tedes que engadir a posibilidade de ter tamén triángulos na escena.

Modifica a escena predeterminada para que inclúa algún triángulo, ademais de esferas e planos como a escena orixinal.

-   Consello: Podedes reutilizar a función para calcular a
    intersección raio-plano que xa está no código, e a maiores
    precisades outra función que, unha vez sabemos que o raio choca co plano, comprobe se este punto de intesección está dentro do triángulo co que estamos a comprobar a intersección raio-triángulo.

## Terceira parte (ata +3 puntos sobre o anterior)

Engade ao motor unha primitiva Triangle Strip (tira de triángulos veciños que comparten vértices): https://en.wikipedia.org/wiki/Triangle_strip.

É dicir, o motor ten que poder traballar cun número arbitrario de vértices que formarán unha tira de triángulos veciños (que non teñen por que ser co-planares):

```
3 vértices: 1 triángulo

4 vértices: 2 triángulos

5 vértices: 3 triángulos

6 vértices: 4 triángulos...
```

Modificade a escea predeterminada a renderizar para que inclúa algunha tira de triángulos, que terá que ser correctamente iluminada.

## Entregables

-   URL a repositorio git co código, no que se vexa o progreso nas versións do traballo.

-   Etiquetade (=git tag=) as distintas versións que correspondan a cada unha das partes.

No repositorio ten que haber tamén exemplos de renders obtidos coas características incorporadas.

Tamén podedes achegar algún texto aclarativo/explicativo se o considerades preciso.

Para a evaluación da práctica é posible que se requira unha defensa interactiva da mesma con todas as persoas do grupo de prácticas.
