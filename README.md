# MA-QAOA

todo


## 1-layer

存在一个哈密顿量phase operator
随便找一个点beta取0，其它点都和这个点连一条边
边取+-pi/2
点取+-pi/4
只需要一层可以解决所有最大割问题
相当于暴力破解


- 四个点三条边
从优化结果来看是先确定中间两个点关系
再确定中间的每一点和最边上点的关系  

## 2-layer
为什么TR MA-QAOA多层效果比TR QAOA差
会不会是卡在local minimal上，试一下小图上的性能