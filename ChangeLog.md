# ImageGen
DataSet лежит  [Тут](https://github.com/YartoKub/ImageGen/tree/main/pred_EEVEE_gold_cube), это устаревшая версия, по мере работы я добавлю больше картинок. Датасет хранится в виде Numpy массивов, там есть и картинки, и направления векторов.

### 05 Апреля 2025

Сделал [модель для смены освещения](https://github.com/YartoKub/ImageGen/blob/main/CubeRelight.ipynb). Хорошая модель сохранена на у меня локально на компе под именем goodNTLmodel001.keras, весит 135МБ. Принесу на флешке.

![animation](https://github.com/user-attachments/assets/f25044c6-b3cc-470a-bd39-45f2f92e0c52)

Отдельные кадры анимации и нормализованная карта изменения освещенности от (0 до 1). Простая карта освещенности принимает значения от -1(затемнение) до 1(осветление), но этот отрезок нельзя показать на картинке.

![image](https://github.com/user-attachments/assets/99128c5c-96ed-4ab4-aebf-0f4852630141)

### 22 Марта 2025 

Сделал [штукенцию](https://github.com/YartoKub/ImageGen/blob/main/FlexibleDataSetCombiner.ipynb) для генерации датасетов. Она умеет: брать список из нескольких разных датасетов, объединять их в большой датасет с перемешиванием и сохранением свезей index-index, а также делить этот датасет на датасетики поменбше чтобы они умещались в оперативную память.

Работаю с картинками

### 22 Февраля 2025

Попробовал использовать  [U-net](https://github.com/YartoKub/ImageGen/blob/main/UNET_normals_generator.ipynb) для генерации нормалей. Качество хорошее, нет размытостей, но часто на генерациях появляются битые пиксели и бляшки. 
Пробовал использовать dropout, но он не исправлял проблему.

![image](https://github.com/user-attachments/assets/33e82b64-f395-42de-a790-4dc9ad90315b)

### 21 Февраля 2025

Значительно улучшил качество генерируемых нормалей. Для этого я натренировал отдельную нейросеть, которая делает нормали четче. 

![image](https://github.com/user-attachments/assets/fed3f97f-b438-4f93-8859-39d5cf166838)

### 01 Февраля 2025

Сделал [Инструмент](https://github.com/YartoKub/ImageGen/blob/main/NormalRelight.ipynb) для рассчета освещения на основе нормалей и вектора.

![image](https://github.com/user-attachments/assets/88c1d4b7-4a45-4ccb-8ca6-bc14cd405272)

# Работа за Первое полугодие: 
### 30 Января  2025 

обучил модель на большом количестве разных фигут, генерация нормалей, как и альбедо, очень хорошая, пускай и довольно размытая

![image](https://github.com/user-attachments/assets/f675fad6-700c-4b9d-b912-5f36e74e1a27)
![image](https://github.com/user-attachments/assets/7a0c8131-b15b-4d01-8b18-9f1b500ef6bf)

### 28 Декабря 2024

Попытка создать нейросеть для переосвещения изображения, результаты очень плохие, модель не смогла найти взаимосвязи.

![image](https://github.com/user-attachments/assets/3e3befda-371a-42c3-9b12-bf2c230438d3)
![image](https://github.com/user-attachments/assets/58bec502-1e65-45cd-85ec-e72acd652036)

### 21 Декабря 2024

Поиск неосвещенного изображения

![image](https://github.com/user-attachments/assets/65fbafa1-9fee-4eef-93e7-024b4d311c96)

### 20 декабря 2024

генерирую карту нормалей из изображения.

![image](https://github.com/user-attachments/assets/aff08f9a-79cb-4114-aeea-482670f5aac2)
![image](https://github.com/user-attachments/assets/3a2d5d8f-ad5a-438c-8b10-54ee4d48b504)










