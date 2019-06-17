import random as rnd
import numpy as np


def estimate_g(file_name, letters):
    N = len(letters)
    states = '_' + letters     # '_' - k0('start of generation' state)

    phi = {}
    for l in states:
        phi[l] = 0

    g = {}
    for k_prev in states:
        for x in letters:
            for k in states:
                g[k_prev + x + k] = 0

    letters = set(letters)

    with open(file_name, 'r') as f:
        ch = f.read(1)
        ch = ch.lower()
        prev_state = '_'
        cur_state = '_'
        while ch:
            if ch in letters:
                cur_state = ch
                if g[prev_state + ch + cur_state] == 0:
                    g[prev_state + ch + cur_state] = 1
            else:
                if prev_state in letters:
                    cur_state = '_'
            prev_state = cur_state
            ch = f.read(1)
            ch = ch.lower()
        return g


def calculate_g_(g, letters):
    '''Returns matrix that represents ability to do a jump from one state to another.'''
    states = '_' + letters
    g_ = {}
    for a in states:
        for b in states:
            g_[a + b] = 0

    for a in states:
        for b in states:
            for x in letters:
                if g[a + x + b]:
                    g_[a + b] = 1
                    break
    return g_


def calculate_g_star(g_, letters):
    '''Calculate matrix of the smallest number of transitions (acts of generating a symbol) to get from
    one state to another.
    '''
    states = '_' + letters
    g_star = {}
    for a in states:
        for b in states:
            if a == b:
                g_star[a + b] = 0
            elif g_[a + b]:
                g_star[a + b] = 1
            else:
                g_star[a + b] = np.inf

    for k in states:
        for i in states:
            for j in states:
                g_star[i + j] = min(g_star[i + j], g_star[i + k] + g_star[k + j])
    return g_star


def init_costs(letters):
    letters = letters + '#'
    costs = {l1 + l2: rnd.randint(0, 5) for l1 in letters for l2 in letters}
    return costs


def preprocess_costs(costs, letters):
    '''To get the lowest cost for all operations Floyd-Warshell algorithm is used.
    1) Add #-symbol and replace in(s) to ch(#, s) and del(s) to ch(s, #);
    2) Build the complete graph (edges between all pairs exist), where nodes are associated with symbols
    and edges are associated with "ch(s1, s2)" operation. Weights of the edges are initial costs;
    3) Use Floyd-Warshell algorithm to obtain the lowest cost for each pair of arguments for ch() operation.
    '''
    letters = letters + '#'
    for k in letters:
        for i in letters:
            for j in letters:
                costs[i + j] = min(costs[i + j], costs[i + k] + costs[k + j])


def levenshtein_dist(word, letters, g_star, g):
    '''Calculates Levenshtein distance from word to automatic language.'''
    m = len(word)
    states = '_' + letters
    f = [{k: np.inf for k in states} for i in range(m + 1)]
    f_ = [{k: np.inf for k in states} for i in range(m + 1)]
    f[0]['_'] = 0
    f_[0]['_'] = 0

    for i in range(1, m + 1):
        for k in states:
            f1 = f[i - 1][k] + 1
            f2 = np.inf
            for k_ in states:
                if f2 > f[i - 1][k_] + (1 - g[k_ + word[i - 1] + k]):
                    f2 = f[i - 1][k_] + (1 - g[k_ + word[i - 1] + k])
            f_[i][k] = min(f1, f2)

        for k in states:
            min_val_f = np.inf
            for k_ in states:
                if min_val_f > f_[i][k_] + g_star[k_ + k]:
                    min_val_f = f_[i][k_] + g_star[k_ + k]
            f[i][k] = min_val_f

    dist = np.inf
    for k in states:
        if f[m][k] < dist:
            dist = f[m][k]
    return dist


if __name__ == '__main__':
    UA_LETTERS = "абвгдеєжзиіїйклмнопрстуфхцчшщьюя'"
    costs = init_costs(UA_LETTERS)
    # costs = {'aa': 3, 'ab': 4, 'ac': 1, 'ba': 3, 'bb': 1, 'bc': 2, 'ca': 1, 'cb': 2, 'cc': 3}
    # print(costs)
    preprocess_costs(costs, UA_LETTERS)
    # print(costs)

    # RU_LETTERS = "абвгдеёжзиыйклмнопрстуфхцчшщьъэюя"
    g_ua = estimate_g('ua_text.txt', UA_LETTERS)
    print(g_ua)
    g_ua_ = calculate_g_(g_ua, UA_LETTERS)
    print(g_ua_)
    g_star_ua = calculate_g_star(g_ua_, UA_LETTERS)
    print(g_star_ua)
    word = 'взлететь'
    lev_dist = levenshtein_dist(word.lower(), UA_LETTERS, g_star_ua, g_ua)
    print('Levenshtein distance from word {} to Ukrainian language is {}'.format(word, lev_dist))