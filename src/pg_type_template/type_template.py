#!env python3
import os
import shutil

from jinja2 import Environment, PackageLoader

def uint8_name(value):
    return value.upper().replace(" ", "_")

class TypeTemplate:
    def __init__(self, model):
        self.model = model
        self.env = Environment(loader=PackageLoader(__package__), trim_blocks=True)
        self.env.filters["uint8_name"] = uint8_name

    def render_to_dir(self, dest_dir):
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
