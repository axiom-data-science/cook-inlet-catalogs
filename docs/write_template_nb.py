import nbformat as nbf
import cook_inlet_catalogs as cic
import pandas as pd
from glob import glob
from pathlib import Path
import intake
from importlib.resources import files
import os
import hvplot.pandas
import hvplot.xarray

imports = f"""\
import pandas as pd
from glob import glob
from pathlib import Path
import intake
from importlib.resources import files
import os
import hvplot.pandas
import hvplot.xarray
import cook_inlet_catalogs as cic
"""

def write_nb(slug):

    nb = nbf.v4.new_notebook()
    
    cat = intake.open_catalog(cic.utils.cat_path(slug))

    text = f"""\
Click here to run this notebook in Binder, a hosted environment: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/axiom-data-science/cook-inlet-catalogs/blob/main/docs/demo_notebooks/{slug}.ipynb/HEAD)

# {slug}

{cat.metadata['summary']}

"""

    imports_cell = nbf.v4.new_code_cell(imports)
    text_cell = nbf.v4.new_markdown_cell(text)
    nb['cells'] = [imports_cell, text_cell]
    
    code = f"""\
cat = intake.open_catalog(cic.utils.cat_path("{slug}"))"""
    code_cell = nbf.v4.new_code_cell(code)

    nb['cells'] += [code_cell]
    
    text = f"""\
## Plot all datasets in catalog
"""
    text_cell = nbf.v4.new_markdown_cell(text)

    code = f"""\
dd, ddlabels = cic.utils.combine_datasets_for_map(cat)
dd.hvplot(**cat.metadata["map"]) * ddlabels.hvplot(**cat.metadata["maplabels"])
"""
    code_cell = nbf.v4.new_code_cell(code)
    nb['cells'] += [text_cell, code_cell]

    
    text = f"""\
## List available datasets in the catalog
"""
    text_cell = nbf.v4.new_markdown_cell(text)

    code = f"""\
dataset_ids = list(cat)
dataset_ids
"""
    code_cell = nbf.v4.new_code_cell(code)
    nb['cells'] += [text_cell, code_cell]

    
    text = f"""\
## Select one dataset to investigate
"""
    text_cell = nbf.v4.new_markdown_cell(text)

    code = f"""\
dataset_id = dataset_ids[2]
print(dataset_id)

dd = cat[dataset_id].read()
dd
"""
    code_cell = nbf.v4.new_code_cell(code)
    nb['cells'] += [text_cell, code_cell]

    
    text = f"""\
## Plot one dataset
"""
    text_cell = nbf.v4.new_markdown_cell(text)

    dataset_ids = list(cat)
    dataset_id = dataset_ids[2]
    keys = list(cat[dataset_id].metadata["plots"].keys())
    # for key in keys:
    #     if "dynamic" in cat[dataset_id].metadata["plots"][key]:
    #         cat.get_entity(dataset_id).metadata.update({"plots": {key: {"dynamic": False}}})
    #         # cat[dataset_id].metadata["plots"][key]["dynamic"] = False

    # dynamic should be True to use in notebooks but False for when compiling for docs
    # have to change this in the metadata
    code = f"""\
keys = list(cat[dataset_id].metadata["plots"].keys())
print(keys)

key = keys[0]

plot_kwargs1 = cat[dataset_id].metadata["plots"][key]
if "clim" in plot_kwargs1 and isinstance(plot_kwargs1["clim"], list):
    plot_kwargs1["clim"] = tuple(plot_kwargs1["clim"])
if "dynamic" in plot_kwargs1:
    plot_kwargs1["dynamic"] = False
"""

    # import pdb; pdb.set_trace()
    plot_code = f"cat[dataset_id].ToHvPlot(**plot_kwargs1).read()"

    if "direction" in keys:

        code += f"""\

key = keys[1]

plot_kwargs2 = cat[dataset_id].metadata["plots"][key]
if "clim" in plot_kwargs2 and isinstance(plot_kwargs2["clim"], list):
    plot_kwargs2["clim"] = tuple(plot_kwargs2["clim"])
"""

        plot_code += f" * cat[dataset_id].ToHvPlot(**plot_kwargs2).read()"


    # import pdb; pdb.set_trace()


    # if key == "direction":
# key = keys[1] 
# plot_kwargs2 = cat[dataset_id].metadata["plots"][key]
# if "clim" in plot_kwargs2:
#     plot_kwargs2["clim"] = tuple(plot_kwargs2["clim"])

    code_cell = nbf.v4.new_code_cell(code)
    plot_cell = nbf.v4.new_code_cell(plot_code)
    nb['cells'] += [text_cell, code_cell, plot_cell]
    
    nbf.write(nb, f'demo_notebooks/{slug}.ipynb')

if __name__ == "__main__":
    
    for slug in cic.slugs:
        write_nb(slug)