# pg_type_template
An extension template for generating a Postgres type

# Usage

To work with `pg_type_template` it is necessary to prepare a model which will be
used to generate a type extension. This model is passed to the `TypeTemplate`
class instance.

Here is an example of such Python script (`example_type_templ.py`):

```
import pg_type_template

model = {
    "ext_name": "example_type",
    "ext_version": "0.0.1",
    "types": [
        {
            "type_name": "example_type",
            "type_values": [
                { "name": "enum 1", "value": 60 },
                { "name": "enum 2", "value": 120 },
                { "name": "enum 3", "value": 180 },
                { "name": "unknown", "value": 255 },
            ]
        }
    ],
    # optional value defaults "GITHUB_TOKEN"
    "github_action_token_name": "GITHUB_TOKEN"
}
templ = pg_type_template.TypeTemplate(model)
templ.render_to_dir(".")
```

To install python package you can use a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

After the script is defined run the following command:

```
pip install git+ssh://git@github.com/adjust/pg_type_template.git
python3 example_type_templ.py
```
