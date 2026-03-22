import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bravais_trainer.settings')
django.setup()

from trainer.models import Lattice

# Данные о решетках
lattices_data = [
    # Сингония, тип, имя файла
    ('triclinic', 'P', 'triclinic_P.png'),
    ('monoclinic', 'P', 'monoclinic_P.png'),
    ('monoclinic', 'C', 'monoclinic_C.png'),
    ('orthorhombic', 'P', 'orthorhombic_P.png'),
    ('orthorhombic', 'C', 'orthorhombic_C.png'),
    ('orthorhombic', 'I', 'orthorhombic_I.png'),
    ('orthorhombic', 'F', 'orthorhombic_F.png'),
    ('tetragonal', 'P', 'tetragonal_P.png'),
    ('tetragonal', 'I', 'tetragonal_I.png'),
    ('rhombohedral', 'P', 'rhombohedral_P.png'),
    ('hexagonal', 'P', 'hexagonal_P.png'),
    ('cubic', 'P', 'cubic_P.png'),
    ('cubic', 'I', 'cubic_I.png'),
    ('cubic', 'F', 'cubic_F.png'),
]

for crystal_system, lattice_type, image_name in lattices_data:
    obj, created = Lattice.objects.get_or_create(
        crystal_system=crystal_system,
        lattice_type=lattice_type,
        defaults={'image_name': image_name}
    )
    if created:
        print(f'Добавлена: {crystal_system} - {lattice_type}')
    else:
        print(f'Уже существует: {crystal_system} - {lattice_type}')

print('Готово!')
