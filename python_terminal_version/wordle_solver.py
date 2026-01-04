import math
import pickle
import os
from multiprocessing import Pool, cpu_count

def encode_pattern(guess, answer):
    g = list(guess)
    a = list(answer)
    out = [0, 0, 0, 0, 0]
    for i in range(5):
        if g[i] == a[i]:
            out[i] = 2
            a[i] = None
            g[i] = None
    for i in range(5):
        if g[i] is not None and g[i] in a:
            out[i] = 1
            a[a.index(g[i])] = None
    code = 0
    for v in out:
        code = code * 3 + v
    return code

def compute_row(args):
    guess, words = args
    row = {}
    for answer in words:
        row[answer] = encode_pattern(guess, answer)
    return (guess, row)

def precompute_patterns(words):
    table = {}
    total = len(words)
    num_cores = cpu_count()
    
    print(f"Using {num_cores} CPU cores for faster computation...")
    
    with Pool(num_cores) as pool:
        args = [(word, words) for word in words]
        results = []
        
        for i, result in enumerate(pool.imap_unordered(compute_row, args, chunksize=50)):
            if i % 500 == 0:
                print(f"Progress: {i}/{total}", end="\r")
            results.append(result)
        
        for guess, row in results:
            table[guess] = row
    
    print(f"Progress: {total}/{total}")
    return table

def load_or_compute_patterns(words):
    cache_file = "python_terminal_version/wordle_patterns_cache.pkl"
    
    if os.path.exists(cache_file):
        print("Loading cached patterns...")
        try:
            with open(cache_file, "rb") as f:
                cached_data = pickle.load(f)
                if cached_data.get("word_count") == len(words):
                    print("Cache loaded!\n")
                    return cached_data["table"]
        except:
            pass
    
    print("Precomputing patterns... (one-time setup, we are loading the possible combinations)")
    print("You can leave it run in the background")
    table = precompute_patterns(words)
    
    try:
        with open(cache_file, "wb") as f:
            pickle.dump({"table": table, "word_count": len(words)}, f)
        print("Patterns cached for next time!")
    except:
        pass
    
    return table

def reduce_words(words, guess, pattern, table):
    return [w for w in words if table[guess][w] == pattern]

def best_guess(candidates, all_words, table):
    best_word = None
    best_score = math.inf
    
    for guess in candidates:
        buckets = {}
        for target in candidates:
            p = table[guess][target]
            buckets[p] = buckets.get(p, 0) + 1
        worst_case = max(buckets.values())
        if worst_case < best_score:
            best_score = worst_case
            best_word = guess
            if worst_case == 1:
                return best_word
    
    if len(candidates) <= 3:
        return best_word
    
    if best_score > 2:
        for guess in all_words:
            if guess in candidates:
                continue
            buckets = {}
            for target in candidates:
                p = table[guess][target]
                buckets[p] = buckets.get(p, 0) + 1
            worst_case = max(buckets.values())
            if worst_case < best_score:
                best_score = worst_case
                best_word = guess
                if worst_case <= 2:
                    break
    
    return best_word

def interactive_solver(words, table):
    candidates = words[:]
    print("Wordle Solver - Interactive Mode")
    print("Pattern: 0=gray, 1=yellow, 2=green")
    print("Example: gray-yellow-green-gray-green = 01202")
    print()
    
    guess = "TRACE"
    print(f"Guess this word: {guess}")
    
    while True:
        pattern_input = input(f"\nPattern for '{guess}': ").strip()
        
        if len(pattern_input) != 5 or not pattern_input.isdigit():
            print("Invalid! Enter exactly 5 digits (0=gray, 1=yellow, 2=green)")
            continue
        
        pattern = 0
        for digit in pattern_input:
            pattern = pattern * 3 + int(digit)
        
        candidates = reduce_words(candidates, guess, pattern, table)
        print(f"Remaining: {len(candidates)}", end="")
        
        if len(candidates) == 0:
            print("\nNo words match. Check your pattern.")
            break
        
        if len(candidates) == 1:
            print(f" → Answer: {candidates[0]}")
            break
        
        if len(candidates) <= 10:
            print(f" → {', '.join(candidates)}")
        else:
            print()
        
        guess = best_guess(candidates, words, table)
        print(f"Guess this word: {guess}")

if __name__ == "__main__":
    with open("python_terminal_version/word_database.txt", "r") as f:
        words = [w.strip().upper() for w in f.readlines() if w.strip()]
    
    words = [w for w in words if len(w) == 5]
    
    print("Wordle Solver")
    print("=" * 50)
    print()
    table = load_or_compute_patterns(words)
    interactive_solver(words, table)
