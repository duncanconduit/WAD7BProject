import random

AVATAR_COLOURS = {
    'red': 'bg-red-300 dark:bg-red-500',
    'blue': 'bg-blue-300 dark:bg-blue-500',
    'green': 'bg-green-300 dark:bg-green-500',
    'yellow': 'bg-yellow-300 dark:bg-yellow-500',
    'purple': 'bg-purple-300 dark:bg-purple-500',
}

def get_random_avatar_colour():
    return random.choice(list(AVATAR_COLOURS.keys()))