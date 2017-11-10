import numpy as np
import random
import copy


WRONG_ANSWER = 0
RIGHT_ANSWER = 1
NUMBER_EXISTS = 2
LEVEL = 30


def check_sudoku(sud):
    row = np.zeros(10, dtype=np.int)
    col = np.zeros(10, dtype=np.int)
    box = np.zeros(10, dtype=np.int)
    for i in range(9):
        for j in range(9):
            row[sud[i,j]] += 1
            col[sud[j,i]] += 1
            x = j%3 + (i%3*3)
            y = j//3 + (i//3*3)
            #print([x,y])
            box[sud[x,y]] += 1
        if np.max(row[1:])>1 or np.max(col[1:])>1 or np.max(box[1:])>1:
            return False
        else:
            row = np.zeros(10, dtype=np.int)
            col = np.zeros(10, dtype=np.int)
            box = np.zeros(10, dtype=np.int)
    return True

def solve_sudoku(sud,mul = False,sol=False):
    tmp = sud.copy()
    for i in range(9):
        for j in range(9):
            if sud[i,j]==0:
                for k in range(9):
                    tmp[i,j]=k+1
                    if check_sudoku(tmp):
                        tmp,mul,sol = solve_sudoku(tmp,mul,sol)
                        #print(tmp)
                        if np.min(tmp)>0:
                            if mul:
                                return sud, False, True
                            return tmp, mul, True
                return sud, mul, sol
    if check_sudoku(tmp):
        return sud, mul, True
def make_sudoku2():
    sud = np.zeros((9,9), dtype=np.int)
    mul = False
    while(not mul):
        while True:
            tmp = sud.copy()
            tmp[int(random.random()*9),int(random.random()*9)] = int(random.random()*9)
            if check_sudoku(tmp):
                break

        _, mul, sol = solve_sudoku(tmp,True)
        if (sol):
            sud=tmp.copy()
    return sud

def make_sudoku(rem = 2):
    sud = np.zeros((9,9), dtype=np.int)
    a = np.array(range(9))+1
    np.random.shuffle(a)
    removed = 0
    while(True):

        for i in range(2):
            np.random.shuffle(a)
            sud[i]=a
        if check_sudoku(sud):
            break
    sud,mul,sol = solve_sudoku(sud)
    solved = copy.deepcopy(sud)
    while(True):
        temp = sud
        a = random.randint(0,8)
        b = random.randint(0,8)
        if(sud[a,b] == 0):
            a = random.randint(0, 9)
            b = random.randint(0, 9)
        else:
            sud[a,b]=0
            _, mul, sol = solve_sudoku(sud)
            if(mul== True | sol == False):
                sud = temp
            else:
                removed +=1
        if(rem == removed): break


    return sud, solved

def load_design():
    f = open('Sudoku_design.txt','r')
    design = f.read()
    return design



class Sudoku():
    def __init__(self,level):
        self.current,self.solved=make_sudoku(level)

    def set_nr(self,a,b,c):
        if self.current[a,b]==0:
            if self.solved[a,b] == c:
                self.current[a,b] = c;
                return RIGHT_ANSWER
            else:
                return WRONG_ANSWER
        else:
            return NUMBER_EXISTS

    def is_game_over(self):
        ans=False

        for elem in self.current:
            if 0 not in self.current:
                ans = True
            else:
                ans = False
                break
        return ans


    def sudoku_to_string(self):
        design = load_design()
        design = list(design)

        # TODO: x, y swap | Lisada disain
        ## KUI kasutab mingid protokolli symbolit, siis muuta protokoll 2ra
        out_str = ''
        for i in self.current:
            for j in i:
                out_str += str(j)
        x = 0
        for i in range(len(design)):

            if design[i]=='*':
                design[i]= out_str[x]
                x +=1;

        design= ''.join(design)

        return design



if __name__ == '__main__':
    sudokus = Sudoku(15)
    print sudokus.sudoku_to_string()