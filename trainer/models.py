from django.db import models

class Lattice(models.Model):
    """Модель решетки Браве"""
    
    # Сингонии
    CRYSTAL_SYSTEMS = [
        ('triclinic', 'Триклинная'),
        ('monoclinic', 'Моноклинная'),
        ('orthorhombic', 'Ромбическая'),
        ('tetragonal', 'Тетрагональная'),
        ('rhombohedral', 'Ромбоэдрическая'),
        ('hexagonal', 'Гексагональная'),
        ('cubic', 'Кубическая'),
    ]
    
    # Типы решеток
    LATTICE_TYPES = [
        ('P', 'Примитивная (P)'),
        ('C', 'Базоцентрированная (C)'),
        ('I', 'Объемно-центрированная (I)'),
        ('F', 'Гранецентрированная (F)'),
    ]
    
    crystal_system = models.CharField('Сингония', max_length=20, choices=CRYSTAL_SYSTEMS)
    lattice_type = models.CharField('Тип решетки', max_length=1, choices=LATTICE_TYPES)
    image_name = models.CharField('Имя файла изображения', max_length=100)
    
    class Meta:
        unique_together = ['crystal_system', 'lattice_type']
        verbose_name = 'Решетка Браве'
        verbose_name_plural = 'Решетки Браве'
    
    def __str__(self):
        return f"{self.get_crystal_system_display()} - {self.get_lattice_type_display()}"
    
    def get_image_path(self):
        """Возвращает путь к изображению"""
        return f"images/lattices/{self.image_name}"
