import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kore-product-manager.settings")

application = get_wsgi_application()
BASE_DIR = Path(__file__).resolve().parent.parent

# Configura a pasta principal de produção
application = WhiteNoise(application, root=str(BASE_DIR / "staticfiles"))

# Faz o WhiteNoise olhar também a pasta onde o Tailwind gera o CSS
application.add_files(str(BASE_DIR / "static"), prefix="static/")

app = application
