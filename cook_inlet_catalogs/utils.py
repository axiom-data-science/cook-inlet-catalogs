import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pandas as pd
import re
import cf_pandas as cfp

# Set up vocab for universal usage
vocab = cfp.Vocab()
reg = cfp.Reg(include="tem", exclude=["F_","qc","air","dew"], ignore_case=True)
vocab.make_entry("temp", reg.pattern(), attr="name")
reg = cfp.Reg(include="sal", exclude=["F_","qc"], ignore_case=True)
vocab.make_entry("salt", reg.pattern(), attr="name")
vocab.make_entry("station", ["station", "Station"], attr="name")
cfp.set_options(custom_criteria=vocab.vocab)


def select_station(df, station):
    dd = df[df.cf["station"] == station]
    idup = ~dd.index.duplicated()
    return dd.iloc[idup]


def is_key(s):
    """to list keys in intake catalog"""
    # Check if the string is a 16-character hexadecimal string
    if re.fullmatch(r'[a-fA-F0-9]{16}', s):
        return False
    else:
        return True


def parse_dates(Year, Month, Day, Hour, Minute):    
    date_str = f"{Year}-{Month}-{Day} {Hour}:{Minute}"
    return pd.to_datetime(date_str, format='%Y-%m-%d %H:%M')


def parse_dates_doy(df: pd.DataFrame) -> pd.DataFrame:
    return pd.to_datetime(df.year.str.cat(df.day_of_year).astype(str).str.cat(df.time_utc), format='%Y%j%H%M')


def plot_map(df, drifter_id, res='10m'):

    # Map
    pc = ccrs.PlateCarree()
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    land = cfeature.NaturalEarthFeature('physical', 'land', res,
                                    edgecolor='face',
                                    facecolor='#F0EFE4')
    ax.add_feature(land)
    ocean = cfeature.NaturalEarthFeature('physical', 'ocean', '10m',
                                     edgecolor='face',
                                     facecolor=cfeature.COLORS['water'])
    ax.add_feature(land)

    # ax.add_feature(cfeature.LAND)
    # ax.add_feature(cfeature.OCEAN)
    # ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    
    # Add high resolution coastline feature
    ax.coastlines(resolution='10m')

    ax.tick_params(left=False, labelleft=False)

    # Add gridlines and labels
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='gray', alpha=0.5, linestyle='-')
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 15}
    gl.ylabel_style = {'size': 15}

    # Drifter
    lonkey, latkey, Tkey = df.cf["longitude"].name, df.cf["latitude"].name, df.cf["T"].name
    df.plot(x=lonkey, y=latkey, ax=ax, legend=False, transform=pc, color="r", label="")
    ax.plot(df.iloc[0][lonkey], df.iloc[0][latkey], "go", ms=15, mec="k", transform=pc, label="start")
    ax.plot(df.iloc[-1][lonkey], df.iloc[-1][latkey], "ko", ms=15, mec="k", transform=pc, label="end");
    
    title = f"Drifter {drifter_id}: {df[Tkey].iloc[0].date()} to {df[Tkey].iloc[-1].date()}"
    ax.set_title(title)
    plt.legend(loc="best")
    
    return fig
