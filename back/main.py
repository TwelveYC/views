import osmnx as ox
import networkx as nx

#
#
# print(g.number_of_nodes())
# print(g.number_of_edges())
# ox.plot_graph(g)
# ox.save_graphml(g, "modena.graphml")
def main():


    ox.config(log_console=True)
    g = ox.graph_from_point((37.79, -122.41), dist=750, network_type='drive')
    ox.plot_graph(g)
    # ox.save_graphml(g, "vvv_drive.graphml")
    # g = nx.read_graphml("/home/yangchao/code/forView/vvv_drive.graphml")
    # g = nx.read_gml("/home/yangchao/code/forView/vvv_drive.gml")
    # print(type(g))
    # print(g.number_of_nodes())
    # print(g.number_of_edges())
    # 1514 个节点
    # 4136 个边
    # h = ox.load_graphml("/home/yangchao/code/forView/vvv.graphml")
    # ox.plot_graph(h)
    # for i in g.edges:
        # if i[2] != 0:
        # print(i)
if __name__ == '__main__':
    main()