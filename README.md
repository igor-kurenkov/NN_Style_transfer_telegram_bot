# Style transfer telegram bot
Это итоговый проект в Deep Learning School осень 2022 продвинутый поток часть 1.

Stepik User ID 351891460

Телеграм-бот для переноса стиля изображения.

адрес демо-бота https://t.me/DLSstyletransferIKbot

Для оценки преподавателем бот задеплоен на Pythonanywhere на бесплатном тарифе, это значит что процессорное время в сутки ограничено. Если бот не реагирует, то возможно суточный ресурс исчерпан. Свяжитесь со мной чтобы я запустил его на резервном аккаунте.
Стилизация реализована на pytorch.

## Скриншот работы бота из Telegram
 
![bot](https://user-images.githubusercontent.com/82575007/215345714-5378d0ef-364f-460c-abd9-1d197a94b7c6.png)

## Режимы работы бота

У бота есть 3 режима работы:
- Перенос стиля с одного изображения на другое (NST)
- Стилизация изображений под картины Ван Гога (GAN)
- Стилизация дневных пейзажей в ночные (GAN)

### Перенос стиля с одного изображения на другое
В данном режиме бот переносит стиль с первого изображения на второй с заданными настройками.

Данный режим использует технологию <a href='https://pytorch.org/tutorials/advanced/neural_style_tutorial.html'>Neural style transfer</a>.

Для этого режима возможна настройка размера выходного изображения
  - 256х256 пикселей
  - 512х512 пикселей
  - 1024x1024 пискселя. Нестабильно на Pythonanywhere
  
Возможные результаты работы данного режима бота:

Изначальное изображение    |  Переносимый стиль        |  Итоговое изображение
:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://github.com/igor-kurenkov/NN_Style_transfer_telegram_bot/blob/master/images/forrest-gump.jpg" height="250">  |  <img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/style_1.jpg" height="250" width="181">  |   <img src="https://github.com/igor-kurenkov/NN_Style_transfer_telegram_bot/blob/master/images/SimpleStyletransferresult.jpeg" height="250"  width="250">

### Стилизация изображений под картины Ван Гога
В данном режиме бот перерисовывает данное ему изображение так, чтобы оно было похоже по стилю на картины Ван Гога. При этом бот  использует предобученную генеративную сеть из этого проекта: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.

Данный режим использует технологию Generative adversarial networks.

Для этого режима возможна настройка размера выходного изображения
  - 256х256 пикселей
  - 512х512 пикселей
  - 1024x1024 пискселя

Пример результатов работы:
Изначальное изображение    |  Итоговое изображение
:-------------------------:|:-------------------------:
<img src="https://github.com/igor-kurenkov/NN_Style_transfer_telegram_bot/blob/master/images/privivka.jpeg" height="250">  |  <img src="https://github.com/igor-kurenkov/NN_Style_transfer_telegram_bot/blob/master/images/VanGoghgresult.jpeg" height="250"  width="250">

### Стилизация изображений под картины Клода Моне
В этом режиме бот перерисовывает данное ему изображение так, чтобы оно было похоже по стилю на картины Ван Гога. При этом бот  использует предобученную генеративную сеть из этого проекта: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.

Данный режим использует технологию Generative adversarial networks.

Для этого режима возможна настройка размера выходного изображения
  - 256х256 пикселей
  - 512х512 пикселей
  - 1024x1024 пискселя

Возможные результаты работы данного режима бота:

Изначальное изображение    |  Итоговое изображение
:-------------------------:|:-------------------------:
<img src="https://github.com/igor-kurenkov/NN_Style_transfer_telegram_bot/blob/master/images/diehard.jpg" height="250">  |  <img src="https://github.com/igor-kurenkov/NN_Style_transfer_telegram_bot/blob/master/images/Monetresult.jpeg" height="250"  width="250">


## Установка
Для запуска данного бота у себя необходимо добавить в основной каталог файл `config.py` со следующим содержанием:
```Python
  API_TOKEN = '<YOUR TOKEN>'

  DEBUG_ID = '<YOUR_DEBUG_ID>'
  
  GET_DEBUG_INFO = True

  LOGGING = True

  MODE = 'NORMAL'

  CONNECTION_TYPE = 'POLLING'

  WEBHOOK_HOST = '<YOUR_WEBHOOK_HOST>'

  WEBAPP_PORT = '<YOUR_WEBAPP_PORT>'
```

Где:
- `<YOUR TOKEN>` -- токен вашего бота, который можно получить у официального бота сервиса Telegram для создания собственных ботов: @BotFather,
- `<YOUR_DEBUG_ID>` -- id человека, которому будут приходить сообщения в телеграм об ошибках,
- GET_DEBUG_INFO -- будет ли на указанный выше id отправляться информация об ошибках (если поставить `False`, то можно не указывать id в строке выше),
- LOGGING -- будет ли выводиться в консоль информация о том, какие действия сейчас совершает бот,
- MODE -- может принимать значения `'EASY'` или `'NORMAL'`, в первом случае при попытке перенесения стиля бот будет сообщать, что он запущен на слабом устройстве, во втором случае все работает штатно.
- CONNECTION_TYPE -- может принимать значения `'POLLING'` или `'WEBHOOKS'`, в зависимости от желаемого вами типа (для более простой работы стоит указать `'POLLING'`)
- `<YOUR_WEBHOOK_HOST>` -- адрес вашего webhook хоста (если выше выбрали `'POLLING'`, то можно не заполнять)
- `<YOUR_WEBAPP_POST>` -- порт вашего webhook хоста (если выше выбрали `'POLLING'`, то можно не заполнять)

Библиотека для работы с нейронными сетями: pytorch

_____

По всем вопросам обращаться в телеграм: @Neuronauticus
