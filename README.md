# mini-readability

<h2>Задача:</h2>
Необходимо вытащить из веб-документа только полезный контент, без рекламы, меню навигации и прочих отвлекающих элементов. Всю полезную информацию нужно отформатировать и записать в текстовый файл, таким образом, чтобы чтение было максимально комфортным. Файл с текстом поместить в директорию, созданную в соответствии с url-адресом страницы. Добавить файл конфигурации, чтобы программа поддавалась настройке.

<h2>Решение:</h2>
Программа выполнена в виде утилиты, для запуска из комндной строки, где в качестве первого аргумента пользователь передает нужный url-адрес. Для запуска приложения необходима версия Python 3.5. Программа выполнена с использованием класса html.parser, который осуществляет обработку веб страницы, инициализируя встроенные методы переопределенные для решения данной задачи. Основной класс - MyHTMLParser(HTMLParser) - он осуществяет обработку документа. Основные методы класса: handle_starttag() - обработка открывающего тега, handle_data() - обработка данных внутри тегов, handle_endtaag() - обработка закрывающего тега. Принцип работы парсера заключается в следующем: когда метод обработки открывающего тега встречает нужный тег, счетчик(переменная типа bool) устанавливается в положение True, модуль обработки данных внутри тегов собирает информацию до тех пор, пока handle_endtag не встретит соответствующий закрывающий тег. Помимо вышеупомянутых методов в классе присутствуют и другие, например для обработки ссылки get_link(). На большинстве сайтов вся полезная информация содержится в тегах "h1" - заголовочный тег, "p" - текстовый абзац и "a" - тег ссылки. По умолчанию именно в этих тегах приложение собирает данные. В зависимости от специфичности верстки сайта, добавлена возможность изменять список допустимых тегов в файле "config.txt". Второй класс - ContentSaver. В нем определены следующие методы: создание директории для сохранения файла, создание файла в этой директории и запись в него полезного контента, а также открытие страницы по url и декодинг в строковый вид.
<h2>Результаты проверки:</h2>
https://lenta.ru/news/2018/10/19/semak_kokorin/ (tags: "h1", "p", "a") - весь основной контент сохранен, без мусора.
https://www.gazeta.ru/politics/news/2018/10/18/n_12183985.shtml?updated (tags: "h1", "p", "a") - весь основной контент сохранен, имеется мусор из "подвальной" части страницы.
http://www.vesti.ru/doc.html?id=3072093&cid=6 (tags: "h1", "p", "a", "h3") - весь основной контент сохранен, как и в предыдущем случае - мусор из "подвальной" части страницы
https://ria.ru/mediawars_analysis/20151216/1343317621.html - основной контент сохранен, много мусора после основного контента.
https://vz.ru/opinions/2018/10/17/946552.html (tags: "h1", "p", "a") - весь основной контент сохранен, немного без мусора.
https://news.ngs.ru/articles/65510491/?from=centercol (tags: "h1", "p", "a") - весь основной контент сохранен, немного мусора.

<h2>Развитие программы:</h2>
В первую очередь необходимо реализовать более гибкую настройку программы в файле конфигурации для парсинга сайтов с особенностями структуры документа. На некоторых страницах контент содержится не только в тегах "p" или "h", но и в других, где необходима более точная настройка с проверкой аргументов у тегов. 
Так же для улучшения работы программы можно добавить новые методы обработки контента, которые будут определять ненужную информацию по её положению на странице или по ключевым словам.
