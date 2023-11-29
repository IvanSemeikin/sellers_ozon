# import subprocess
# subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Функция для загрузки данных из файла на GitHub
def load_data(file_path):
    full_path = f'{file_path}.xlsx'
    data = pd.read_excel(full_path)
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    return data

# Функция для определения таблиц для графиков
def show_data(button_name):
    # Таблица продавцов-лидеров по продажам
    sellers_data_sales = load_data(f"Общая_таблица_проценты_{button_name.lower()}_sales")
    sellers_data_revenue = load_data(f"Общая_таблица_проценты_{button_name.lower()}_revenue")
    # Проверка и приведение данных к DataFrame
    if not isinstance(sellers_data_sales, pd.DataFrame):
        sellers_data_sales = pd.DataFrame(sellers_data_sales)
    if not isinstance(sellers_data_revenue, pd.DataFrame):
        sellers_data_revenue = pd.DataFrame(sellers_data_revenue)
    return sellers_data_sales, sellers_data_revenue


# Отображение таблицы с долей лидера от всей категории
def show_table_percentage(button_name):
    st.header(f"Доля лидера от всей категории || {button_name}")

    # Загрузка данных по продажам
    sales_data = load_data(f"Общая_таблица_проценты_{button_name.lower()}_sales")
    st.subheader(f"Доля лидера от всей категории")
    st.dataframe(sales_data)
    
# Отображение таблицы с топ продавцами   
def show_table_top_sellers(button_name, metric_type):
    st.header(f"Топ продавцов по {metric_type.capitalize()} || {button_name}")

    # Таблица продавцов-лидеров по продажам
    sellers_data_sales = load_data(f"Общая_таблица_продавцы_{button_name.lower()}_sales")
    st.subheader(f"Топ продавцов по {metric_type.capitalize()}")
    st.dataframe(sellers_data_sales)
    
# Отображение графика для продаж
def show_graph_top_sellers_sales(button_name, metric_type):
    st.header(f"График топ продавцов по {metric_type.capitalize()} || {button_name}")

    # Линейный график по продавцам-лидерам
    melted_sellers_data_sales = pd.melt(sellers_data_sales, id_vars=['Category'], var_name='Month', value_name='Sales')
    available_seller_categories = melted_sellers_data_sales['Category'].unique()

    # Генерация уникального ключа для виджета st.multiselect
    multiselect_key = f"multiselect_{button_name}_{metric_type}"
    
    selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, key=multiselect_key, default=available_seller_categories)
    filtered_sellers_data_sales = melted_sellers_data_sales[melted_sellers_data_sales['Category'].isin(selected_seller_categories)]
    fig_sellers = px.line(filtered_sellers_data_sales, x='Month', y='Sales', color='Category', title=f'Top Sellers by {metric_type.capitalize()}')
    st.plotly_chart(fig_sellers)

# Отображение графика для выручки
def show_graph_top_sellers_revenue(button_name, metric_type):
    st.header(f"График топ продавцов по {metric_type.capitalize()} || {button_name}")

    # Линейный график по продавцам-лидерам
    melted_sellers_data_revenue = pd.melt(sellers_data_revenue, id_vars=['Category'], var_name='Month', value_name='Sales')
    available_seller_categories = melted_sellers_data_revenue['Category'].unique()

    # Генерация уникального ключа для виджета st.multiselect
    multiselect_key = f"multiselect_{button_name}_{metric_type}"
    
    selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, key=multiselect_key, default=available_seller_categories)
    filtered_sellers_data_revenue = melted_sellers_data_revenue[melted_sellers_data_revenue['Category'].isin(selected_seller_categories)]
    fig_sellers = px.line(filtered_sellers_data_revenue, x='Month', y='Sales', color='Category', title=f'Top Sellers by {metric_type.capitalize()}')
    st.plotly_chart(fig_sellers)




# Основной код Streamlit
text = "<h1 style='text-align: center;'>Привет! Здесь информация по продавцам <font color='blue'>OZON</font><br>(по <font color='red'>WB</font> появится в следующем релизе)</h1>"
st.markdown(text, unsafe_allow_html=True)

# Выбор кнопки
selected_button = st.radio("Выберите категорию:", ["fbo", "fbs", "retail", "crossborder", "total"])

# попробую новые функции
show_table_percentage(selected_button)
show_table_percentage(selected_button)
show_table_top_sellers(selected_button, "sales")
show_table_top_sellers(selected_button, "revenue")
sellers_data_sales, sellers_data_revenue = show_data(selected_button)
show_graph_top_sellers_sales(selected_button, "sales")
show_graph_top_sellers_revenue(selected_button, "revenue")
# *********************************************************************************************************

st.header("ПОПЫТКА СДЕЛАТЬ БОЛЬШЕ ФИЛЬТРОВ")
st.header("Более удобный просмотр категорий")

# Выбор кнопки
selected_button_cat = st.radio("Выберите категорию еще раз:", ["fbo", "fbs", "retail", "crossborder", "total"])
sellers_data_sales_new, sellers_data_revenue_new = show_data(selected_button_cat)

# # Разделяем индекс на три столбца
# sellers_data_sales_new[['cat_level_1', 'cat_level_2', 'cat_level_3']] = sellers_data_sales_new['Category'].str.split('_', expand=True)
# # Переупорядочиваем столбцы
# sellers_data_sales_new = sellers_data_sales_new[['cat_level_1', 'cat_level_2', 'cat_level_3'] + months_names]
def filter_dataframe(df):
    # Получаем уникальные значения для каждого уровня категории
    cat_level_1_options = df['Category'].apply(lambda x: x.split('_')[0]).unique()

    # Выбор первого уровня
    selected_cat_level_1 = st.selectbox('Выбери первый уровень', cat_level_1_options)

    # Фильтруем DataFrame по выбранному первому уровню
    filtered_df_level_1 = df[df['Category'].apply(lambda x: x.split('_')[0]) == selected_cat_level_1]

    # Выбор второго уровня, добавив вариант "Все варианты"
    cat_level_2_options = ['Все варианты'] + filtered_df_level_1['Category'].apply(lambda x: x.split('_')[1]).unique().tolist()
    selected_cat_level_2 = st.selectbox('Выбери второй уровень', cat_level_2_options)

    # Фильтруем DataFrame по выбранному второму уровню, если не выбран "Все варианты"
    if selected_cat_level_2 != 'Все варианты':
        filtered_df_level_2 = filtered_df_level_1[filtered_df_level_1['Category'].apply(lambda x: x.split('_')[1]) == selected_cat_level_2]
    else:
        filtered_df_level_2 = filtered_df_level_1

    # Выбор третьего уровня, добавив вариант "Все варианты"
    cat_level_3_options = ['Все варианты'] + filtered_df_level_2['Category'].apply(lambda x: x.split('_')[2]).unique().tolist()
    selected_cat_level_3 = st.selectbox('Выбери третий уровень', cat_level_3_options)

    # Фильтруем DataFrame по выбранным уровням, если не выбран "Все варианты"
    if selected_cat_level_3 != 'Все варианты':
        final_filtered_df = filtered_df_level_2[filtered_df_level_2['Category'].apply(lambda x: x.split('_')[2]) == selected_cat_level_3]
    else:
        final_filtered_df = filtered_df_level_2

    # Выводим отфильтрованный DataFrame
    st.write('Отфильтрованный DataFrame:', final_filtered_df)
    return final_filtered_df
df_graphic = filter_dataframe(sellers_data_sales_new)

def line_chart_from_dataframe(df):
    st.header("Линейный график")

    # Удалим столбец 'Category' и сделаем его индексом
    df.set_index('Category', inplace=True)

    # Транспонируем датафрейм
    df_transposed = df.T

    # Строим линейный график
    fig = px.line(df_transposed, title="Линейный график")

    # Отображаем график
    st.plotly_chart(fig)
    
line_chart_from_dataframe(df_graphic)

# *************************************************************************************************************
st.header("Топ категорий в выбранный месяц")
# Получаем список названий столбцов - месяцев для выпадающего списка
months_names = sellers_data_sales_new.columns.tolist()
# Выпадающий список
selected_option_month = st.selectbox('Выбери месяц', months_names)

