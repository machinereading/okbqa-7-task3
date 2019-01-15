import os
import sys
import argparse
from collections import Counter

OTHER = -1
MAIN = [59, 183, 248, 292, 306, 335]
TRAIN_ALL = [28, 51, 59, 163, 168, 183, 195, 248, 292, 306, 317, 335, 401, 402, 403]
ENTITY_LIST = [
'Abby',
'Al',
'Al Kostelic',
'Al Minser',
'Al Pacino',
'Alan',
'Albert Einstein',
'Alex',
'All',
'Amber',
'Amger',
'Andie McDowell',
'Andr',
'Andre',
'Andrea',
'Andrea\'s friend',
'Andrew',
'Angela Delvecchio',
'Annabelle',
'Artelle',
'Ashley',
'Aunt Edna',
'Aunt Iris',
'Aunt Lillian',
'Aunt Phyllis',
'Aunt Syl',
'Aurora',
'Avery',
'Barbara',
'Barry',
'Ben',
'Bernie Spellman',
'Best Man',
'Bethel',
'Betty',
'Big Bully',
'Bill Clinton',
'Bill Dreskin\'s father',
'Billy Dreskin',
'Bing',
'Bishop Tutu',
'Black Bart',
'Bob',
'Bobby Rush',
'Boss Man Bing',
'Brad',
'Braverman',
'Brent Mussberger',
'Brian',
'Brittany',
'Carl',
'Carol Willick',
'Carol and Susan\'s caterer',
'Carol\'s grandmother',
'Caroline',
'Casey',
'Casting Guy',
'Cathy Bates',
'Celia',
'Chandler Bing',
'Chandler\'s date',
'Chandler\'s date\'s husband',
'Chandler\'s date\'s husband\'s secretary',
'Chandler\'s ex-girlfriend',
'Chandler\'s girlfriend',
'Chandler\'s imaginary friend',
'Chandler\'s secretary',
'Charles Bing',
'Chrissy',
'Christine',
'Coma Guy',
'Customer',
'Damone',
'Dan',
'Dana',
'Danielle',
'Danny Arshak',
'Daryl Hannah',
'Dave Thomas',
'David Hasselhof',
'Deb',
'Debbie',
'Debra',
'Dee',
'Demi Moore',
'Denise DeMarco',
'Dick Clark',
'Dillon',
'Director',
'Director\'s Assistant',
'Donna Reid',
'Dorothy',
'Dr. Baldhara',
'Dr. Bazida',
'Dr. Drake Remoray',
'Dr. Flanen',
'Dr. Franzblau',
'Dr. Horton',
'Dr. Mitchell',
'Dr. Oberman',
'Dr. Remore',
'Dr. Rosen',
'Dr. Wong',
'Drew Barrymore',
'Dudley Moore',
'Duncan',
'Ed',
'Ed Begley',
'Eddie',
'Eddie Minowick',
'Eddie Moskowitz',
'Eddie\'s ex-girlfriend',
'Eddie\'s previous roommate',
'Emma',
'Eric Estrada',
'Eric Prower',
'Erica Ford',
'Ernest Borgnine',
'Err',
'Error',
'Estelle',
'Estelle Leonard',
'Esther Livingston',
'Ethan',
'Evelyn Dermer',
'Ewing',
'Fake Monica',
'Fleischman',
'Flench',
'Flight Attendant',
'Florence Henderson',
'Foghorn Leghorn',
'Frank Buffay',
'Frankie',
'Frannie',
'Freud',
'Fun Bobby',
'Gail',
'George',
'George Bailey',
'George Stephanopoulos',
'Girl',
'Girls',
'Gloria Tribbiani',
'Grandmother',
'Gunther',
'Guy',
'Guy 1',
'Guys',
'Hannibal Lecter',
'Helen',
'Henry',
'Hombre Man',
'Howard',
'Huey Lewis',
'Hugh Grant',
'Ingrid Bergman',
'Intercom',
'Interviewer',
'Ive',
'Jack',
'Jack 1',
'Jack 2',
'Jack Geller',
'Jade',
'James Bond',
'Jamie',
'Jane',
'Janice',
'Janitor',
'Jason Costalano',
'Jason Hurley',
'Jay Leno',
'Jeannie',
'Jill',
'Jill Goodacre',
'Jill Green',
'Jill\'s mom',
'Jim Crochee',
'Jimmy Hauser',
'Joan Collins',
'Joanne',
'Joanne\'s father',
'Joey Tribbiani',
'Joey Tribbiani Sr.',
'Joey\'s Co-star',
'Joey\'s cousin',
'Joey\'s date',
'Joey\'s date\'s friend',
'Joey\'s tailor',
'John Savage',
'John Voit',
'Johnny Shapiro',
'Jordie',
'Joseph Stalin',
'Judy Geller',
'Judy Jetson',
'Julie',
'Julie\'s friend',
'Karen',
'Kid',
'Kip',
'Kristin',
'Laurie Schaffer',
'Leon',
'Leonard Green',
'Leroy',
'Leslie',
'Liam Neeson',
'Lifson',
'Lily Buffay',
'Linda',
'Lipson',
'Little Bully',
'Lizzie',
'Lola',
'Lori',
'Lorne Green',
'Lorraine',
'Lowell',
'Luisa',
'Luisa\'s supervisor',
'Lydia',
'Lydia\'s baby',
'Lydia\'s husband',
'Lydia\'s mom',
'Malibu Ken',
'Man',
'Man 1',
'Man 2',
'Marcel',
'Marcel Marceau',
'Mark',
'Marsha',
'Marty',
'Mary Tyler Moore',
'Max',
'Melanie',
'Messier',
'Michael',
'Michelle',
'Milton',
'Mindy',
'Mira',
'Miss Buffay',
'Miss Crankypants',
'Miss Kitty',
'Moncia',
'Monica Geller',
'Monica\'s ex-boyfriend',
'Monica\'s grandmother',
'Morly Safer',
'Mother Theresa',
'Mover',
'Mr. Adelman',
'Mr. Clean',
'Mr. Douglas',
'Mr. Greene',
'Mr. Heckles',
'Mr. Peanut',
'Mr. Ratstatter',
'Mr. Roger',
'Mr. Roper',
'Mr. Salty',
'Mr. Treeger',
'Mr. Tribbiani',
'Mr. Wineburg',
'Mrs. Adelman',
'Mrs. Bing',
'Mrs. Buffay',
'Mrs. Cobb',
'Mrs. Geller',
'Mrs. Green',
'Mrs. Greene',
'Mrs. Tribbiani',
'Mrs. Wallace',
'Mrs. Wallace\'s sister',
'Mrs. Wineburg',
'Ms. Thomas',
'Nathan',
'Nina Bookbinder',
'Norman Mailer',
'Nurse',
'Paolo',
'Paul',
'Paul\'s ex-girlfriend',
'Paula',
'Paulo',
'Person 1',
'Person 2',
'Pete',
'Pete Carney',
'Phoebe Buffay',
'Phoebe and Rachel',
'Phoebe\'s Assistant',
'Phoebe\'s Friends',
'Phoebe\'s boyfriend',
'Phoebe\'s date',
'Phoebe\'s friend',
'Phoebe\'s grandmother',
'Phoebe\'s grandmother\'s boyfriend',
'Phoebe\'s hairdresser',
'Phoebe\'s stepfather',
'Phoebe, Joey, and Ross',
'Pizza Guy',
'Producer',
'Rachel Green',
'Rachel and Phoebe',
'Rachel\'s date',
'Rachel\'s friend',
'Rachel\'s interviewer',
'Rachel\'s interviewer\'s cousin',
'Rachel\'s sister',
'Radio',
'Ramone',
'Randy Brown',
'Receptionist',
'Richard',
'Richard Burke',
'Richard\'s son',
'Rick',
'Rob',
'Rob Dohnen',
'Rob Roy',
'Robbie',
'Robert Pillman',
'Rod Steiger',
'Rodney McDowell',
'Rodrigo',
'Roger',
'Roland',
'Rona',
'Ronni Rappelano',
'Rose',
'Rose Marie',
'Ross Geller',
'Ross\' date',
'Ross\' grandmother',
'Russ',
'Ryan',
'Sandra Green',
'Sandy',
'Scott Alexander',
'Security Guard',
'Shannon Cooper',
'Shelley',
'Shirley',
'Sidney Marks',
'Silvian',
'Soupy Sales',
'Spike Lee',
'Stacy Roth',
'Steffi Graf',
'Stella Niedman',
'Stephanie',
'Steve',
'Store Guy',
'Stranger',
'Susan Bunch',
'Susan Sallidor',
'Susie',
'Tanya',
'Tattoo Artist',
'Teacher',
'Terry',
'The Guys',
'The Whole Party',
'Tilly',
'Tina',
'Tina\'s husband',
'Toby',
'Tommy Rollerson',
'Tony',
'Tony DeMarco',
'Tony Randall',
'Tova Borgnine',
'Tracy',
'Trainer',
'Travis',
'Tso',
'Ugly Naked Guy',
'Uma Thurman',
'Uncle Freddie',
'Uncle Sal',
'Uncle Sal\'s wife',
'Underdog',
'Unknown',
'Ursula',
'Van Damme',
'Vidal Buffay',
'Waiter',
'Waitress',
'Warren Beatty',
'Wedding Planner',
'Wendy',
'Weve',
'Woman',
'Woman 1',
'Yamaguchi',
'Yasmine Blepe',
'Young Ethan',
'Girl 2',
'Girl 3',
'Monica\'s grandfather'
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
    gold_file = 'data/ref_friendsnew.out'#os.path.join(args.ref_out)
    auto_file = 'data/sys_friendsnew.out'#os.path.join(args.sys_out)
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
        name = ENTITY_LIST[key] if key >= 0 else '##OTHERS##'
        s = '%40s: P = %6.2f (%4d/%4d), R = %6.2f (%4d/%4d), F1 = %6.2f' % (name, prf[0] * 100.0, main_correct[key], auto_main_counts[key], prf[1] * 100.0, main_correct[key], gold_main_counts[key], prf[2] * 100.0)
        eval.append(s)

    eval.append('********* All Entities F1 Scores **********')
    for key in sorted(all_f1.keys()):
        prf = all_f1[key]
        name = ENTITY_LIST[key] if key >= 0 else '##OTHERS##'
        s = '%40s: P = %6.2f (%4d/%4d), R = %6.2f (%4d/%4d), F1 = %6.2f' % (name, prf[0] * 100.0, all_correct[key], auto_all_counts[key], prf[1] * 100.0, all_correct[key], gold_all_counts[key], prf[2] * 100.0)
        eval.append(s)

    print('\n'.join(eval))
    # fout = open(os.path.join(args.output_dir, 'scores.txt'), 'w')
    # fout.write('accuracy:{0}\n'.format(100.0 * all_avg_f1))
    # fout.close()

    return all_accuracy, main_accuracy, all_avg_f1, main_avg_f1

if __name__ == "__main__":
    main()