import yaml


def load_content(file_path="app/content/content.yaml"):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}


def get_field_content(content, field_name, content_key=None):
    try:
        field_content = content["forms"]["fields"][field_name]

        if content_key:
            return field_content.get(content_key)
        return field_content
    except KeyError as e:
        print(f"Error accessing {field_name}: {e}")
        return f"'{field_name}' not found in content."


def prepare_country_options(content):
    try:
        prompt = get_field_content(content, "requester_country", "prompt_to_select")
        countries = get_field_content(content, "requester_country", "countries")

        if prompt is None:
            raise TypeError("Country prompt is missing from content")

        if countries is None:
            raise TypeError("Countries list is missing from content")

        if not isinstance(prompt, str):
            raise TypeError("Country prompt must be a string")

        if not isinstance(countries, list):
            raise TypeError("Countries must be a list")

        result = [("", prompt)] + [(country, country) for country in countries]
    except (KeyError, TypeError) as e:
        print(f"Error accessing requester country choices: {e}")
        result = []
    return result
