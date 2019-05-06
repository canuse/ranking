import numpy as np


class ranking():
    def __init__(self, record_list=[[]]) -> None:
        """
        Init class ranking. Suppose all records are saved in the record_list.
        Each record of the record_list should be a list or a tuple with 4 items, the names and their score.
        Example: [['Sam','Alice',4,5],['Bob','Sam',1,3]]
        :param record_list: 4*n list
        """
        self.record_list = record_list
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
        self.ranking = []
        # A copy of list to return.

    def massey(self) -> np.array:
        """
        The Massey Ranking.
        Returns the item name, ranking and the score.
        """
        # We first init the Massey matrix
        self.score_list = np.zeros(self.item_num)
        for i in self.record_list:
            if i[2]==i[3]:
                # Throw away draw games
                continue
            winner = self.all_item.index(i[0])
            looser = self.all_item.index(i[1])
            self.score_list[winner] += i[2] - i[3]
            self.score_list[looser] += i[3] - i[2]
            self.item_mat[winner][winner] += 1
            self.item_mat[looser][looser] += 1
            self.item_mat[winner][looser] -= 1
            self.item_mat[looser][winner] -= 1
        # replace the last line with 1
        self.item_mat[-1] = np.ones(self.item_num)
        self.score_list[-1] = 0
        # solve the matrix
        score = np.linalg.solve(self.item_mat, self.score_list)
        for i in range(self.item_num):
            self.ranking.append([self.all_item[i],0,score[i]])
        self.ranking.sort(key=lambda x:x[-1],reverse=True)
        for i in range(self.item_num):
            self.ranking[i][1]=i+1
            if i>0 and self.ranking[i][2]==self.ranking[i-1][2]:
                self.ranking[i][1]=self.ranking[i-1][1]
        return self.ranking

