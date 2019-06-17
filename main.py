from utils import estimate_g, calculate_g_, calculate_g_star, init_costs, preprocess_costs, levenshtein_dist


UA_LETTERS = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'"
RU_LETTERS = "абвгдеёжзиыйклмнопрстуфхцчшщьъэюя"

ua_set = set(UA_LETTERS)
ru_set = set(RU_LETTERS)

ua_unique = ua_set.difference(ru_set)
ru_unique = ru_set.difference(ua_set)


def check_for_unique_symbols(word):
    for s in word:
        if s in ua_unique:
            return 'Українська'
        elif s in ru_unique:
            return 'Русский'
    return None


if __name__ == '__main__':
    g_ua = estimate_g('ua_text.txt', UA_LETTERS)
    g_ru = estimate_g('ru_text.txt', RU_LETTERS)
    # costs = init_costs(UA_LETTERS)
    # preprocess_costs(costs, UA_LETTERS)
    g_ua_ = calculate_g_(g_ua, UA_LETTERS)
    g_ru_ = calculate_g_(g_ru, RU_LETTERS)
    g_star_ua = calculate_g_star(g_ua_, UA_LETTERS)
    g_star_ru = calculate_g_star(g_ru_, RU_LETTERS)
    # word = 'взлететь'
    word = input('Enter the word: ')
    language = check_for_unique_symbols(word)
    if language is None:
        lev_dist_to_ua = levenshtein_dist(word.lower(), UA_LETTERS, g_star_ua, g_ua)
        lev_dist_to_ru = levenshtein_dist(word.lower(), RU_LETTERS, g_star_ru, g_ru)
        print('Levenshtein distance from word {} to Ukrainian language is {}'.format(word, lev_dist_to_ua))
        print('Levenshtein distance from word {} to Russian language is {}'.format(word, lev_dist_to_ru))
        language = 'Українська'
        if lev_dist_to_ru < lev_dist_to_ua:
            language = 'Русский'
    print('Seems like the language of this word is: {}'.format(language))
