import plotly.express as px
import pandas as pd
from dataConverter import DATA_DAYS, DATA_ALL_HOURS, get_provinces_GeoJSON, get_nuts3, get_ptp_regions_data

#Map imports
import folium
import branca.colormap as cm

def make_pie_chart(_values='Брой ПТП' , _title='брой ПТП'):
    df = pd.DataFrame(DATA_DAYS)
    fig = px.pie(df, values=_values , names='ден',
                title=_title,
                labels={'Загинали':'Брой загинали', 'Ранени':'Брой ранени', 'Брой ПТП':'Брой ПТП'},
                #hover_data={'Ранени': True, 'Загинали': True}
                )
    #make hover data show
    fig.update_traces(textposition='inside', textinfo='percent+label')

    

    #fig.show()
    return fig



#make_pie_chart()

def make_bar_chart_animated(options):
    df = pd.DataFrame(DATA_ALL_HOURS)
    df_long = df.melt(id_vars='час', 
                  value_vars=options,
                  var_name='Категория',
                  value_name='Стойност')
    fig = px.bar(
        df_long,
        x="Категория",
        y="Стойност",
        color="Категория",
        animation_frame="час",
        barmode="group",
        title="Анимирани ПТП данни по часове"
    )

    # Fix Y-axis so it does NOT change during animation
    y_max = df_long["Стойност"].max()
    fig.update_yaxes(range=[0, y_max])

    #fig.show()
    return fig

def make_bar_chart(options):
    df = pd.DataFrame(DATA_ALL_HOURS)
    df_long = df.melt(id_vars='час', 
                  value_vars=options,
                  var_name='Категория',
                  value_name='Стойност')
    fig = px.bar(
        df_long,
        x="час",
        y="Стойност",
        color="Категория",
        barmode="group",
        title="ПТП статистика по часове (статичен график)"
    )

    fig.update_layout(
        xaxis_title="Час",
        yaxis_title="Брой",
        legend_title="Категории",
        xaxis_tickangle=45,  # makes the hour labels readable
        bargap=0.3,        # space between hour groups (0–1)
        bargroupgap=0.07,   # space between bars in each group
        xaxis_type='category'
    )
    return fig

def map(option: str) -> folium.Map:
    m = folium.Map(location=[42.7, 25.4], zoom_start=7, tiles="CartoDB positron")

    provinces: dict = get_provinces_GeoJSON()
    nuts3: dict = get_nuts3()
    ptp: dict = get_ptp_regions_data()
    
    def sofia_fix(name: str) -> str:
        if name.lower() == "софийска":
            return "софия"
        
        if name.lower() == "софия":
            return "софия (столица)"
        
        return name.lower()
    
    is_percentage: bool = option.strip().endswith("%")
    
    def value_map(val: str) -> int:
            return int(float(val) * 100) if is_percentage else int(val)

    stats = { sofia_fix(item[0]) : value_map(item[ptp[0].index(option)]) for item in ptp[1:-1] }

    colormap = cm.LinearColormap(["green", "yellow", "red"], vmin=vmin, vmax=max(stats.values())) \
            if (vmin := min(stats.values())) < 0 else \
            cm.linear.YlOrBr_06.scale(0, max(stats.values()))
    
    colormap.caption = option

    for feature in provinces["features"]:
        name = next(o for o in nuts3 if o["oblast"] == feature["properties"]["nuts3"])["name"]
        value = stats.get(name.lower(), 0)
        color = colormap(value) if value is not None else "#cccccc"

        folium.GeoJson(
            feature,
            style_function=lambda x, col=color: {
                "fillColor": col,
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7,
            },
            highlight_function=lambda x: {
                "weight": 3,
                "color": "yellow"
            },
            tooltip=folium.Tooltip(
                f"<b>{name}</b><br>{value}%" if is_percentage else f"<b>{name}</b><br>Брой: {value}",
                sticky=True
            ),
        ).add_to(m)

    m.add_child(colormap)
    #m.save("bg_map.html")

    return m