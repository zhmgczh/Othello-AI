import json
import numpy
import math
import random
import time
DIR=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)) # 方向向量
# 放置棋子，计算新局面
def place(board,x,y,color):
	if x<0:
		return False
	board[x][y]=color
	valid=False
	global size
	for d in range(size):
		i=x+DIR[d][0]
		j=y+DIR[d][1]
		while 0<=i and i<size and 0<=j and j<size and board[i][j]==-color:
			i+=DIR[d][0]
			j+=DIR[d][1]
		if 0<=i and i<size and 0<=j and j<size and board[i][j]==color:
			while True:
				i-=DIR[d][0]
				j-=DIR[d][1]
				if i==x and j==y:
					break
				valid=True
				board[i][j]=color
	return valid
# 产生决策
'''
def randplace(board,color):
	moves=[]
	global size
	for i in range(size):
		for j in range(size):
			if board[i][j]==0:
				newBoard=board.copy()
				if place(newBoard,i,j,color):
					moves.append((i,j))
	if len(moves)==0:
		return -1,-1
	return random.choice(moves)
'''
placed=0
myColor=1
opColor=-1
size=8
live=[[3,5,5,5,5,5,5,3],[5,8,8,8,8,8,8,5],[5,8,7,6,6,7,8,5],[5,8,6,5,5,6,8,5],[5,8,6,5,5,6,8,5],[5,8,7,6,6,7,8,5],[5,8,8,8,8,8,8,5],[3,5,5,5,5,5,5,3]]
live=numpy.array(live)
table=[[91150,-2750,10,0,0,10,-2750,91150],[-2750,-74450,-5,-10,-10,-5,-74450,-2750],[10,-5,-10,-5,-5,-10,-5,10],[0,-10,-5,0,0,-5,-10,0],[0,-10,-5,0,0,-5,-10,0],[10,-5,-10,-5,-5,-10,-5,10],[-2750,-74450,-5,-10,-10,-5,-74450,-2750],[91150,-2750,10,0,0,10,-2750,91150]]
table=numpy.array(table)
start_time=0
time_limit=6
def do_change_live(a,b):
	global live
	if a>0:
		live[a-1][b]-=1
		if b>0:
			live[a-1][b-1]-=1
		if b<7:
			live[a-1][b+1]-=1
	if a<7:
		live[a+1][b]-=1
		if b>0:
			live[a+1][b-1]-=1
		if b<7:
			live[a+1][b+1]-=1
	if b>0:
		live[a][b-1]-=1
	if b<7:
		live[a][b+1]-=1
def undo_change_live(a,b):
	global live
	if a>0:
		live[a-1][b]+=1
		if b>0:
			live[a-1][b-1]+=1
		if b<7:
			live[a-1][b+1]+=1
	if a<7:
		live[a+1][b]+=1
		if b>0:
			live[a+1][b-1]+=1
		if b<7:
			live[a+1][b+1]+=1
	if b>0:
		live[a][b-1]+=1
	if b<7:
		live[a][b+1]+=1
def max_level(board,depth,beta,player):
	moves=[]
	end_flag=True
	player_num=0
	global size
	for i in range(size):
		for j in range(size):
			if board[i][j]==0:
				new_board=board.copy()
				if place(new_board,i,j,player):
					end_flag=False
					moves.append((i,j))
			elif board[i][j]==player:
				player_num+=1
	if len(moves)==1:
		depth+=1
	global placed,start_time,time_limit
	if depth==0 or placed==64 or end_flag or player_num==0:
		if placed==64 or player_num==0:
			return evaluate(board,1)
		else:
			return evaluate(board,0)
	random.shuffle(moves)
	evaluation=0
	alpha=-20000000
	alphas=-20000000
	for i in range(len(moves)):
		if time.time()+0.01>start_time+time_limit:
			break
		new_board=board.copy()
		if place(new_board,moves[i][0],moves[i][1],player):
			placed+=1
			do_change_live(moves[i][0],moves[i][1])
			evaluation=min_level(new_board,depth-1,alphas,-player)
			undo_change_live(moves[i][0],moves[i][1])
			placed-=1
			if evaluation>=beta:
				return evaluation
			if evaluation>alpha:
				alpha=evaluation
				alphas=alpha
	return alpha
def min_level(board,depth,alpha,player):
	moves=[]
	end_flag=True
	player_num=0
	global size
	for i in range(size):
		for j in range(size):
			if board[i][j]==0:
				new_board=board.copy()
				if place(new_board,i,j,player):
					end_flag=False
					moves.append((i,j))
			elif board[i][j]==player:
				player_num+=1
	if len(moves)==1:
		depth+=1
	global placed,start_time,time_limit
	if depth==0 or placed==64 or end_flag or player_num==0:
		if placed==64 or player_num==0:
			return evaluate(board,1)
		else:
			return evaluate(board,0)
	random.shuffle(moves)
	evaluation=0
	beta=20000000
	betas=20000000
	for i in range(len(moves)):
		if time.time()+0.01>start_time+time_limit:
			break
		new_board=board.copy()
		if place(new_board,moves[i][0],moves[i][1],player):
			placed+=1
			do_change_live(moves[i][0],moves[i][1])
			evaluation=max_level(new_board,depth-1,betas,-player)
			undo_change_live(moves[i][0],moves[i][1])
			placed-=1
			if evaluation<=alpha:
				return evaluation
			if evaluation<beta:
				beta=evaluation
				betas=beta
	return beta
def evaluate(board,type):
	global myColor,opColor,live,table,size
	if type==0:
		table=[[91150,-2750,10,0,0,10,-2750,91150],[-2750,-74450,-5,-10,-10,-5,-74450,-2750],[10,-5,-10,-5,-5,-10,-5,10],[0,-10,-5,0,0,-5,-10,0],[0,-10,-5,0,0,-5,-10,0],[10,-5,-10,-5,-5,-10,-5,10],[-2750,-74450,-5,-10,-10,-5,-74450,-2750],[91150,-2750,10,0,0,10,-2750,91150]]
		#table=[[10000000,-275000,10,0,0,10,-275000,10000000],[-275000,-7445000,-5,-10,-10,-5,-7445000,-275000],[10,-5,-10,-5,-5,-10,-5,10],[0,-10,-5,0,0,-5,-10,0],[0,-10,-5,0,0,-5,-10,0],[10,-5,-10,-5,-5,-10,-5,10],[-275000,-7445000,-5,-10,-10,-5,-7445000,-275000],[10000000,-275000,10,0,0,10,-275000,10000000]]
		table=numpy.array(table)
		__reg17=0
		__reg19=0
		__reg26=-13500
		__reg21=-13600
		__reg13=0
		__reg22=-500
		__reg25=100
		if board[0][0]==0 and board[0][7]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[0][__reg3]!=myColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[0][1]==myColor and board[0][6]==0) or (board[0][1]==0 and board[0][6]==myColor):
					__reg13+=__reg22
				elif board[0][1]==0 and board[0][6]==0:
					__reg13+=__reg25
			else:
				if board[0][1]==myColor or board[0][6]==myColor:
					__reg17+=__reg21
		if board[7][0]==0 and board[7][7]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[7][__reg3]!=myColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[7][1]==myColor and board[7][6]==0) or (board[7][1]==0 and board[7][6]==myColor):
					__reg13+=__reg22
				elif board[7][1]==0 and board[7][6]==0:
					__reg13+=__reg25
			else:
				if board[7][1]==myColor:
					__reg17+=__reg21
				if board[7][6]==myColor:
					__reg17+=__reg21
		if board[0][0]==0 and board[7][0]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[__reg3][0]!=myColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[1][0]==myColor and board[6][0]==0) or (board[1][0]==0 and board[6][0]==myColor):
					__reg13+=__reg22
				elif board[1][0]==0 and board[6][0]==0:
					__reg13+=__reg25
			else:
				if board[1][0]==myColor or board[6][0]==myColor:
					__reg17+=__reg21
		if board[0][7]==0 and board[7][7]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[__reg3][7]!=myColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[1][7]==myColor and board[6][7]==0) or (board[1][7]==0 and board[6][7]==myColor):
					__reg13+=__reg22
				elif board[1][7]==0 and board[6][7]==0:
					__reg13+=__reg25
			else:
				if board[1][7]==myColor or board[6][7]==myColor:
					__reg17+=__reg21
		__reg20=0
		if board[0][0]==0 and board[0][7]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[0][__reg3]!=opColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[0][1]==opColor and board[0][6]==0) or (board[0][1]==0 and board[0][6]==opColor):
					__reg20+=__reg22
				elif board[0][1]==0 and board[0][6]==0:
					__reg20+=__reg25
			else:
				if board[0][1]==opColor or board[0][6]==opColor:
					__reg19+=__reg21
		if board[7][0]==0 and board[7][7]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[7][__reg3]!=opColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[7][1]==opColor and board[7][6]==0) or (board[7][1]==0 and board[7][6]==opColor):
					__reg20+=__reg22
				elif board[7][1]==0 and board[7][6]==0:
					__reg20+=__reg25
			else:
				if board[7][1]==opColor or board[7][6]==opColor:
					__reg19+=__reg21
		if board[0][0]==0 and board[7][0]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[__reg3][0]!=opColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[1][0]==opColor and board[6][0]==0) or (board[1][0]==0 and board[6][0]==opColor):
					__reg20+=__reg22
				elif board[1][0]==0 and board[6][0]==0:
					__reg20+=__reg25
			else:
				if board[1][0]==opColor or board[6][0]==opColor:
					__reg19+=__reg21
		if board[0][7]==0 and board[7][7]==0:
			__reg3=2
			__reg9=1
			while __reg3<=5:
				if board[__reg3][7]!=opColor:
					__reg9=0
				__reg3+=1
			if __reg9==1:
				if (board[1][7]==opColor and board[6][7]==0) or (board[1][7]==0 and board[6][7]==opColor):
					__reg20+=__reg22
				elif board[1][7]==0 and board[6][7]==0:
					__reg20+=__reg25
			else:
				if board[1][7]==opColor or board[6][7]==opColor:
					__reg19+=__reg21
		if board[0][0]==0:
			if board[1][1]==opColor:
				__reg19+=__reg26
			elif board[1][1]==myColor:
				__reg17+=__reg26
		if board[0][7]==0:
			if board[1][6]==opColor:
				__reg19+=__reg26
			elif board[1][6]==myColor:
				__reg17+=__reg26
		if board[7][0]==0:
			if board[6][1]==opColor:
				__reg19+=__reg26
			elif board[6][1]==myColor:
				__reg17+=__reg26
		if board[7][7]==0:
			if board[6][6]==opColor:
				__reg19+=__reg26
			elif board[6][6]==myColor:
				__reg17+=__reg26
		__reg4=0
		__reg5=0
		__reg7=84
		if board[0][0]!=0:
			if board[0][0]==opColor:
				__reg4+=2080
			elif board[0][0]==myColor:
				__reg5+=2080
			__reg6=1
			while __reg6<size and board[0][__reg6]==board[0][0]:
				__reg6+=1
				if board[0][0]==opColor:
					__reg4+=__reg7
					continue
				if board[0][0]==myColor:
					__reg5+=__reg7
			while __reg6<size and board[__reg6][0]==board[0][0]:
				__reg6+=1
				if board[0][0]==opColor:
					__reg4+=__reg7
					continue
				if board[0][0]==myColor:
					__reg5+=__reg7
			table[0][1]=100
			table[1][0]=100
			table[1][1]=100
		if board[0][7]!=0:
			if board[0][7]==opColor:
				__reg4+=2080
			elif board[0][7]==myColor:
				__reg5+=2080
			__reg6=7
			while __reg6>=0 and board[0][__reg6]==board[0][7]:
				__reg6-=1
				if board[0][7]==opColor:
					__reg4+=__reg7
					continue
				if board[0][7]==myColor:
					__reg5+=__reg7
			__reg6=1
			while __reg6<size and board[__reg6][7]==board[0][7]:
				__reg6+=1
				if board[0][7]==opColor:
					__reg4+=__reg7
					continue
				if board[0][7]==myColor:
					__reg5+=__reg7
			table[0][6]=100
			table[1][6]=100
			table[1][7]=100
		if board[7][0]!=0:
			if board[7][0]==opColor:
				__reg4+=2080
			elif board[7][0]==myColor:
				__reg5+=2080
			__reg6=1
			while __reg6<size and board[7][__reg6]==board[7][0]:
				__reg6+=1
				if board[7][0]==opColor:
					__reg4+=__reg7
					continue
				if board[7][0]==myColor:
					__reg5+=__reg7
			__reg6=7
			while __reg6>=0 and board[__reg6][0]==board[7][0]:
				__reg6-=1
				if board[7][0]==opColor:
					__reg4+=__reg7
					continue
				if board[7][0]==myColor:
					__reg5+=__reg7
			table[7][1]=100
			table[6][0]=100
			table[6][1]=100
		if board[7][7]!=0:
			if board[7][7]==opColor:
				__reg4+=2080
			elif board[7][7]==myColor:
				__reg5+=2080
			__reg6=7
			while __reg6>=0 and board[7][__reg6]==board[7][7]:
				__reg6-=1
				if board[7][7]==opColor:
					__reg4+=__reg7
					continue
				if board[7][7]==myColor:
					__reg5+=__reg7
			__reg6=7
			while __reg6>=0 and board[__reg6][7]==board[7][7]:
				__reg6-=1
				if board[7][7]==opColor:
					__reg4+=__reg7
					continue
				if board[7][7]==myColor:
					__reg5+=__reg7
			table[6][6]=100
			table[6][7]=100
			table[7][6]=100
		__reg18=0
		__reg14=0
		__reg11=0
		__reg12=0
		__reg15=0
		__reg16=0
		__reg23=0
		__reg24=0
		placed=0
		for i in range(size):
			for j in range(size):
				if board[i][j]==opColor:
					__reg11+=1
					__reg15+=live[i][j]
					__reg18+=table[i][j]
					placed+=1
				elif board[i][j]==myColor:
					__reg12+=1
					__reg16+=live[i][j]
					__reg14+=table[i][j]
					placed+=1
				if board[i][j]==0:
					new_board=board.copy()
					if place(new_board,i,j,opColor):
						__reg23+=1
					new_board=board.copy()
					if place(new_board,i,j,myColor):
						__reg24+=1
				
		__reg27=__reg12-__reg11
		__reg30=__reg15-__reg16
		__reg28=__reg5-__reg4
		__reg32=__reg14-__reg18
		__reg29=__reg17-__reg19
		__reg31=__reg24-__reg23
		if placed>50:
			return __reg27*2+__reg30*20+__reg28*750+__reg29+__reg13+__reg31*45
		else:
			return __reg27*10+__reg30*20+__reg28*750+__reg29+__reg13+__reg31*30
	else:
		op_num=0
		my_num=0
		for i in range(size):
			for j in range(size):
				if board[i][j]==opColor:
					op_num+=1
				elif board[i][j]==myColor:
					my_num+=1
		evaluation=(my_num-op_num)*7883
		return evaluation
def output_board(board):
	for i in range(size):
		for j in range(size):
			print('%2d '%board[i][j],end='')
		print()
	print()
def make_decision(board,moves,color):
	if len(moves)==0:
		return -1,-1
	x=0
	y=0
	max_evaluation=-20000000
	alpha=-20000000
	limit=4
	random.shuffle(moves)
	global placed
	for i in range(len(moves)):
		new_board=board.copy()
		if place(new_board,moves[i][0],moves[i][1],color):
			placed+=1
			do_change_live(moves[i][0],moves[i][1])
			evaluation=min_level(new_board,limit-1,alpha,-color)
			undo_change_live(moves[i][0],moves[i][1])
			placed-=1
			if evaluation>max_evaluation:
				x=moves[i][0]
				y=moves[i][1]
				max_evaluation=evaluation
				alpha=evaluation
	if max_evaluation>-20000000:
		return x,y
	return moves[0][0],moves[0][1]

def get_moves(board,color):
	moves=[]
	for i in range(size):
		for j in range(size):
			if board[i][j]==0:
				new_board=board.copy()
				if place(new_board,i,j,color):
					moves.append((i,j))
	return moves
class Node:
	pv=0
	c=1.96
	def __init__(self,x,y,par,moves,max_or_min):
		self.x=x
		self.y=y
		self.par=par
		self.cw=0
		self.cv=0
		self.moves=moves
		self.sons=[]
		self.max_or_min=max_or_min
	def is_full(self):
		return len(self.moves)==len(self.sons)
	def ucb(self):
		return self.cw/self.cv+Node.c*math.sqrt(math.log(Node.pv)/self.cv)
	def max_ucb_son(self):
		res=self.sons[0]
		max_ucb=float('-inf')
		for i in self.sons:
			tmp=i.ucb()*self.max_or_min
			if tmp>max_ucb:
				res=i
				max_ucb=tmp
		return res
evaluations=[]
Index=[]
def sort_moves(board,moves,color,max_or_min):
	global size,evaluations,Index
	tot_num=0
	for i in range(size):
		for j in range(size):
			if board[i][j]!=0:
				tot_num+=1
	for i in range(len(moves)):
		new_board=board.copy()
		place(new_board,moves[i][0],moves[i][1],color)
		if tot_num==63:
			evaluations.append(evaluate(new_board,1))
		else:
			evaluations.append(evaluate(new_board,0))
		Index.append(i)
	sorted(Index,key=lambda i:evaluations[i]*max_or_min,reverse=True)
	new_moves=[]
	for i in range(len(moves)):
		new_moves.append(moves[Index[i]])
	return new_moves
def expand(board,node,color):
	if node.is_full():
		return None
	move=node.moves[len(node.sons)]
	new_board=board.copy()
	son=Node(move[0],move[1],node,get_moves(new_board,-color),-node.max_or_min)
	#random.shuffle(son.moves)
	son.moves=sort_moves(board,son.moves,-color,son.max_or_min)
	Node.pv+=1
	son.cv+=1
	node.sons.append(son)
	return son
def simulation(board,moves,color):
	global size,myColor,opColor
	while len(moves)>0:
		move=random.choice(moves)
		place(board,move[0],move[1],color)
		color=-color
		moves=get_moves(board,color)
	win=False
	myScore=0
	opScore=0
	for i in range(size):
		for j in range(size):
			if board[i][j]==myColor:
				myScore+=1
			elif board[i][j]==opColor:
				opScore+=1
	if myScore==opScore:
		return 0.5
	elif myScore<opScore:
		return 0
	else:
		return 1
def back_propagation(node,result):
	while node!=None:
		node.cw+=result
		node=node.par
def MCTS(board,moves,color):
	global start_time,time_limit
	root=Node(None,None,None,moves,-1)
	while time.time()+0.5<start_time+time_limit:
		cur=root
		new_board=board.copy()
		new_color=color
		while cur.is_full():
			Node.pv+=1
			cur.cv+=1
			if len(cur.moves)==0:
				break
			cur=cur.max_ucb_son()
			new_color=-new_color
			place(new_board,cur.x,cur.y,new_color)
		if len(cur.moves)==0:
			continue
		Node.pv+=1
		cur.cv+=1
		new_color=-new_color
		new_node=expand(new_board,cur,new_color)
		place(new_board,new_node.x,new_node.y,new_color)
		result=simulation(new_board,new_node.moves,-new_color)
		back_propagation(new_node,result)
	'''
	print(Node.pv)
	for i in root.sons:
		print(i.x,' ',i.y,' ',i.cv,' ',i.cw)
	'''
	if len(root.sons)==0:
		return -1,-1
	res=root.max_ucb_son()
	return res.x,res.y

# 处理输入，还原棋盘
def initBoard():
	global size
	fullInput=json.loads(input())
	requests=fullInput["requests"]
	responses=fullInput["responses"]
	board=numpy.zeros((size,size),dtype=numpy.int)
	board[3][4]=board[4][3]=1
	board[3][3]=board[4][4]=-1
	global placed
	placed=4
	myColor=1
	opColor=-1
	if requests[0]["x"]>=0:
		myColor=-1
		opColor=1
		if place(board,requests[0]["x"],requests[0]["y"],-myColor):
			do_change_live(requests[0]["x"],requests[0]["y"])
			placed+=1
	turn=len(responses)
	for i in range(turn):
		if place(board,responses[i]["x"],responses[i]["y"],myColor):
			do_change_live(responses[i]["x"],responses[i]["y"])
			placed+=1
		if place(board,requests[i+1]["x"],requests[i+1]["y"],-myColor):
			do_change_live(requests[i+1]["x"],requests[i+1]["y"])
			placed+=1
	return board,myColor,opColor
'''
board=[]
board.append([ 0, 0, 0, 0, 0, 0, 0, 0])
board.append([ 0, 0, 1, 0, 0, 0, 0, 0])
board.append([-1,-1,-1, 1, 1, 0, 0, 0])
board.append([ 0,-1,-1,-1, 1, 0, 0, 0])
board.append([ 0, 1,-1, 1, 1, 0, 0, 0])
board.append([ 0, 0,-1, 1, 1,-1, 0, 0])
board.append([ 0, 0, 0, 0, 0, 0, 0, 0])
board.append([ 0, 0, 0, 0, 0, 0, 0, 0])
board=numpy.array(board)
myColor=-1
opColor=1
placed=18
'''
'''
start_time=time.time()
size=8
board,myColor,opColor=initBoard()
can_go_list=get_moves(board,myColor)
x,y=MCTS(board,can_go_list,myColor)
print(json.dumps({"response":{"x":x,"y":y}}))
'''
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
class AI(object):
	def __init__(self,chessboard_size,color,time_out):
		self.chessboard_size=chessboard_size
		self.color=color
		self.time_out=time_out
		self.candidate_list=[]
	def go(self,chessboard):
		self.candidate_list.clear()
		chessboard=numpy.array(chessboard)
		global placed,myColor,opColor,size,start_time,time_limit,live,table
		start_time=time.time()
		time_limit=self.time_out
		myColor=self.color
		opColor=-myColor
		size=self.chessboard_size
		placed=0
		live=[[3,5,5,5,5,5,5,3],[5,8,8,8,8,8,8,5],[5,8,7,6,6,7,8,5],[5,8,6,5,5,6,8,5],[5,8,6,5,5,6,8,5],[5,8,7,6,6,7,8,5],[5,8,8,8,8,8,8,5],[3,5,5,5,5,5,5,3]]
		live=numpy.array(live)
		good_points=[]
		not_bad_points=[]
		for i in range(size):
			for j in range(size):
				if chessboard[i][j]==0:
					new_board=chessboard.copy()
					if place(new_board,i,j,self.color):
						self.candidate_list.append((i,j))
						if (i==0 or i==7) and (j==0 or j==7):
							good_points.append((i,j))
						elif not ((i<=1 or 7-i<=1) and (j<=1 or 7-j<=1)):
							not_bad_points.append((i,j))
				else:
					placed+=1
					do_change_live(i,j)
		x=-1
		y=-1
		if len(good_points)>0:# and (placed<=50):
			x,y=make_decision(chessboard,good_points,self.color)
		elif len(not_bad_points)>0:# and (placed<=32 or self.color==-1):
			x,y=make_decision(chessboard,not_bad_points,self.color)
		else:
			x,y=make_decision(chessboard,self.candidate_list,self.color)
		if x!=-1 or y!=-1:
			self.candidate_list.append((x,y))