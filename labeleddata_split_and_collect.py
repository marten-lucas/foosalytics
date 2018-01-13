import glob
import os
from random import randint
import shutil 
import xml.etree.ElementTree as ET
import pandas as pd

def xml_collect_files (path):
        xml_list=[]
        row_count=0
        for xml_file in glob.glob(path + '/*.xml',recursive=True):
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
                row_count += 1
                print('CSV'+str(row_count)+':'+value[0])
                if row_count==file_limit: break
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        return xml_df
        

        


def xmllist_copy_split(xml_df, ratio, dir_train, dir_test, dir_label, dir_image):
        dir_root = os.path.dirname(os.path.abspath(__file__))
        xml_df_test = pd.DataFrame(data=None, columns=xml_df.columns)
        xml_df_train = xml_df
        
        test_volume = int(len(xml_df_train)*ratio)
        
        if test_volume:
                while test_volume:
                        rnd_index= randint(0,len(xml_df_train)-1)
                        xml_df_test.loc[len(xml_df_test)] = xml_df_train.iloc[rnd_index]
                        xml_df_train.drop([rnd_index],inplace=True)
                        xml_df_train.index = pd.RangeIndex(len(xml_df_train.index))
                        print("Train:"+str(len(xml_df_train))+";Test:"+str(len(xml_df_test))+";remaining"+str(test_volume))
                        test_volume-=1

                test_csv_filename='foosalytics_test_labels.csv'
                xml_df_test.to_csv(test_csv_filename, index=None)
                shutil.move(os.path.join(dir_root, test_csv_filename), os.path.join(dir_test,test_csv_filename))
                df_files_copy(xml_df_test, dir_test, dir_label, dir_image)
        
        train_csv_filename='foosalytics_train_labels.csv'
        xml_df_train.to_csv(train_csv_filename, index=None)
        shutil.move(os.path.join(dir_root, train_csv_filename), os.path.join(dir_train,train_csv_filename))
        df_files_copy(xml_df_train, dir_train, dir_label, dir_image)

        
def df_files_copy(df, dir_output, dir_label, dir_image):
        copy_count=0
        for xmlfile_name in df["filename"].tolist():
                imagefile_name = xmlfile_name.replace('.xml','.jpg')
                for imagefile in glob.glob(dir_image + '/**/' + imagefile_name ,recursive=True):
                        shutil.copyfile(imagefile, os.path.join(dir_output,imagefile_name))
                        copy_count+=1
                        print(str(copy_count)+" files copied:"+imagefile_name)
                

inputdir_label = "/media/FoosWin/labels"
inputdir_images = "/media/FoosWin/images"
outputdir_train = "/home/foosalyticsapp/foosalytics/train"
outputdir_test = "/home/foosalyticsapp/foosalytics/test"
train_test_split = 0.2
file_limit=-1

xml_df_labels = []
xml_df_labels = xml_collect_files(inputdir_label)
xmllist_copy_split (xml_df_labels, train_test_split, outputdir_train, outputdir_test, inputdir_label, inputdir_images )
print("finished")