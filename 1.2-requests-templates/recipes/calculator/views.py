from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    }
}


def get_recipe(request, name):
    servings = int(request.GET.get('servings', 1))
    recipe = {key: value * servings for key, value in DATA.get(name).items()}
    context = {
        'recipe':
            recipe
    }
    return render(request, 'calculator/index.html', context)
