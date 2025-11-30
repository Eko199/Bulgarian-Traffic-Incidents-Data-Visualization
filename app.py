# app.py
import streamlit as st
import time
import analogueClock as ac
import dataConverter as dc
import graphMaker as gm
from streamlit_folium import st_folium


st.set_page_config(page_title="ПТП данни", layout="centered")

st.title("Визуализация на данни за ПТП в България от 01.01.2025 г. до 30.06.2025 г.")

placeholder = st.empty()

st.markdown("<h3 style='text-align: center; color: black;'>Брой ПТП в часови интервал за ден от седмицата</h3>", unsafe_allow_html=True)


#Day selector
selected_day = st.select_slider(
    "Изберете ден от седмицата:",
    options=dc.WEEKDAYS,
    value=dc.WEEKDAYS[0]
)

#Display clocks side by side
col1, col2 = st.columns(2)

with col1:
    st.write("### AM Clock")
    fig_am = ac.analogue_clock(dc.DATA_HOUR[selected_day], "am")
    st.pyplot(fig_am)

with col2:
    st.write("### PM Clock")
    fig_pm = ac.analogue_clock(dc.DATA_HOUR[selected_day], "pm")
    st.pyplot(fig_pm)

#Color legend 
st.markdown("<h6 style='text-align: center; color: black;'>Легенда за цветове - Брой ПТП</h6>", unsafe_allow_html=True)

legend_labels = [
    "0-3", "4-7", "8-14", "15-25", "26-35", "36-45", "46-50", ">51"
]

legend_labels = ["0-3", "4-7", "8-14", "15-25", "26-35", "36-45", "46-50", ">51"]

legend_cols = st.columns(len(legend_labels))
for i, label in enumerate(legend_labels):
    with legend_cols[i]:
        # Combine AM/PM colors in one box with label below
        st.markdown(
            f"""
            <div style='text-align:center'>
                <div style='background-color:{ac.colorsDay[i]};height:15px;margin-bottom:2px'></div>
                <div style='background-color:{ac.colorsNight[i]};height:15px;margin-bottom:2px'></div>
                <div style='font-size:12px'>{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

#Display pie charts side by side
st.header("Разпределение по дни от седмицата")
c1,c2=st.columns(2)
with c1:
    st.plotly_chart(gm.make_pie_chart(), use_container_width=True)
with c2:
    st.plotly_chart(gm.make_pie_chart(_values='Ранени', _title='ранени'), use_container_width=True)    

st.markdown("<h5 style='text-align: center; color: black;'>загинали</h5>", unsafe_allow_html=True)
st.plotly_chart(gm.make_pie_chart(_values='Загинали', _title=''), use_container_width=True)

st.header("🚦 ПТП по часове")

options = st.multiselect(
    "Изберете показатели за визуализация:",
    ['ПТП - общо', 'Загинали - общо', 'Ранени - общо'],
    default=['ПТП - общо']  # default selection
)

if not options:
    st.warning("Моля, изберете поне един показател.")
    st.stop()

st.header("ПТП по часове — Анимирана графика")
st.plotly_chart(gm.make_bar_chart_animated(options), use_container_width=True)  

st.header("ПТП по часове — графика")
st.plotly_chart(gm.make_bar_chart(options), use_container_width=True)

st.header("Карта на България с ПТП по области (01.01.2025 - 30.06.2025)")
st_data = st_folium(gm.map(), width=1225, height=700)

