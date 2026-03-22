from django import forms

class QuizSetupForm(forms.Form):
    """Форма настройки квиза"""
    num_questions = forms.IntegerField(
        label='Количество вопросов',
        min_value=1,
        max_value=14,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class QuizQuestionForm(forms.Form):
    """Динамическая форма для вопроса квиза"""
    def __init__(self, *args, **kwargs):
        lattice = kwargs.pop('lattice', None)
        super().__init__(*args, **kwargs)
        
        if lattice:
            # Варианты для сингонии
            crystal_system_choices = [
                ('triclinic', 'Триклинная'),
                ('monoclinic', 'Моноклинная'),
                ('orthorhombic', 'Ромбическая'),
                ('tetragonal', 'Тетрагональная'),
                ('rhombohedral', 'Ромбоэдрическая'),
                ('hexagonal', 'Гексагональная'),
                ('cubic', 'Кубическая'),
            ]
            
            # Варианты для типа решетки
            lattice_type_choices = [
                ('P', 'Примитивная (P)'),
                ('C', 'Базоцентрированная (C)'),
                ('I', 'Объемно-центрированная (I)'),
                ('F', 'Гранецентрированная (F)'),
            ]
            
            self.fields['crystal_system'] = forms.ChoiceField(
                label='Сингония',
                choices=crystal_system_choices,
                widget=forms.RadioSelect,
                required=True
            )
            
            self.fields['lattice_type'] = forms.ChoiceField(
                label='Тип решетки',
                choices=lattice_type_choices,
                widget=forms.RadioSelect,
                required=True
            )
