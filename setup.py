from setuptools import setup

setup(
    name="pg_type_template",
    version="0.0.1",
    install_requires=["Jinja2>=3.0.1"],
    packages=["pg_type_template"],
    package_data={"pg_type_template": ["templates/*",
                                        "templates/*/*",
                                        "templates/*/*/*",
                                        "templates/.github/workflows/*",
                                        "templates/.gitignore"]}
)
