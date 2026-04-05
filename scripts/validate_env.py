import importlib
import yaml


def validate_yaml():
    with open("openenv.yaml", "r") as f:
        config = yaml.safe_load(f)

    print("✔ YAML loaded")

    # Check entry point
    module_name, class_name = config["entry_point"].split(":")
    module = importlib.import_module(module_name)
    getattr(module, class_name)

    print("✔ Entry point valid")

    # Check tasks
    for task in config["tasks"]:
        gen_module, gen_fn = task["generator"].split(":")
        grader_module, grader_cls = task["grader"].split(":")

        gen_mod = importlib.import_module(gen_module)
        getattr(gen_mod, gen_fn)

        grader_mod = importlib.import_module(grader_module)
        getattr(grader_mod, grader_cls)

        print(f"✔ Task validated: {task['name']}")

    print("\n✅ All validations passed!")


if __name__ == "__main__":
    validate_yaml()