# Automatic Topic Classification of Regional Newspapers Corpus

### data
Folder with all the data.
- ##### metadata
    - regional_rus.csv
        Original file with metadata and without text.
    - df_w_text.csv
        Table with relevant part of metadata and with lemmatized text.
    - df_w_text.csv
        Table with relevant part of metadata and with plain text.
    - dummies_table.csv, dummies_train.csv, dummies_test.csv
        Tables with one-hot-coded metadata and with text. First contains all data, second -- data with known topics, third -- data with unknown topics.
- ##### results
    - predicted_%classificatorName_%vectorizerName_%launchType.csv
        Output tables: text + binary predicted topics.
        *launchType* -- test or train, test -- topics for data are not known, train -- topics are known
    - predicted_%classificatorName_%vectorizerName_%launchType_hr.csv
       Same, but topics are presented as text.
    - %vectorizerName_%classifierName.png
        Confusion matrices.
    - results.md 
- ##### word2vec_models
    Word2Vec models with different parameters trained on the corpus.
- ##### stop_ru.txt
	Stopwords.

### Code files
- ##### init_models.py
    Main file. Contains table preparation, initializes models with chosen classificator. Returns table with text, predicted topics and initial topics (if they are known).
- ##### models.py
    File with three vectorization models. 
- ##### test_models.py
    Runs models.
- ##### make_it_human_readable.py
    Converts file with binary choices for every topic to file with text and names of topics. Gets five columns for train data -- text, true topics, predicted topics, topics which must've been predicted but haven't and topics which have been predicted but shouldn't have. For data with unknown topics gets only columns with text and predicted topics.
- ##### plot_cm.py
    Plots confusion matrix from table with binary choices for every topic.
- ##### new_w2v_model.py
    Builds new Word2Vec model.
- ##### get_w2v_models.py
    Builds Word2Vec models with different parameters using *new_w2v_model.py*.
