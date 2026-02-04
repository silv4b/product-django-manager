import os
from pathlib import Path


def fix_static_load():
    templates_dir = Path("templates")
    fixed_count = 0

    if not templates_dir.exists():
        print(f"❌ Pasta 'templates' não encontrada!")
        return

    for html_file in templates_dir.rglob("*.html"):
        try:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Verifica se usa {% static %} mas não tem {% load static %}
            has_static_tag = "{% static" in content
            has_load_static = "{% load static %}" in content

            if has_static_tag and not has_load_static:
                # Insere no início do arquivo
                new_content = "{% load static %}\n" + content

                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print(f"✅ Corrigido: {html_file.relative_to(Path.cwd())}")
                fixed_count += 1

        except Exception as e:
            print(f"❌ Erro ao processar {html_file}: {e}")

    print(f"\n✨ Total de arquivos corrigidos: {fixed_count}")


if __name__ == "__main__":
    fix_static_load()
