from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
import streamlit as st
import plotly.express as px
import pandas as pd
import sys
sys.path.append('/home/adminuser/venv/lib/python3.9/site-packages')
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
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_excel(fl, sheet_name="Arkusz1")
    else:
        # os.chdir(r"C:\Users\AEPAC\Desktop\Streamlit")
        # df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")
        st.write(" ### Załaduj dane")
    return df


df = load_data()


# FILTRY
st.sidebar.header("Choose your filter: ")
# Create for Region
# towar = st.sidebar.selectbox(
#     "Pick your towar", df["klucz_towaru_wz"].unique())


# df z towarem i wartością sprzedaży w wybranym przedziale czasu
df_towar = df.groupby('klucz_towaru_wz')['wartosc_pln'].sum().reset_index()
# Sortowanie nowego DataFrame po sumie wartości sprzedaży:
df_towar = df_towar.sort_values(
    by='wartosc_pln', ascending=False).reset_index(drop=True)
# Zaokrąglenie sumy wartości sprzedaży do pełnych tysięcy:
df_towar['wartosc_pln'] = df_towar['wartosc_pln'].apply(
    lambda x: round(x, 0))

##########################################
gd = GridOptionsBuilder.from_dataframe(df_towar)
# gd.configure_pagination(enabled=True)
# gd.configure_default_column(editable=True, groupable=True)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions = gd.build()
st.header("This is Agrid table")

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


# def dataframe_with_selections(df_towar):
#     df_with_selections = df_towar.copy()
#     df_with_selections.insert(0, "Select", False)

#     # Get dataframe row-selections from user with st.data_editor
#     edited_df = st.data_editor(
#         df_with_selections,
#         hide_index=True,
#         column_config={
#             "Select": st.column_config.CheckboxColumn(required=True)},
#         disabled=df_towar.columns,
#     )

#     # Filter the dataframe using the temporary column, then drop the column
#     selected_rows = edited_df[edited_df.Select].reset_index()
#     return selected_rows.drop('Select', axis=1)


# selection = dataframe_with_selections(df_towar)
# st.write("Your selection:")
# st.write(selection)
# st.write(selection.iloc[-1])
####################################


# # Pobranie indeksu ostatnio zaznaczonego wiersza z sesji
# last_selected_row_index = st.session_state.get(session_key, 0)

# # Utworzenie edytowalnego DataFrame za pomocą widgetu st.data_editor
# edited_df = st.data_editor(df_towar)
# edited_df.insert(0, "Select", False)
# # Sprawdź, czy coś zostało zaznaczone
# if not edited_df.empty:
#     # Pobierz indeksy zaznaczonych wierszy
#     selected_rows = edited_df.index.tolist()

#     # Sprawdź, czy indeksy zaznaczonych wierszy różnią się od ostatnio zaznaczonego
#     if selected_rows != [last_selected_row_index]:
#         # Zaktualizuj ostatnio zaznaczony indeks w sesji
#         st.session_state[session_key] = selected_rows[-1]

#         # Wyświetl informacje o ostatnim zaznaczonym wierszu
#         st.markdown(f"Last selected row: {selected_rows[-1]}")

# # Jeśli nic nie jest zaznaczone, wyświetl ostrzeżenie
# else:
#     st.warning("Please select a row in the data editor.")
####################################

# # Ustawienie klucza sesji
# session_key = "selected_row_index"

# # Pobranie indeksu zaznaczonego wiersza z sesji
# selected_row_index = st.session_state.get(session_key, 0)

# # Utworzenie edytowalnego DataFrame za pomocą widgetu st.table
# edited_df = st.data_editor(df_towar, key=session_key)

# # Sprawdź, czy coś zostało zaznaczone
# if not edited_df.empty:
#     # Pobierz wartość w kolumnie "command" z zaznaczonego wiersza
#     # favorite_command = edited_df[selected_row_index]["klucz_towaru_wz"]
#     st.write(selected_row_index)
# st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
# else:
#     st.warning("Please select a row in the data editor.")

####################################
# gb = GridOptionsBuilder.from_dataframe(df_towar)
# gb.configure_selection(selection_mode="single", use_checkbox=True)
# gb.configure_side_bar()
# gridOptions = gb.build()

# data = AgGrid(df_towar,
#               gridOptions=gridOptions,
#               enable_enterprise_modules=True,
#               allow_unsafe_jscode=True,
#               update_mode=GridUpdateMode.SELECTION_CHANGED,
#               columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)

# # selected_rows = data["selected_rows"]

# # if len(selected_rows) != 0:
# #    selected_rows[0]


# st.write("Your selection:")
# # st.write(selection)


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
    df_koszty_all = df[df['klucz_towaru_wz'] == towar]
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

    df_koszty_wsp = df[df['klucz_towaru_wz'] == towar]
    fig_marza = px.scatter(df_koszty_wsp, x='data_wystawienia_wz', y=[
                           'marza_posr_tech'], trendline="ols")
    st.write(fig_marza)
#################
st.write(df)


cl3, cl4 = st.columns(2)
# Represent only large countries
with cl3:
    st.dataframe(df_towar.style.format(thousands=" ", precision=0))

with cl4:
    df_towar_chart = df_towar.query('wartosc_pln > 30000')
    st.dataframe(df_towar_chart.style.format(thousands=" ", precision=0))
    fig = px.pie(df_towar_chart, values='wartosc_pln', names='klucz_towaru_wz',
                 title='Population of European continent')
    st.write(fig)
