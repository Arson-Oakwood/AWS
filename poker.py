#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertoolsю
# Можно свободно определять свои функции и т.п.
# -----------------
import itertools


RANKS = {
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9, "T": 10,
    "J": 11, "Q": 12, "K": 13, "A": 14
}


def sort_hand(element):
    return RANKS[element[0]]


def ranks_filter(ranks, sorted_hand):
    filler = []
    for i in sorted_hand:
        if RANKS[i[0]] == ranks[1]:
            filler.append(i)
    for i in sorted_hand:
        if i not in filler and len(filler) <= 4:
            filler.append(i)
    return sorted(filler, key=sort_hand)


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    ranks = []
    for i in hand:
        ranks.append(RANKS[i[0]])
    ranks.sort(reverse=True)
    return ranks


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    suit = []
    for i in hand:
        suit.append(i[1])
    for i in suit:
        if suit.count(i) >= 5:
            return True
    return False


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    counter = itertools.count(start=2)
    for i in range(len(ranks) - 1):
        if ranks[i] - ranks[i + 1] == 1:
            next(counter)
    if next(counter) >= 6:
        return True
    return False


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    counter = itertools.count(start=2)
    step = 0
    if n == 1:
        return ranks[0]
    for i in range(len(ranks) - 1):
        if ranks[i] == ranks[i + 1]:
            step = next(counter)
        if not ranks[i] == ranks[i + 1]:
            if n == step:
                return ranks[i]
            counter = itertools.count(start=2)
            step = 0
    if n == step:
        return ranks[-1]
    return None


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    counter = itertools.count(start=2)
    pairs = ()
    for i in range(len(ranks) - 1):
        if ranks[i] == ranks[i + 1]:
            if next(counter) <= 2:
                pairs += (ranks[i],)
            else:
                counter = itertools.count(start=2)
                pairs = ()
        else:
            counter = itertools.count(start=2)
    if len(pairs) == 2:
        return pairs
    return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    suit = 0
    filler = []
    ranks = hand_rank(hand)
    sorted_hand = sorted(hand, key=sort_hand, reverse=True)
    if ranks[0] == 8:
        for i in range(len(sorted_hand) - 1):
            if RANKS[sorted_hand[i][0]] - RANKS[sorted_hand[i + 1][0]] == 1 and \
                            sorted_hand[i][1] == sorted_hand[i + 1][1] and len(filler) <= 4:
                filler.append(sorted_hand[i])
            if len(filler) == 4:
                filler.append(sorted_hand[i + 1])
        return sorted(filler, key=sort_hand)

    elif ranks[0] == 7:
        for i in sorted_hand:
            if RANKS[i[0]] == ranks[1] or \
                                    RANKS[i[0]] == ranks[2] and i not in filler:
                filler.append(i)
        return sorted(filler, key=sort_hand)

    elif ranks[0] == 6:
        for i in sorted_hand:
            if RANKS[i[0]] == ranks[1] or \
                            RANKS[i[0]] == ranks[2]:
                filler.append(i)
        return sorted(filler, key=sort_hand)

    elif ranks[0] == 5:
        for i in sorted_hand:
            filler.append(i[1])
        for i in filler:
            if filler.count(i) >= 5:
                suit = i
                filler = []
        for i in sorted_hand:
            if i[1] == suit and len(filler) <= 4:
                filler.append(i)
        return sorted(filler, key=sort_hand)


    elif ranks[0] == 4:
        for i in range(len(sorted_hand) - 1):
            if RANKS[sorted_hand[i][0]] - RANKS[sorted_hand[i + 1][0]] == 1 \
                    and len(filler) <= 4:
                filler.append(sorted_hand[i])
                if len(filler) == 4:
                    filler.append(sorted_hand[i + 1])
        return sorted(filler, key=sort_hand)

    elif ranks[0] == 3:
        return ranks_filter(ranks, sorted_hand)

    elif ranks[0] == 2:
        for i in sorted_hand:
            if RANKS[i[0]] == ranks[1][0] or RANKS[i[0]] == ranks[1][1]:
                filler.append(i)
        for i in sorted_hand:
            if i not in filler and len(filler) <= 4:
                filler.append(i)
        return sorted(filler, key=sort_hand)

    elif ranks[0] == 1:
        return ranks_filter(ranks, sorted_hand)

    elif ranks[0] == 0:
        for i in sorted_hand:
            if len(filler) <= 4:
                filler.append(i)
        return sorted(filler, key=sort_hand)

    return


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    return


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    assert (best_hand("TS KS 2S 7C 6S 8C 7S".split())
            == ['2S', '6S', '7S', 'TS', 'KS'])
    assert (best_hand("7S TC 8H 7C 9S AC JD".split())
            == ['7S', '8H', '9S', 'TC', 'JD'])
    assert (best_hand("5S TC 8H 5C AS 5C JD".split())
            == ['5S', '5C', '5C', 'JD', 'AS'])
    assert (best_hand("JS 3C 8H 5C AS AC 3D".split())
            == ['3C', '3D', 'JS', 'AS', 'AC'])
    assert (best_hand("JS 3C QC 5C AS QH 2D".split())
            == ['5C', 'JS', 'QC', 'QH', 'AS'])
    assert (best_hand("JS 3C 6C 5C 9S QH 8D".split())
            == ['6C', '8D', '9S', 'JS', 'QH'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')

if __name__ == '__main__':
    test_best_hand()
    # test_best_wild_hand()
