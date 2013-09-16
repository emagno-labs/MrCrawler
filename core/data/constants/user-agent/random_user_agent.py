import random
import os

UA_LIST = os.path.join('core', 'data', 'user_agent', 'user-agent-list.txt')
   
def get_random_user_agent():
   ua_file = open(UA_LIST, 'r')
   uas = ua_file.readlines()
   ua = random.choice(uas)
      
   return 'teste'  # ua.strip()
