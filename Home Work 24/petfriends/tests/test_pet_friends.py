from Home24.api import PetFriends
from Home24.settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Бося', animal_type='Котан',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo(name='Босяра', animal_type='Котан',
                                     age='8'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Удал", "котан", "5", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Фира', animal_type='Кот', age=7):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_photo(pet_photo = 'images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__),pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] !=''

    else:
        raise Exception('There is no me pets')

def test_get_api_key_with_invalid_email(email='867509mail.ru', password=valid_password):
    """Негативный кейс на отправку невалидного электронного адреса"""

    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_get_api_key_with_invalid_password(email=valid_email, password='123'):
    """Негативный кейс на отправку невалидного пароля"""

    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_add_new_pet_with_invalid_name(name=12345, animal_type='котун',
                                       age='5', pet_photo='images/cat1.jpg'):
    """Негативный кейс на добавление питомца с невалидным именем """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца c обработкой исключения
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверное имя')


def test_add_new_pet_without_name(name='', animal_type='котун', age='4',
                                     pet_photo='images/cat1.jpg'):
    """Негативный тест на добавление без имени"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверное имя')
    else:
        assert status == 200
        print("Баг - питомец добавлен без имени")


def test_try_unsuccessful_delete_empty_pet_id():
    """Проверяем, что нельзя удалить питомца с пустым id"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_id = ''
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 400 or 404
    print('удалить питомца без id нельзя')


def test_add_new_pet_with_invalid_animal_type(name='Котун', animal_type=12345,
                                              age='8', pet_photo='images/cat1.jpg'):
    """Негативный кейс на добавление питомца с неверным форматом вида"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('Неверный вид питомца')


def test_add_new_pet_with_none_value_animal_type(name='Котун', animal_type='',
                                                 age='4', pet_photo='images/cat1.jpg'):
    """Негативный кейс на добавление питомца с пустым значением вида"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('не указан вид питомца')
    else:
        assert status == 200
        print("Баг - питомец добавлен без вида")


def test_add_new_pet_with_invalid_age(name='Котун', animal_type='котя',
                                      age='сорок', pet_photo='images/cat1.jpg'):
    """Негативный кейс на добавление питомца с неверным значением возраста"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except AttributeError:
        print('неверно указан возраст питомца')
    else:
        assert status == 200
        print("Баг - питомец добавлен с некоректным возрастом")