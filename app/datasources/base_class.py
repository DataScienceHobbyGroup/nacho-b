class datasource_base_class:
    '''Abstract base class to act as an interface to define methods that must be present in data sources'''

    def new_data_available(self) -> bool:
        '''Returns true if there are more rows abailable, false if not'''
        pass

    def get_next_row(self) -> dict:
        '''Returns the next data row if one exists, throws an exception if not'''
        pass
