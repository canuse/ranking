import numpy as np


class ranking():
    def __init__(self, record_list=[[]]) -> None:
        """
        Init class ranking. Suppose all records are saved in the record_list.
        Each record of the record_list should be a list or a tuple with 4 items, the names and their score.
        Example: [['Sam','Alice',4,5],['Bob','Sam',1,3]]
        :param record_list: 4*n list
        """
        self.all_item = []
        # all items in the record to build the n*n matrix
        for record in record_list:
            if record[0] not in self.all_item:
                self.all_item.append(record[0])
            if record[1] not in self.all_item:
                self.all_item.append(record[1])
        self.item_num = len(self.all_item)
        # number od unique items
        self.item_mat = np.zeros(shape=(self.item_num, self.item_num))
        # The matrix, considered as the Massey matrix in MasseyRanking, fo example.
        self.ranking = np.zeros(shape=(self.item_num, 2))
        # A copy of list to return.

