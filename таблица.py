import matplotlib.pyplot as plt
import numpy as np
import random

# 🔹 Данные для первых 4 дней
days = ["1", "2", "3", "4", "5", "6", "7"]
data_input = [
    ["20°C", "21°C", "22°C", "19°C"],  # Температура
    ["60%", "58%", "55%", "70%"],      # Влажность
    ["3 м/с", "5 м/с", "2 м/с", "4 м/с"],  # Ветер
    ["1015", "1013", "1010", "1012"],      # Давление
    ["20%", "40%", "60%", "30%"]           # Облачность
]

rows = ["Температура", "Влажность", "Ветер", "Давление", "Облачность"]

# 🔹 Функция для генерации последних 3 дней с учетом тренда
def extend_data_trend(data_row, type_row):
    numeric = [int(val.replace("°C","").replace("%","").replace(" м/с","")) for val in data_row]
    extended = numeric.copy()
    
    for i in range(4, 7):
        if type_row in ["Температура", "Давление"]:
            x = np.array([0,1,2,3])
            y = np.array(numeric)
            a, b = np.polyfit(x, y, 1)
            next_val = int(a*i + b + random.randint(-1,1))
            extended.append(next_val)
        elif type_row in ["Влажность", "Облачность", "Ветер"]:
            avg = int(np.mean(extended[-4:]))
            next_val = avg + random.randint(-3,3)
            if type_row in ["Влажность", "Облачность"]:
                next_val = max(0, min(100, next_val))
            elif type_row == "Ветер":
                next_val = max(0, next_val)
            extended.append(next_val)
    
    formatted = []
    for val in extended:
        if type_row == "Температура":
            formatted.append(f"{val}°C")
        elif type_row in ["Влажность", "Облачность"]:
            formatted.append(f"{val}%")
        elif type_row == "Ветер":
            formatted.append(f"{val} м/с")
        elif type_row == "Давление":
            formatted.append(str(val))
    return formatted

# 🔹 Генерация полного набора данных
data = [extend_data_trend(data_input[i], rows[i]) for i in range(len(rows))]

# 🔹 Создаем таблицу
fig, ax = plt.subplots(figsize=(9, 3))
ax.axis("off")

table = ax.table(
    cellText=data,
    rowLabels=rows,
    colLabels=days,
    loc="center",
    cellLoc="center",
    bbox=[0.25, 0, 0.8, 1]
)

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.5)

# 🔹 Выделяем прогнозные дни (5,6,7) синим цветом
for row in range(len(rows)+1):
    for col in range(4, 7):  # колонки 5,6,7
        table.get_celld()[(row, col)].set_facecolor("#ADD8E6")  # светло-синий цвет

plt.title("Таблица погоды на 7 дней (прогноз выделен синим)", fontsize=14, pad=20)
plt.show()
