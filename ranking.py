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
        self.item_mat = np.zeros(shape=(self.item_num, self.item_num))
        self.ranking = []
        score_list = np.zeros(self.item_num)
        for i in self.record_list:
            if i[2] == i[3]:
                # Throw away draw games
                continue
            winner = self.all_item.index(i[0])
            looser = self.all_item.index(i[1])
            score_list[winner] += i[2] - i[3]
            score_list[looser] += i[3] - i[2]
            self.item_mat[winner][winner] += 1
            self.item_mat[looser][looser] += 1
            self.item_mat[winner][looser] -= 1
            self.item_mat[looser][winner] -= 1
        # replace the last line with 1
        self.item_mat[-1] = np.ones(self.item_num)
        score_list[-1] = 0
        # solve the matrix
        score = np.linalg.solve(self.item_mat, score_list)
        for i in range(self.item_num):
            self.ranking.append([self.all_item[i], 0, score[i]])
        self.ranking.sort(key=lambda x: x[-1], reverse=True)
        for i in range(self.item_num):
            self.ranking[i][1] = i + 1
            if i > 0 and self.ranking[i][2] == self.ranking[i - 1][2]:
                self.ranking[i][1] = self.ranking[i - 1][1]
        return self.ranking

    def colley(self) -> np.array:
        """
        The Colley Ranking.
        Returns the item name, ranking and the score.
        """
        # We first init the Colley matrix
        self.item_mat = np.zeros(shape=(self.item_num, self.item_num))
        self.ranking = []
        score_list = np.ones(self.item_num)
        for i in range(self.item_num):
            self.item_mat[i][i] = 2
        for i in self.record_list:
            if i[2] == i[3]:
                # Throw away draw games
                continue
            winner = self.all_item.index(i[0])
            looser = self.all_item.index(i[1])
            score_list[winner] += 0.5
            score_list[looser] -= 0.5
            self.item_mat[winner][winner] += 1
            self.item_mat[looser][looser] += 1
            self.item_mat[winner][looser] -= 1
            self.item_mat[looser][winner] -= 1
        # solve the matrix
        score = np.linalg.solve(self.item_mat, score_list)
        for i in range(self.item_num):
            self.ranking.append([self.all_item[i], 0, score[i]])
        self.ranking.sort(key=lambda x: x[-1], reverse=True)
        for i in range(self.item_num):
            self.ranking[i][1] = i + 1
            if i > 0 and self.ranking[i][2] == self.ranking[i - 1][2]:
                self.ranking[i][1] = self.ranking[i - 1][1]
        return self.ranking

    def find_dup(self) -> None:
        for i in self.record_list:
            if i[2] == i[3]:
                self.record_list.append([i[0], i[1], i[2] + 0.5, i[2] - 0.5])
                self.record_list.append([i[1], i[0], i[2] + 0.5, i[2] - 0.5])

    def borda(self,ranks:list)->list:
        """
        borda merge
        Input example:
        [
        [['A',3],['B',1],['D',2]],
        [['A',2],['B',1],['D',4],['C',3]],
        ]
        :param ranks: A list of items and their rank.
        :return: the merged ranking list
        """
        # first get all items
        all_item=[]
        scores=[]
        length_of_rank=[]
        for i in ranks:
            length_of_rank.append(len(i))
            for j in i:
                if not j[0] in all_item:
                    all_item.append(j[0])
        for i in all_item:
            scores.append([i])
            for j in range(len(length_of_rank)):
                scores[-1].append(-1)
        # Do broda count
        for i in range(len(ranks)):
            for j in range(len(ranks[i])):
                scores[all_item.index(ranks[i][j][0])][i+1]=ranks[i][j][1]
            # add unranked items
            for j in range(len(all_item)):
                if scores[j][i+1]==-1:
                    scores[j][i+1]=0.5*length_of_rank[i]+0.5
        borda=[]
        for i in scores:
            borda.append([i[0],sum(i[1:]),0])
        borda.sort(key=lambda x:x[1],reverse=False)
        for i in range(len(borda)):
            borda[i][2] = i + 1
            if i > 0 and borda[i][1] == borda[i - 1][1]:
                borda[i][2] = borda[i - 1][2]
        return borda

