import pytest
from settings import valid_email, valid_password
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# Проверяем что на странице с моими питомцами присутствуют все питомцы
def test_all_my_pets_are_on_page(show_my_pets):
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located
                                                     ((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    # Запрашиваем элементы статистики и сохраняем их в переменную
    statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located
                                                     ((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Запрашиваем элементы карточек питомцев и сохраняем их в переменную
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    # Получаем количество карточек питомцев
    number_of_pets = len(pets)
    # Проверяем что количество питомцев из статистики равно количеству карточек питомцев
    assert number == number_of_pets


#Проверяем что на странице с моими питомцами у всех питомцев разные имена
def test_no_same_pets_names(show_my_pets):
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Запрашиваем элементы с данными о питомцах и сохраняем их в переменную
    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    '''Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
       и разделяем по пробелу. Выбираем имена и добавляем их в список pets_name.'''
    pets_name = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_name.append(split_data_pet[0])
    # Перебираем имена и если имя повторяется то прибавляем к счетчику r единицу.
    # Проверяем, если r == 0 то повторяющихся имен нет.
    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
    assert r == 0
    print(r)
    print(pets_name)


# Проверяем что на странице с моими питомцами нет одинаковых карточек питомцев
def test_no_same_pets(show_my_pets):
    # Устанавливаем явное ожидание
    element = WebDriverWait(pytest.driver, 10).until \
        (EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Запрашиваем элементы с данными о питомцах и сохраняем их в переменную
    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    ''' Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
        и разделяем по пробелу. '''
    list_data = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        list_data.append(split_data_pet)
    '''Собираем имя, возраст и породу в одно слово для каждого питомца, 
       получившиеся слова добавляем в строку
       и между ними вставляем пробел'''
    line = ''
    for i in list_data:
        line += ''.join(i)
        line += ' '
    # Превращаем строку в список
    list_line = line.split(' ')
    # Превращаем список в множество
    set_list_line = set(line.split(' '))
    # Получаем количество элементов списка и множества
    qw1 = len(list_line)
    qw2 = len(set_list_line)
    # Находим разницу
    get_diff = qw1 - qw2
    # Если разница в количестве элементов == 0 значит нет одинаковых карточек питомцев
    assert get_diff == 0


# Проверяем что на странице с моими питомцами минимум у половины питомцев есть фото.
def test_pets_has_photo(show_my_pets):
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    # Запрашиваем элементы статистики и сохраняем их в переменную
    stats = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")
    # Запрашиваем элементы с атрибутом img и сохраняем их в переменную
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')
    # Получаем количество питомцев из данных статистики
    number = stats[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    # Находим половину от количества питомцев
    half = number // 2
    # Находим количество питомцев с фотографией
    number_of_photos = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            number_of_photos += 1
    # Проверяем что количество питомцев с фотографией больше или равно половине количества питомцев
    assert number_of_photos >= half
    print(f'количество фото: {number_of_photos}')
    print(f'Половина от числа питомцев: {half}')


# Проверяем что мы находимся на странице "Мои питомцы"
def test_my_pets_page():
    # Устанавливаем явное ожидание
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим валидный email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим валидный пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    # Нажимаем на ссылку "Мои питомцы"
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
    # Проверяем что мы оказались на странице "Мои питомцы"
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'


# Проверка карточек питомцев
def test_check_all_pets():
    # Устанавливаем неявное ожидание
    pytest.driver.implicitly_wait(10)
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что загрузилась главная страница
    assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    assert names[0].text != ''
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ',' in descriptions[i].text
        parts = descriptions[i].text.split(",")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


'''Проверяем что на странице с моими питомцами у всех питомцев есть имя, возраст и порода
   НО если в имени есть цифры, то тест будет не пройден вне зависимости от остальных входных данных, 
   т. к. длина строки будет больше на эту цифру.'''
def test_my_pets_have_name_age_and_gender(show_my_pets):
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located
                                                     ((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Запрашиваем элементы с данными о питомцах и сохраняем их в переменную
    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
    '''Перебираем данные из pet_data, оставляем имя, возраст и породу, остальное меняем на пустую строку
       и разделяем по пробелу. Находим количество элементов в получившемся списке и сравниваем их
       с ожидаемым результатом'''
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        result = len(split_data_pet)
        assert result == 3