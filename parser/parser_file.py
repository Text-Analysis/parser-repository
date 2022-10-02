import ast
from ast import FunctionDef, ClassDef


class ParserFile:

    def __init__(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.tree = ast.parse(content)
        except IOError as error:
            print(error)

    def get_data(self):
        classes_data = self.__get_classes_data(self.tree.body)
        functions_data = self.__get_functions_data(self.tree.body)
        return {
            "classes": classes_data,
            "functions": functions_data,
        }

    def __get_classes_data(self, node) -> list:
        classes = [n for n in node if isinstance(n, ClassDef)]
        content = []
        for class_ in classes:
            class_data = self.__get_class_data(class_)
            content.append(class_data)
        return content

    def __get_class_data(self, class_node: ClassDef):
        name = class_node.name
        first_line = class_node.lineno
        last_line = class_node.end_lineno
        documentation = self.__get_documentation(class_node)
        methods_content = self.__get_functions_data(class_node.body)
        return {
            "name": name,
            "doc": documentation,
            "first_line": first_line,
            "last_line": last_line,
            "methods": methods_content,
        }

    def __get_functions_data(self, node) -> list:
        functions = [n for n in node if isinstance(n, FunctionDef)]
        content = []
        for func in functions:
            func_data = self.__get_function_data(func)
            content.append(func_data)
        return content

    def __get_function_data(self, method_node: FunctionDef):
        name = method_node.name
        first_line = method_node.lineno
        last_line = method_node.end_lineno
        documentation = self.__get_documentation(method_node)

        arguments = []
        for index, argument in enumerate(method_node.args.args):
            value = ""
            defaults_len = len(method_node.args.defaults)
            position = -defaults_len + index + 1
            if defaults_len > position >= 0:
                value = method_node.args.defaults[position].value
            arg_obj = {
                "name": argument.arg,
                "default_value": value
            }
            arguments.append(arg_obj)
        return {
            "name": name,
            "doc": documentation,
            "args": arguments,
            "first_line": first_line,
            "last_line": last_line
        }

    @staticmethod
    def __get_documentation(node):
        documentation = ""
        for n in node.body:
            if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant):
                documentation = n.value.value
        return documentation
