# import subprocess
# subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Функция для загрузки данных из файла на GitHub
def load_data(file_path):
    full_path = f'{file_path}.xlsx'
    return pd.read_excel(full_path)

# Функция для отображения таблицы и графика
def show_data(button_name, metric_type):
    st.header(f"Данные по {metric_type.capitalize()} || {button_name}")

    # Загрузка данных по продажам
    sales_data = load_data(f"Общая_таблица_проценты_{button_name.lower()}_sales")
    st.subheader(f"Доля лидера от всей категории")
    st.dataframe(sales_data)

    # Преобразование данных для графика
    melted_sales_data = pd.melt(sales_data, id_vars=['Category'], var_name='Month', value_name='Percentage')
    
    # График по продажам
    fig_sales = px.bar(melted_sales_data, x='Month', y='Percentage', color='Category',
                       title=f'{metric_type.capitalize()} Sales Distribution')
    st.plotly_chart(fig_sales)

    
    # # Преобразование данных для графика
    # melted_sales_data = pd.melt(sales_data, id_vars=['Category'], var_name='Month', value_name='Percentage')

    # # График по продажам
    # fig_sales = px.bar(melted_sales_data, x='Seller', y='Percentage', color='Month',
    #                    title=f'{metric_type.capitalize()} Sales Distribution')
    # st.plotly_chart(fig_sales)

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
