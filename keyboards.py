from aiogram import types

KEYBOARDS = {
    'hide': types.ReplyKeyboardRemove(selective=False),
    'example': {
        'variants': ['This is', 'an example', 'keyboard'],
        'markup': None,
    },
}

### Create keyboard markups
# example
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row(*[types.KeyboardButton(variant) for variant in KEYBOARDS['example']['variants']])
KEYBOARDS['example']['markup'] = markup