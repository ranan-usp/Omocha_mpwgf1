
# Enter your Python code here


from pya import *
import re
import json
import sys
import pprint
import numpy as np

class OriginalError(Exception):
    pass

def create_Box(cell,index,center_point,size):
    
    points = np.concatenate([np.array(center_point) - size//2,
                             np.array(center_point) + size//2])
    
    cell.shapes(index).insert(Box.new(points[0],points[1],points[2],points[3]))

 

"""

def create_dacvia(cell,m_index,via_index,DBU,base_pos,first_l,last_l,mode = 0):

    met_width = 0.4*DBU
    via_width = 0.2*DBU
    via_offset = (met_width-via_width)//2
    
    count_x = 1
    count_y = 2

    for l in range(first_l,last_l+1):
    
      create_Box2(cell,m_index[l-1],base_pos,[base_pos[0]+met_width*count_x,base_pos[1]+met_width*count_y])
            
      if l != last_l:
        current_y = base_pos[1]

        for y in range(count_y):
          current_x = base_pos[0]
          for x in range(count_x):
            via_pos_x,via_pos_y = current_x+via_offset,current_y+via_offset
            create_Box2(cell,via_index[l-1],[via_pos_x,via_pos_y],[via_pos_x+via_width,via_pos_y+via_width])
            if x != count_x-1:
              current_x = current_x+met_width
          current_y = current_y+met_width

"""

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
    cell = lv.active_cellview().cell

    # layoutの取得
    layout = cell.layout()
    
    DBU = 1 / cell.layout().dbu

    m1_index = layout.layer(LayerInfo.new(34,0))
    m2_index = layout.layer(LayerInfo.new(36,0))
    m3_index = layout.layer(LayerInfo.new(42,0))
    m4_index = layout.layer(LayerInfo.new(46,0))
    m5_index = layout.layer(LayerInfo.new(81,0))
    m_index = [m1_index,m2_index,m3_index,m4_index,m5_index]
    
    v1_index = layout.layer(LayerInfo.new(35,0))
    v2_index = layout.layer(LayerInfo.new(38,0))
    v3_index = layout.layer(LayerInfo.new(40,0))
    v4_index = layout.layer(LayerInfo.new(41,0))
    v5_index = layout.layer(LayerInfo.new(82,0))
    v_index = [v1_index,v2_index,v3_index,v4_index,v5_index]

    border_index = layout.layer(LayerInfo.new(63,0))


    center_point = [0,0]

    for dy in range(10):
        for dx in range(10):
            current_point = [dx*DBU,dy*DBU]
            size = 1*DBU
            create_Box(cell,border_index,current_point,size)
