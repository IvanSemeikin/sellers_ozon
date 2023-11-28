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

    # Если столбец 'Category' отсутствует, добавим его, используя индексы
    if 'Category' not in data.columns:
        data.insert(0, 'Category', data.index)
    
    return data


# Функция для отображения таблицы и графика
def show_data(button_name, metric_type):
    st.header(f"Данные по {metric_type.capitalize()} || {button_name}")

    # Загрузка данных по продажам
    sales_data = load_data(f"Общая_таблица_проценты_{button_name.lower()}_sales")
    st.subheader(f"Доля лидера от всей категории")
    st.dataframe(sales_data)

    # *************************************************** График начало *********************************************************
    # *************************************************** полурабочий код начало *********************************************************
    # Преобразование данных для линейного графика
    # melted_sales_data = pd.melt(sales_data, id_vars=['Category'], var_name='Month', value_name='Percentage')
    
    # # Список доступных категорий
    # available_categories = melted_sales_data['Category'].unique()
    
    # # Выбор пользователем категорий
    # selected_categories = st.multiselect('Выберите категории для отображения', available_categories, default=None)
    
    # # Если пользователь не выбрал категории, используем все доступные
    # if not selected_categories:
    #     selected_categories = available_categories
    
    # # Фильтрация данных по выбранным категориям
    # filtered_sales_data = melted_sales_data[melted_sales_data['Category'].isin(selected_categories)]
    
    # # Линейный график по продажам
    # fig_sales = px.line(filtered_sales_data, x='Month', y='Percentage', color='Category',
    #                     title=f'Sales Distribution', height=600)
    
    # # Отображение графика без названий категорий под ним
    # st.plotly_chart(fig_sales, use_container_width=True, sharing='streamlit', config={'displayModeBar': False})
    
    # # Преобразование данных для линейного графика по продавцам
    # melted_sellers_data_sales = pd.melt(sellers_data_sales, id_vars=['Category'], var_name='Month', value_name='Sales')
    
    # # Список доступных категорий для продавцов
    # available_seller_categories = melted_sellers_data_sales['Category'].unique()
    
    # # Выбор пользователем категорий для продавцов
    # selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, default=None)
    
    # # Если пользователь не выбрал категории для продавцов, используем все доступные
    # if not selected_seller_categories:
    #     selected_seller_categories = available_seller_categories
    
    # # Фильтрация данных по выбранным категориям для продавцов
    # filtered_sellers_data_sales = melted_sellers_data_sales[melted_sellers_data_sales['Category'].isin(selected_seller_categories)]
    
    # # Линейный график по продавцам-лидерам
    # fig_sellers = px.line(filtered_sellers_data_sales, x='Month', y='Sales', color='Category',
    #                       title=f'Top Sellers by Sales', height=600)
    
    # # Отображение графика без названий категорий под ним
    # st.plotly_chart(fig_sellers, use_container_width=True, sharing='streamlit', config={'displayModeBar': False})

    # *************************************************** полурабочий код конец *********************************************************
    
    # Преобразование данных для линейного графика по продавцам
    melted_sellers_data_sales = pd.melt(sellers_data_sales, id_vars=['Category'], var_name='Month', value_name='Sales')

    
    # Список доступных категорий
    available_categories = melted_sales_data['Category'].unique()
    
    # Выбор пользователем категорий
    selected_categories = st.multiselect('Выберите категории для отображения', available_categories, default=None)
    
    # Если пользователь не выбрал категории, используем все доступные
    if not selected_categories:
        selected_categories = available_categories
    
    # Фильтрация данных по выбранным категориям
    filtered_sales_data = melted_sales_data[melted_sales_data['Category'].isin(selected_categories)]
    
    # Линейный график по продажам
    fig_sales = px.line(filtered_sales_data, x='Month', y='Percentage', color='Category',
                        title=f'Sales Distribution', height=600)
    
    # Отображение графика без названий категорий под ним
    st.plotly_chart(fig_sales, use_container_width=True, sharing='streamlit', config={'displayModeBar': False})
    
    # Преобразование данных для линейного графика по продавцам
    melted_sellers_data_sales = pd.melt(sellers_data_sales, id_vars=['Category'], var_name='Month', value_name='Sales')
    
    # Список доступных категорий для продавцов
    available_seller_categories = melted_sellers_data_sales['Category'].unique()
    
    # Выбор пользователем категорий для продавцов
    selected_seller_categories = st.multiselect('Выберите категории для отображения', available_seller_categories, default=None)
    
    # Если пользователь не выбрал категории для продавцов, используем все доступные
    if not selected_seller_categories:
        selected_seller_categories = available_seller_categories
    
    # Фильтрация данных по выбранным категориям для продавцов
    filtered_sellers_data_sales = melted_sellers_data_sales[melted_sellers_data_sales['Category'].isin(selected_seller_categories)]
    
    # Линейный график по продавцам-лидерам
    fig_sellers = px.line(filtered_sellers_data_sales, x='Month', y='Sales', color='Category',
                          title=f'Top Sellers by Sales', height=600)
    
    # Отображение графика без названий категорий под ним
    st.plotly_chart(fig_sellers, use_container_width=True, sharing='streamlit', config={'displayModeBar': False})


    # ************* График конец *******************
    
    # Таблица продавцов-лидеров по продажам
    sellers_data_sales = load_data(f"Общая_таблица_продавцы_{button_name.lower()}_sales")
    st.subheader(f"Топ продавцов по {metric_type.capitalize()}")
    st.dataframe(sellers_data_sales)

# Основной код Streamlit
st.title("Привет! Здесь информация по продавцам OZON")

# Выбор кнопки
selected_button = st.radio("Выберите категорию:", ["fbo", "fbs", "retail", "crossborder", "total"])

# Вывод данных для продаж
show_data(selected_button, "sales")

# Вывод данных для выручки
show_data(selected_button, "revenue")
