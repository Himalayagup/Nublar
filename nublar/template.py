import os
import settings
import inspect
from .utils import removing_slashes

# Get the template folder path from settings, defaulting to 'templates'
template_folder = getattr(settings, "TEMPLATE_FOLDER", "templates")

# Remove leading/trailing slashes from the template folder path
if template_folder:
    template_folder = removing_slashes(template_folder)
else:
    template_folder = "templates"

def render_template(template_name, context, caller_directory_path=None):
    # The templates are assumed to be in the 'templates' directory
    global template_folder
    template_folder = template_folder  # Use the global template folder
    template_path = None  # Variable to store the resolved template path

    # If caller_directory_path is provided, try to load the template from that directory first
    if caller_directory_path:
        # Construct the full template path by joining the caller's directory and template folder
        app_level_template_path = os.path.join(os.path.join(caller_directory_path, template_folder), template_name)

        # If the template exists in the caller's directory, set the template_path
        if os.path.exists(app_level_template_path) and os.path.isfile(app_level_template_path):
            template_path = app_level_template_path

    # If the template wasn't found in the caller's directory, use the default template folder
    if not template_path:
        template_path = os.path.join(template_folder, template_name)

    # Raise an error if the template file doesn't exist
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template '{template_name}' not found.")

    # Read the template content from the file
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Replace placeholders in the template with values from the context dictionary
    for key, value in context.items():
        placeholder = f"{{{{ {key} }}}}"  # Format placeholders as {{ key }}
        template_content = template_content.replace(placeholder, str(value))  # Replace the placeholder with the context value

    return template_content  # Return the rendered template content
