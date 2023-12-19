
# Enter your Python code here


from pya import *
import re
import json
import copy
import sys
import pprint
import numpy as np
from collections import defaultdict

class OriginalError(Exception):
    pass

# json data
def save_json(data,save_path):

    # dictをjsonで保存
    with open(save_path,"w") as f:
        data = json.dumps(data)
        f.write(data)

def load_json(path):

    # jsonデータをdictでload
    data = None
    with open(path,mode = "r") as fr:
        data = json.load(fr)
    return data

# layer map
def get_layer_map():

    global LAYOUT
    # layer index information
    layer_map = dict()
    for i,num in zip(LAYOUT.layer_infos(),LAYOUT.layer_indexes()):
        print(i.name)
        index = ','.join([str(v) for v in str(i).split('/')])
        layer_map[num] = index

    return layer_map

# layout structure
def get_structure():

    # https://www.klayout.de/doc/code/class_Path.html

    global TOP_CELL

    save_data = dict()
    text_data = dict()

    width = 0.3*DBU
    for index,layer in get_layer_map().items():
        
        sel = TOP_CELL.shapes(index)
        p_list = list()
        for temp in sel.each():
            if temp.is_path():
                # width = temp.path.width
                path = [[v.x,v.y] for v in temp.path.each_point()]
                length = len(path)
                for idx in range(length-1):
                    p1 = copy.deepcopy(path[idx])
                    p2 = copy.deepcopy(path[idx+1])
                    if p1[0] == p2[0] and p1[1] == p2[1]:
                        continue
                    p1,p2 = sorted([p1,p2])
                    p1 = np.array(p1) - width/2
                    p2 = np.array(p2) + width/2
                    p_list.append([p1[0],p1[1],p2[0],p2[1]])
            elif temp.is_text():
                text = temp.text
                string = text.string
                px = text.x
                py = text.y
                text_data[string] = [layer,px,py]
            else:
                p1,p2 = temp.bbox().p1,temp.bbox().p2
                p_list.append([p1.x,p1.y,p2.x,p2.y])
        save_data[layer] = p_list
        save_data['text'] = text_data

    save_json(save_data,"/home/oe23ranan/Omocha_mpwgf1/block/json/"+TOP_CELL.name+".json")

# make bmesh
def make_bmesh():

    global LAYOUT,TOP_CELL

    border_index = LAYOUT.layer(LayerInfo.new(63,0))

    center_point = [0,0]

    for dy in range(10):
        for dx in range(10):
            current_point = [dx,dy]
            size = 1
            create_Box(TOP_CELL,border_index,current_point,size)

# sub cell
def make_subcell(cell,name):

    global LAYOUT
    global DBU
    
    # subcell
    sub_cell = LAYOUT.create_cell(name)
    inst = CellInstArray.new(sub_cell.cell_index(),Trans.new(0, 0))
    cell.insert(inst)
    
    return sub_cell

# get DBU point
def get_DBU_point(point):

    global DBU

    return np.array(point)*DBU

# get DBU size
def get_DBU_size(size):

    global DBU

    return size*DBU

# get coordinate
def get_pos(cell):

    temp = cell.bbox()
    p1,p2 = temp.p1,temp.p2

    return (p1.x+p2.x)//2,(p1.y+p2.y)//2

# box pattern1
def create_Box(cell,index,point,width,height):

    point = get_DBU_point(point)

    # size of box
    size = get_DBU_point([width,height])
    
    points = np.concatenate([point - size//2,
                             point + size//2])
    
    cell.shapes(index).insert(Box.new(points[0],points[1],points[2],points[3]))

# box pattern2
def create_Box2(cell,index,p1,p2):

    cell.shapes(index).insert(Box.new(p1[0],p1[1],p2[0],p2[1]))

# path
def create_Path(cell,index,path,width):

    # width of path
    width = get_DBU_size(width)

    points = list()
    for point in path:
        point = get_DBU_point(point)
        points.append(Point.new(point[0],point[1]))

    cell.shapes(index).insert(Path.new(points,width))

# text
def create_Text(cell,index,point,string):

    # point = get_DBU_point(point)

    cell.shapes(index).insert(Text.new(string,point[0],point[1]))

# via
def create_via(cell,point,layers = [0],rot = 0):

    m1_index = LAYOUT.layer(LayerInfo.new(34,0))
    m2_index = LAYOUT.layer(LayerInfo.new(36,0))
    m3_index = LAYOUT.layer(LayerInfo.new(42,0))
    m4_index = LAYOUT.layer(LayerInfo.new(46,0))
    m5_index = LAYOUT.layer(LayerInfo.new(81,0))
    v1_index = LAYOUT.layer(LayerInfo.new(35,0))
    v2_index = LAYOUT.layer(LayerInfo.new(38,0))
    v3_index = LAYOUT.layer(LayerInfo.new(40,0))
    v4_index = LAYOUT.layer(LayerInfo.new(41,0))
    v5_index = LAYOUT.layer(LayerInfo.new(82,0))

    m_width = 0.38
    m_height = 0.90
    via_size = 0.26

    for layer in layers:

        if layer == 1:
            under_index = m1_index
            upper_index = m2_index
            via_index = v1_index
        elif layer == 2:
            under_index = m2_index
            upper_index = m3_index
            via_index = v2_index
        elif layer == 3:
            under_index = m3_index
            upper_index = m4_index
            via_index = v3_index

        if rot == 0:

            create_Box(cell,under_index,point,m_width,m_height)
            create_Box(cell,upper_index,point,m_width,m_height)

            upper_point = [point[0],point[1]+m_height/4]
            create_Box(cell,via_index,upper_point,via_size,via_size)
            under_point = [point[0],point[1]-m_height/4]
            create_Box(cell,via_index,under_point,via_size,via_size)

        elif rot == 90:

            create_Box(cell,under_index,point,m_height,m_width)
            create_Box(cell,upper_index,point,m_height,m_width)

            upper_point = [point[0]+m_height/4,point[1]]
            create_Box(cell,via_index,upper_point,via_size,via_size)
            under_point = [point[0]-m_height/4,point[1]]
            create_Box(cell,via_index,under_point,via_size,via_size)

# cdac
def create_Cdac():

    global TOP_CELL
    CELL = make_subcell(TOP_CELL,"carray")

    sub_cell = make_subcell(CELL,"mim_cap")

    # param
    BIT = 5
    width = 0.28
    height = 10
    hikidashi_height = 2
    m_index = m2_index

    # center
    point = [0,width]
    create_Box(sub_cell,m_index,point,width,height)
    # left
    point = [width*-2,0]
    create_Box(sub_cell,m_index,point,width,height)
    # right
    point = [width*2,0]
    create_Box(sub_cell,m_index,point,width,height)
    # under
    point = [0,height*(-1/2)-width*(1/2)]
    create_Box(sub_cell,m_index,point,width*5,width)
    create_Text(sub_cell,m_index,point,"cap_out")
    # upper
    point = [0,height/2+width + hikidashi_height/2]
    create_Box(sub_cell,m_index,point,width,hikidashi_height)
    create_Text(sub_cell,m_index,point,"cap_in")
    # cap_mk
    point = [0,-width/2]
    create_Box(sub_cell,cap_index,point,width*5,height+width)

    # 接続する配線番号
    wait =[0]
    for i in range(2,BIT+1):
      count = 0     
      for index in range(len(wait)):
        wait.insert(index+count,i)             
        count+=1
    wait = wait + [1] + wait[::-1][1:]

    array_cell = CellInstArray(
        sub_cell.cell_index(),
        Trans(Point(0,0)),
        Vector(0,0),
        Vector(width*4*DBU,0),
        1,2**BIT
    )

    CELL.insert(array_cell)

    paths = [[] for _ in range(BIT+1)]
    base_y = height/2 + hikidashi_height + width
    for x in range(2**BIT):
        current_x = x*width*4
        current_h = hikidashi_height*(BIT-wait[x]+1)
        current_y = base_y + current_h/2
        point = [current_x,current_y]
        create_Box(CELL,m_index,point,width,current_h)
        point = [current_x,current_y+current_h/2]
        create_via(CELL,point,layers = [2])
        paths[wait[x]].append(point)

    for path in paths:
        create_Path(CELL,m3_index,path,width)
        middle_point = path[len(path)//2]
        path = [middle_point,[(x+5)*width*4,middle_point[1]]]
        create_Path(CELL,m3_index,path,width)

# mos
def create_Mos(cell,layout_data,offset,r = False):

    global DBU

    left_data = defaultdict(list)
    right_data = defaultdict(list)
    for layer,contents in layout_data.items():

        l1,l2 = layer.split(',')
        layer_index = LAYOUT.layer(LayerInfo.new(int(l1),int(l2)))
        for points in contents:
            middle_x = points[2] + points[0]
            if abs(middle_x) >= 3910:
                if middle_x <= -3910:
                    left_data[layer_index].append([points[:2],points[2:]])
                else:
                    right_data[layer_index].append([points[:2],points[2:]])
            else:
                
                if r == True:
                    p2 = np.array(points[:2])*np.array([1,-1]) + np.array(offset)*DBU
                    p1 = np.array(points[2:])*np.array([1,-1]) + np.array(offset)*DBU

                else:
                    p1 = np.array(points[:2]) + np.array(offset)*DBU
                    p2 = np.array(points[2:]) + np.array(offset)*DBU
                create_Box2(cell,layer_index,p1,p2)

    return left_data,right_data

# mos
def create_MultiMos(M,N):

    global TOP_CELL,LAYOUT

    pfet_name = "100_55_1_pfet_06v0"
    nfet_name = "100_70_1_nfet_06v0"

    pdummy_cell = make_subcell(TOP_CELL,'pdummy')
    pdummy2_cell = make_subcell(TOP_CELL,'pdummy2')
    pconnect_cell = make_subcell(TOP_CELL,'pconnect')
    ndummy_cell = make_subcell(TOP_CELL,'ndummy')
    ndummy2_cell = make_subcell(TOP_CELL,'ndummy2')
    nconnect_cell = make_subcell(TOP_CELL,'nconnect')

    pfet_data = load_json("/home/oe23ranan/Omocha_mpwgf1/block/json/"+pfet_name+".json")
    nfet_data = load_json("/home/oe23ranan/Omocha_mpwgf1/block/json/"+nfet_name+".json")

    mos_data = {
        'Mdiff':{'t':'nfet','m':2,'x':6,'y':0,'r':True},
        'Ml1':{'t':'nfet','m':1,'x':4,'y':1,'r':False},
        'Minn':{'t':'nfet','m':1,'x':5,'y':1,'r':False},
        'Minp':{'t':'nfet','m':1,'x':6,'y':1,'r':False},
        'Ml2':{'t':'nfet','m':1,'x':7,'y':1,'r':False},

        'M1':{'t':'pfet','m':1,'x':5,'y':2,'r':True},
        'M2':{'t':'pfet','m':1,'x':6,'y':2,'r':True},

        'Ml3':{'t':'pfet','m':1,'x':1,'y':2,'r':True},
        'Ml4':{'t':'pfet','m':1,'x':2,'y':2,'r':True},

        'M3':{'t':'pfet','m':1,'x':9,'y':2,'r':True},
        'M4':{'t':'pfet','m':1,'x':10,'y':2,'r':True},
    }   

    dummy_flg = {
        pdummy_cell:0,
        pdummy2_cell:0,
        pconnect_cell:0,
        ndummy_cell:0,
        ndummy2_cell:0,
        nconnect_cell:0
    }
    dummy_pos = {
        pdummy_cell:[0,0],
        pdummy2_cell:[0,0],
        pconnect_cell:[0,0],
        ndummy_cell:[0,0],
        ndummy2_cell:[0,0],
        nconnect_cell:[0,0]
    }

    y_space = [1,0,1]

    mos_area = set()
    skip_gate = list()
    for name,contents in mos_data.items():
        mos_cell = make_subcell(TOP_CELL,name)

        for multi in range(contents['m']):
            offset = (2*(contents['x']-contents['m']//2 + multi),7*contents['y'] + y_space[contents['y']])
            skip_gate.append(offset)
            layout_data = pfet_data if contents['t'] == 'pfet' else nfet_data
            left_data,right_data = create_Mos(mos_cell,layout_data,offset,r = contents['r']) 
    
    for j in range(N):

        if j in [0,1]:
            dummy_cell = ndummy_cell
            dummy2_cell = ndummy2_cell
            connect_cell = nconnect_cell
        else:
            dummy_cell = pdummy_cell
            dummy2_cell = pdummy2_cell
            connect_cell = pconnect_cell

        dummy_rot = Trans.R0

        # dummy
        for i in range(M):

            offset = (2*i,7*j + y_space[j])
            barea = set([(offset[0] + dx,offset[1] + dy) for dx in range(-2,3) for dy in range(-2,3)])
            mos_area |= barea

            if offset in skip_gate:
                continue

            if dummy_flg[dummy_cell] == 0:
                layout_data = nfet_data if dummy_cell == ndummy_cell else pfet_data
                left_data,right_data = create_Mos(dummy_cell,layout_data,offset)
                dummy_pos[dummy_cell] = get_pos(dummy_cell)
                dummy_flg[dummy_cell] = 1
            else:
                origin_pos = dummy_pos[dummy_cell]
                LAYOUT.cell(TOP_CELL.name).insert(CellInstArray(dummy_cell,Trans(Point(-1*origin_pos[0]+offset[0]*DBU,-1*origin_pos[1]+offset[1]*DBU))))
        
        # connect
        for i in range(M*2):
            offset = (i,7*j + y_space[j])
            width = 0.3
            if dummy_flg[connect_cell] == 0:
                for idx,point in enumerate([[offset[0],offset[1]-2],[offset[0],offset[1]+2]]):
                    if connect_cell == nconnect_cell:
                        create_Box(connect_cell,contact_index,point,0.22,0.22)
                        create_Box(connect_cell,m1_index,point,width,1.0)
                        create_Box(connect_cell,m1_index,point,1.0,width)
                    elif connect_cell == pconnect_cell:

                        if idx == 0:
                            point[1] += 0.045
                        else:
                            point[1] -= 0.045
                        create_Box(connect_cell,contact_index,point,0.22,0.22)
                        create_Box(connect_cell,m1_index,point,1.0,width)
                        create_Box(connect_cell,v1_index,point,0.26,0.26)
                        create_Box(connect_cell,m2_index,point,width,1.09)
                        create_Box(connect_cell,m2_index,point,1.0,width)
                dummy_pos[connect_cell] = get_pos(connect_cell)
                dummy_flg[connect_cell] = 1
            else:
                origin_pos = dummy_pos[connect_cell]
                LAYOUT.cell(TOP_CELL.name).insert(
                    CellInstArray(connect_cell,
                                  Trans(Point(-1*origin_pos[0]+offset[0]*DBU,-1*origin_pos[1]+offset[1]*DBU))))

        # side dummy
        if dummy_flg[dummy2_cell] == 0:
            for layer_index,contents in left_data.items():
                for point in contents:
                    point = np.array(point) + [0,(7*j+ + y_space[j])*DBU]
                    create_Box2(dummy2_cell,layer_index,point[0],point[1])
            for layer_index,contents in right_data.items():
                for point in contents:
                    point = np.array(point) + [(2*M-2)*DBU,(7*j+ + y_space[j])*DBU]
                    create_Box2(dummy2_cell,layer_index,point[0],point[1])
            dummy_pos[dummy2_cell] = get_pos(dummy2_cell)
            dummy_flg[dummy2_cell] = 1
        else:
            origin_pos = dummy_pos[dummy2_cell]
            LAYOUT.cell(TOP_CELL.name).insert(CellInstArray(dummy2_cell,Trans(Point(0,-1*origin_pos[1]+offset[1]*DBU))))

    create_Meshes(mos_area)

    # routing("/home/oe23ranan/Omocha_mpwgf1/block/json/Route.json")
        
    origin_pos = get_pos(TOP_CELL)
    TOP_CELL.transform(Trans(Point(-1*origin_pos[0],-1*origin_pos[1])))
    # TOP_CELL.transform(DTrans(0,0))
    
# mesh structure
def create_Mesh(cell_name,point,width,mode = 'full'):

    global TOP_CELL
    sub_cell = make_subcell(TOP_CELL,cell_name)

    if mode == 'full':
        create_Box(sub_cell,m1_index,point,width,1.0)
        create_Box(sub_cell,m1_index,point,1.0,width)
        create_Box(sub_cell,m2_index,point,width,1.0)
        create_Box(sub_cell,m2_index,point,1.0,width)
    elif mode == 'half':
        create_Box(sub_cell,m1_index,point,width,1.0)
        create_Box(sub_cell,m1_index,point,1.0,width)

    return sub_cell

# mesh
def create_Meshes(mos_area):

    global LAYOUT,TOP_CELL

    temp = sorted(list(mos_area))
    min_x,min_y = temp[0]
    max_x,max_y = temp[-1]

    flg = 0
    for y in range(min_y - 1 - 2, max_y + 2 + 1):
        for x in range(min_x - 1, max_x + 2):
            point = (x,y)
            if flg == 0:
                mesh_cell = create_Mesh('mesh',point,0.5)
                flg = 1
            else:
                origin_pos = get_pos(mesh_cell)
                if point not in mos_area:
                    LAYOUT.cell(TOP_CELL.name).insert(CellInstArray(mesh_cell,Trans(Point(-1*origin_pos[0]+point[0]*DBU,-1*origin_pos[1]+point[1]*DBU))))

# routing
def routing(data_path):

    routing_data = load_json(data_path)

    offset = [0,0]

    for layer,contents in routing_data.items():

        if layer == 'text':
            for string,content in contents.items():
                layer = content[0]
                l1,l2 = layer.split(',')
                layer_index = LAYOUT.layer(LayerInfo.new(int(l1),int(l2)))
                point = np.array(content[1:3]) + np.array(offset)*DBU
                create_Text(TOP_CELL,layer_index,point,string)
        else:

            l1,l2 = layer.split(',')
            layer_index = LAYOUT.layer(LayerInfo.new(int(l1),int(l2)))
            for points in contents:
                p1 = np.array(points[:2]) + np.array(offset)*DBU
                p2 = np.array(points[2:]) + np.array(offset)*DBU
                create_Box2(TOP_CELL,layer_index,p1,p2)

if __name__ == '__main__':

    app = Application.instance()
    mw = app.main_window()

    # layoutのcurrent_viewを取得
    try:
        lv = mw.current_view()
        if lv is None:
            raise OriginalError('Cancelled')
    except OriginalError as e:
        print(e)

    # cellの取得
    # https://www.klayout.de/doc/code/class_Cell.html
    TOP_CELL = lv.active_cellview().cell

    print(TOP_CELL.name)
    print(TOP_CELL.bbox())
    
    # layoutの取得
    LAYOUT = TOP_CELL.layout()
    # dbu
    DBU = 1 / TOP_CELL.layout().dbu

    m1_index = LAYOUT.layer(LayerInfo.new(34,0))
    m2_index = LAYOUT.layer(LayerInfo.new(36,0))
    m3_index = LAYOUT.layer(LayerInfo.new(42,0))
    m4_index = LAYOUT.layer(LayerInfo.new(46,0))
    m5_index = LAYOUT.layer(LayerInfo.new(81,0))
    contact_index = LAYOUT.layer(LayerInfo.new(33,0))
    v1_index = LAYOUT.layer(LayerInfo.new(35,0))
    v2_index = LAYOUT.layer(LayerInfo.new(38,0))
    v3_index = LAYOUT.layer(LayerInfo.new(40,0))
    v4_index = LAYOUT.layer(LayerInfo.new(41,0))
    v5_index = LAYOUT.layer(LayerInfo.new(82,0))
    cap_index = LAYOUT.layer(LayerInfo.new(117,5))

    # get_structure()
    create_MultiMos(12,3)
    routing("/home/oe23ranan/Omocha_mpwgf1/block/json/Route.json")

    
    