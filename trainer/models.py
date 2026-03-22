"""
Модели данных для решеток Браве.
"""
from django.db import models


class Meta:
    """Мета-класс для модели Lattice."""
    unique_together = ['crystal_system', 'lattice_type']
    verbose_name = 'Решетка Браве'
    verbose_name_plural = 'Решетки Браве'


class Lattice(models.Model):
    """Модель решетки Браве с сингонией, типом и изображением."""

    CRYSTAL_SYSTEMS = [
        ('triclinic', 'Триклинная'),
        ('monoclinic', 'Моноклинная'),
        ('orthorhombic', 'Ромбическая'),
        ('tetragonal', 'Тетрагональная'),
        ('rhombohedral', 'Ромбоэдрическая'),
        ('hexagonal', 'Гексагональная'),
        ('cubic', 'Кубическая'),
    ]

    LATTICE_TYPES = [
        ('P', 'Примитивная (P)'),
        ('C', 'Базоцентрированная (C)'),
        ('I', 'Объемно-центрированная (I)'),
        ('F', 'Гранецентрированная (F)'),
    ]

    crystal_system = models.CharField(
        max_length=20,
        choices=CRYSTAL_SYSTEMS,
        verbose_name='Сингония'
    )
    lattice_type = models.CharField(
        max_length=1,
        choices=LATTICE_TYPES,
        verbose_name='Тип решетки'
    )
    image_name = models.CharField(
        max_length=100,
        verbose_name='Имя файла изображения'
    )

    class Meta:
        """Мета-класс для модели Lattice."""
        unique_together = ['crystal_system', 'lattice_type']
        verbose_name = 'Решетка Браве'
        verbose_name_plural = 'Решетки Браве'

    def __str__(self):
        """Возвращает строковое представление решетки."""
        crystal_name = dict(self.CRYSTAL_SYSTEMS).get(self.crystal_system, self.crystal_system)
        type_name = dict(self.LATTICE_TYPES).get(self.lattice_type, self.lattice_type)
        return f"{crystal_name} - {type_name}"

    def get_image_path(self):
        """Возвращает путь к изображению решетки."""
        return f"images/lattices/{self.image_name}"
