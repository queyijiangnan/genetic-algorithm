import numpy as np
import math as m
import decimal
from decimal import Decimal as dec
power = []
power.append(4.096/pow(2,10))
power.append(4.096/pow(2,10))
class evolution():
    def __init__(self,batch,cross_rate,bianyi,lens):#种群规模，交叉概率，变异概率，个体长度
        self.batch = batch
        self.cross_rate = cross_rate
        self.bianyi = bianyi
        self.pop  = []
        self.len = lens
        for i in range(self.batch):#种群初始化
            person = []
            for i in range(20):
                person.append(int(np.random.rand(1).round()))
            self.pop.append(person)
    
    def target(self,x1,x2):#目标函数
        output = 100*((x2+x1**2)**2)+(1-x1)**2
        return output
    
    def get_code(self,x1,x2):#获得编码
        output1 = []
        output2 = []
        num1 = int((x1+2.048)/power[0])
        num2 = int((x2+2.048)/power[1])
        for i in range(10):
            output1.append(int(num1%2))
            num1 = (num1-num1%2)/2
        output1 = output1[::-1]#逆序
        for i in range(10):
            output2.append(int(num2%2))
            num2 = (num2-num2%2)/2
        output2 = output2[::-1]
        output = output1+output2
        return output

    def get_num(self,codes):#获得数字
        x1_code = codes[0:10][::-1]
        x2_code = codes[10:20][::-1]
        x1 = 0
        x2 = 0
        for i in range(10):
            x1 +=pow(2,i)*x1_code[i]
        for i in range(10):
            x2 += pow(2,i)*x2_code[i]
        #return float(format(x1*power[0]-2.048,'.4f')),float(format(x2*power[1]-2.048,'.4f'))
        return x1*power[0]-2.048,x2*power[1]-2.048
    
    def cross(self,x1,x2):#对两个个体进行交叉，返回两个01数组
        weather = (np.random.rand(1)<self.cross_rate)
        a1,a2 =list(x1),list(x2)
        if weather:
            left,right  = np.sort(np.random.randint(0,self.len-1,2))
            tem = list(a1[left:right])
            a1[left:right] = list(a2[left:right])
            a2[left:right] = list(tem)
            return self.bian(a1),self.bian(a2)
        else:
            return None,None
    def bian(self,x1):#变异函数
        slecet = np.random.rand(self.len)
        for i in range(self.len):
            if self.bianyi>=slecet[i]:
                x1[i] = (x1[i]+1)%2
        return x1
    def get_adapt(self,pop):#生成输入种群的适应度数组并返回
        adapt = []
        for j in pop:
            result  =self.get_num(j)
            adapt.append(self.target(result[0],result[1])) 
        return np.array(adapt)
    def rotary(self,pop,out_num):#对输入种群数组进行轮盘赌,返回下标数组 
        adapt = self.get_adapt(pop)
        pro = adapt/adapt.sum()
        cross_pop = []
        for i in range(1,len(pop)):
            pro[i] += pro[i-1]
        for j in range(out_num):#选择出参加交叉的个体
            point = np.random.rand(1)
            for k in range(len(pro)):
                if point<= pro[k]:
                    cross_pop.append(k)
                    break
        return cross_pop
    def start(self,epoch,hold):#参数为进化次数,精英保留数
        #1.先保留hold个精英直接到下一代，每代将种群按照每个个体适应度进行轮盘赌选择出可以进行交叉的个体
        #2.选出的个体按照交叉概率成对进行交叉，产生新的个体，同时按照变异概率进行变异
        #3.第二步产生的子代按照变异概率进行变异，最后将除保留精英外个体进行轮盘赌得到下一代"""
        mas = []
        for i in range(epoch):
            next_pop = []#下一代
            mas = []
            cross_output = []#当代交叉结果
            adapt = self.get_adapt(self.pop)
            max_hold = list(np.argpartition(adapt,-hold)[-hold:])
            into_cross = self.rotary(self.pop,self.batch)
            for j in range(int(self.batch/2)):#交叉
                x1,x2 = self.cross(self.pop[into_cross[j*2]],self.pop[into_cross[j*2+1]])
                if x1:
                    cross_output.append(x1)
                    cross_output.append(x2)
            for k in max_hold:#放入最大
                next_pop.append(list(self.pop[k]))
                mas.append(list(self.pop[k]))
            for l in mas:
                self.pop.remove(l)
            cross_output = list(cross_output+self.pop)
            into_next = self.rotary(cross_output,self.batch-hold)
            for j in into_next:
                next_pop.append(cross_output[j])
            self.pop = list(next_pop)
        print("最优秀个体为%.4f" %(self.get_adapt(mas)[hold-1]))
        if float(format(self.get_adapt(mas)[hold-1],'.4f'))>=38.8503:
            print("成功")
            return 1
        else:
            return 0

    def start2(self,epoch,hold):#你应该放弃轮盘赌，来拥抱直接选择
        adapt = []
        for i in range(epoch):
            next_pop = []#下一代
            cross_output = []#当代交叉结果
            into_cross = self.rotary(self.pop,self.batch)
            for j in range(int(self.batch/2)):#交叉
                x1,x2 = self.cross(self.pop[into_cross[j*2]],self.pop[into_cross[j*2+1]])
                if x1:
                    cross_output.append(x1)
                    cross_output.append(x2)
            cross_output = list(cross_output+self.pop)
            adapt = self.get_adapt(cross_output)
            max_hold = list(np.argpartition(adapt,-hold)[-hold:])
            for j in max_hold:
                next_pop.append(list(cross_output[j]))
            self.pop = list(next_pop)
            if float(format(adapt[max_hold[-1]],'.4f')) == 3905.9262:
                print("第%d代成功" %i)
                break
        print("结束后最优秀个体为",float(format(adapt[max_hold[-1]],'.4f')))
        print("x1和x2的值",self.get_num(cross_output[max_hold[-1]]))



#种群规模，交叉率，变异率，个体编码长度 次数 保留个数
sums = 0
for i  in range(10):
    evl = evolution(200,0.7,0.1,20)
    evl.start2(500,200)















# 100 0.6 0.06 500 10 准确率0.825 0.9
# 200 0.6 0.06 500 10 0.875
# 30 0.6 0.03 1000 4 0.475
# 30 0.6 0.06 1000 4 0.575
# 50 0.6 0.06 500 10 0.7
# 20 0.6 0.1 5000 10 0.9 0.825 
# 20 0.7 0.1 3000 10 0.925
#start2
# 200 0.7 0.1 1000 200 1
# 20 0.7 0.1 2000 20 0.875
# 60          2000 60 0.875
# 100 0.95
# 150 0.975
#180 1.0
# 200 1.0 500dai 
# 10 5000 0.85
