#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
from collections import Counter
from prettytable import PrettyTable

def das_tretas_vish(batch_tweets):
   tweet_texts, screen_names, hashtags, words, urls, symbols = extract_entities(batch_tweets)

   common_entities = get_common_tweet_entities(batch_tweets, entity_threshold=5)

   for label, data in (("Word", words),
                    ("Sreen Name", screen_names),
                    ("Hashtag", hashtags),
                    ("Urls", urls),
                    ("Symbols", symbols),
                    ("Common Entities", common_entities)):
      pt = PrettyTable(field_names=[label, "Count"])
      c = Counter(data)
      [ pt.add_row(kv) for kv in c.most_common()[:10] ]
      pt.align[label], pt.align["Count"] = "l", "r"
      print (pt)

   print ("Diversidade léxica das palavras: %.2f" % lexical_diversity(words))
   print ("Diversidade léxica dos screen_names: %.2f" % lexical_diversity(screen_names))
   print ("Diversidade léxica das hashtags: %.2f" % lexical_diversity(hashtags))
   print ("Média de palavras por tweet: %.2f" % average_words(tweet_texts))

def extract_entities(tweets):
   tweet_texts = [ tweet['text']
                   for tweet in tweets ]

   screen_names = [ user_mention['screen_name']
                    for tweet in tweets
                        for user_mention in tweet['entities']['user_mentions'] ]

   hashtags = [ hashtag['text']
                for tweet in tweets
                    for hashtag in tweet['entities']['hashtags'] ]

   words = [ w
             for t in tweet_texts
                 for w in t.split() ]

   urls = [ url["expanded_url"]
            for tweet in tweets
                for url in tweet['entities']['urls'] ]

   symbols = [ symbol['text']
               for tweet in tweets
                   for symbol in tweet['entities']['symbols'] ]

   return tweet_texts, screen_names, hashtags, words, urls, symbols

def lexical_diversity(tokens):
   if (len(tokens) > 0):
      return 100.0 * len(set(tokens)) / len(tokens)
   else:
      return 0

def average_words(tweets):
   total_words = sum([ len(s.split()) for s in tweets ])
   return 1.0 * total_words / len(tweets)

def get_common_tweet_entities(statuses, entity_threshold=3):
   tweet_entities = [  e
                     for status in statuses
                         for entity_type in extract_entities([status])
                             for e in entity_type
                    ]

   return tweet_entities

   # c = Counter(tweet_entities).most_common()

   # # Compute frequencies
   # return [ (k,v)
   #          for (k,v) in c
   #              if v >= entity_threshold
   #        ]


