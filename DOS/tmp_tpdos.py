#!/usr/bin/python
#encoding=utf-8
import os
import numpy as np
import pickle
from pylab import *
import matplotlib.pyplot as plt
from collections import OrderedDict
"""
用来画指定元素的pdos，且dos值除以原子个数
TODO：
    指定元素各个轨道的pdos
例子：
    1.画原子1到10的总的pdos  plt_pdos.py 1 10
    2.画第5个原子单个原子的pdos：plt_pdos.py 5 5
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Feb 1, 2018"

efermi3 = {'DOSCARc10': 4.8479, 'DOSCARc6': 4.9184, 'DOSCARc3': 4.7125, 'DOSCARc1': 4.6259,
          'DOSCARg10': 5.0984, 'DOSCARg6': 4.8537, 'DOSCARg3': 4.5914,
          'DOSCARv1': 5.4008, 'DOSCARi1': 5.0992, 'DOSCARboundary': 4.3149, 'DOSCARboundary_2': 6.0228,
           'DOSCAR3gbi1': 4.5275, 'DOSCAR3gbv1': 0}

efermi5 = {'DOSCARc10': 4.4614, 'DOSCARc6': 4.7120, 'DOSCARc3': 4.6864, 'DOSCARc1': 0,
          'DOSCARg10': 4.7049, 'DOSCARg6': 4.3865, 'DOSCARg3': 0,'DOSCARg1':4.7549,
          'DOSCARv1': 5.4677, 'DOSCARi1': 5.1309, 'DOSCARboundary': 4.5854, 'DOSCARboundary_2': 6.1302,
           'DOSCAR5gbi1':4.6563, 'DOSCAR5gbv1':4.8059}

carbon_number3 = {'DOSCARc10': '85 94', 'DOSCARc6': '85 90', 'DOSCARc3': '85 87', 'DOSCARc1': '85 85',
                 'DOSCARg10': '85 94', 'DOSCARg6': '85 90', 'DOSCARg3': '85 87',
                 'DOSCARv1': '85 85', 'DOSCARi1': '85 85','DOSCAR3gbi1':'85 85', 'DOSCAR3gbv1':'85 85'}

carbon_number5 = {'DOSCARc10': '71 80', 'DOSCARc6': '71 76', 'DOSCARc3': '71 73', 'DOSCARc1': '71 71',
                 'DOSCARg10': '71 80', 'DOSCARg6': '71 76', 'DOSCARg3': '71 73','DOSCARg1': '71 71',
                 'DOSCARv1': '71 71', 'DOSCARi1': '71 71','DOSCAR5gbi1':'71 71', 'DOSCAR5gbv1':'71 71' }


def read_doscar(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    index = 0
    global natoms

    natoms = int(lines[index].strip().split()[0])
    index = 5
    nedos = int(lines[index].strip().split()[2])
    efermi = E_fermi
    # efermi = float(lines[index].strip().split()[3])
    # print('Total atom number was {0}'.format(natoms))
    # print('nedos was {0}'.format(nedos))
    # print('Fermi energy was {0} eV'.format(efermi))
    return lines, index, natoms, nedos, efermi

def get_totaldos(lines, index, natoms, nedos, efermi):
    write_content = []     # write doscar0
    plt = []         #plot figures
    for n in range(nedos):
        part_content = ''
        plt_content = []
        line = lines[index].strip().split()
        e = float(line[0])
        e_f = e-efermi
        plt_content.append(round(float(e_f),8))
        part_content += '%15.8f '%(e_f)
        for col in range(1, len(line)):
            dos = float(lines[index].strip().split()[col])
            if gogal == 'total':
                pass
            else:
                if col == 1:
                    dos = dos/natoms

            part_content += '%15.8f ' % (dos)
            plt_content.append(round(float(dos),8))
        part_content += '\n'
        write_content.append(part_content)
        plt.append(plt_content)
        index += 1
    return write_content,plt

def get_pdos(lines,index,natoms,nedos,efermi):
    '''
    :param lines: 输入文件内容，按照行读取所有内容
    :param index: 开始行号
    :param natoms: 原子个数
    :param nedos: dos中点的个数
    :param efermi: 费米面位置
    :return: 返回第一个为可以写入读取的分dos的列表，第二个为可以用来画图的列表
    画图的部分数据分别为：横坐标值，spd三个轨道分别的值，spd加起来的total值，各个轨道加起来的值
    x s p1 p2 p3 d1 d2 d3 d4 d5 total s p_total d_total(共14列，0,1-9,10,11-13)
    '''
    write_content = []     # write doscar0
    plt = []         #plot figures
    a = lines[index-1].strip().split()

    for n in range(nedos):
        part_content = ''
        plt_content = []
        s, p, d, total = (0, 0, 0, 0)

        line = lines[index].strip().split()
        if len(line) == 10:
            e = float(line[0])
            e_f = e-efermi
            plt_content.append(round(float(e_f),8))
            part_content += '%15.8f  '%(e_f)
            for col in range(1, len(line)):
                dos = float(lines[index].strip().split()[col])
                if col == 1:
                    s = dos
                elif col > 1 and col <= 4:
                    p += dos
                elif col > 4:
                    d += dos
                plt_content.append(round(float(dos),8))
            total = s + p + d
            # each_atom =
            part_content += '%15.8f' % (total)
            part_content += '%15.8f' % (s)
            part_content += '%15.8f' % (p)
            part_content += '%15.8f' % (d)
            part_content += '\n'
            plt_content.append(total)
            plt_content.append(s)
            plt_content.append(p)
            plt_content.append(d)
            write_content.append(part_content)
            plt.append(plt_content)
            index += 1
    return write_content,plt

def get_index(natoms,nedos):
    '''
    :param natoms:原子个数
    :param nedos: dos取点个数
    :return: 返回每个元素开始的行号
    '''
    ele_index = OrderedDict()
    ele_index['totaldos'] = 6
    p_index = [ 6 + (nedos+1) * x for x in range(1,natoms+1)]
    for i in range(1,natoms+1):
        ele_index[i] = p_index[i-1]
    return  ele_index

def get_input_number(number_string):
    '''
    :return: 返回输入指定开始和结尾原子的列表
    '''
    return  [x for x in range(int(number_string.split()[0]),int(number_string.split()[1])+1 )]

def run(filename,numberstring):
    '''
    :param filename: 读取内容的文件名
    :param numberstring: 所要画的元素的开始标号和结束标号
    :return: 返回总dos取点个数值，元素序号的列表，元素序号及对应dos图内容的字典
    '''
    lines, index, natoms, nedos, efermi = read_doscar(filename)
    element_index = get_index(natoms,nedos)
    element_number = get_input_number(numberstring)
    print('You choose element number was: {0}'.format(' '.join([str(x) for x in element_number])))
    write_p_dos = OrderedDict()
    plt_p_dos = OrderedDict()
    for i in element_number:
        num_index = element_index[i]
        content, plt_content = get_pdos(lines, num_index, natoms, nedos, efermi)
        if len(content) != 0:
            write_p_dos[i] = content
            plt_p_dos[i] = plt_content
    return nedos,element_number,write_p_dos,plt_p_dos

def conbine_pdos(nedos, element_number, write_p_dos,plt_p_dos):
    write_final = []
    plt_final = []
    key = list(write_p_dos.keys())
    for i in range(nedos):
        total = 0
        s_dos = 0
        p_dos = 0
        d_dos = 0
        for m in list(key):
            e_f = float(write_p_dos[m][i].split()[0])
            total += float(write_p_dos[m][i].split()[1])
            s_dos += float(write_p_dos[m][i].split()[2])
            p_dos += float(write_p_dos[m][i].split()[3])
            d_dos += float(write_p_dos[m][i].split()[4])
        if gogal == 'total':
            write_final.append('%15.8f  %15.8f  %15.8f  %15.8f  %15.8f' % (e_f, total, s_dos, p_dos, d_dos))
        else:
            # p_atoms = len(element_number)
            p_atoms = natoms
            write_final.append('%15.8f  %15.8f  %15.8f  %15.8f  %15.8f'%(e_f,total/p_atoms,s_dos,p_dos,d_dos))


        plt_tmp = []
        for iii in range(1, 14):
            val = 0
            if iii == 11:
                p_e_f = float(plt_p_dos[list(key)[0]][i][0])
                plt_tmp.insert(0,p_e_f)
                for n in list(key):
                    val += float(plt_p_dos[n][i][iii])
                if gogal == 'total':
                    pass
                else:
                    val = val / p_atoms
                plt_tmp.append(val)
            else:
                for n in list(key):
                    val += float(plt_p_dos[n][i][iii])
                if gogal == 'total':
                    pass
                else:
                    val = val / p_atoms
                plt_tmp.append(val)
        plt_final.append(plt_tmp)
    return write_final,plt_final

def write(content, gogalfilename):
    _remove_path(os.path.join(os.getcwd(),gogalfilename))
    f = open(gogalfilename,'a')
    for i in content:
        f.write(i + '\n')
    f.close()

def _remove_path(path):
    if os.path.exists(path):
        os.remove(path)
        print('{0} ******* This file path exists, removed'.format(path))

def totaldos():
    lines, index, natoms, nedos, efermi = read_doscar(filename)
    a,b = get_totaldos(lines,index+1,natoms,nedos,efermi)
    return b

#main
def which_number(numberstring):
    nedos, element_number, write_p_dos, plt_p_dos = run(filename, numberstring)
    write_final, plt_final = conbine_pdos(nedos, element_number, write_p_dos, plt_p_dos)
    return plt_final

def plt_dos(totaldata,*args):
    linewidth = 3
    xmin = -1
    xmax = 2
    ymin = 0
    ymax = 1.5
    min_gap_value = -0.1
    max_gap_value = 2
    fffsize = 10
    def get_gap(lable,a2,b2):
        gap = []
        for m in range(len(b2)):
            if b2[m] == 0:
                if a2[m] > min_gap_value and a2[m] < max_gap_value:
                    gap.append(m)
        try:
            # gap_value = a2[max(gap)] - a2[min(gap)]   #会找出gap最小值
            gap_value = a2[max(gap)]  #默认最小值为0
        except ValueError:
            print("{0} don't have gap".format(lable))
            gap_value = 0
        if gap_value != 0:
            # print('{0}: gap was {1:.8f}eV\n    max gap was {2:.8f}\n    min gap was {3:.8f}'.format(lable,gap_value,a2[max(gap)],a2[min(gap)]))
            print('{0}: gap was {1:.8f}eV'.format(lable,gap_value))
            #plt.text(0, 65, '%.5f eV' % gap_value, size=15)
        else:
            print('{0} gap was 0'.format(lable))

    pdata1 = args[0]
    p_data = np.array(pdata1)
    y1 = p_data[:, 10]

    pdata2 = args[1]
    p_data2 = np.array(pdata2)
    y2 = p_data2[:,10]

    pdata3 = args[2]
    p_data3 = np.array(pdata3)
    y3 = p_data3[:, 10]

    pdata4 = args[3]
    p_data4 = np.array(pdata4)
    y4 = p_data4[:, 10]

    t_data = np.array(totaldata)
    x1 = t_data[:, 0]
    ytotal = t_data[:,1]

    if ymax != 0:
        plt.ylim(ymin,ymax)
    else:
        plt.ylim(ymin, max(ytotal))
    plt.yticks(fontsize=fffsize)
    plt.xlim(xmin,xmax)
    plt.xticks(fontsize=fffsize)
    plt.plot(x1, ytotal, color='dimgrey', linewidth=linewidth, label='Total')
    plt.plot(x1, y1, color='#8f8ce7', linewidth=linewidth, label='Sb')
    plt.plot(x1, y2, color='skyblue', linewidth=linewidth, label='Ge')
    plt.plot(x1, y3, color='#69d84f', linewidth=linewidth, label='Te')
    plt.plot(x1, y4, color='#fc86aa', linewidth=linewidth, label='C')
    plt.plot([0] * 800, [x for x in range(800)], '--', color='black', linewidth=linewidth)
    plt.legend(loc='upper right', bbox_to_anchor=(1.025, 0.93),fancybox=False, ncol=1,fontsize=fffsize,frameon=False)  # ncol 控制有几列，bbox控制位置
    get_gap('Total Dos',x1,y1)

    plt.axes((0.42, 0.55, 0.35, 0.25))
    # ax = gca()
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    plt.xlim(-0.2,0.5)
    plt.ylim(0,1)
    plt.yticks([])
    plt.xticks(fontsize=10)
    plt.plot(x1, ytotal, color='dimgrey',linewidth=linewidth, label='Total')
    plt.plot(x1, y1,  color='#8f8ce7',linewidth=linewidth, label='Sb')
    plt.plot(x1, y2, color='skyblue',linewidth=linewidth, label='Ge')
    plt.plot(x1, y3, color='#69d84f',linewidth=linewidth, label='Te')
    plt.plot(x1, y4, color='#fc86aa',linewidth=linewidth, label='C')
    plt.plot([0] * 80, [x for x in range(80)], '--', color='black', linewidth=linewidth)

    plt.show()

def sigma3_dump(filename,plt=False):
    plttotaldos = totaldos()
    Sb = which_number('1 24')
    Ge = which_number('25 36')
    Te = which_number('37 84')
    try:
        carbon = carbon_number3[filename]
        C = which_number(carbon)
    except KeyError:
        C = False

    readname = 'tmp-3-'+filename
    fw = open(readname,'wb')
    pickle.dump(plttotaldos,fw)
    pickle.dump(Sb,fw)
    pickle.dump(Ge,fw)
    pickle.dump(Te,fw)
    if C:
        pickle.dump(C,fw)
    fw.close()
    if plt:
        if C:
            plt_dos(plttotaldos,Sb,Ge,Te,C)
        else:
            plt_dos(plttotaldos,Sb,Ge,Te)

def sigma3_load(filename):
    readname = 'tmp-3-'+filename
    fr = open(readname,'rb')
    plttotaldos = pickle.load(fr)
    Sb = pickle.load(fr)
    Ge = pickle.load(fr)
    Te = pickle.load(fr)

    try:
        C = pickle.load(fr)
        plt_dos(plttotaldos, Sb, Ge, Te, C)
    except EOFError:
        plt_dos(plttotaldos, Sb, Ge, Te)
    fr.close()

def sigma5_dump(filename,plt=False):
    plttotaldos = totaldos()

    Sb = which_number('1 20')
    Ge = which_number('21 30')
    Te = which_number('31 70')

    try:
        carbon = carbon_number5[filename]
        C = which_number(carbon)
    except KeyError:
        C = False

    readname = 'tmp-5-'+filename
    fw = open(readname,'wb')
    pickle.dump(plttotaldos,fw)
    pickle.dump(Sb,fw)
    pickle.dump(Ge,fw)
    pickle.dump(Te,fw)
    if C:
        pickle.dump(C,fw)
    fw.close()
    if plt:
        if C:
            plt_dos(plttotaldos,Sb,Ge,Te,C)
        else:
            plt_dos(plttotaldos,Sb,Ge,Te)

def sigma5_load(filename):
    readname = 'tmp-5-' + filename
    fr = open(readname, 'rb')
    plttotaldos = pickle.load(fr)
    Sb = pickle.load(fr)
    Ge = pickle.load(fr)
    Te = pickle.load(fr)
    try:
        C = pickle.load(fr)
        plt_dos(plttotaldos, Sb, Ge, Te, C)
    except EOFError:
        plt_dos(plttotaldos, Sb, Ge, Te)
    fr.close()


if __name__ == "__main__":

    # filename = 'DOSCARboundary_2'
    # filename = 'DOSCARv1'
    # filename = 'DOSCARi1'
    # filename = 'DOSCARc10'
    filename = 'DOSCARboundary'

    gogal = 'p'
    try:
        E_fermi = efermi3[filename]
    except KeyError:
        E_fermi = float(input('Please input E-fermi:'))

    plt_dos(filename)
    # sigma3_dump(filename)
    # sigma3_load(filename)