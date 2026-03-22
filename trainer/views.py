import random
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lattice
from .forms import QuizSetupForm, QuizQuestionForm

def index(request):
    """Главная страница"""
    return render(request, 'index.html')


def lattice_table(request):
    """Страница с таблицей решеток"""
    lattices = {}
    crystal_systems = ['triclinic', 'monoclinic', 'orthorhombic', 'tetragonal',
                       'rhombohedral', 'hexagonal', 'cubic']
    lattice_types = ['P', 'C', 'I', 'F']

    for cs in crystal_systems:
        lattices[cs] = {}
        for lt in lattice_types:
            try:
                lattice = Lattice.objects.get(crystal_system=cs, lattice_type=lt)
                lattices[cs][lt] = lattice
            except Lattice.DoesNotExist:
                lattices[cs][lt] = None

    system_names = {
        'triclinic': 'Триклинная',
        'monoclinic': 'Моноклинная',
        'orthorhombic': 'Ромбическая',
        'tetragonal': 'Тетрагональная',
        'rhombohedral': 'Ромбоэдрическая',
        'hexagonal': 'Гексагональная',
        'cubic': 'Кубическая',
    }

    type_names = {
        'P': 'Примитивная',
        'C': 'Базоцентрированная',
        'I': 'Объемно-центрированная',
        'F': 'Гранецентрированная',
    }

    context = {
        'lattices': lattices,
        'crystal_systems': crystal_systems,
        'lattice_types': lattice_types,
        'system_names': system_names,
        'type_names': type_names,
    }
    return render(request, 'lattice_table.html', context)


def quiz_setup(request):
    """Настройка квиза"""
    if request.method == 'POST':
        form = QuizSetupForm(request.POST)
        if form.is_valid():
            num_questions = form.cleaned_data['num_questions']
            all_lattices = list(Lattice.objects.all())

            if len(all_lattices) == 0:
                messages.error(request, 'Нет доступных решеток. Сначала добавьте решетки через админ-панель.')
                return redirect('index')

            if len(all_lattices) < num_questions:
                num_questions = len(all_lattices)

            selected_lattices = random.sample(all_lattices, num_questions)

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
    """Страница с вопросом квиза"""
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

            crystal_correct = (user_crystal == lattice.crystal_system)
            type_correct = (user_type == lattice.lattice_type)

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

    system_names = {
        'triclinic': 'Триклинная',
        'monoclinic': 'Моноклинная',
        'orthorhombic': 'Ромбическая',
        'tetragonal': 'Тетрагональная',
        'rhombohedral': 'Ромбоэдрическая',
        'hexagonal': 'Гексагональная',
        'cubic': 'Кубическая',
    }

    context = {
        'form': form,
        'lattice': lattice,
        'question_number': current_index + 1,
        'total_questions': len(lattice_ids),
        'system_names': system_names,
    }
    return render(request, 'quiz_question.html', context)


def quiz_result(request):
    """Результаты квиза"""
    results = request.session.get('quiz_results', [])

    if not results:
        return redirect('quiz_setup')

    lattices = {l.id: l for l in Lattice.objects.all()}

    system_names = {
        'triclinic': 'Триклинная',
        'monoclinic': 'Моноклинная',
        'orthorhombic': 'Ромбическая',
        'tetragonal': 'Тетрагональная',
        'rhombohedral': 'Ромбоэдрическая',
        'hexagonal': 'Гексагональная',
        'cubic': 'Кубическая',
    }

    type_names = {
        'P': 'Примитивная (P)',
        'C': 'Базоцентрированная (C)',
        'I': 'Объемно-центрированная (I)',
        'F': 'Гранецентрированная (F)',
    }

    detailed_results = []
    total_points = 0

    for result in results:
        lattice = lattices[result['lattice_id']]
        detailed_results.append({
            'lattice': lattice,
            'user_crystal': system_names.get(result['user_crystal'], result['user_crystal']),
            'user_type': type_names.get(result['user_type'], result['user_type']),
            'correct_crystal': system_names[lattice.crystal_system],
            'correct_type': type_names[lattice.lattice_type],
            'crystal_correct': result['crystal_correct'],
            'type_correct': result['type_correct'],
            'points': result['points']
        })
        total_points += result['points']

    request.session.flush()

    context = {
        'results': detailed_results,
        'total_points': total_points,
        'max_points': len(results),
        'percentage': (total_points / len(results)) * 100 if results else 0
    }
    return render(request, 'quiz_result.html', context)
