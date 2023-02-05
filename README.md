# Домашнее задание по теме "Веб-скрапинг"
## Выбор ноутбука
Вы выбираете себе новый компьютер для покупки. Вы овладели навыками работы с инструментами веб-скрапинга и вам не терпится их применить для решения этой задачи. Вы решаете собрать и сравнить компьютеры с разных сайтов и выбрать из них лучший по вашему мнению. Вы решаете хранить собранные данные в таблице и автоматически выставлять к записям рейтинг "привлекательности для покупки"

Таблицу лучше не усложнять и сделать проще:
 ```
 Table computers {
  id int 
  url varchar // ссылка на страницу товара
  visited_at timestamp //время посещения страницы
  name varchar // наименование товара
  cpu_hhz float // частота процессора, ГГЦ
  ram_gb int // объем ОЗУ, Гб
  ssd_gb int // Объем SSD, Гб
  price_rub int // Цена, руб
  rank float // вычисляемый рейтинг
}
 ```
Например компьютер с ОЗУ 8Gb и ценой 40000 руб может иметь ранк:


                     rank=8∗5.6+40000∗−0.0001=40.8


Это при условии если учитывается только два параметра и выбраны именно такие веса (5.6 и -0.0001) для них.

## Требования:
 - Напишите скрапер собирающий информацию с сайтов на ваш выбор 
 - должно быть не менее 500 записей о технике должны быть данные с не менее чем 2 сайтов должно быть складывание в базу
 - должно быть автоматическое вычисление рейтинга сразу (можно средствами субд)
 - напишите readme.md с кратким описанием инструкцией запуска
 - используйте requirements.txt для указания сторонних зависимостей и их версий
 - используйте реляционную субд
 
 ## Ожидаемый результат
Реализуйте программу согласно требованиям описанным выше.
Ответом на задание будет считаться ссылка на ваш Merge Request в вашем репозитории. Убедитесь, что проверяющий может комметировать ваш Merge Request чтобы вы смогли получить обратную связь по сделанному заданию.
В ответе также в readme файле укажите какие веса для параметров вы выбрали и топ 5 записей из получившейся у вас таблицы.

# Решение задания по теме "Веб-скрапинг"
Зависимости в файле **requirements.txt**, примеры HTTP запросов в файле **requests.http**.
- В решении используется 2 скрапера с сайтов "notik.ru" и "laptop.ru".
- Общее количество строк с собранными данными: 1277.
- Нет проверок на пустые поля, так как их нет в требовании.
- При добавлении новой строки в БД автоматически вычисляется рейтинг по формуле:


           rank = cpu_hhz * 0.09 + ram_gb * 5.9 + disk_ssd * 0.5 + item['price'] * -0.002
           
![Топ 5 записей](https://github.com/ayanchevsky/HomeWork2/blob/master/top5.PNG) 


Запуск:
```
 scrapy crawl computers
 scrapy crawl nouts
 ```
