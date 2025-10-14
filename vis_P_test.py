from pyvis.network import Network
import re
import os
import time as tm
import tracemalloc

# 定义颜色字典
color_map = {
    # 进程相关类型（橙色系）
    "system32_process": "rgb(255, 165, 0)",  # 标准橙
    "windows_process": "rgb(255, 140, 0)",  # 暗橙色
    "programfiles_process": "rgb(255, 215, 0)",  # 金色
    "user_process": "rgb(255, 160, 0)",  # 深橙色（避免番茄红）
    "process": "rgb(255, 180, 50)",  # 琥珀橙（避免橙红色）

    # 文件相关类型（绿色系）
    "system32_file": "rgb(46, 139, 87)",  # 海绿
    "windows_file": "rgb(60, 179, 113)",  # 中绿
    "programfiles_file": "rgb(107, 139, 35)",  # 橄榄绿
    "user_file": "rgb(34, 139, 34)",  # 森林绿
    "file": "rgb(50, 205, 50)",  # 酸橙绿
    "combined_files": "rgb(124, 252, 0)",  # 草坪绿

    # 网络相关类型（蓝色系）
    "connection": "rgb(30, 144, 255)",  # 道奇蓝
    "session": "rgb(65, 105, 225)",  # 皇家蓝
    "IP_Address": "rgb(135, 206, 235)",  # 天蓝
    "domain_name": "rgb(70, 130, 180)",  # 钢蓝
    "web_object": "rgb(0, 0, 255)",  # 纯蓝
}


NET = ["connection", 'session', 'IP_Address', 'domain_name', 'web_object']
NETOPT = ['web quest', 'sock send', 'bind', 'connected_session', 'connect', 'connected remote ip', 'resolve', 'refer']
m_node = []
change = {}
count = 0
RES = True
ccount = 0
att=[]
mas = []
def import_mas(path):
    global mas
    with open(path,'r') as file:
        lines = file.readlines()
        for i in lines:
            item = i.replace("'",'').replace(']','').strip().split(',')
            for j in item[:2]:
                if j.strip() not in mas:
                    mas.append(j.strip())
    # print(mas)



def import_res():
    global m_node
    file_path = 'result.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        matches = re.findall(r'\'(.*?)\'', file.readline())
        for i in matches:
            if i not in m_node:
                m_node.append(i)
        print(len((set(m_node))))

def n_color(node,ATTACK):
    if ATTACK:
        return "red"
    else:
        # if node in NET :
        #     return  'blue'
        # else:
        #     return  'orange'
        return color_map[node]

def e_color(src,ATTACK):
    if ATTACK:
        return "red"
    else:
        # if edge in NETOPT:
        #     return "blue"
        # else:
        #     return 'orange'
        return n_color(src,False)
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
            # type_0_node = "attack_" + type_0_node
            pass
        if len(node)>=3:
            if match(node[2]):
                # type_2_node = "attack_" + type_2_node
                pass
    return type_0_node, type_2_node

def match(node):
    global m_node
    if m_node == []:
        return False
    # if node in change.keys():
    #     Node = change[node]
    #     if Node in m_node:
    #         return True
    #     return False
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

def create_graphtool_graph(source_file):
    global ccount
    tp_count = 0
        # 打开输入文件
    with open(source_file, "r") as file:
        lines = file.readlines()
        ccount=0
        # 创建一个空的 GraphTool 图
        G = Network(notebook = True,directed = True,cdn_resources='remote')
        G_1 = Network(notebook = True,directed = True,cdn_resources='remote')
        G_2 = Network(notebook = True,directed = True,cdn_resources='remote')
        G_3 = Network(notebook = True,directed = True,cdn_resources='remote')
        G_4 = Network(notebook = True,directed = True,cdn_resources='remote')

        nodes_seen = set()
        change={}
        for line in lines:
            scan_and_replace(line)
            current = line.split()
            if len(current) <3:
                print(current)
                continue
            type_0_node, type_2_node = node_type(current)

            # 替换节点
            for idx, node in enumerate(current):
                cur = current[idx]
                current[idx] = cur
                if node in change.values():
                    current[idx] = change[node]
            # 添加节点到图
            for node in (current[0], current[2]):
                ATTACK = False
                TP = False
                if node not in nodes_seen:
                    nodes_seen.add(node)
                    if match(node):
                        ATTACK = True
                        # ccount+=1
                        att.append(node)
                        # print(node)
                        if node not in m_node:
                            if node not in change.values():
                                # print(node)
                                pass
                        for i in mas:
                            if i in node:
                                TP = True
                                if TP:
                                    tp_count +=1
                                break
                    if node == current[0] and node not in G.nodes:
                        G.add_node(node,label = type_0_node,title = node ,color =n_color(type_0_node,False),size = 15, attack=ATTACK,fp = not TP)
                        if ATTACK:
                            ccount+=1
                        continue
                    if node == current[2] and node not in G.nodes:
                        G.add_node(node,label = type_2_node,title = node,color = n_color(type_2_node,False),size = 15, attack=ATTACK,fp =not  TP)
                        if ATTACK:
                            ccount+=1
                        continue
            ATTACK = False
            if match(current[0]) and match(current[2]):
                ATTACK = True
            # 添加边到图
            edge_attack = True if ATTACK else False
            G.add_edge(current[0], current[2],
                       label=current[1],
                       color=e_color(type_0_node, False),
                       width=3,
                       title=edge_attack)
            # G.add_edge(current[0], current[2], label=current[1], color=e_color(type_0_node,False), width=3,data={"attack": ATTACK})
            G.show_buttons(filter_=['physics'])


        G.show(source_file.replace("output/",'vis')+'.html')
        html_path = source_file.replace("output/", 'vis') + '.html'
        # G.show(html_path)

        # 注入修正后的JavaScript代码
        replacement_script = '''
               <div style="position:absolute; top:20px; left:20px; z-index:1000; background:white; padding:10px; border-radius:5px;">
                    <button onclick="window.setColorAttack()" style="background:#ff4444; color:white; margin:5px;">attack</button>
                    <button onclick="window.setColorOriginal()" style="background:#44ff44; color:black; margin:5px;">origin</button>
                    <button onclick="window.setColorByGroup()" style="background:#4444ff; color:white; margin:5px;">type</button>
                    <button onclick="window.initColorData()" style="background:#4444ff; color:white; margin:5px;">init</button>
                </div>
<script>
// 暴露函数到全局作用域
window.setColorAttack = function() {
    const nodes = network.body.nodes;
    Object.values(nodes).forEach(node => {
        const isAttack = node.options.attack;
        if (isAttack) {
            node.options.color = { background: 'red',border:'red',highlight:{background: 'red',border:'red'}};
            node.options.size = 25;
            if (node.options.fp){
            node.options.color = { background:'black',border:'black',highlight:{background:'black',border:'black'}};
            node.options.size = 25;
            }
        }
        else {
            node.options.color = node.originalColor;
            node.options.size = 15;
        }
        node.x = node.orix;
    });
    const edges = network.body.edges;
    Object.values(edges).forEach(edge => {
        if (edge.from.options.attack && edge.to.options.attack){
        edge.options.color = { background: 'red',border:'red',highlight:'red',hover: 'red'};
        edge.options.width = 7;
        }
        edge.options.color.opacity = 1;
        edge.options.font.color = edge.originallab;
         });
    network.redraw();
};

window.setColorOriginal = function() {
    const nodes = network.body.nodes;
    Object.values(nodes).forEach(node => {
        node.options.color = node.originalColor;
        node.options.size = node.originalSize;
        node.x = node.orix;
    });
    const edges = network.body.edges;
    Object.values(edges).forEach(edge => {
        edge.options.color = edge.originalColor;
        edge.options.color.opacity = 1;
        edge.options.font.color = edge.originallab;

    });
    network.redraw();
};

window.setColorByGroup = function() {
    const nodes = network.body.nodes;
    Object.values(nodes).forEach(node => {
        if (node.options.attack){
            node.options.color = { background: 'red', border: 'red', highlight: { background: 'red', border: 'red' } };
            node.options.size = 25;
            if (node.options.fp){
            node.options.color = { background:'black',border:'black',highlight:{background:'black',border:'black'}};
            node.options.size = 25;
            node.x=node.orix+1000000;
        }
        }  
        else {
            node.options.color = { background: 'rgba(0, 0, 0, 0)', border: 'rgba(0, 0, 0, 0)', 
                                     highlight: { background: 'rgba(0, 0, 0, 0)', border: 'rgba(0, 0, 0, 0)' } };
            node.options.size = 15;
        }
    });
    const edges = network.body.edges;
    Object.values(edges).forEach(edge => {
        if (edge.from.options.attack && edge.to.options.attack){
        edge.options.color = { color:'red',highlight:'red',hover: 'red'};
        edge.options.width = 7;
        }
        else
        {
            edge.options.color.opacity=0;
            edge.options.font.color = 'rgba(0,0,0,0)';
        }
    });
    network.redraw();
};


// 初始化原始颜色数据
window.initColorData = function() {
    const nodes = network.body.nodes;
    Object.values(nodes).forEach(node => {
        node.originalColor = node.options.color;
        node.originalSize = 15;
        node.orix = node.x;
    });
    const edges = network.body.edges;
    Object.values(edges).forEach(edge => {
        edge.originalColor = edge.options.color;
        edge.originallab = edge.options.font.color;
    });
};

// 绑定初始化事件
network.on("afterInit", function() {
    initColorData();
    network.on("stabilized", function() {
        initColorData();
    });
    window.initColorData();
});
</script>
</body>
               '''

        with open(html_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            f.seek(0)
            f.write(content.replace('</body>', replacement_script))
            f.truncate()

        print(f"可视化文件已生成：{html_path}")
        # G_1.show(source_file.replace("output/",'vis/pyvis/1_')+'.html')
        # G_2.show(source_file.replace("output/", 'vis/pyvis/2_')+'.html')
        # G_3.show(source_file.replace("output/", 'vis/pyvis/3_')+'.html')set
        # G_4.show(source_file.replace("output/", 'vis/pyvis/4_')+'.html')


        print("Graph visualization completed.")
        print(ccount)
        print(len(att))
        print(len(set(att)))
        print("tp number:"+str(tp_count))
    # except FileNotFoundError as e:
    #     print(f"Error: {e}")
    # except Exception as e:
    #     print(f"Unexpected error: {e}")


if __name__ == '__main__':
    start_time = tm.perf_counter()
    tracemalloc.start()
    import_res()
    import_mas("processed_apt_output.txt")
    for file in os.listdir("output"):
        if file.startswith("seq_") and not file.endswith(".gexf") and "test" in file:
            create_graphtool_graph("output/" + file)
    end_time = tm.perf_counter()
    time_cost = end_time - start_time
    time = tm.time()
    current, peak = tracemalloc.get_traced_memory()
    file = open("sys", 'a')
    file.write(str(time) + " vis_P_te.py excuted\ntime:{}s\n memory:{}MB\n".format(time_cost, peak / 1024 / 1024))
