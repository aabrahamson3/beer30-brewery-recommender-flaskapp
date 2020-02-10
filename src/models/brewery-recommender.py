import pickle

def load_model():
    """ Load the model from the .pickle file """
    model_file = open("src/models/stem_model_vs200.pickle", "rb")
    loaded_model = pickle.load(model_file)
    model_file.close()
    return loaded_model

def beer2beer(state, city, keyword):
    for i in lookup_dict:
        if lookup_dict[i]['name'] == beer:
            recs = model.docvecs.most_similar(str(i), topn=8000)
            try:   
                return location_filter(recs, state, city, 3)
                
    print ('Looks like we coulnd\'t find that one')
    
def get_recs_from_wordvec(keyword, topn=8000, state, city, n_recs=3, stem=True):
    if stem == True:
        ls = LancasterStemmer()
        vec = model[ls.stem(keyword)]
        tags = model.docvecs.most_similar([vec], topn=topn)