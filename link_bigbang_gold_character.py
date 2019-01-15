import pickle
import re

ALL_CHARACTERS = [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114]
MAIN_CHARACTERS = [100,101,102,103,104]

ENAME_TO_ID = {}
EID_TO_NAME = {}

def get_eid_by_mention(mention, speaker):
    mention = re.sub(r'[^\w]', ' ', mention).replace(' ', '').lower()

    #first-person pronoun match
    if (mention in ['i', 'my', 'me', 'mine']):
        if (speaker in ENAME_TO_ID):
            return ENAME_TO_ID[speaker]

    # all_match
    for ename_key in ENAME_TO_ID:
        r_ename_key = re.sub(r'[^\w]', ' ', ename_key).replace(' ', '').lower()
        if (mention == r_ename_key):
            return ENAME_TO_ID[ename_key]

    # first_name_match
    for ename_key in ENAME_TO_ID:
        names = ename_key.split()
        if (len(names) > 1):
            r_ename_key = re.sub(r'[^\w]', ' ', names[0]).replace(' ', '').lower()
            if (mention == r_ename_key):
                return ENAME_TO_ID[ename_key]
    return 1000

# entity_map
f = open('data/bigbang_entity_map.txt')
for line in f:
    eid, ename = line.strip().split('\t')
    eid = int(eid)
    if (eid not in ALL_CHARACTERS):
        continue
    ENAME_TO_ID[ename] = eid
    EID_TO_NAME[eid] = ename
f.close()


# Parse Prediction
with open('evaluate_result.pickle', 'rb') as handle:
    data = pickle.load(handle)
    predict_data = data['prediction']

# Parse Gold Data and
f = open('data/bigbang.english.v4_gold_conll','r',encoding='utf-8')
key = ''
nlp_datas = {}
gold_datas = []
for line in f:
    if ('#begin document' in line):
        key = line[17:32] + '_' + str(int(line[-3:-1]))
        nlp_datas[key] = []
    elif ('#end document' not in line and len(line) > 1):
        items = line.strip().split()
        nlp_datas[key].append({'word':items[3],
                                'lemma':items[6],
                                'speaker': items[9].replace('_',' ')})

        entityid = items[-1]
        if ('(' in entityid):
            gold_datas.append({'st':len(nlp_datas[key]) - 1,
                               'en':-1,
                               'entityid':int(entityid.replace('(','').replace(')','')),
                               'doc_key':key})
        if (')' in entityid):
            gold_datas[-1]['en'] = len(nlp_datas[key]) - 1
f.close()

#################### dummy_gold_predict_data_generate ###################
dummy_predict_data = {}
for item in gold_datas:
    doc_key = item['doc_key']
    if doc_key not in dummy_predict_data:
        dummy_predict_data[doc_key] = []
    added_to_curr_cluster = False
    for cnum,cluster in enumerate(dummy_predict_data[doc_key]):
        if (cluster[0][2] == item['entityid']):
            dummy_predict_data[doc_key][cnum].append((item['st'],item['en'],item['entityid']))
            added_to_curr_cluster = True
            break
    if not added_to_curr_cluster:
        dummy_predict_data[doc_key].append([(item['st'],item['en'],item['entityid'])])

new_predict_data = {}
for key in dummy_predict_data:
    cluster_list = dummy_predict_data[key]
    new_cluster_list = []
    for cluster in cluster_list:
        if (len(cluster) > 1):
            ttt = []
            for cluster_item in cluster:
                ttt.append((cluster_item[0],cluster_item[1]))
            new_cluster_list.append(tuple(ttt))
    new_predict_data[key] = new_cluster_list

predict_data = new_predict_data
###################################################

# majority voting
for doc_key, cluster_list in predict_data.items():
    for cluster_idx,cluster in enumerate(cluster_list):
        eid_list = []
        for i,boundary in enumerate(cluster):
            st = boundary[0]
            en = boundary[1]
            speaker = nlp_datas[doc_key][st]['speaker']
            mention = ''
            for j in range(st,en+1):
                mention = mention + nlp_datas[doc_key][j]['word'] + ' '
            mention = mention.strip()

            inferred_eid = get_eid_by_mention(mention,speaker)
            if (inferred_eid < 1000):
                eid_list.append(inferred_eid)

        # set most common id to cluster id, unless all are 0
        cluster_eid =  max(set(eid_list), key=eid_list.count) if len(eid_list) > 0 else 1000
        predict_data[doc_key][cluster_idx] = {'cluster_eid':cluster_eid,
                                              'cluster':cluster}


f_out = open('data/sys_bigbang.out','w',encoding='utf-8')
for index,item in enumerate(gold_datas):
    doc_key = item['doc_key']
    st = item['st']
    en = item['en']
    speaker = nlp_datas[doc_key][st]['speaker']
    mention = ''
    for j in range(st, en + 1):
        mention = mention + nlp_datas[doc_key][j]['word'] + ' '
    mention = mention.strip()

    e_id = -1
    for cluster in predict_data[doc_key]:
        for boundary in cluster['cluster']:
            if (boundary[0] == st and boundary[1] == en):
                e_id = cluster['cluster_eid']
                break
        if (e_id >= 0):
            break
    if (e_id < 0):
        e_id = get_eid_by_mention(mention, speaker)

    f_out.write(str(e_id))
    if (index < len(gold_datas)-1):
        f_out.write('\n')

f.close()