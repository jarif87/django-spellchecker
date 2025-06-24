from django.shortcuts import render, redirect
from .sustain import vocab, probs


def delete_letter(word, verbose=False):
    delete_l = []
    split_l = [(word[:i], word[i:]) for i in range(len(word))]
    delete_l = [L + R[1:] for L, R in split_l if R]
    if verbose:
        pass  # Removed print statement as it's commented out
    return delete_l


def switch_letter(word, verbose=False):
    def swap(c, i, j):
        c = list(c)
        c[i], c[j] = c[j], c[i]
        return ''.join(c)

    switch_l = []
    split_l = [(word[:i], word[i:]) for i in range(len(word))]
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]
    if verbose:
        pass  # Removed print statement
    return switch_l


def replace_letter(word, verbose=False):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    replace_l = []
    split_l = [(word[:i], word[i:]) for i in range(len(word))]
    replace_l = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in letters]
    replace_set = set(replace_l)
    if word in replace_set:
        replace_set.remove(word)
    replace_l = sorted(list(replace_set))
    if verbose:
        pass  # Removed print statement
    return replace_l


def insert_letter(word, verbose=False):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    split_l = [(word[:i], word[i:]) for i in range(len(word))]
    insert_l = [a + l + b for a, b in split_l for l in letters]
    if verbose:
        pass  # Removed print statement
    return insert_l


def edit_one_letter(word, allow_switches=True):
    edit_one_set = set()
    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))
    return edit_one_set


def edit_two_letters(word, allow_switches=True):
    edit_two_set = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_two_set.update(edit_two)
    return edit_two_set


def get_corrections(word, probs, vocab, verbose=False):
    suggestions = list(edit_two_letters(word).intersection(vocab))
    n_best = [[s, probs.get(s, -1)] for s in reversed(suggestions)]
    if verbose:
        print("suggestions = ", suggestions)
    return n_best


def handler(request):
    result = None
    if request.method == 'POST':
        my_word = request.POST.get('Name', '').strip()
        if my_word:  # Only process if not empty
            result = get_corrections(my_word, probs, vocab, verbose=False)
        else:
            result = []  # Empty result for empty input
    return render(request, "index.html", {'response': result})