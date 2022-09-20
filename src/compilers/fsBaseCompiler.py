from abc import ABC, abstractmethod
from json import load
import jsonschema


def extendValidator(validator_class) -> jsonschema.Draft7Validator:
    """An admittedly gross solution for jsonschema defaults"""
    validate_properties = validator_class.VALIDATORS["properties"]

    def setDefaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    def schemaWarn(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "warn" in subschema and property in instance:
                print(f"WARNING:{property} {subschema.get('warn')}")

        for error in validate_properties(
            validator,
            properties,
            instance,
            schema,
        ):
            yield error

    return jsonschema.validators.extend(
        validator_class,
        {"properties": setDefaults, "properties": schemaWarn},
    )


class BaseCompiler(ABC):
    """Abstract Compiler Class"""

    build = None
    json = None
    schema = 
    max_processes = None

    # key:val pairs to be avoided during normalization
    protectedKeys = ["input"]
    # json arg to command arg map
    argMap = {"arg": "--arg="}

    @abstractmethod
    def compile(self, file) -> None:
        """compile how?"""

    def __init__(self, json, max_processes=1) -> None:
        """creates and prepares compiler"""

        self.json = json
        self.json["max_processes"] = max_processes
        self.schema = self.schema
        resolver = jsonschema.RefResolver(
            schema_path="file:{}".format()
        )

        self.normalize()
        # get extended validator and create instance with our schema
        validator = extendValidator(jsonschema.Draft7Validator)(self.schema)

        try:
            validator.validate(self.json)
        except jsonschema.ValidationError as e:
            raise e
        except Exception as e:
            print(e)

    def normalize(self) -> None:
        """normalize all non protected keyvals"""
        for key in dict(self.json).keys():
            if key not in self.protectedKeys:
                self.json[key] = str(self.json[key]).lower()
