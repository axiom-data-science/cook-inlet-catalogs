---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
---

```{code-cell}
import intake
import hvplot.pandas
import hvplot.xarray
import cook_inlet_catalogs as cic
import holoviews as hv
```

# Drifters (EPSCoR)

Alaska EPSCoR Drifter Deployment

* Several drifters are run at a time.
* Data portal: [https://ak-epscor.portal.axds.co/](https://ak-epscor.portal.axds.co/)
* Data page: [https://ak-epscor.portal.axds.co/#metadata/e773c142-c003-4441-a32a-8656e051f630/project/folder_metadata/5826151](https://ak-epscor.portal.axds.co/#metadata/e773c142-c003-4441-a32a-8656e051f630/project/folder_metadata/5826151)
* files: [https://ak-epscor.portal.axds.co/#metadata/e773c142-c003-4441-a32a-8656e051f630/project/files](https://ak-epscor.portal.axds.co/#metadata/e773c142-c003-4441-a32a-8656e051f630/project/files)
* Descriptive summary of drifter deployment: [https://www.alaska.edu/epscor/about/newsletters/May-2022-feature-current-events.php](https://www.alaska.edu/epscor/about/newsletters/May-2022-feature-current-events.php)



```{code-cell}
cat = intake.open_catalog(cic.utils.cat_path("drifters_epscor"))
```

## Plot all datasets in catalog

```{code-cell}
dd, ddlabels = cic.utils.combine_datasets_for_map(cat)
dd.hvplot(**cat.metadata["map"]) * ddlabels.hvplot(**cat.metadata["maplabels"])
```

## List available datasets in the catalog

```{code-cell}
dataset_ids = list(cat)
dataset_ids
```

## Select one dataset to investigate

```{code-cell}
try:
    dataset_id = dataset_ids[2]
except:
    dataset_id = dataset_ids[0]
print(dataset_id)

dd = cat[dataset_id].read()
dd
```

## Plot one dataset

```{code-cell}
keys = list(cat[dataset_id].metadata["plots"].keys())
print(keys)

plots = []
for key in keys:
    plot_kwargs = cat[dataset_id].metadata["plots"][key]
    if "clim" in plot_kwargs and isinstance(plot_kwargs["clim"], list):
        plot_kwargs["clim"] = tuple(plot_kwargs["clim"])
    if "dynamic" in plot_kwargs:
        plot_kwargs["dynamic"] = False
    plots.append(cat[dataset_id].ToHvPlot(**plot_kwargs).read())
hv.Layout(plots).cols(1)
```
