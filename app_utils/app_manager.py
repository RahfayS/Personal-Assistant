import re
import logging



class AppManager():

    def __init__(self):
        pass

    def search(self,query, search_word = 'search'):
        '''Takes every word after user says "search" or another search_word and returns all words after search_word'''
        
        # Take every word after 'search' in query
        search_pattern = r'(?<=search\s).*'
        match = re.search(search_pattern, query)

        search_term = match.group().strip()
        logging.info(f'Searching... {search_term}')

        return search_term