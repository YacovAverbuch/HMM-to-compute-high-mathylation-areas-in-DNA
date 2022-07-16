
import numpy as np
import matplotlib.pyplot as plt
import argparse

# C is mathylated, T in not
# [x, y] x = num(C), y = num(C) + num(T)


def plot_results_2_states(fasta, ph, pl, likelihood_table):
    x = np.arange(fasta.shape[1])
    plt.plot(x, [ph]*len(x), 'r-')  # HIGH
    plt.plot(x, [pl]*len(x), 'g-')  # LOW
    positions = np.argmax(likelihood_table, axis=0)
    colors = ['red' if i == 0 else 'green' for i in positions]
    prop = fasta[0, :] / fasta[1, :]
    plt.scatter(x=x, y=prop, c=colors, s=0.4)
    plt.ylim(-0.1, 1.1)
    plt.show()


def plot_results_3_states(fasta, ph, likelihood_table):
    x = np.arange(fasta.shape[1])
    plt.plot(x, [ph[0]]*len(x), 'r-', linewidth=0.5)  # HIGH
    plt.plot(x, [ph[1]]*len(x), 'g-', linewidth=0.5)  # LOW
    plt.plot(x, [ph[2]]*len(x), 'b-', linewidth=0.5)  # OTHER
    positions = np.argmax(likelihood_table, axis=0)
    colors = ['red' if i == 0 else ('green' if i == 1 else 'blue') for i in positions]
    prop = fasta[0, :] / fasta[1, :]
    plt.scatter(x=x, y=prop, c=colors, s=0.4)
    plt.ylim(-0.1, 1.1)
    plt.show()


def eliminate_zeros(arr):
    return arr[arr[:, 1] != 0]


def eliminate_zeros_add_one(arr):
    arr[:, 0] += 1
    arr[:, 1] += 2
    return arr


def array_to_prob(arr):
    return arr[:, 0] / arr[:, 1]


def smooth(arr):
    ret = np.zeros(arr.shape[0] + 7)
    for i in range(7):
        ret[i:-(7-i)] += arr
    return (ret / 7)[3:-4]


def get_base_line_values(arr):
    HIGH = 'High'
    LOW = 'Low'
    for i in range(0, arr.shape[0], 200):
        x = np.arange(1, 201)
        plt.plot(x, arr[200*i: 200*(i+1)], 'b-')
        plt.ylim(0, 1)
        plt.show()
        input('cont?')
    low_threshold = 0.3
    high_threshold = 0.7
    state = 'Low'
    transitions = 0
    sum_high, sum_low = 0, 0
    for i in range(arr.shape[0]):
        if arr[i] < low_threshold and state == HIGH:
            transitions += 1
            state = LOW
        if arr[i] > high_threshold:
            state = HIGH
        if state == HIGH:
            sum_high += 1
        if state == LOW:
            sum_low += 1

    print('num of transitions: ' + str(transitions))
    print('prob for transition from low to high: ' + str(1 / (sum_low / transitions)))
    print('prob for transition from high to low: ' + str(1 / (sum_high / transitions)))



# def calc_ll(hl, lh, emission_table):
#     a = Automata(hl, lh)
#     sum_ll = []
#     for element in itertools.product([0, 1], repeat=emission_table.shape[1]):
#         cur = 0
#         for i in range(1, emission_table.shape[1]):
#             cur += a.transition_probabilities[element[i-1], element[i]]
#         for i in range(0, emission_table.shape[1]):
#             cur += emission_table[element[i], i]
#         sum_ll += [cur]
#     return logsumexp(sum_ll)

