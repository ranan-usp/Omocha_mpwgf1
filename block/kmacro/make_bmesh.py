
# Enter your Python code here


from pya import *
import re
import json
import sys
import pprint
import numpy as np
from collections import defaultdict

class OriginalError(Exception):
    pass

# データ保存関連
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

# layer mapを取得
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

    global TOP_CELL

    save_data = dict()
    for index,layer in get_layer_map().items():
        
        sel = TOP_CELL.shapes(index)
        p_list = list()
        for temp in sel.each():
            p1,p2 = temp.bbox().p1,temp.bbox().p2
            p_list.append([p1.x,p1.y,p2.x,p2.y])
        save_data[layer] = p_list

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

# box
def create_Box(cell,index,point,width,height):

    point = get_DBU_point(point)

    # size of box
    size = get_DBU_point([width,height])
    
    points = np.concatenate([point - size//2,
                             point + size//2])
    
    cell.shapes(index).insert(Box.new(points[0],points[1],points[2],points[3]))

# box
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

    point = get_DBU_point(point)

    cell.shapes(index).insert(Text.new(string,point[0],point[1]))

# via
def create_via(cell,point):

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

    create_Box(cell,m2_index,point,m_width,m_height)
    create_Box(cell,m3_index,point,m_width,m_height)

    via_size = 0.26
    upper_point = [point[0],point[1]+m_height/4]
    create_Box(cell,v2_index,upper_point,via_size,via_size)
    under_point = [point[0],point[1]-m_height/4]
    create_Box(cell,v2_index,under_point,via_size,via_size)

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
        create_via(CELL,point)
        paths[wait[x]].append(point)

    for path in paths:
        create_Path(CELL,m3_index,path,width)
        middle_point = path[len(path)//2]
        path = [middle_point,[(x+5)*width*4,middle_point[1]]]
        create_Path(CELL,m3_index,path,width)

# mos
def create_Mos(cell,layout_data,offset):

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

                p1 = np.array(points[:2]) + np.array(offset)*DBU
                p2 = np.array(points[2:]) + np.array(offset)*DBU
                create_Box2(cell,layer_index,p1,p2)

    return left_data,right_data

# mos
def create_MultiMos(name,M,N):

    global TOP_CELL,LAYOUT

    dummy_cell = make_subcell(TOP_CELL,'dummy')
    dummy2_cell = make_subcell(TOP_CELL,'dummy2')
    layout_data = load_json("/home/oe23ranan/Omocha_mpwgf1/block/json/"+name+".json")

    mos_data = {
        'mos1':{'m':3,'x':4,'y':0},
        'mos2':{'m':5,'x':11,'y':0},
        'mos3':{'m':3,'x':4,'y':1},
        'mos4':{'m':3,'x':9,'y':2},
    }   


    mos_area = set()
    skip_gate = list()
    for name,contents in mos_data.items():
        mos_cell = make_subcell(TOP_CELL,name)

        for multi in range(contents['m']):
            offset = (2*(contents['x']-contents['m']//2 + multi),7*contents['y'])
            skip_gate.append(offset)
            left_data,right_data = create_Mos(mos_cell,layout_data,offset) 

    dummy_flg = 0
    for j in range(N):

        for i in range(M):

            offset = (2*i,7*j)
            barea = set([(offset[0] + dx,offset[1] + dy) for dx in range(-2,3) for dy in range(-2,3)])
            mos_area |= barea

            if offset in skip_gate:
                continue

            target_cell = dummy_cell

            if target_cell != dummy_cell:
                # left_data,right_data = create_Mos(target_cell,layout_data,offset) 
                pass
            elif dummy_flg == 0 and target_cell == dummy_cell:
                left_data,right_data = create_Mos(target_cell,layout_data,offset)
                dummy_flg = 1
            else:
                LAYOUT.cell(TOP_CELL.name).insert(CellInstArray(target_cell,Trans(Point(offset[0]*DBU,offset[1]*DBU))))

        # dummy
        if j == 0:
            for layer_index,contents in left_data.items():
                for point in contents:
                    create_Box2(dummy2_cell,layer_index,point[0],point[1])
            for layer_index,contents in right_data.items():
                for point in contents:
                    point = np.array(point) + [(2*M-2)*DBU,0]
                    create_Box2(dummy2_cell,layer_index,point[0],point[1])
        else:
            LAYOUT.cell(TOP_CELL.name).insert(CellInstArray(dummy2_cell,Trans(Point(0,offset[1]*DBU))))

        if j == 0:

            point = [0,0]
            mesh_cell = create_Mesh(point,0.5)
            print(mesh_cell.prop_id)

        for y in range(-3,4):
            for x in range(-3,2*M + 2):
                point = (x,y+j*7)
                if point not in mos_area:
                    LAYOUT.cell(TOP_CELL.name).insert(CellInstArray(mesh_cell,Trans(Point(point[0]*DBU,point[1]*DBU))))
                
    top_cell_bbox = TOP_CELL.bbox()
    TOP_CELL.transform(Trans(Point(-1*(top_cell_bbox.p2.x +  top_cell_bbox.p1.x)/2,0)))

    LAYOUT.delete_property(0)

def create_Mesh(point,width):

    global TOP_CELL
    sub_cell = make_subcell(TOP_CELL,'mesh')

    create_Box(sub_cell,m1_index,point,width,1.0)
    create_Box(sub_cell,m1_index,point,1.0,width)
    create_Box(sub_cell,m2_index,point,width,1.0)
    create_Box(sub_cell,m2_index,point,1.0,width)

    return sub_cell

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
    v1_index = LAYOUT.layer(LayerInfo.new(35,0))
    v2_index = LAYOUT.layer(LayerInfo.new(38,0))
    v3_index = LAYOUT.layer(LayerInfo.new(40,0))
    v4_index = LAYOUT.layer(LayerInfo.new(41,0))
    v5_index = LAYOUT.layer(LayerInfo.new(82,0))
    cap_index = LAYOUT.layer(LayerInfo.new(117,5))

    name = "100_55_1_pfet_06v0"
    # name = "100_70_1_nfet_06v0"
    create_MultiMos(name,20,3)