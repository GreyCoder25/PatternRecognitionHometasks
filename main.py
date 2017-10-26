import numpy as np
import estimating_probabilities as p_est


UA_LETTERS = set('абвгґдеєжзиіїйклмнопрстуфхцчшщьюя')
RU_LETTERS = set('абвгдеёжзиыйклмнопрстуфхцчшщьъэюя')

p_est.estimate_probabilities('ua_text.txt', UA_LETTERS)