"""
Configuração de Testes para o Kore Product Manager

Este módulo fornece configuração para executar testes de forma eficiente.
Define listas de testes para diferentes propósitos (rápido, completo, etc).
"""

# Suíte de testes rápida para desenvolvimento
# Executa apenas testes de modelos e formulários
QUICK_TESTS = [
    "products.tests.test_models",
    "products.tests.test_forms",
]

# Suíte de testes completa incluindo testes de integração
# Inclui modelos, formulários, views e integração
FULL_TESTS = [
    "products.tests.test_models",
    "products.tests.test_forms",
    "products.tests.test_views",
    "products.tests.test_integration",
]

# Testes de modelos apenas (mais rápido)
# Executa apenas testes de modelos do Django
MODEL_TESTS = [
    "products.tests.test_models",
]

# Testes de views apenas
# Executa apenas testes de visualização do Django
VIEW_TESTS = [
    "products.tests.test_views",
]

# Testes de integração apenas (mais lento)
# Executa testes de fluxo de trabalho completo
INTEGRATION_TESTS = [
    "products.tests.test_integration",
]


def run_test_suite(suite_type="quick"):
    """
    Executa a suíte de testes baseada no tipo especificado.

    Args:
        suite_type: Tipo de suíte de testes - 'quick', 'full', 'models', 'views' ou 'integration'

    Returns:
        Número de falhas nos testes executados.
    """
    import django
    from django.conf import settings
    from django.test.utils import get_runner

    django.setup()

    TestRunner = get_runner(settings)

    if suite_type == "quick":
        test_labels = QUICK_TESTS
    elif suite_type == "full":
        test_labels = FULL_TESTS
    elif suite_type == "models":
        test_labels = MODEL_TESTS
    elif suite_type == "views":
        test_labels = VIEW_TESTS
    elif suite_type == "integration":
        test_labels = INTEGRATION_TESTS
    else:
        raise ValueError(f"Unknown suite type: {suite_type}")

    runner = TestRunner(verbosity=2, keepdb=False)
    failures = runner.run_tests(test_labels)

    return failures
