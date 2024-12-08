import os
import xml.etree.ElementTree as ET

def xml2txt_fun(xml_file_name, txt_file_name):
    # 读取XML文件
    tree = ET.parse(xml_file_name)
    root = tree.getroot()

    # 遍历XML元素
    # for child in root:
    #     print(child.tag, child.attrib)
    with open(txt_file_name,'w') as txt_f:
        # 访问特定元素
        for object in root.findall('object'):
            bndbox = object.find('bndbox')
            x_min = bndbox.find('xmin').text
            y_min = bndbox.find('ymin').text
            x_max = bndbox.find('xmax').text
            y_max = bndbox.find('ymax').text

            txt_f.write(str(x_min) + ' ' + str(y_min) + ' ' + str(x_max) + ' ' + str(y_max) + '\n')


def xml2txt(dir_path):

    xml_file_names = os.listdir(dir_path+'\\xml_label')

    for i in xml_file_names:
        file_spilt_name = i.rsplit('.',maxsplit = 1)
        txt_file_name = dir_path + '\\txt_label\\' + file_spilt_name[0] + '.txt'
        xml_file_name = dir_path + '\\xml_label\\' +i
        xml2txt_fun(xml_file_name,txt_file_name)


dir_path = 'F:\huawei_data\HWtestdataset_stage_label'
xml2txt(dir_path)

