# %%
import pandas as pd

# import dtale
import plotly.express as px

def str_to_seconds(x):
    if isinstance(x, str):
        hours, minutes, seconds = x.split(":")
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

def replace_months(x:str):
    x = x.replace("janvier", "01")
    x = x.replace("février", "02")
    x = x.replace("mars", "03")
    x = x.replace("avril", "04")
    x = x.replace("mai", "05")
    x = x.replace("juin", "06")
    x = x.replace("juillet", "07")
    x = x.replace("août", "08")
    x = x.replace("septembre", "09")
    x = x.replace("octobre", "10")
    x = x.replace("novembre", "11")
    x = x.replace("décembre", "12")
    return x

# %%
df_duree = pd.read_csv(
    "data/barometre-jt-durees.csv",
    sep=";",
    encoding="latin",
    skiprows=2,
    names=[
        "date",
        "thematique",
        "TF1",
        "France2",
        "France3",
        "Canal+",
        "Arte",
        "M6",
        "Total",
        "nan",
    ],
)

df_duree.drop(columns=["nan"], inplace=True)

df_duree["date"] = df_duree["date"].map(replace_months)

df_duree["date"] = pd.to_datetime(df_duree["date"], format="%m-%y")

df_duree = df_duree.melt(
        id_vars=["date", "thematique"],
        var_name="chaine",
        value_vars=[
            "TF1", 
            "France2", 
            "France3", 
            "Canal+", 
            "Arte", 
            "M6",
            "Total",
            ],
        value_name="duree",
    )

df_duree["duree"] = df_duree["duree"].map(str_to_seconds)


# %%
df_sujets = pd.read_csv(
    "data/barometre-jt-sujets.csv",
    sep=";",
    encoding="latin",
    skiprows=2,
    names=[
        "date",
        "thematique",
        "TF1",
        "France2",
        "France3",
        "Canal+",
        "Arte",
        "M6",
        "Total",
        "nan",
    ],
)

df_sujets.drop(columns=["nan"], inplace=True)

df_sujets["date"] = df_sujets["date"].map(replace_months)

df_sujets["date"] = pd.to_datetime(df_sujets["date"], format="%m-%y")

df_sujets = df_sujets.melt(
        id_vars=["date", "thematique"],
        var_name="chaine",
        value_vars=[
            "TF1", 
            "France2", 
            "France3", 
            "Canal+", 
            "Arte", 
            "M6",
            "Total",
            ],
        value_name="sujets",
    )

# %%
df = df_duree.merge(
    df_sujets, 
    on=["date", "thematique", "chaine"]
    )

df.head()

# %%
df_plot = df[df["chaine"] != "Total"]

# round to year
df_plot["date"] = df_plot["date"].dt.year
             
df_plot = df_plot.groupby(["date", "thematique", "chaine"]).sum(numeric_only=True).reset_index()

df_total_theme = df_plot.groupby(["date", "chaine"]).sum(numeric_only=True).reset_index()

df_plot = df_plot.merge(df_total_theme, on=["date", "chaine"], suffixes=("", "_total"), how="left")

df_plot["sujet_pourcent"] = df_plot["sujets"] / df_plot["sujets_total"]

# sort by channel
df_plot = df_plot.sort_values(
    by=[
        "chaine",
        "date"
        ], 
    key=lambda x: x.map({"TF1": 1, "France2": 2, "France3": 3, "Canal+": 4, "Arte": 5, "M6": 6})
    )

animated_plot = px.bar(
    df_plot,
    x="thematique",
    y="sujet_pourcent",
    color="chaine",
    color_discrete_map={
        "TF1": "#081E9B",
        "France2": "#FD1A32",
        "France3": "#01B2FF",
        "Canal+": "black",
        "Arte": "#FA4D23",
        "M6": "#8C95AE",
    },
    barmode="group",
    animation_frame="date",
    animation_group="thematique",
    # range_y=[0, 3600],
    title="Nombre de sujets par thématique et par chaîne",
)

# slow animation
animated_plot.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2500

# update y axis to percentage
animated_plot.update_yaxes(tickformat=".0%")

# x axis sort by y value
animated_plot.update_xaxes(categoryorder="mean descending")

animated_plot.show()

animated_plot.write_html("output/jt-animated.html")

# %%
# df_plot = df[df["chaine"] == "Total"]

# # round to year
# df_plot["date"] = df_plot["date"].dt.year
             
# df_plot = df_plot.groupby(["date", "thematique"]).sum(numeric_only=True).reset_index()

# df_total_theme = df_plot.groupby(["date"]).sum(numeric_only=True).reset_index()

# df_plot = df_plot.merge(df_total_theme, on="date", suffixes=("", "_total"), how="left")

# df_plot["sujet_pourcent"] = df_plot["sujets"] / df_plot["sujets_total"]

# animated_plot = px.bar(
#     df_plot,
#     x="thematique",
#     y="sujet_pourcent",
#     # color="chaine",
#     animation_frame="date",
#     animation_group="thematique",
#     # range_y=[0, 3600],
#     title="Nombre de sujets par thématique et par chaîne",
# )

# # slow animation
# animated_plot.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2500

# # update y axis to percentage
# animated_plot.update_yaxes(tickformat=".0%")

# # x axis sort by y value
# animated_plot.update_xaxes(categoryorder="total descending")

# animated_plot.show()
# %%
