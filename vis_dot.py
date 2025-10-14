import networkx as nx
import re
from networkx.drawing.nx_pydot import write_dot
# 定义颜色字典
COLOR = {
    "read": '#f20013',
    "connected_remote_ip": '#0808ff',
    'connected_session': '#0808ff',
    'executed': '#f20013',
    'bind': '#f20013',
    'sock_send': '#0808ff',
    'connect': "#0808ff",
    'fork': '#f20013',
    'web_request': '#0808ff',
    'refer': '#0808ff',
    'write': '#f20013',
    'delete': '#f20013',
    'execute': '#f20013',
    'resolve': '#f20013',
}
NET = ["connection", 'session', 'IP_Address', 'domain_name', 'web_object']
NETOPT = ['web quest', 'sock send', 'bind', 'connected_session', 'connect', 'connected remote ip', 'resolve', 'refer']
m_node = []
change = {}
count = 0
RES = True
ccount = 0


def import_res():
    global m_node
    file_path = 'result.txt'
    file = open(file_path, 'r', encoding='utf-8')
    matches = re.findall(r'\'(.*?)\'', file.readline())
    for i in matches:
        if i not in m_node:
            m_node.append(i)
            print(i)


def node_type(node):
    global ccount
    type_0_node = ''
    type_2_node = ''
    if node[1] == "read" or node[1] == "write" or node[1] == "delete" or node[1] == "execute":
        if "c:/windows/system32" in node[0]:
            type_0_node = "system32_process"
        elif "c:/windows" in node[0]:
            type_0_node = "windows_process"
        elif "c:/programfiles" in node[0]:
            type_0_node = "programfiles_process"
        elif "c:/users" in node[0]:
            type_0_node = "user_process"
        else:
            type_0_node = "process"

        if not ";" in node[2]:
            if "c:/windows/system32" in node[2]:
                type_2_node = "system32_file"
            elif "c:/windows" in node[2]:
                type_2_node = "windows_file"
            elif "c:/programfiles" in node[2]:
                type_2_node = "programfiles_file"
            elif "c:/users" in node[2]:
                type_2_node = "user_file"
            else:
                type_2_node = "file"
        else:
            type_2_node = "combined_files"
    elif node[1] == "fork":
        if "c:/windows/system32" in node[0]:
            type_0_node = "system32_process"
        elif "c:/windows" in node[0]:
            type_0_node = "windows_process"
        elif "c:/programfiles" in node[0]:
            type_0_node = "programfiles_process"
        elif "c:/users" in node[0]:
            type_0_node = "user_process"
        else:
            type_0_node = "process"

        if "c:/windows/system32" in node[2]:
            type_2_node = "system32_process"
        elif "c:/windows" in node[2]:
            type_2_node = "windows_process"
        elif "c:/programfiles" in node[2]:
            type_2_node = "programfiles_process"
        elif "c:/users" in node[2]:
            type_2_node = "user_process"
        else:
            type_2_node = "process"

    elif node[1] == "connect" or node[1] == "bind":
        if "c:/windows/system32" in node[0]:
            type_0_node = "system32_process"
        elif "c:/windows" in node[0]:
            type_0_node = "windows_process"
        elif "c:/programfiles" in node[0]:
            type_0_node = "programfiles_process"
        elif "c:/users" in node[0]:
            type_0_node = "user_process"
        else:
            type_0_node = "process"

        if node[1] == "connect":
            type_2_node = "connection"  # "IP_Address"
        else:
            type_2_node = "session"

    elif node[1] == "resolve":
        type_0_node = "IP_Address"
        type_2_node = "domain_name"
    elif node[1] == "web_request":
        type_0_node = "domain_name"
        type_2_node = "web_object"
    elif node[1] == "refer":
        type_0_node = "web_object"
        type_2_node = "web_object"
    elif node[1] == "executed":
        if "c:/windows/system32" in node[0]:
            type_0_node = "system32_file"
        elif "c:/windows" in node[0]:
            type_0_node = "windows_file"
        elif "c:/programfiles" in node[0]:
            type_0_node = "programfiles_file"
        elif "c:/users" in node[0]:
            type_0_node = "user_file"
        else:
            type_0_node = "file"

        if "c:/windows/system32" in node[2]:
            type_2_node = "system32_process"
        elif "c:/windows" in node[2]:
            type_2_node = "windows_process"
        elif "c:/programfiles" in node[2]:
            type_2_node = "programfiles_process"
        elif "c:/users" in node[2]:
            type_2_node = "user_process"
        else:
            type_2_node = "process"
    elif node[1] == "sock_send":
        type_0_node = "session"
        type_2_node = "session"
    elif node[1] == "connected_remote_ip":
        type_0_node = "IP_Address"
        if not node[2].startswith("connection_"):
            if "c:/windows/system32" in node[2]:
                type_2_node = "system32_process"
            elif "c:/windows" in node[2]:
                type_2_node = "windows_process"
            elif "c:/programfiles" in node[2]:
                type_2_node = "programfiles_process"
            elif "c:/users" in node[2]:
                type_2_node = "user_process"
            else:
                type_2_node = "process"
        else:
            type_2_node = "connection"
    elif node[1] == "connected_session":
        type_0_node = "IP_Address"
        type_2_node = "session"
    if RES:
        if match(node[0]):
            type_0_node = "attack_" + type_0_node
            # print(type_0_node)
            # ccount +=1
        if match(node[2]):
            type_2_node = "attack_" + type_2_node
            # ccount += 1
            # print(type_2_node)
    return type_0_node, type_2_node


def match(node):
    global m_node
    if node in change.values():
        for i in change.keys():
            for j in m_node:
                if j in i:
                    return True
        return False
    else:
        if node in m_node:
            return True
        return False


def scan_and_replace(node_line):
    global change, count
    nodes = node_line.split()
    for node in nodes:
        if len(node) >= 100:
            if node not in change:
                change[node] = f'team{count}'
                count += 1
                # print(f"Recorded long node: {node[:30]}... -> {change[node]}")  # 打印超长节点


def create_gephi_graph(source_file):
    global ccount
    try:
        # 打开输入文件
        with open(source_file, "r") as file:
            lines = file.readlines()

        # 创建一个空的 NetworkX 图
        G = nx.DiGraph()
        nodes_seen = set()

        for line_no, line in enumerate(lines, start=1):
            scan_and_replace(line)
            current = line.split()
            type_0_node, type_2_node = node_type(current)
            # 替换节点
            for idx, node in enumerate(current):
                cur = current[idx]
                current[idx] = cur
                if node in change:
                    current[idx] = change[node]
            if 'c:/programfiles/mozillafirefox/firefox.exe_2848' in current:
                print(1)
            node_0 = current[0]
            node_2 = current[2]
            # 添加节点到图
            if node_0 not in nodes_seen or True:
                opt_0_type = ''
                nodes_seen.add(node_0)
                if match(node_0) and RES:
                    opt_0_type = "attack"
                elif type_0_node in NET:
                    opt_0_type = "network"
                else:
                    opt_0_type = 'system_node'
                G.add_node(node_0, type=type_0_node, opt_type=opt_0_type)
            if 'c:/programfiles/mozillafirefox/firefox.exe_2848' in current:
                print(G.nodes['c:/programfiles/mozillafirefox/firefox.exe_2848'])
            if node_2 not in nodes_seen or True:
                opt_2_type=''
                nodes_seen.add(node_2)
                if match(node_2) and RES:
                    opt_2_type = "attack"
                elif type_2_node in NET:
                    opt_2_type = "network"
                else:
                    opt_2_type = 'system_node'
                G.add_node(node_2, type=type_2_node, opt_type=opt_2_type)

            # 获取边的标签和颜色
            edge_label = current[1]
            rea_edge_label = edge_label
            # 添加边到图
            ed_opt = ''
            if current[1] in NETOPT:
                ed_opt = 'network'
            else:
                ed_opt = 'system'
            if RES:
                if match(current[0]) and match(current[2]):
                    rea_edge_label = "attack_" + edge_label
                    print("attack edge: ", current[2], current[0])
                    ccount += 1
                    ed_opt = "attack"
            G.add_edge(node_0, node_2, opt=rea_edge_label, opt_type=ed_opt)

        # 导出为 GEXF 格式
        # gexf_filename = 'S2_vis.gexf'
        # nx.write_gexf(G, gexf_filename)

        # pydot_graph = to_pydot(G)
        # pydot_graph.write_dot('S2_vis.dot')

        mapping = {}
        for node in G.nodes():
            new_name = node.replace("c:/", "c//").replace(':','_')#.replace("/", "_").replace("\\", "_").replace(".", "_")
            if new_name != node:
                mapping[node] = new_name
        if mapping:
            nx.relabel_nodes(G, mapping, copy=False)

        # print(G.nodes['c:/programfiles/mozillafirefox/firefox.exe_2848'])
        dot_filename = 'S2_vis.dot'
        write_dot(G, dot_filename)
        # print(f"GEXF file saved as {pydot_graph}")
        print(ccount)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    import_res()
    print(m_node)
    # 调用函数
    create_gephi_graph("output/seq_graph_testing_preprocessed_logs_S2-CVE-2015-3105_windows.dot.txt")
