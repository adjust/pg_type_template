#!env python3
import os
import shutil

from jinja2 import Environment, PackageLoader

def sort_by_name(value):
    """
    Jinja filter which sorts C macros by their names.
    """
    return sorted(value, key=lambda t: t["name"])

def uint8_name(value):
    """
    Jinja filter which generates C macro name.
    """
    return value.upper().replace(" ", "_").replace("-", "_")

class TypeTemplate:
    """
    A class that generates PostgreSQL extensions which adds new enum data type.
    """
    def __init__(self, model):
        self.check_values(model)

        self.model = model
        self.env = Environment(loader=PackageLoader(__package__), trim_blocks=True)
        self.env.filters["uint8_name"] = uint8_name
        self.env.filters["sort_by_name"] = sort_by_name

    def check_values(self, model):
        """
        Check Postgresql extension model values.

        The function raises ValueError exception if any enum value is outside of
        allowed range.
        """
        for model_type in model["types"]:
            for type_values in model_type["type_values"]:
                if type_values["value"] < 0 or type_values["value"] > 255:
                    raise ValueError(f"value '{type_values['value']}' of '{type_values['name']}' is out of range")

    def render_to_dir(self, dest_dir):
        """
        Generate new PostgreSQL extension into dest_dir directory.
        """
        for template_name in self.env.list_templates():
            template = self.env.get_template(template_name)

            file_path, file_ext = os.path.splitext(template_name)
            dir_path = os.path.join(dest_dir, os.path.dirname(file_path))
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            # If it isn't template file just copy it
            if file_ext != ".jinja":
                shutil.copyfile(template.filename,
                    os.path.join(dest_dir, template.name))
            else:
                template_root = template_name.split(os.path.sep)[0]

                if template_root in ["src", "test"]:
                    for model_type in self.model["types"]:
                        template.stream(model_type).dump(
                            os.path.join(dest_dir,
                                file_path.replace("type_name", model_type["type_name"])
                            ))
                else:
                    template.stream(self.model).dump(
                        os.path.join(dest_dir,
                            file_path.replace("ext_name", self.model["ext_name"])
                                .replace("ext_version", self.model["ext_version"])
                        ))
