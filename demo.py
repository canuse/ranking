import ranking

if __name__ == "__main__":
    a = ranking.ranking([
        ['a', 'b', 5, 5],
        ['a', 'c', 5, 3],
        ['b', 'c', 4, 3],
        ['a', 'c', 5, 3],
        ['a', 'd', 5, 1],
        ['b', 'c', 5, 3],
        ['b', 'd', 5, 1],
        ['c', 'd', 3, 1],
        ['a', 'd', 4, 3],
        ['d', 'a', 4, 1],
    ])
    print(a.massey())
    print(a.colley())
    a.find_dup()
    print(a.massey())
    print(a.colley())

    print(a.borda([
        [['A',3],['B',1],['D',2]],
        [['A',2],['B',1],['D',4],['C',3]],
        [['E',1]]
        ]))
