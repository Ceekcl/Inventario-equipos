from django.db import models


class Equipo(models.Model):
    class Estado(models.TextChoices):
        OPERATIVO = "Operativo", "Operativo"
        EN_REPARACION = "En reparación", "En reparación"
        DADO_DE_BAJA = "Dado de baja", "Dado de baja"

    tipo = models.CharField("Tipo de equipo", max_length=80)
    marca = models.CharField("Marca", max_length=80)
    modelo = models.CharField("Modelo", max_length=120)
    numero_serie = models.CharField(
        "Número de serie",
        max_length=120,
        unique=True,
    )
    ubicacion = models.CharField("Ubicación", max_length=120)
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=Estado.choices,
        default=Estado.OPERATIVO,
    )

    class Meta:
        ordering = ["numero_serie"]
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def clean(self):
        super().clean()
        self.numero_serie = self.numero_serie.strip().upper()

    def __str__(self):
        return f"{self.numero_serie} — {self.marca} {self.modelo}"