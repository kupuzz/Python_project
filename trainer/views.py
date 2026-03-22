"""
Представления для работы с решетками Браве и квизом.
"""
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from trainer.models import Lattice
from trainer.forms import QuizSetupForm, QuizQuestionForm


# Словари для отображения названий (вынесены в константы)
SYSTEM_NAMES = {
    'triclinic': 'Триклинная',
    'monoclinic': 'Моноклинная',
    'orthorhombic': 'Ромбическая',
    'tetragonal': 'Тетрагональная',
    'rhombohedral': 'Ромбоэдрическая',
    'hexagonal': 'Гексагональная',
    'cubic': 'Кубическая',
}

TYPE_NAMES = {
    'P': 'Примитивная',
    'C': 'Базоцентрированная',
    'I': 'Объемно-центрированная',
    'F': 'Гранецентрированная',
}

TYPE_NAMES_FULL = {
    'P': 'Примитивная (P)',
    'C': 'Базоцентрированная (C)',
    'I': 'Объемно-центрированная (I)',
    'F': 'Гранецентрированная (F)',
}


def index(request):
    """Главная страница."""
    return render(request, 'index.html')


def lattice_table(request):
    """Страница с таблицей всех решеток Браве."""
    crystal_systems = ['triclinic', 'monoclinic', 'orthorhombic', 'tetragonal',
                       'rhombohedral', 'hexagonal', 'cubic']
    lattice_types = ['P', 'C', 'I', 'F']

    # Создаем словарь для таблицы
    lattices = {}
    for cs in crystal_systems:
        lattices[cs] = {}
        for lt in lattice_types:
            try:
                lattices[cs][lt] = Lattice.objects.get(crystal_system=cs, lattice_type=lt)
            except Lattice.DoesNotExist:
                lattices[cs][lt] = None

    context = {
        'lattices': lattices,
        'crystal_systems': crystal_systems,
        'lattice_types': lattice_types,
        'system_names': SYSTEM_NAMES,
        'type_names': TYPE_NAMES,
    }
    return render(request, 'lattice_table.html', context)


def quiz_setup(request):
    """Настройка квиза: выбор количества вопросов."""
    if request.method == 'POST':
        form = QuizSetupForm(request.POST)
        if form.is_valid():
            num_questions = form.cleaned_data['num_questions']
            all_lattices = list(Lattice.objects.all())

            if not all_lattices:
                messages.error(request, 'Нет доступных решеток. Сначала добавьте решетки.')
                return redirect('index')

            # Выбираем случайные решетки
            num_questions = min(num_questions, len(all_lattices))
            selected_lattices = random.sample(all_lattices, num_questions)

            # Сохраняем в сессии
            request.session['quiz_lattices'] = [l.id for l in selected_lattices]
            request.session['quiz_current'] = 0
            request.session['quiz_results'] = []

            return redirect('quiz_question')
    else:
        form = QuizSetupForm()

    context = {
        'form': form,
        'total_lattices': Lattice.objects.count()
    }
    return render(request, 'quiz_setup.html', context)


def quiz_question(request):
    """Страница с вопросом квиза."""
    lattice_ids = request.session.get('quiz_lattices', [])
    current_index = request.session.get('quiz_current', 0)
    results = request.session.get('quiz_results', [])

    if current_index >= len(lattice_ids):
        return redirect('quiz_result')

    lattice = Lattice.objects.get(id=lattice_ids[current_index])

    if request.method == 'POST':
        form = QuizQuestionForm(request.POST, lattice=lattice)
        if form.is_valid():
            user_crystal = form.cleaned_data['crystal_system']
            user_type = form.cleaned_data['lattice_type']

            crystal_correct = user_crystal == lattice.crystal_system
            type_correct = user_type == lattice.lattice_type

            if crystal_correct and type_correct:
                points = 1.0
            elif crystal_correct or type_correct:
                points = 0.25
            else:
                points = 0

            results.append({
                'lattice_id': lattice.id,
                'user_crystal': user_crystal,
                'user_type': user_type,
                'crystal_correct': crystal_correct,
                'type_correct': type_correct,
                'points': points
            })

            request.session['quiz_results'] = results
            request.session['quiz_current'] = current_index + 1

            return redirect('quiz_question')
    else:
        form = QuizQuestionForm(lattice=lattice)

    context = {
        'form': form,
        'lattice': lattice,
        'question_number': current_index + 1,
        'total_questions': len(lattice_ids),
        'system_names': SYSTEM_NAMES,
    }
    return render(request, 'quiz_question.html', context)


def quiz_result(request):
    """Результаты квиза."""
    results = request.session.get('quiz_results', [])

    if not results:
        return redirect('quiz_setup')

    lattices = {l.id: l for l in Lattice.objects.all()}

    detailed_results = []
    total_points = 0

    for result in results:
        lattice = lattices[result['lattice_id']]
        detailed_results.append({
            'lattice': lattice,
            'user_crystal': SYSTEM_NAMES.get(result['user_crystal'], result['user_crystal']),
            'user_type': TYPE_NAMES_FULL.get(result['user_type'], result['user_type']),
            'correct_crystal': SYSTEM_NAMES[lattice.crystal_system],
            'correct_type': TYPE_NAMES_FULL[lattice.lattice_type],
            'crystal_correct': result['crystal_correct'],
            'type_correct': result['type_correct'],
            'points': result['points']
        })
        total_points += result['points']

    request.session.flush()

    max_points = len(results)
    percentage = (total_points / max_points) * 100 if max_points > 0 else 0

    context = {
        'results': detailed_results,
        'total_points': total_points,
        'max_points': max_points,
        'percentage': percentage,
    }
    return render(request, 'quiz_result.html', context)
