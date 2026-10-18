from django.shortcuts import render

from .forms import NumeroForm, TextoForm
from .servicios import analizar_texto, convertir_numero


def index(request):
    form_numero = NumeroForm(prefix="num")
    form_texto = TextoForm(prefix="txt")
    resultado = None
    filas = None

    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "numero":
            form_numero = NumeroForm(request.POST, prefix="num")
            if form_numero.is_valid():
                resultado = convertir_numero(
                    form_numero.cleaned_data["numero"],
                    form_numero.cleaned_data["base"],
                )
        elif accion == "texto":
            form_texto = TextoForm(request.POST, prefix="txt")
            if form_texto.is_valid():
                filas = analizar_texto(form_texto.cleaned_data["texto"])

    return render(
        request,
        "conversor/index.html",
        {
            "form_numero": form_numero,
            "form_texto": form_texto,
            "resultado": resultado,
            "filas": filas,
        },
    )
