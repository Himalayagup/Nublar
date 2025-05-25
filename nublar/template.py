import os
import re
import settings
import inspect
import html
from .utils import removing_slashes

# Get the template folder path from settings, defaulting to 'templates'
template_folder = getattr(settings, "TEMPLATE_FOLDER", "templates")

# Remove leading/trailing slashes from the template folder path
if template_folder:
    template_folder = removing_slashes(template_folder)
else:
    template_folder = "templates"

class TemplateFilters:
    """Built-in template filters."""
    
    @staticmethod
    def safe(value):
        """Mark a string as safe (not escaped)."""
        if value is None:
            return ""
        return str(value)

    @staticmethod
    def escape(value):
        """Escape HTML special characters."""
        if value is None:
            return ""
        return html.escape(str(value))

    @staticmethod
    def title(value):
        """Convert a string to title case."""
        if value is None:
            return ""
        return str(value).title()

    @staticmethod
    def upper(value):
        """Convert a string to uppercase."""
        if value is None:
            return ""
        return str(value).upper()

    @staticmethod
    def lower(value):
        """Convert a string to lowercase."""
        if value is None:
            return ""
        return str(value).lower()

    @staticmethod
    def length(value):
        """Return the length of a value."""
        if value is None:
            return 0
        return len(value)

    @staticmethod
    def default(value, default_value=""):
        """Return the value if it exists, otherwise return the default."""
        if value is None or value == "":
            return default_value
        return value

    @staticmethod
    def truncate(value, length=30, suffix="..."):
        """Truncate a string to the specified length."""
        if value is None:
            return ""
        value = str(value)
        if len(value) <= length:
            return value
        return value[:length].rstrip() + suffix

    @staticmethod
    def join(value, separator=", "):
        """Join a list with the specified separator."""
        if value is None:
            return ""
        if not isinstance(value, (list, tuple)):
            return str(value)
        # Convert each item to string and strip quotes
        items = [str(item).strip('"\'') for item in value]
        return separator.join(items)

    @staticmethod
    def date(value, format="%Y-%m-%d"):
        """Format a date using the specified format."""
        if value is None:
            return ""
        if hasattr(value, 'strftime'):
            return value.strftime(format)
        return str(value)

    @staticmethod
    def int(value):
        """Convert a value to an integer."""
        if value is None:
            return 0
        try:
            return int(float(str(value)))
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def float(value):
        """Convert a value to a float."""
        if value is None:
            return 0.0
        try:
            return float(str(value))
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def round(value, digits=0):
        """Round a number to the specified number of digits."""
        if value is None:
            return 0
        try:
            return round(float(str(value)), digits)
        except (ValueError, TypeError):
            return 0

def apply_filters(value, filter_chain):
    """Apply a chain of filters to a value."""
    # print(f"\nApplying filters to value: {value} (type: {type(value)})")
    # print(f"Filter chain: {filter_chain}")
    
    if not filter_chain:
        # print("No filters to apply, returning string value")
        return str(value)

    filters = TemplateFilters()
    current_value = value
    for filter_name, args in filter_chain:
        # print(f"\nApplying filter: {filter_name} with args: {args}")
        filter_method = getattr(filters, filter_name, None)
        if filter_method:
            try:
                # Convert args to appropriate types
                processed_args = []
                for arg in args:
                    try:
                        # Try to convert to float first (for numeric args)
                        processed_args.append(float(arg))
                    except ValueError:
                        # If not a number, keep as string
                        processed_args.append(arg.strip('"\''))  # Strip quotes from string args
                # print(f"Processed args: {processed_args}")
                
                current_value = filter_method(current_value, *processed_args)
                # print(f"Value after filter {filter_name}: {current_value} (type: {type(current_value)})")
            except Exception as e:
                # print(f"Filter error in {filter_name}: {e}")
                current_value = str(current_value)
        else:
            # print(f"Filter {filter_name} not found, converting to string")
            current_value = str(current_value)

    # Ensure the final value is a string and strip any extra quotes
    result = str(current_value).strip('"\'')
    # print(f"Final filtered value: {result}")
    return result

def parse_filters(var_name):
    """Parse variable name and its filters."""
    # Split the variable name and filters
    parts = var_name.split('|')
    var_name = parts[0].strip()
    
    # Parse filters and their arguments
    filter_chain = []
    for filter_part in parts[1:]:
        filter_parts = filter_part.strip().split(':')
        filter_name = filter_parts[0].strip()
        filter_args = [arg.strip() for arg in filter_parts[1:]] if len(filter_parts) > 1 else []
        filter_chain.append((filter_name, filter_args))

    return var_name, filter_chain

def process_control_structures(content, context):
    """Process if statements and for loops in the template."""
    # print("\nProcessing control structures:")
    # print(f"Context: {context}")
    
    # Process if statements
    def process_if(match):
        condition = match.group(1).strip()
        if_content = match.group(2)
        else_content = match.group(3) if match.group(3) else ""
        # print(f"\nProcessing if condition: {condition}")

        try:
            # Create a safe evaluation environment with proper type conversion
            safe_dict = {}
            for k, v in context.items():
                if k.startswith('_'):
                    continue
                if isinstance(v, (dict, list)):
                    safe_dict[k] = v
                else:
                    safe_dict[k] = str(v)
            # print(f"Safe dict for evaluation: {safe_dict}")
            
            result = eval(condition, {"__builtins__": {}}, safe_dict)
            # print(f"Condition result: {result}")
            return if_content if result else else_content
        except Exception as e:
            # print(f"If condition error: {e}")
            return ""

    if_pattern = r'{%\s*if\s+(.+?)\s*%}(.*?)(?:{%\s*else\s*%}(.*?))?{%\s*endif\s*%}'
    content = re.sub(if_pattern, process_if, content, flags=re.DOTALL)

    # Process for loops
    def process_for(match):
        loop_var = match.group(1).strip()
        iterable = match.group(2).strip()
        loop_content = match.group(3)
        # print(f"\nProcessing for loop: {loop_var} in {iterable}")

        try:
            # Get the iterable from context
            items = eval(iterable, {"__builtins__": {}}, context)
            # print(f"Items to iterate: {items}")
            
            if not isinstance(items, (list, tuple)):
                # print(f"Converting single item to list: {items}")
                items = [items]
            
            result = []
            for item in items:
                loop_context = context.copy()
                loop_context[loop_var] = item
                # print(f"Loop context for {loop_var}: {loop_context}")
                
                # Render the loop content with the new context
                rendered = render_template_content(loop_content, loop_context)
                # print(f"Rendered content: {rendered}")
                result.append(str(rendered))
            
            final_result = "".join(result)
            # print(f"Final loop result: {final_result}")
            return final_result
        except Exception as e:
            print(f"For loop error: {e}")
            return ""

    for_pattern = r'{%\s*for\s+(\w+)\s+in\s+(.+?)\s*%}(.*?){%\s*endfor\s*%}'
    content = re.sub(for_pattern, process_for, content, flags=re.DOTALL)

    return content

def render_template_content(content, context):
    """Render template content with the given context."""
    # print("\nRendering template content:")
    # print(f"Initial content length: {len(content)}")
    # print(f"Context: {context}")

    # Process control structures
    content = process_control_structures(content, context)
    # print(f"After control structures, content length: {len(content)}")

    # Replace variables with filters
    def replace_var(match):
        var_name = match.group(1).strip()
        # print(f"\nProcessing variable: {var_name}")
        
        try:
            # Parse variable name and filters
            var_name, filter_chain = parse_filters(var_name)
            # print(f"Parsed variable name: {var_name}")
            # print(f"Filter chain: {filter_chain}")
            
            # Get the value from context
            parts = var_name.split('.')
            value = context
            for part in parts:
                # print(f"Accessing part: {part} from {value}")
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = getattr(value, part, None)
                # print(f"Value after accessing {part}: {value} (type: {type(value)})")

            # Apply filters and ensure string output
            result = apply_filters(value, filter_chain)
            # print(f"After applying filters: {result}")
            return str(result).strip('"\'')  # Strip any extra quotes
        except Exception as e:
            # print(f"Variable replacement error for {var_name}: {e}")
            return ""

    var_pattern = r'{{(.+?)}}'
    content = re.sub(var_pattern, replace_var, content)
    # print(f"Final content length: {len(content)}")

    return content

def render_template(template_name, context, caller_directory_path=None):
    """Main template rendering function."""
    # First try to find the template in the app's templates directory
    template_path = None
    if caller_directory_path:
        app_templates_path = os.path.join(caller_directory_path, template_folder, template_name)
        if os.path.exists(app_templates_path) and os.path.isfile(app_templates_path):
            template_path = app_templates_path

    # If not found in app directory, try the global templates directory
    if not template_path:
        global_path = os.path.join(os.getcwd(), template_folder, template_name)
        if os.path.exists(global_path) and os.path.isfile(global_path):
            template_path = global_path

    if not template_path:
        searched_paths = [
            app_templates_path if caller_directory_path else None,
            global_path
        ]
        searched_paths = [p for p in searched_paths if p is not None]
        raise FileNotFoundError(
            f"Template '{template_name}' not found. Searched in:\n" +
            "\n".join(f"{i+1}. {path}" for i, path in enumerate(searched_paths))
        )

    # Read and render the template
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return render_template_content(content, context)
