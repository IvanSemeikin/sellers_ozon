import subprocess
subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

import streamlit as st
import pandas as pd
# import plotly.express as px

# Функция для загрузки данных из файла на GitHub
def load_data(file_path):
    full_path = f'{file_path}.xlsx'
    return pd.read_excel(full_path)

# Функция для отображения таблицы и графика
def show_data(button_name, metric_type):
    st.header(f"{metric_type.capitalize()} Data for {button_name}")

    # Загрузка данных по продажам
    sales_data = load_data(f"Общая_таблица_проценты_{button_name.lower()}_sales")
    st.subheader(f"Percentage Leader vs. Category Sales")
    st.dataframe(sales_data)

        # График по продажам
    fig_sales, ax_sales = plt.subplots()
    ax_sales.bar(sales_data['Seller'], sales_data['Percentage'])
    ax_sales.set_title(f'{metric_type.capitalize()} Sales Distribution')
    st.pyplot(fig_sales)

    # Таблица продавцов-лидеров по продажам
    sellers_data_sales = load_data(f"Общая_таблица_продавцы_{button_name.lower()}_sales")
    st.subheader(f"Top Sellers by {metric_type.capitalize()} Sales")
    st.dataframe(sellers_data_sales)

# Основной код Streamlit
st.title("Привет! Здесь информация по продавцам OZON")

# Выбор кнопки
selected_button = st.radio("Выберите категорию:", ["fbo", "fbs", "retail", "crossboarder", "total"])

# Вывод данных для продаж
show_data(selected_button, "sales")

# Вывод данных для выручки
show_data(selected_button, "revenue")
