# [OKBQA-7 Task3 : Multimodal Character Identification on Videos](http://7.okbqa.org/hackathon/task/task3)

## Task Definition
This task aims to link each mention to a certain character in dialogue based on given dialouge text and corresponding video. 
Let a mention be a nominal referring to a person (e.g., *she*, *mom*, *Judy*), and an entity be a character in a dialogue.

![Example](https://image.ibb.co/fm4iP8/multi_modal_character_identification.png)

## Introduction
Character identification on text have been studied on Friends dataset and shown practical performance for identifying main characters([Chen et al., 2017](http://www.aclweb.org/anthology/K17-1023); [Choi&Chen, 2018](http://www.aclweb.org/anthology/S18-1007)).  However, these studies solved the problem in the form of entity linking on pre-defined characters. Thus, these modules couldn’t be applied to other than the Friends script unless module is re-trained on the newly constructed data. This task should be approached in the form of coreference resolution to be applied to arbitrary dialogue or video script. There is a study that introduces coreference resolution based approach for this task([Chen et al., 2017](http://www.aclweb.org/anthology/K17-1023)), but coreference resolution is difficult problem in NLP, so the performance is not practical(F1 : 57.46% for 9 main characters). 

Therefore, if we expand the task to get not only dialouge text but also video as inputs, the performance would be improved to a practical level by utilizing richer features.  This task is the extension of [SemEval2018 Task4](https://github.com/emorynlp/semeval-2018-task4). There are two main extensions. Firstly, it adds multi modality by utilizing video as a input. Secondly, the final module of this task could be applied to arbitrary dialogue or video script.

## Task Organizers

* Prof. Key-Sun Choi, [Semantic Web Research Center](http://semanticweb.kaist.ac.kr/), [KAIST](http://www.kaist.edu).
* Prof. Byoung-Tak Zhang, [Biointelligence Lab](https://bi.snu.ac.kr/), [Seoul National University](http://www.useoul.edu/).
* Kijong Han, [Semantic Web Research Center](http://semanticweb.kaist.ac.kr/), [KAIST](http://www.kaist.edu). (han0ah@kaist.ac.kr)
* Seong-Ho Choi, [Biointelligence Lab](https://bi.snu.ac.kr/), [Seoul National University](http://www.useoul.edu/).
* Giyeon Shin, [Semantic Web Research Center](http://semanticweb.kaist.ac.kr/), [KAIST](http://www.kaist.edu).

## Datasets
* This dataset is based on [SemEval2018 Task4 dataset](https://github.com/emorynlp/semeval-2018-task4). We added time and video information
* Dataset will be released on 07/18

The first two seasons of the TV show Friends are annotated for this task. 
Each season consists of episodes, each episode comprises scenes, and each scene is segmented into sentences. 
The followings describe the distributed datasets:

* [friends.train.episode_delim.conll](data/friends.train.episode_delim.conll): the training data where each episode is considered a document.
* [friends.test.episode_delim.conll](data/friends.test.episode_delim.conll): the test data where each episode is considered a document.

No dedicated development set was distributed for this task; feel free to make your own development set for training or perform cross-validation on the training sets.

## Format
All datasets follow the CoNLL 2012 Shared Task data format.
Documents are delimited by the comments in the following format:

```
#begin document (<Document ID>)[; part ###]
...
#end document
```

Each sentence is delimited by a new line ("\n") and each column indicates the following:

1. Document ID: `/<name of the show>-<season ID><episode ID>` (e.g., `/friends-s01e01`).
1. Scene ID: the ID of the scene within the episode.
1. Token ID: the ID of the token within the sentence.
1. Word form: the tokenized word.
1. Part-of-speech tag: the part-of-speech tag of the word (auto generated).
1. Constituency tag: the Penn Treebank style constituency tag (auto generated).
1. Lemma: the lemma of the word (auto generated).
1. Frameset ID: not provided (always `_`).
1. Word sense: not provided (always `_`).
1. Speaker: the speaker of this sentence.
1. Named entity tag: the named entity tag of the word (auto generated).
1. Start time: start time of the sentence on video. (millisecond)
1. End time: start time of the sentence on video. (millisecond)
1. Video file: Pre-processed sequence of image file from the video corresponding to the sentence. This column represents the file name of the pickle object
(Pickle object will be released on 08/01)
1. Entity ID: the entity ID of the mention, that is consistent across all documents.

Here is a sample from the training dataset:

```
/friends-s01e01  0  0  He     PRP   (TOP(S(NP*)    he     -  -  Monica_Geller   *  55422 59256 00005.pickle (284)
/friends-s01e01  0  1  's     VBZ          (VP*    be     -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  2  just   RB        (ADVP*)    just   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  3  some   DT        (NP(NP*    some   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  4  guy    NN             *)    guy    -  -  Monica_Geller   *  55422 59256 00005.pickle (284)
/friends-s01e01  0  5  I      PRP  (SBAR(S(NP*)    I      -  -  Monica_Geller   *  55422 59256 00005.pickle (248)
/friends-s01e01  0  6  work   VBP          (VP*    work   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  7  with   IN     (PP*))))))    with   -  -  Monica_Geller   *  55422 59256 00005.pickle -
/friends-s01e01  0  8  !      .             *))    !      -  -  Monica_Geller   *  55422 59256 00005.pickle -
```
```
/friends-s01e01  0  0  C'mon  VB   (TOP(S(S(VP*))  c'mon  -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  1  ,      ,                 *  ,      -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  2  you    PRP           (NP*)  you    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle (248)
/friends-s01e01  0  3  're    VBP            (VP*  be     -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  4  going  VBG            (VP*  go     -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  5  out    RP           (PRT*)  out    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  6  with   IN             (PP*  with   -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  7  the    DT             (NP*  the    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
/friends-s01e01  0  8  guy    NN            *))))  guy    -  -  Joey_Tribbiani  *  59459 61586 00006.pickle (284)
/friends-s01e01  0  9  !      .               *))  !      -  -  Joey_Tribbiani  *  59459 61586 00006.pickle -
```

A mention may include more than one word:

```
/friends-s01e02  0  0  Ugly         JJ   (TOP(S(NP(ADJP*  ugly         -  -  Chandler_Bing  *  332158 334460 00038.pickle (380
/friends-s01e02  0  1  Naked        JJ                *)  naked        -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  2  Guy          NNP               *)  Guy          -  -  Chandler_Bing  *  332158 334460 00038.pickle 380)
/friends-s01e02  0  3  got          VBD             (VP*  get          -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  4  a            DT              (NP*  a            -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  5  Thighmaster  NN               *))  thighmaster  -  -  Chandler_Bing  *  332158 334460 00038.pickle -
/friends-s01e02  0  6  !            .                *))  !            -  -  Chandler_Bing  *  332158 334460 00038.pickle -

```

The mapping between the entity ID and the actual character can be found in [`friends_entity_map.txt`](data/friends_entity_map.txt).

## Input
You can use [friends.train.episode_delim.conll](data/friends.train.episode_delim.conll) as a training input, and [friends.test.episode_delim.conll](data/friends.test.episode_delim.conll) as a test input.

## Output and Evaluation
Your output must consist of the entity ID of each mention, one per line, in the sequential order.  There are 6 mentions in the above example, which will generate the following output:

```
284
284
248
248
284
380
```


Given this output, the evaluation script will measure,

1. The label accuracy considering only 7 entities, that are the 6 main characters (Chandler, Joey, Monica, Phoebe, Rachel, and Ross) and all the others as one entity.
1. The macro average between the F1 scores of the 7 entities.
1. The label accuracy considering all entities, where characters not appearing in the tranining data are grouped as one entity, others.
1. The macro average between the F1 scores of all entities.
1. The F1 scores for 7 entities.
1. The F1 scores for all entities.
