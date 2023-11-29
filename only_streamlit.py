# import subprocess
# subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import random

# Функция для загрузки данных из файла на GitHub
def load_data(file_path):
    full_path = f'{file_path}.xlsx'
    data = pd.read_excel(full_path)
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    return data

# Функция для определения таблиц для графиков
def show_data(button_name):
    sellers_data_sales = load_data(f"Общая_таблица_проценты_{button_name.lower()}_sales")
    sellers_data_revenue = load_data(f"Общая_таблица_проценты_{button_name.lower()}_revenue")

    # Проверка и приведение данных к DataFrame
    if not isinstance(sellers_data_sales, pd.DataFrame):
        sellers_data_sales = pd.DataFrame(sellers_data_sales)
    if not isinstance(sellers_data_revenue, pd.DataFrame):
        sellers_data_revenue = pd.DataFrame(sellers_data_revenue)

    # Создаем копии данных с установленными индексами
    sellers_data_sales_ind = sellers_data_sales.set_index('Category').copy()
    sellers_data_revenue_ind = sellers_data_revenue.set_index('Category').copy()

    return sellers_data_sales_ind, sellers_data_revenue_ind, sellers_data_sales, sellers_data_revenue



# Отображение таблицы с топ продавцами   
def show_table_top_sellers(button_name):
    # Таблица продавцов-лидеров по продажам и выручке
    sellers_sales = load_data(f"Общая_таблица_продавцы_{button_name.lower()}_sales")
    sellers_revenue = load_data(f"Общая_таблица_продавцы_{button_name.lower()}_revenue")
    # Проверка и приведение данных к DataFrame
    if not isinstance(sellers_sales, pd.DataFrame):
        sellers_sales = pd.DataFrame(sellers_data_sales)
    if not isinstance(sellers_revenue, pd.DataFrame):
        sellers_revenue = pd.DataFrame(sellers_data_revenue)
    sellers_sales.set_index('Category', inplace=True)
    sellers_revenue.set_index('Category', inplace=True) 
    return sellers_sales, sellers_revenue
    
# Отображение графика для продаж
def show_graph_top_sellers_sales(button_name, metric_type):
    st.header(f"График по категориям Продажи || {button_name}")

    # Сброс индекса
    sellers_data_sales_reset = sellers_data_sales.reset_index()

    # Линейный график по продавцам-лидерам
    melted_sellers_data_sales = pd.melt(sellers_data_sales_reset, id_vars=['Category'], var_name='Month', value_name='Sales')
    available_seller_categories = melted_sellers_data_sales['Category'].unique()

    # Генерация уникального ключа для виджета st.multiselect
    multiselect_key = f"multiselect_{button_name}_{metric_type}"
    # Добавление случайной линии по умолчанию
    default_selected_category = random.choice(available_seller_categories)

    selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, key=multiselect_key, default=[])
    
    # Если не выбраны категории, установить случайную линию
    if not selected_seller_categories:
        selected_seller_categories = [default_selected_category]

    filtered_sellers_data_sales = melted_sellers_data_sales[melted_sellers_data_sales['Category'].isin(selected_seller_categories)]
    fig_sellers = px.line(filtered_sellers_data_sales, x='Month', y='Sales', color='Category', title=f'Top Sellers by {metric_type.capitalize()}', width=1000)
    st.plotly_chart(fig_sellers)
    
    # selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, key=multiselect_key, default=available_seller_categories)
    # filtered_sellers_data_sales = melted_sellers_data_sales[melted_sellers_data_sales['Category'].isin(selected_seller_categories)]
    # fig_sellers = px.line(filtered_sellers_data_sales, x='Month', y='Sales', color='Category', title=f'Top Sellers by {metric_type.capitalize()}', width=1000)
    # st.plotly_chart(fig_sellers)



# Отображение графика для выручки
def show_graph_top_sellers_revenue(button_name, metric_type):
    st.header(f"График по категориям Выручка || {button_name}")

    # Сброс индекса
    sellers_data_revenue_reset = sellers_data_revenue.reset_index()
    
    # Линейный график по продавцам-лидерам
    melted_sellers_data_revenue = pd.melt(sellers_data_revenue_reset, id_vars=['Category'], var_name='Month', value_name='Sales')
    available_seller_categories = melted_sellers_data_revenue['Category'].unique()

    # Генерация уникального ключа для виджета st.multiselect
    multiselect_key = f"multiselect_{button_name}_{metric_type}"
    # Добавление случайной линии по умолчанию
    default_selected_category = random.choice(available_seller_categories)

    selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, key=multiselect_key, default=[])
    
    # Если не выбраны категории, установить случайную линию
    if not selected_seller_categories:
        selected_seller_categories = [default_selected_category]

    filtered_sellers_data_sales = melted_sellers_data_revenue[melted_sellers_data_revenue['Category'].isin(selected_seller_categories)]
    fig_sellers = px.line(filtered_sellers_data_sales, x='Month', y='Sales', color='Category', title=f'Top Sellers by {metric_type.capitalize()}', width=1000)
    st.plotly_chart(fig_sellers)
    # selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, key=multiselect_key, default=available_seller_categories)
    # filtered_sellers_data_revenue = melted_sellers_data_revenue[melted_sellers_data_revenue['Category'].isin(selected_seller_categories)]
    # fig_sellers = px.line(filtered_sellers_data_revenue, x='Month', y='Sales', color='Category', title=f'Top Sellers by {metric_type.capitalize()}', width=1000)
    # st.plotly_chart(fig_sellers)




# Основной код Streamlit
text = "<h1 style='text-align: center;'>Привет! Здесь информация по продавцам <font color='blue'>OZON</font><br>(по <font color='red'>WB</font> появится в следующем релизе)</h1>"
st.markdown(text, unsafe_allow_html=True)

# Выбор кнопки
selected_button = st.radio("Выберите категорию:", ["fbo", "fbs", "retail", "crossborder", "total"])

# попробую новые функции
sellers_data_sales, sellers_data_revenue, sellers_data_sales_new, sellers_data_revenue_new = show_data(selected_button)
sellers_sales, sellers_revenue = show_table_top_sellers(selected_button)
# ПРОДАЖИ
st.header(f"Доля максимального значения Продаж продавца ко всем продажам категории || {selected_button}")
st.dataframe(sellers_data_sales)
st.header(f"Топ продавцов по Продажам || {selected_button}")
st.dataframe(sellers_sales)
show_graph_top_sellers_sales(selected_button, "sales")
# ВЫРУЧКА
st.header(f"Доля максимального значения Выручки продавца ко всей выручке категории || {selected_button}")
st.dataframe(sellers_data_revenue)
st.header(f"Топ продавцов по Выручке || {selected_button}")
st.dataframe(sellers_revenue)
show_graph_top_sellers_revenue(selected_button, "revenue")
# *********************************************************************************************************

st.header("ПОПЫТКА СДЕЛАТЬ БОЛЬШЕ ФИЛЬТРОВ")
st.header("Более удобный просмотр категорий")

# Выбор кнопки
selected_button_cat = st.radio("Выберите категорию еще раз:", ["fbo", "fbs", "retail", "crossborder", "total"])
# sellers_data_sales_new, sellers_data_revenue_new = show_data(selected_button_cat)

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
    
def line_chart_from_dataframe(df):
    # st.header("Линейный график")
    # Удалим столбец 'Category' и сделаем его индексом
    df.set_index('Category', inplace=True)
    # Транспонируем датафрейм
    df_transposed = df.T
    # Строим линейный график с настройкой ширины
    fig = px.line(df_transposed, title="Линейный график", width=1000)
    # Отображаем график
    st.plotly_chart(fig)

st.header("Данные по продажам или выручке")
# Выбор кнопки
selected_button_sales_or_revenue = st.radio("Что будем смотреть:", ["продажи", "выручка"])
if selected_button_sales_or_revenue == "продажи":
    st.header("Данные по продажам")
    df_graphic_sales = filter_dataframe(sellers_data_sales_new)
    line_chart_from_dataframe(df_graphic_sales)
else:
    st.header("Данные по выручке")
    df_graphic_revenue = filter_dataframe(sellers_data_revenue_new)
    line_chart_from_dataframe(df_graphic_revenue)

# *************************************************************************************************************
st.header("Топ категорий в выбранный месяц")
# Получаем список названий столбцов - месяцев для выпадающего списка
months_names = sellers_data_sales.columns.tolist()
# Выпадающий список
selected_option_month = st.selectbox('Выбери месяц', months_names)

# Слайдер для выбора одного числа
single_value = st.slider("Выберите число", min_value=0, max_value=20, value=5, step=1)
st.write("Выбрано число:", single_value)
# ***************************************************************************************************************
# Выбор нужного столбца по продажам
selected_column = sellers_data_sales[selected_option_month]
# Сортировка данных по убыванию
sorted_data = selected_column.sort_values(ascending=False)
# Отображение указанного количества строк
result_sales = sorted_data.head(single_value)
# Вывод результата
st.header("Данные по продажам")
st.write(result_sales)
# ***************************************************************************************************************

# Выбор нужного столбца по выручке
selected_column = sellers_data_revenue[selected_option_month]
# Сортировка данных по убыванию
sorted_data = selected_column.sort_values(ascending=False)
# Отображение указанного количества строк
result_revenue = sorted_data.head(single_value)
# Вывод результата
st.header("Данные по выручке")
st.write(result_revenue)
st.header("НУЖНО ВЫБРАТЬ КАКОЙ ВИД ОСТАВИТЬ: КАК ВЫШЕ ИЛИ КАК НИЖЕ")
col1, col2 = st.columns(2)
col1.subheader("Данные по продажам")
col1.table(result_sales)

col2.subheader("Данные по выручке")
col2.table(result_revenue)

# ***************************************************************************************************************
st.header("НОВЫЙ ЭТАП (ЛИСТ): СРЕДНИЕ ЗНАЧЕНИЯ")
st.write("Только категории без нулевых значений!")
st.header("ПРОДАЖИ")
st.header("Общие средние")
# Слайдер для выбора одного числа
single_value_avg = st.slider("Выберите число показанных категорий (используется для всех средних ниже (6 таблиц)", min_value=0, max_value=20, value=5, step=1)
# Создаем копию датафрейма
sellers_data_sales_copy_total = sellers_data_sales.copy()
# Удаляем строки, в которых есть хотя бы одно значение 0
sellers_data_sales_copy_total = sellers_data_sales_copy_total[(sellers_data_sales_copy_total != 0).all(axis=1)]
# Считаем среднее для каждой строки
sellers_data_sales_copy_total['mean_value'] = sellers_data_sales_copy_total.mean(axis=1)

# Выбор нужного столбца со средними значениями
sel_col_sales_total = sellers_data_sales_copy_total['mean_value']
# Сортировка данных по убыванию
sorted_data_sales_total = sel_col_sales_total.sort_values(ascending=False)
# Отображение указанного количества строк
result_sales_avg_total = sorted_data_sales_total.head(single_value_avg)
# Выводим результат
st.write(result_sales_avg_total)
# ****************************************
st.header("Средние за 22 год")
# Создаем копию датафрейма и оставляем только столбцы, где в названии есть '22'
sellers_data_sales_copy_22 = sellers_data_sales.filter(like='22').copy()
# Удаляем строки, в которых есть хотя бы одно значение 0
sellers_data_sales_copy_22 = sellers_data_sales_copy_22[(sellers_data_sales_copy_22 != 0).all(axis=1)]
# Считаем среднее для каждой строки
sellers_data_sales_copy_22['mean_value_22'] = sellers_data_sales_copy_22.mean(axis=1)

# Выбор нужного столбца со средними значениями
sel_col_sales_22 = sellers_data_sales_copy_22['mean_value_22']
# Сортировка данных по убыванию
sorted_data_sales_22 = sel_col_sales_22.sort_values(ascending=False)
# Отображение указанного количества строк
result_sales_avg_22 = sorted_data_sales_22.head(single_value_avg)
# Выводим результат
st.write(result_sales_avg_22)
# ****************************************
st.header("Средние за 23 год")
# Создаем копию датафрейма и оставляем только столбцы, где в названии есть '23'
sellers_data_sales_copy_23 = sellers_data_sales.filter(like='23').copy()
# Удаляем строки, в которых есть хотя бы одно значение 0
sellers_data_sales_copy_23 = sellers_data_sales_copy_23[(sellers_data_sales_copy_23 != 0).all(axis=1)]
# Считаем среднее для каждой строки
sellers_data_sales_copy_23['mean_value_23'] = sellers_data_sales_copy_23.mean(axis=1)

# Выбор нужного столбца со средними значениями
sel_col_sales_23 = sellers_data_sales_copy_23['mean_value_23']
# Сортировка данных по убыванию
sorted_data_sales_23 = sel_col_sales_22.sort_values(ascending=False)
# Отображение указанного количества строк
result_sales_avg_23 = sorted_data_sales_23.head(single_value_avg)
# Выводим результат
st.write(sorted_data_sales_23)
# ******************************** то, что сверху, но для выручки *************************************************
st.header("ВЫРУЧКА")
st.header("Общие средние")

# Создаем копию датафрейма
sellers_data_revenue_copy_total = sellers_data_revenue.copy()
# Удаляем строки, в которых есть хотя бы одно значение 0
sellers_data_revenue_copy_total = sellers_data_revenue_copy_total[(sellers_data_revenue_copy_total != 0).all(axis=1)]
# Считаем среднее для каждой строки
sellers_data_revenue_copy_total['mean_value'] = sellers_data_revenue_copy_total.mean(axis=1)

# Выбор нужного столбца со средними значениями
sel_col_revenue_total = sellers_data_revenue_copy_total['mean_value']
# Сортировка данных по убыванию
sorted_data_revenue_total = sel_col_revenue_total.sort_values(ascending=False)
# Отображение указанного количества строк
result_revenue_avg_total = sorted_data_revenue_total.head(single_value_avg)
# Выводим результат
st.write(result_revenue_avg_total)
# ****************************************
st.header("Средние за 22 год")
# Создаем копию датафрейма и оставляем только столбцы, где в названии есть '22'
sellers_data_revenue_copy_22 = sellers_data_revenue.filter(like='22').copy()
# Удаляем строки, в которых есть хотя бы одно значение 0
sellers_data_revenue_copy_22 = sellers_data_revenue_copy_22[(sellers_data_revenue_copy_22 != 0).all(axis=1)]
# Считаем среднее для каждой строки
sellers_data_revenue_copy_22['mean_value_22'] = sellers_data_revenue_copy_22.mean(axis=1)

# Выбор нужного столбца со средними значениями
sel_col_revenue_22 = sellers_data_revenue_copy_22['mean_value_22']
# Сортировка данных по убыванию
sorted_data_revenue_22 = sel_col_revenue_22.sort_values(ascending=False)
# Отображение указанного количества строк
result_revenue_avg_22 = sorted_data_revenue_22.head(single_value_avg)
# Выводим результат
st.write(result_revenue_avg_22)
# ****************************************
st.header("Средние за 23 год")
# Создаем копию датафрейма и оставляем только столбцы, где в названии есть '23'
sellers_data_revenue_copy_23 = sellers_data_revenue.filter(like='23').copy()
# Удаляем строки, в которых есть хотя бы одно значение 0
sellers_data_revenue_copy_23 = sellers_data_revenue_copy_23[(sellers_data_sales_copy_23 != 0).all(axis=1)]
# Считаем среднее для каждой строки
sellers_data_revenue_copy_23['mean_value_23'] = sellers_data_revenue_copy_23.mean(axis=1)

# Выбор нужного столбца со средними значениями
sel_col_revenue_23 = sellers_data_revenue_copy_23['mean_value_23']
# Сортировка данных по убыванию
sorted_data_revenue_23 = sel_col_revenue_23.sort_values(ascending=False)
# Отображение указанного количества строк
result_revenue_avg_23 = sorted_data_revenue_23.head(single_value_avg)
# Выводим результат
st.write(result_revenue_avg_23)


