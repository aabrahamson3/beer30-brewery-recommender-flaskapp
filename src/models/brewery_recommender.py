import pickle
from gensim.models import Doc2Vec, KeyedVectors
from nltk.stem.lancaster import LancasterStemmer
# from gensim.models.callbacks import CallbackAny2Vec
from nltk.stem import LancasterStemmer

# def load_model():
#     """ Load the model from the .pickle file """
#     model_file = open("src/models/ls-s300-20epoch.model", "rb")
#     loaded_model = pickle.load(model_file)
#     model_file.close()
#     return loaded_model

def load_alt_model():
    """ Load the model from the .pickle file """
    loaded_model = Doc2Vec.load('src/models/ls-s300-20epoch.model')
    return loaded_model

def beer2beer(state, city, kw_or_beer):
    lookup_file = open("src/models/lookup_dict.pickle", "rb")
    lookup_dict = pickle.load(lookup_file)
    lookup_file.close()
    model = load_alt_model()
    state = state.upper()
    city = city.title()
    kw_or_beer = kw_or_beer.title()
    for i in lookup_dict:
        if lookup_dict[i]['name'] == kw_or_beer:
            recs = model.docvecs.most_similar(str(i), topn=10000)
            return location_filter2(recs, lookup_dict, state, city, 3)
    print ('Looks like we coulnd\'t find that one')
    
def get_recs_from_wordvec(state, city, keyword, n_recs=3, topn=8000, stem=True):
    lookup_file = open("src/models/lookup_dict.pickle", "rb")
    lookup_dict = pickle.load(lookup_file)
    lookup_file.close()
    state = state.upper()
    city = city.title()
    if stem == True:
        ls = LancasterStemmer()
        model = load_alt_model()
        try:
            vec = model[ls.stem(keyword)]
            tags = model.docvecs.most_similar([vec], topn=topn)
            return location_filter2(tags, lookup_dict, state, city, n_recs)
        except KeyError:
            return

# def location_filter(ranked_beers, lookup_dict, state, city, n):
#     """ 
#     This takes a list of tuples where the 1st element is a beer_id. It searches through the lookup dictionary
#     to match breweries based upon their location. And returns n number of recommendations

#     It returns the beer_id as key, and brewery_name, beer id, and beer name as values
#     """
#     located_brewery = {}
#     # state = 'CA'
#     # city = 'Los Angeles'
#     counter = 0

#     for beer in ranked_beers:
#         if counter < n:
#             dict_state = lookup_dict[beer[0]]['state']
#             dict_city = lookup_dict[beer[0]]['city']
#             brewery_id = lookup_dict[beer[0]]['brewery_id']
#             brewery_name = lookup_dict[beer[0]]['brewery_name']
#             beer_name = lookup_dict[beer[0]]['name']
#             if (dict_state == state) and (dict_city == city):
#         #             print(beer_breweries_lookup[beer[0]])
#                 if brewery_id in located_brewery:
#                     continue
#                 else:  
#                     located_brewery[brewery_id] = (brewery_name, beer[0], beer_name)
#                 counter += 1
    
#     return located_brewery

def location_filter2(ranked_beers, lookup_dict, state, city, n):
    """ 
    This takes a list of tuples where the 1st element is a beer_id. It searches through the lookup dictionary
    to match breweries based upon their location. And returns n number of recommendations

    It returns the beer_id as key, and brewery_name, beer id, and beer name as values
    """
    located_brewery = {}
    # state = 'CA'
    # city = 'Los Angeles'
    counter = 0

    for beer in ranked_beers:
        if counter < n:
            dict_state = lookup_dict[beer[0]]['state']
            dict_city = lookup_dict[beer[0]]['city']
            brewery_id = lookup_dict[beer[0]]['brewery_id']
            brewery_name = lookup_dict[beer[0]]['brewery_name']
            beer_name = lookup_dict[beer[0]]['name']
            if (len(state) > 0) and (len(city)>0):
                if (dict_state == state) and (dict_city == city):
            #             print(beer_breweries_lookup[beer[0]])
                    if brewery_id in located_brewery:
                        continue
                    else:  
                        located_brewery[brewery_id] = (brewery_name, beer[0], beer_name)
                
                    counter += 1
            # ignores state field
            elif len(state) == 0:
                if (dict_city == city):        
                    if brewery_id in located_brewery:
                        continue
                    else:  
                        located_brewery[brewery_id] = (brewery_name, beer[0], beer_name)
                
                    counter += 1

            elif len(city) == 0:        
                if (dict_state == state):
                    if brewery_id in located_brewery:
                        continue
                    else:  
                        located_brewery[brewery_id] = (brewery_name, beer[0], beer_name)
                
                    counter += 1
    if len(located_brewery) > 0:
        return located_brewery
    else:
        return 

