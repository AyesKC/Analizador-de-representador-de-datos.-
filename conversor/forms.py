from django import forms

from .servicios import BASES_VALIDAS, ErrorDeEntrada, validar_numero


class NumeroForm(forms.Form):
    numero = forms.CharField(
        label="Número",
        required=False,  # la validación se hace con mensajes propios
        widget=forms.TextInput(attrs={"placeholder": "Ej.: 255", "autocomplete": "off"}),
    )
    base = forms.TypedChoiceField(
        label="Base de origen",
        choices=[(b, f"Base {b}") for b in BASES_VALIDAS],
        coerce=int,
        initial=10,
    )

    def clean(self):
        datos = super().clean()
        if self.errors.get("base"):
            return datos
        try:
            datos["valor"] = validar_numero(datos.get("numero", ""), datos["base"])
        except ErrorDeEntrada as exc:
            self.add_error("numero", str(exc))
        return datos


class TextoForm(forms.Form):
    texto = forms.CharField(
        label="Texto (máx. 20 caracteres)",
        required=False,
        strip=False,  # los espacios también son caracteres
        widget=forms.TextInput(attrs={"placeholder": "Ej.: niño", "autocomplete": "off"}),
    )

    def clean_texto(self):
        texto = self.cleaned_data.get("texto", "")
        if texto == "":
            raise forms.ValidationError("Debe ingresar un texto.")
        if len(texto) > 20:
            raise forms.ValidationError("El texto no puede superar los 20 caracteres.")
        return texto
