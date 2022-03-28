import yaml

def read_yaml(filename:str) -> dict:
    with open(filename, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error reading {filename}")
            raise exc