import glob
import os
from random import randint
from shutil import copyfile
import xml.etree.ElementTree as ET
import pandas as pd




if os.name == 'nt':
        inputdir_label = "E:\Foosalytics\labels"
        inputdir_images = "E:\Foosalytic\images"
        outputdir_train = "E:\Foosalytics\train"
        outputdir_test = "E:\Foosalytics\test"
else:
        inputdir_label = "~/foosalytics/labels"
        inputdir_images = "~/foosalytics/images"
        outputdir_train = "~/foosalytics/train"
        outputdir_test = "~/foosalytics/test"

train_test_split = 0.2

xml_df_labels = []
xml_df_labels = xml_collect_files (inputdir_label)
xmllist_copy_split (xml_df_labels, train_test_split, outputdir_train, outputdir_test, inputdir_label, inputdir_images )



def xml_collect_files(path):
        for xml_file in glob.glob(path + '/**/*.xml',recursive=True):
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for member in root.findall('object'):
                    value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
                xml_list.append(value)
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        return xml_df
        

        


def xmllist_copy_split(xml_df, ratio, dir_train, dir_test, dir_label, dir_image):
        xml_df_test = []
        xml_df_train = xml_df
        test_indexlist = []
        test_indexlist = random_index_get(len(xml_list))
        
        
        for test_index in test_indexlist:
                xml_df_test = xml_df_test.append(xml_df_train[test_index])

        for test_index in test_indexlist:
                xml_df_train.pop(test_index)
        
        xml_df_test.xml_df.to_csv('dir_test/foosalytics_test_labels.csv', index=None)
        df_files_copy(xml_list_test, dir_test, dir_label, dir_image)
        
        xml_df_train.xml_df.to_csv('dir_ttrain/foosalytics_train_labels.csv', index=None)
        df_files_copy(xml_df_train, dir_train, dir_label, dir_image)

        
def df_files_copy(df, dir_output, dir_label, dir_image):
        for xmlfile_name in df["filename"].tolist():
                imagefile_name = xmlfile_name.replace('.xml','.jpg')
                for imagefile in glob.glob(dir_image + '/**/' + imagefile_name ,recursive=True):
                        copyfile(imagefile, join(dir_output,'/',imagefile_name))
                
        
        
def random_index_get(max_index):
        index =[]
        for i in range(ratio*100): index.append(random.randint(0,max_index))
        return index
        
