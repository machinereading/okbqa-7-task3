import os
import sys
import argparse
from collections import Counter

OTHER = -1
MAIN = [100,101,102,103]
TRAIN_ALL = [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
ENTITY_LIST = [
"Leonard Hofstadter",
"Sheldon Cooper",
"Penny",
"Howard Wolowitz",
"Raj Koothrappali",
"Leslie Winkle",
"Eric Gablehauser",
"Mary Cooper",
"Receptionist",
"Missy Cooper",
"Sheldon's father",
"Louis",
"Penny's ex-boyfriend",
"Leonard's grandma",
"Joyce Kim"
]

main_entities = set(MAIN + [OTHER])
all_entities  = set(TRAIN_ALL + [OTHER])

def parse_key_file(filepath):
    with open(filepath, "rb") as f:
        keys = []
        for line in f:
            line = line.strip()
            if not line: return keys
            try:
                keys.append(int(line))
            except ValueError:
                print('Invalid key: "'+line+'" in '+filepath)
                return None
        return keys
    return None

def measure_macro_f1(entities, correct_counts, auto_counts, gold_counts):
    f1s = dict()
    for entity in entities.intersection(gold_counts.keys()):
        if correct_counts[entity] != 0:
            p = float(correct_counts[entity]) / auto_counts[entity]
            r = float(correct_counts[entity]) / gold_counts[entity]
            f1s[entity] = [p, r, 2.0 * p * r / (p + r)]
        else:
            f1s[entity] = [0.0] * 3;
    return f1s

def main():
    #parser = argparse.ArgumentParser(description="SemEval 2018 Task 4: Character Identification Evaluation Script")
    #parser.add_argument("ref_out",  type=str, help="Path to the input directory that contains ref/answer.txt and res/answer.txt, that are the gold and the system output files")
    #parser.add_argument("sys_out", type=str, help="Path to the output directory where scores.txt will be saved")
    #args = parser.parse_args()

    # read key files
    gold_file = 'data/ref_bigbang.out'#os.path.join(args.ref_out)
    auto_file = 'data/sys_bigbang.out'#os.path.join(args.sys_out)
    gold_keys = parse_key_file(gold_file)
    auto_keys = parse_key_file(auto_file)

    if not auto_keys:
        return

    if len(gold_keys) != len(auto_keys):
        print('Key mismatch: gold = %d keys, system = %d keys' % (len(gold_keys), len(auto_keys)))
        return

    # count correct entities
    main_correct     = Counter()
    all_correct      = Counter()
    gold_main_counts = Counter()
    gold_all_counts  = Counter()
    auto_main_counts = Counter()
    auto_all_counts  = Counter()

    for auto_key, gold_key in zip(auto_keys, gold_keys):
        # all entities
        auto_all_key = auto_key if auto_key in all_entities else OTHER
        gold_all_key = gold_key if gold_key in all_entities else OTHER

        auto_all_counts[auto_all_key] += 1
        gold_all_counts[gold_all_key] += 1
        if auto_all_key == gold_all_key: all_correct[auto_all_key] += 1

        # main + other entities
        auto_main_key = auto_key if auto_key in main_entities else OTHER
        gold_main_key = gold_key if gold_key in main_entities else OTHER

        auto_main_counts[auto_main_key] += 1
        gold_main_counts[gold_main_key] += 1
        if auto_main_key == gold_main_key: main_correct[auto_main_key] += 1

    # measure label accuracy
    total_count = len(gold_keys)
    all_accuracy  = float(sum(all_correct.values()))  / total_count
    main_accuracy = float(sum(main_correct.values())) / total_count

    # measure macro F1 scores
    all_f1  = measure_macro_f1(all_entities, all_correct, auto_all_counts, gold_all_counts)
    main_f1 = measure_macro_f1(main_entities, main_correct, auto_main_counts, gold_main_counts)

    all_avg_f1  = float(sum([prf[2] for prf in all_f1.values()]))  / len(all_f1)  if len(all_f1)  > 0 else 0.0
    main_avg_f1 = float(sum([prf[2] for prf in main_f1.values()])) / len(main_f1) if len(main_f1) > 0 else 0.0

    # print evaluation
    eval = [
        '********** Main + Other Entities **********',
        'Label Accuracy  : %6.2f (%d/%d)' % (100.0 * main_accuracy, sum(main_correct.values()), total_count),
        'Average Macro F1: %6.2f' % (100.0 * main_avg_f1),
        '************** All Entities ***************',
        'Label Accuracy  : %6.2f (%d/%d)' % (100.0 * all_accuracy, sum(all_correct.values()), total_count),
        'Average Macro F1: %6.2f' % (100.0 * all_avg_f1)]

    eval.append('***** Main + Other Entities F1 Scores *****')
    for key in sorted(main_f1.keys()):
        prf = main_f1[key]
        name = ENTITY_LIST[key-100] if key >= 100 else '##OTHERS##'
        s = '%40s: P = %6.2f (%4d/%4d), R = %6.2f (%4d/%4d), F1 = %6.2f' % (name, prf[0] * 100.0, main_correct[key], auto_main_counts[key], prf[1] * 100.0, main_correct[key], gold_main_counts[key], prf[2] * 100.0)
        eval.append(s)

    eval.append('********* All Entities F1 Scores **********')
    for key in sorted(all_f1.keys()):
        prf = all_f1[key]
        name = ENTITY_LIST[key-100] if key >= 100 else '##OTHERS##'
        s = '%40s: P = %6.2f (%4d/%4d), R = %6.2f (%4d/%4d), F1 = %6.2f' % (name, prf[0] * 100.0, all_correct[key], auto_all_counts[key], prf[1] * 100.0, all_correct[key], gold_all_counts[key], prf[2] * 100.0)
        eval.append(s)

    print('\n'.join(eval))
    # fout = open(os.path.join(args.output_dir, 'scores.txt'), 'w')
    # fout.write('accuracy:{0}\n'.format(100.0 * all_avg_f1))
    # fout.close()

    return all_accuracy, main_accuracy, all_avg_f1, main_avg_f1

if __name__ == "__main__":
    main()