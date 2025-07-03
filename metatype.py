from dataclasses import dataclass
from tkinter import filedialog
import warnings

class GeneratorWarning(UserWarning):
    pass

class StarterPack:
    class python:
        @staticmethod
        def tkinter_minimal():
            to_return = """
import tkinter as tk

def rgb(r:int,g:int,b:int):
    return "#{02.x}{02.x}{02.x}".format(r,g,b)

root = tk.Tk(screenName="starter tkinter window")
root.geometry("800x600")
root.configure(background = rgb(255,255,255))
root.mainloop()
"""
            return to_return
            
    

@dataclass
class pair:
    pair_type: type
    pair_value: object
    mutable: bool = True


@dataclass
class get_argument:
    name: str


def Structure(class_name: str, **attr):
    to_add = "["
    args = ""
    property_functions = []

    index = 0
    if len(attr.items()) > 100:
        message = "Larger generations means your ide potentially crashing. Be mindful of the amount of items inputed."
        warnings.warn(message, GeneratorWarning)

    for key, value in attr.items():
        property_functions.append(
            f"""
    @property
    def {key}(self):return self[{index}].value
        
    @{key}.setter
    def {key}(self,new_value):self[{index}].value = new_value
        
        """
        )
        index += 1

        to_add += f"mutable({key}),"
        if isinstance(value, str):
            args += f"{key}='{value}',"
        elif isinstance(value, type(None)):
            args += f"{key},"
        elif isinstance(value, pair):
            if value.pair_value == None:
                args += f"{key}:{value.pair_type.__name__},"
            elif isinstance(value.pair_value, str):
                args += f"{key}:{value.pair_type.__name__} = '{value.pair_value}',"
            else:
                args += f"{key}:{value.pair_type.__name__} = {value.pair_value},"
        else:
            args += f"{key}={value},"

    to_add = to_add[: len(to_add) - 1] + "]"
    args = args[: len(args) - 1]

    main_join = f"""
class {class_name}(tuple):
    def __new__(cls,{args}):
        return super().__new__(cls,@)
    """
    main_join = main_join.replace("@", str(to_add))

    for property_expression in property_functions:
        main_join += property_expression + "\n"

    return main_join


def MinimalClass(
    class_name: str,
    refrence_name: str = "self",
    arguments: dict = {},
    indent: str = "        ",
    **attr,
):
    class_variables = ""
    args = ""
    if len(arguments.items()) > 100:
        message = "Larger generations means your ide potentially crashing. Be mindful of the amount of items inputed."
        warnings.warn(message, GeneratorWarning)

    for key, value in arguments.items():
        if isinstance(value, str):
            args += f"{key} = '{value}',"
        elif value == None:
            class_variables += f"{key},"
        elif isinstance(value, pair):
            if value.pair_value == None:
                args += f"{key}:{value.pair_type.__name__},"
            elif isinstance(value.pair_value, str):
                args += f"{key}:{value.pair_type.__name__} = '{value.pair_value}',"
        else:
            args += f"{key} = {value},"
    args = args[: len(args) - 1]

    if len(arguments) > 0:
        base = f"""
class {class_name}:
    def __init__({refrence_name},{args}):\n"""
    else:
        base = f"""
class {class_name}:
    def __init__({refrence_name}):\n"""

    if len(attr.items()) > 100:
        message = "Larger generations means your ide potentially crashing. Be mindful of the amount of items inputed."
        warnings.warn(message, GeneratorWarning)

    for key, value in attr.items():
        if isinstance(value, str):
            class_variables += indent + f"{refrence_name}.{key} = '{value}'\n"
        elif value == None:
            class_variables += indent + f"{refrence_name}.{key}:Any \n"
        elif isinstance(value, pair):

            if value.pair_value == None:
                class_variables += (
                    indent + f"{refrence_name}.{key}:{value.pair_type.__name__} \n"
                )

            elif isinstance(value.pair_value, str):
                class_variables += (
                    indent
                    + f"{refrence_name}.{key}:{value.pair_type.__name__} = '{value.pair_value}' \n"
                )
        elif isinstance(value, get_argument):
            class_variables += indent + f"{refrence_name}.{key} = {value.name} \n"
        else:
            class_variables += indent + f"{refrence_name}.{key} = {value}\n"

    return base + class_variables


def FunctionTemplate(function_name: str, indent: str = "", **function_arguments):
    args = ""
    if len(function_arguments.items()) > 100:
        message = "Larger generations means your ide potentially crashing. Be mindful of the amount of items inputed."
        warnings.warn(message, GeneratorWarning)

    for key, value in function_arguments.items():
        if isinstance(value, str):
            args += f"{key} = '{value}',"
        elif value == None:
            args += f"{key},"
        elif isinstance(value, pair):
            if value.pair_value == None:
                args += f"{key}:{value.pair_type.__name__},"
            elif isinstance(value.pair_value, str):
                args += f"{key}:{value.pair_type.__name__} = '{value.pair_value}',"
        else:
            args += f"{key} = {value},"
    args = args[: len(args) - 1]

    base = f"""
{indent}def {function_name}({args}):
    {indent}pass"""
    return base


def copy_code(container_name: str):
    file_name = filedialog.askopenfilename(
        title="open python file", filetypes=[("python script", "*.py")]
    )
    with open(file_name, "r") as file:
        with open(container_name, "w") as new_file:
            new_file.write(f"#file source:{file_name}\n\n{file.read()}")
            
    return ""


def template(directorty: str, *args):
    with open(directorty, "w") as temp:
        base = """from dataclasses import dataclass
@dataclass
class mutable:
    value:object
    mutable:bool = True

            """
        for generated in args:
            base += generated + "\n"

        temp.write(base)
