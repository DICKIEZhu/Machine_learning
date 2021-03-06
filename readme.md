# MNIST/FashionMNIST/CIFAR10,循环神经网络(RNN/LSTM/GRU)
递归神经网络(RNN)是神经网络的一种，被广泛用于自然语言处理与手写字体的识别中。本次的分析工作主要分为以下几部分：
* 使用递归神经网络和其变体(长短期记忆网络LSTM、GRU)在多个数据集(MNIST/FashionMNIST/CIFAR10)上进行训练、测试，比较效果
* 简单分析不同数据集给参数调整(递归神经网络层数、训练迭代次数)及过拟合现象带来的影响
* 分析其他超参数(学习率/隐藏层节点数/Dropout)对训练结果带来的影响

## 使用环境
* Google Colab
* Python 3.6.7
* Pytorch 1.1.0
* GCC 8.2.0

## 参数
* device:根据硬件条件决定是否使用GPU进行加速
* sequence_length:时间序列
* input_size:输入的维度
* hidden_size:隐藏层节点数
* num_layers:隐藏层数量
* num_classes:分类种类
* num_direction:是否适用双向循环神经网络，如果使用双向循环神经网络，将该值置为2，否则置为1
* batch_size:每批使用的样本数量
* num_epochs:训练的迭代次数
* learning_rate:学习率
* rnn_structure:选择RNN结构(RNN/LSTM/GRU)

## 数据加载
* train_loader:训练集
* test_loader:测试集

## 循环神经网络的构建
本循环神经网络由一个4层的循环神经层和一个全连接层组成
* rnn:循环神经网络层，共2层，各层节点数为128个
* fc:全连接层，128->10

## 定义函数
* train:训练函数
* test:测试函数
* 实例化网络
* 使用CrossEntropyLoss作为准则函数
* 使用Adam优化器
* 保存训练结果
* 下载记录损失值变化的数组与训练结果

## 比较RNN/LSTM/GRU这三种递归神经网络的效果
普通的RNN神经网络结构存在着梯度消失或者梯度爆炸的问题，对权值更新和学习效果带来不利的影响。为了解决梯度消失与梯度爆炸的问题，LSTM及其简化版本GRU被相继提出，并获得了不错的效果。<br>
**工作：**
将RNN/LSTM/GRU应用于MNIST测试集上，比较其学习效果。以下为默认的参数设置：
<div align=center><img width="200" height="200" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/%E9%BB%98%E8%AE%A4%E8%B6%85%E5%8F%82%E6%95%B0.png"/></div>
以下为三种递归神经网络在MNIST数据集上的表现：
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/1-1.png"/></div>
<div align=center>图 1-1 RNN/LSTM/GRU在MNIST上的训练过程</div>
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/1-2.png"/></div>
<div align=center>图 1-2 递归网络层数×4的RNN/LSTM/GRU在MNIST上的训练过程</div>
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/1-3.png"/></div>
<div align=center>图 1-3 迭代训练次数×4的RNN/LSTM/GRU在MNIST上的训练过程</div><br>

**结论：**
在三组实验下，LSTM与GRU均取得了比普通RNN更高的识别准确率，但在本次实验中，提升训练阶段的迭代次数后，RNN与LSTM、GRU之间的差距出现了明显减小。

## 简单分析数据集的复杂程度对递归神经网络的隐藏层数和迭代训练次数选择和过拟合现象的影响
**思考1：**
在前面在MNIST的实验中，增加递归网络的层数反而使得RNN/LSTM/GRU的效果变差。本次采用的三种数据集MNIST->FashionMNIST->CIFAR10，图像内容由手写数字->黑白物品->彩色物品与动物，复杂度逐渐提升，这是否意味着需要更多的递归网络层数，以获取更复杂的特征？
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-1.png"/></div>
<div align=center>图 2-1 RNN/LSTM/GRU在FashionMNIST上的训练过程</div>
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-2.png"/></div>
<div align=center>图 2-2 递归网络层数×2的RNN/LSTM/GRU在FashionMNIST上的训练过程</div>
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-3.png"/></div>
<div align=center>图 2-3 递归网络层数×4的RNN/LSTM/GRU在FashionMNIST上的训练过程</div>
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-4.jpg"/></div>
<div align=center>图 2-4 RNN/LSTM/GRU在CIFAR10上的训练过程</div>
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-5.jpg"/></div>
<div align=center>图 2-5 递归网络层数×2的RNN/LSTM/GRU在CIFAR10上的训练过程</div>
<div align=center><img width="450" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-6.jpg"/></div>
<div align=center>图 2-6 递归网络层数×4的RNN/LSTM/GRU在CIFAR10上的训练过程</div><br>

**结论：**
在MNIST/FashionMNIST/CIFAR10三个数据集中，无论是普通的RNN，还是LSTM、GRU，其递归神经网络部分的层数的增加(2层->4层->8层)均未能提升网络性能，反而使得测试准确率逐步下降。<br><br>

**思考2：**
如果数据集越简单，是否意味着需要需要更少的训练迭代次数和更容易出现过拟合的倾向性？
<br>
使用LSTM在MNIST/FashionMNIST/CIFAR10数据集上尝试不同的迭代次数，获取训练中的损失值变化和测试准确率。
<img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-7.jpg"/><img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-8.png"/><img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-9.png"/>
<div align=center> 图2-7~9 迭代训练16次 </div>

<img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-10.png"/><img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-11.png"/><img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-12.png"/>
<div align=center> 图2-10~12 迭代训练32次 </div>

<img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-13.png"/><img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-14.png"/><img width="280" height="280" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/2-15.png"/>
<div align=center> 图2-13~15 迭代训练64次 </div>
<br>
<br>

**表1 迭代训练结果汇总**

| 数据集 | 2 | 8 | 16 | 32|64|128|
| - | - | - | - | -|-|-|
| MNIST |97.86% | 98.65% | 98.68% | 98.89%|98.89%|98.82%|
| FashionMNIST | 82.63%| 87.51% | 87.61% |89.3% |90.19%|90.22%|
| CIFAR10 | 41.56%| 50.84% | 54.85% | 55.98%|54.20%|53.58%|

<br>

**结论：**
对于简单的数据集，2次迭代训练即可使递归神经网络获得相当好的性能，而复杂的数据集则需要相对更多的迭代训练来逐渐提升性能。至于数据集复杂度对于过拟合现象的影响，在本实验中，当迭代训练次数较高时，复杂度最高的CIFAR10出现了最为明显的性能下降现象，这似乎说明着当数据集的复杂程度更高时，在训练递归神经网络时更应该注意是否发生过拟合现象。<br>

## 尝试其他超参数对递归神经网络的学习效果的影响
该部分实验由LSTM在CIFAR10数据集上迭代训练进行。
* 学习率：学习率作为最重要的超参数，对网络的训练效果往往起着决定性的作用。本实验分别采用0.03, 0.01, 0.003, 0.001, 0.0003, 0.0001的6种学习率进行训练。实验结果显示0.03的学习率使得神经网络完全没有任何学习效果(测试准确率为10%)，0.001的学习率取得了最好的效果，随着学习率进一步降低，在训练中损失值的下降速度明显变缓，收敛速度降低，而且在测试集上的准确率也逐渐降低。
<div align=center><img width="550" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/3-1.png"/></div>
<div align=center>图 3-1 Learning_rate = 0.03, 0.01, 0.003, 0.001, 0.0003</div><br>

* 隐藏层节点数：分别采用了32, 64, 128, 256, 512的5种隐藏层节点数进行训练。实验结果显示，128个隐藏层节点数的递归神经网络取得最好的准确率(56%)，同时，更多的隐含层节点数也在训练中表现出更强的过拟合的倾向性。
<div align=center><img width="550" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/3-2.png"/></div>
<div align=center>图 3-2 Hidden_size = 32, 64, 128, 256, 512 </div><br>

* Dropout：Dropout指的是在训练的过程中，使某些神经元按照一定的概率不工作，旨在减小过拟合的发生。常用的Dropout值有0.3，0.5，0.7。本实验中采用0.1,0.3,0.5,0.7,0.9这5种dropout取值进行训练。实验结果显示，最大的dropout值可以显著降低过拟合现象，但也会降低网络的准确性，当dropout值为0.5时在CIFAR10数据集上取得较理想的效果。
<div align=center><img width="550" height="450" src="https://github.com/DICKIEZhu/Machine_learning/blob/master/3-3.png"/></div>
<div align=center>图 3-3 dropout = 0.1, 0.3, 0.5, 0.7, 0.9 </div>

## 总结
* 在本实验中，LSTM和GRU的性能要明显优于普通RNN
* 在MNIST/FashionMNIST/CIFAR10数据集上，2层的递归神经网络的训练效果最好，提高递归神经网络的层数反而使系统的性能下降
* 随着数据集的复杂度的提升，递归神经网络需要更多的迭代训练次数来提升性能，但是，更复杂的数据集似乎也使得递归神经网络的过拟合的倾向性增强
* 在CIFAR10数据集中，LSTM的学习率、隐藏层节点数、dropout的取值均会对学习速度和预测的准确率带来明显的影响，合适的参数取值能使递归神经网络的性能提到提升
