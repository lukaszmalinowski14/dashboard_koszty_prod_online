import plotly.express as px
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
import streamlit as st
import pandas as pd
import sys
from datetime import datetime
from dateutil import parser

# sys.path.append('/home/adminuser/venv/lib/site-packages')
# sys.path.append('/home/adminuser/venv/lib/site-packages/st_aggrid')
# import os
# import warnings
# import openpyxl as pl
# , DataReturnMode, ColumnsAutoSizeMode

# warnings.filterwarnings('ignore')

st.set_page_config(page_title="Superstore!!!",
                   page_icon=":bar_chart:", layout="wide")
st.title(" :bar_chart: Analiza kosztów produkcji")
st.markdown(
    '<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# okno do wczytywania danych

fl = st.file_uploader(":file_folder: Upload a file",
                      type=(["csv", "txt", "xlsx", "xls"]))


@st.cache_data
def load_data():
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(fl, sheet_name="Arkusz1")
    # os.chdir(r"C:\Users\AEPAC\Desktop\Streamlit")
    # df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")
    if df.empty:
        st.write(" ### Załaduj dane")
    return df


df = load_data()
# df['data_wystawienia_wz'] = pd.to_datetime(
#     df['data_wystawienia_wz'], format='%Y-%m-%d')


# FILTRY
st.sidebar.header("Choose your filter: ")
min_date = df["data_wystawienia_wz"].min()
max_date = df["data_wystawienia_wz"].max()


filter_min_date = st.sidebar.date_input("Start", value=min_date)
filter_max_date = st.sidebar.date_input("End", value=max_date)


# Create a list containing the start and end dates

month = filter_min_date.month
day = filter_min_date.day
year = filter_min_date.year
date_min_str = str(day)+'.'+str(month)+'.'+str(year)

# Convert the string to a date
date_min = datetime.strptime(date_min_str, "%d.%m.%Y")
month = filter_max_date.month
day = filter_max_date.day
year = filter_max_date.year
date_min_str = str(day)+'.'+str(month)+'.'+str(year)
date_max = datetime.strptime(date_min_str, "%d.%m.%Y")

# Filter the DataFrame based on the date range
df_filtered = df.loc[(df["data_wystawienia_wz"] >= date_min)
                     & (df["data_wystawienia_wz"] <= date_max)]


# Create for date
# towar = st.sidebar.selectbox(
#     "Pick your towar", df["klucz_towaru_wz"].unique())


# df z towarem i wartością sprzedaży w wybranym przedziale czasu
df_towar = df_filtered.groupby('klucz_towaru_wz').agg(
    wartosc_pln=('wartosc_pln', 'sum'),
    zysk=('przychod_posr_tech', 'sum')
).reset_index()


# Sortowanie nowego DataFrame po sumie wartości sprzedaży:
df_towar = df_towar.sort_values(
    by='wartosc_pln', ascending=False).reset_index(drop=True)
# Zaokrąglenie sumy wartości sprzedaży do pełnych tysięcy:
df_towar['wartosc_pln'] = df_towar['wartosc_pln'].apply(
    lambda x: round(x, 0))
# df_towar['suma_wartosc'] = df_towar["wartosc_pln"].sum()

##########################################
gd = GridOptionsBuilder.from_dataframe(df_towar)
# gd.configure_pagination(enabled=True)
# gd.configure_default_column(editable=True, groupable=True)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions = gd.build()

########################################
# podsumowanie wybranego okresu:

st.divider()
st.header("Podsumowanie:")
sprzedaz_total = df_filtered['wartosc_pln'].sum()
formated_sprzedaz_total = "{:,.0f}".format(sprzedaz_total).replace(",", " ")
zysk_total = df_filtered['przychod_posr_tech'].sum()
formated_zysk_total = "{:,.0f}".format(zysk_total).replace(",", " ")
marza = zysk_total/sprzedaz_total
formated_marza_total = "{:.0%}".format(marza)

col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"## Sprzedaż: {formated_sprzedaz_total} PLN")
with col2:
    st.write(f"## Zysk: {formated_zysk_total} PLN")
with col3:
    st.write(
        f"## Marża: {formated_marza_total}")
st.divider()
########################################
st.header("Towary:")

grid_table = AgGrid(df_towar, gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    height=300,
                    allow_unsafe_jscode=True,
                    # enable_enterprise_modules = True,
                    theme='balham')

sel_row = grid_table["selected_rows"]
# st.write(sel_row)
# st.write(type(sel_row))
towar = sel_row[0]["klucz_towaru_wz"]


##########################################
st.divider()
# wyswietlanie statystyk wybranego towaru
zysk = sel_row[0]["zysk"]
formated_zysk = "{:,.0f}".format(zysk).replace(",", " ")
sprzedaz = sel_row[0]["wartosc_pln"]
formated_sprzedaz = "{:,.0f}".format(sprzedaz).replace(",", " ")
marza = zysk/sprzedaz
formated_marza = "{:.0%}".format(marza)

col1, col2, col3 = st.columns(3)
with col1:
    st.write("## Wybrany towar: "+str(towar))
with col2:
    st.write(f"## Zysk: {formated_zysk} PLN")
with col3:
    st.write(
        f"## Sprzedaż: {formated_sprzedaz} PLN, \n ## Marża: {formated_marza}")
st.divider()
#######################################

# wyswietlanie wyników
cl1, cl2 = st.columns(2)
with cl1:

    # wyswietlenie wykresu analitycznego z parametrami zysku
    # # jednostkowy koszty zakup
    # df_koszt_zakup = df[df['klucz_towaru_wz'] == 'GL00001114930']
    # df_koszt_zakup = df_koszt_zakup[['data_wystawienia_wz',
    #                                 'jednostkowy_koszt_zakup']]
    # # st.dataframe(df_koszt_zakup)
    # scatter_zakup = px.scatter(
    #     df_koszt_zakup, x="data_wystawienia_wz", y="jednostkowy_koszt_zakup")
    # st.write(scatter_zakup)

    # # jednostkowy koszty koop
    # df_koszt_koop = df[df['klucz_towaru_wz'] == 'GL00001114930']
    # df_koszt_koop = df_koszt_koop[['data_wystawienia_wz',
    #                                'jednostkowy_koszt_koop']]
    # # st.dataframe(df_koszt_zakup)
    # df_koszt_koop = px.scatter(
    #     df_koszt_koop, x="data_wystawienia_wz", y="jednostkowy_koszt_koop")
    # st.write(df_koszt_koop)

    # wszystko na jednym
    df_koszty_all = df_filtered[df_filtered['klucz_towaru_wz'] == towar]
    df_koszty_all = df_koszty_all[['data_wystawienia_wz',
                                   'jednostkowy_koszt_koop', 'jednostkowy_koszt_zakup', 'jednostkowy_koszt_mterialu', 'jednostkowy_koszt_operacji_posr_tech']]
    # Tworzenie wykresu scatter
    fig_all = px.scatter(df_koszty_all, x='data_wystawienia_wz', y=['jednostkowy_koszt_koop', 'jednostkowy_koszt_zakup', 'jednostkowy_koszt_mterialu', 'jednostkowy_koszt_operacji_posr_tech'], color_discrete_map={
        'jednostkowy_koszt_koop': 'green', 'jednostkowy_koszt_zakup': 'blue'}, trendline="ols")

    # Ustawienia wyglądu wykresu
    fig_all.update_layout(title=towar,
                          xaxis_title='X-axis',
                          yaxis_title='Y-axis',
                          legend_title='Legend',
                          width=800,  # Dostosuj szerokość
                          # height=600  # Dostosuj wysokość
                          )
    st.write(fig_all)

with cl2:

    df_koszty_wsp = df_filtered[df_filtered['klucz_towaru_wz'] == towar]
    fig_marza = px.scatter(df_koszty_wsp, x='data_wystawienia_wz', y=[
                           'marza_posr_tech'], trendline="ols")
    st.write(fig_marza)
#################
# st.write(df)
st.write(df_filtered)


# cl3, cl4 = st.columns(2)
# # Represent only large countries
# with cl3:
#     st.dataframe(df_towar.style.format(thousands=" ", precision=0))

# with cl4:
#     df_towar_chart = df_towar.query('wartosc_pln > 30000')
#     st.dataframe(df_towar_chart.style.format(thousands=" ", precision=0))
#     fig = px.pie(df_towar_chart, values='wartosc_pln', names='klucz_towaru_wz',
#                  title='Population of European continent')
#     st.write(fig)
