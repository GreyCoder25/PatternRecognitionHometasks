from utils import estimate_g


UA_LETTERS = set('абвгґдеєжзиіїйклмнопрстуфхцчшщьюя')
RU_LETTERS = set('абвгдеёжзиыйклмнопрстуфхцчшщьъэюя')

g_ua = estimate_g('ua_text.txt', UA_LETTERS)
g_ru = estimate_g('ru_text.txt', RU_LETTERS)


def recognize_language(word, p_lang1, p_letter_lang1, p_pair_lang1, p_lang2, p_letter_lang2, p_pair_lang2):
    LANG1 = 'Українська'
    LANG2 = 'Русский'

    p_word_cond_lang1 = p_letter_lang1[word[0]]
    for i in range(1, len(word)):
        p_word_cond_lang1 *= p_pair_lang1[word[i-1:i+1]]

    p_word_cond_lang2 = p_letter_lang2[word[0]]
    for i in range(1, len(word)):
        p_word_cond_lang2 *= p_pair_lang2[word[i-1:i+1]]

    if p_lang1 * p_word_cond_lang1 > p_lang2 * p_word_cond_lang2:
        print(LANG1)
    else:
        print(LANG2)


P_UA = 0.5
P_RU = 0.5

while True:
    recognize_language(input('Enter the word: '), P_UA, p_letter_ua, p_pair_ua, P_RU, p_letter_ru, p_pair_ru)