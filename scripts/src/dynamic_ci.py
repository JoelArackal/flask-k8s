import os
import sys
from jinja2 import Environment, PackageLoader



if __name__=="__main__":
    script = "script.py"

    template = Environment(
        loader=PackageLoader("src"),
    ).get_template("dynamic_ci_template.j2.yaml")

    output_path = "./dynamic_ci.yaml"

    with open(output_path,"w") as f:
        f.write(template.render(
            script=script,
            regions=["eu","us","uae"]
        ))

        print("Rendered dynamic ci config")