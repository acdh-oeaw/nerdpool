def main(
    recipes_dir: (
        "Directory of the recipes to patch",
        "option",
        "r",
    ) = "nerdpool/nerdpool_recipes",
    nerdpool_template: (
        "Template file used to patch the recipes",
        "option",
        "t",
    ) = "nerdpool_recipe_patch_template.py",
    recipes_list: ("List of filenames to process", "option") = None,
):
    """Function that runs through a given directory and patches all prodigy recipes found in there
    with the given template. Expects a multiline docstring within every function to patch.
    """
    with open(nerdpool_template, "r") as templ:
        templ_str = templ.read()
        templ_list = templ_str.split("<<<end_imports")
        if len(templ_list) > 1:
            imports = templ_list[0]
            templ = templ_list[1]
        else:
            imports = False
            templ = templ_list[0]
        for f1 in Path(recipes_dir).rglob("*.py"):
            print(f1)
            with open(f1, "r") as recipe:
                txt = recipe.read().replace("from .. ", "from prodigy ")
                txt = txt.replace("from ..", "from prodigy.")
                txt = txt.replace("from . ", "from prodigy_recipes ")
                txt = txt.replace("from .", "from prodigy_recipes.")
            with open(f1, "w") as recipe_out:
                recipe_out.write(txt)
            if recipes_list is not None:
                if str(f1).split("/")[-1] not in recipes_list:
                    continue
            with open(f1, "r") as recipe:
                txt = recipe.read()
                txt1 = re.subn(
                    r"(return {\n\s*.+?$)",
                    r'{}\n\n    \1\n        "update": update,'.format(templ),
                    txt,
                    flags=re.M | re.DOTALL,
                )
                txt = txt1[0]
                if imports:
                    print("running through imports")
                    txt = f"{imports}\n{txt}"
            with open(f1, "w") as recipe_out:
                recipe_out.write(txt)


if __name__ == "__main__":
    import plac
    import re
    from pathlib import Path

    plac.call(main)
