# from graphviz import Digraph
#
# dot = Digraph(comment='The Test Table')
# # 添加圆点A,A的标签是Dot A
# dot.node('A', 'Dot A')
# # 添加圆点 B, B的标签是Dot B
# dot.node('B', 'Dot B')
# # dot.view()
# # 添加圆点 C, C的标签是Dot C
# dot.node(name='C', label= 'Dot C',color='red')
# # dot.view()
#
# # 创建一堆边，即连接AB的两条边，连接AC的一条边。
# dot.edges(['AB', 'AC', 'AB'])
# # dot.view()
# # 在创建两圆点之间创建一条边
# dot.edge('B', 'C', 'test')
# dot.view()
#
# # 获取DOT source源码的字符串形式
# print(dot.source)
# dot.view()
# dot.render('test-table.gv', view=True)

# from graphviz import Digraph
#
# dot = Digraph(comment='The Round Table')
#
# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir Bedevere the Wise')
# dot.node('L', 'Sir Lancelot the Brave')
#
# dot.edges(['AB', 'AL'])
# dot.edge('B', 'L', constraint='false')
#
# dot.view()
import os

from graphviz import Digraph
grap_g = Digraph("G",format="png")


sub_g0 = Digraph(comment="process1",graph_attr={"style":'filled',"color":'lightgrey'},node_attr={"style":"filled","color":"red"})
a = sub_g0.node("a0","a0")
print(a)
sub_g0.node("a1","a1")
sub_g0.node("a2","a2")
sub_g0.node("a3","a3")
sub_g0.edge("a0","a1","down")
sub_g0.edge("a1","a2")
sub_g0.edge("a2","a3")
sub_g0.edge("a3", "a0")

sub_g1 = Digraph(comment="process1",graph_attr={"style":'filled'})
sub_g1.node("B","b0",_attributes={"style":"filled","color":"red"})
sub_g1.node("C","b1")
sub_g1.node("D","b2")
sub_g1.node("E","b3")
sub_g1.edges(["BC","CD","DE"])

grap_g.node(
"start", label="start",shape="Mdiamond")
grap_g.node(
"end", label="end", shape="Mdiamond")
grap_g.node
grap_g.subgraph(sub_g0)
grap_g.subgraph(sub_g1)
grap_g.edge("start","a0")
grap_g.edge("start","B")

grap_g.edge("a1","E")
grap_g.edge("D","a3")

grap_g.edge("a3","end")
grap_g.edge("E","end")

grap_g.render('test-table2', view=True)

grap_g = None
grap_g = Digraph("G",format="png")
sub_g0 = None
sub_g0 = Digraph(comment="process1",graph_attr={"style":'filled',"color":'lightgrey'},node_attr={"style":"filled","color":"red"})
a = sub_g0.node("a0","a0")
print(a)
sub_g0.node("a1","a1")
sub_g0.node("a2","a2")
sub_g0.node("a3","a3")
sub_g0.edge("a0","a1","down")
sub_g0.edge("a1","a2")
sub_g0.edge("a2","a3")
sub_g0.edge("a3", "a0")
sub_g1 = None
sub_g1 = Digraph(comment="process1",graph_attr={"style":'filled'})
sub_g1.node("B","b0",_attributes={"style":"filled","color":"red"})
sub_g1.node("C","b1")
sub_g1.node("D","b2")
sub_g1.node("E","b3")
sub_g1.edges(["BC","CD","DE"])

grap_g.node(
"start", label="start",shape="Mdiamond")
grap_g.node(
"end", label="end", shape="Mdiamond")
grap_g.node
grap_g.subgraph(sub_g0)
grap_g.subgraph(sub_g1)
grap_g.edge("start","a0")
grap_g.edge("start","B")

grap_g.edge("a1","E")
grap_g.edge("D","a3")

grap_g.edge("a3","end")
grap_g.edge("E","end")

folder = "./viztest"
os.makedirs(folder)
grap_g.render(folder+'/test-table3', view=True)
