import os
import glob
from os import listdir, getcwd
from os.path import join
from xml.dom import minidom


def xml_to_txt( lut ,input ,output):

    # Start writing  
    for xml in glob.glob( os.path.join(input , "*.xml") ): 

        xmldoc = minidom.parse(xml)  
        # define output filename    
        fname_out = xml.split("\\")[-1] 
        fname_out = (os.path.join(output, fname_out.split(".")[0] + '.txt'))

        with open(fname_out, "w") as f:
            # Get image properties
            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                # get class label
                classid =  (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    # label_str = "-1"
                    print ("warning: label '%s' not in look-up table" % classid)
                    continue
                    
                # get bbox coordinates
                xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                b = (int(xmin), int(xmax), int(ymin), int(ymax))
                # Write out the file
                f.write(label_str + " " + " ".join([("%d" % a) for a in b]) + '\n')

        # print ("wrote %s" % fname_out)    

if __name__ == '__main__' :

    input = getcwd()
    output = getcwd()


    input = os.path.join(input, "annotations", "xmls")
    #print(glob.glob(os.path.join(input , "*.xml") )) testing that we get correct path list
    output = os.path.join(output, "region_labels")
    # Create output path if not already exists
    if not os.path.exists(output):
        print("path does not exist")
        os.makedirs(output)

    #  Define your classes , you can add more 
    lut={}
    lut["knife"] = 0
    lut["billete"] = 1
    lut["pistol"] = 2

    # Write out to txts
    xml_to_txt(lut, input, output)