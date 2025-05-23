import os
import settings
import inspect
from .utils import removing_slashes

template_folder = getattr(settings, "TEMPLATE_FOLDER", "templates")
if template_folder:
    template_folder = removing_slashes(template_folder)
else:
    template_folder = "templates"

def render_template(template_name, context, caller_directory_path=None):
    # The templates are assumed to be in the 'templates' directory
    global template_folder
    template_folder = template_folder
    template_path = None
    if caller_directory_path:
        app_level_template_path = os.path.join(os.path.join(caller_directory_path, template_folder), template_name)
        if os.path.exists(app_level_template_path) and os.path.isfile(app_level_template_path):
            template_path = app_level_template_path
    if not template_path:
        template_path = os.path.join(template_folder, template_name)
    print(template_path)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template '{template_name}' not found.")

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Replace placeholders in the template with values from the context
    for key, value in context.items():
        placeholder = f"{{{{ {key} }}}}"
        template_content = template_content.replace(placeholder, str(value))

    return template_content