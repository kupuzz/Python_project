"""
Формы для настройки квиза и вопросов.
"""
from django import forms

# Общие константы для избежания дублирования кода
CRYSTAL_SYSTEM_CHOICES = [
    ('triclinic', 'Триклинная'),
    ('monoclinic', 'Моноклинная'),
    ('orthorhombic', 'Ромбическая'),
    ('tetragonal', 'Тетрагональная'),
    ('rhombohedral', 'Ромбоэдрическая'),
    ('hexagonal', 'Гексагональная'),
    ('cubic', 'Кубическая'),
]

LATTICE_TYPE_CHOICES = [
    ('P', 'Примитивная (P)'),
    ('C', 'Базоцентрированная (C)'),
    ('I', 'Объемно-центрированная (I)'),
    ('F', 'Гранецентрированная (F)'),
]


class QuizSetupForm(forms.Form):
    """Форма настройки количества вопросов в квизе."""
    num_questions = forms.IntegerField(
        label='Количество вопросов',
        min_value=1,
        max_value=14,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class QuizQuestionForm(forms.Form):
    """Динамическая форма для вопроса квиза с выбором сингонии и типа решетки."""

    def __init__(self, *args, **kwargs):
        lattice = kwargs.pop('lattice', None)
        super().__init__(*args, **kwargs)

        if lattice:
            self.fields['crystal_system'] = forms.ChoiceField(
                label='Сингония',
                choices=CRYSTAL_SYSTEM_CHOICES,
                widget=forms.RadioSelect,
                required=True
            )

            self.fields['lattice_type'] = forms.ChoiceField(
                label='Тип решетки',
                choices=LATTICE_TYPE_CHOICES,
                widget=forms.RadioSelect,
                required=True
            )
