# Style transfer telegram bot
Этот бот для телеграма переносит стиль с одних фотографий на другие.

## Режимы работы бота

У бота есть 3 режима работы:
- Перенос стиля с одного изображения на другое (NST)
- Стилизация изображений под картины Ван Гога (GAN)
- Стилизация дневных пейзажей в ночные (GAN)

### Перенос стиля с одного изображения на другое
В данном режиме бот переносит стиль с первого изображения на второй с заданными настройками.

Данный режим использует технологию Neural style transfer.

Для этого режима возможна настройка размера выходного изображения
  - 256х256 пикселей
  - 512х512 пикселей
  - 1024x1024 пискселя. Нестабильно на Pythonanywhere
  
Возможные результаты работы данного режима бота:

Изначальное изображение    |  Переносимый стиль        |  Итоговое изображение
:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/corgi.jpg" height="250" width="250">  |  <img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/style_1.jpg" height="250" width="181">  |   <img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/corgi_st_1.jpeg" height="250"  width="250">

### Стилизация изображений под картины Ван Гога
В данном режиме бот перерисовывает данное ему изображение так, чтобы оно было похоже по стилю на картины Ван Гога. При этом бот  использует предобученную генеративную сеть из этого проекта: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.

Данный режим использует технологию Generative adversarial networks.

Для этого режима возможна настройка размера выходного изображения
  - 256х256 пикселей
  - 512х512 пикселей
  - 1024x1024 пискселя

### Стилизация дневных пейзажей в ночные
В этом режиме бот преобразовывает дневное изображение в ночное. При этом бот  использует предобученную генеративную сеть из этого проекта: https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.

Данный режим использует технологию Generative adversarial networks.

Для этого режима возможна настройка размера выходного изображения
  - 256х256 пикселей
  - 512х512 пикселей
  - 1024x1024 пискселя

Возможные результаты работы данного режима бота:

Изначальное изображение    |  Итоговое изображение
:-------------------------:|:-------------------------:
<img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/field.jpg" height="250" width="375">  |  <img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/vangogh_1.jpeg" height="250"  width="250">
<img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/nature.jpg" height="250" width="378">  |  <img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/vangogh_2.jpeg" height="250"  width="250">

<img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/rocks.jpg" height="250" width="378">  |  <img src="https://github.com/alresin/Style_transfer_telegram_bot/blob/master/images/monet_2.jpeg" height="250"  width="250">


## Информация по запуску бота
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
