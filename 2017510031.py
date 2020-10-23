# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:37:02 2020

@author: LENOVO
"""

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
import csv
import json
import sys
from lxml import etree

    
def is_nan(value):
    try:
        import math
        return math.isnan(float(value))
    except:
        return False
inputfile=sys.argv[1]
outputfile=sys.argv[2]
choice=sys.argv[3]

#csv to xml part

def CSVtoXML(inputfile,outputfile):
    #okunan satırların atılacağı liste    
    allData=list()
    if inputfile=='DEPARTMENTS.csv':
        #sadece departments.csv dosyasında encoding belirtmemiz gerekiyo ama program içerisinde
        #oluşturulmuş csv dosyalarında ise utf-8 belirtilmesi gerekmiyor

       with open(inputfile,encoding="utf-8") as csv_file:
           csv_reader = csv.reader(csv_file, delimiter=';')
           for row in csv_reader:
             allData.append(row)
           
    else:
    
       with open(inputfile) as csv_file:
           csv_reader = csv.reader(csv_file, delimiter=';')
           for row in csv_reader:
            
            allData.append(row)
    
    
    
    
    outputfile=open(outputfile,'wb')
    
    #uygun tree yapısı oluşturma 
    root=Element('departmants')
    tree=ElementTree(root)
    index=0
    for data in allData:
        
                if index<=1:
                    
                    temp = data[1]
                
                if index==1 or temp != data[1]:
                    
                    uni=Element('university')
                    root.append(uni)
                   
                    uni.set('name',data[1])
                    uni.set('uType',data[0])
                    temp = data[1]
               
                if index>=1:
                    item=Element('item')
                    uni.append(item)
                    item.set('faculty',data[2])
                    item.set('id',data[3])   
                    name=Element('name')
                    item.append(name)
                    if data[5]=='İngilizce':
                        name.set('lang','en')
                    else:
                        name.set('lang','tr')
                    if data[6]=='İkinci Öğretim':  
                        name.set('second','Yes')
                    else:
                        name.set('second','No')
                    name.text=data[4]  
                    
                    if data[7]!='':
                        scholarship=Element('grant')
                        item.append(scholarship)
                        scholarship.text=data[7]
                    
                    period=Element('period')
                    item.append(period)
                    period.text=data[8]
                    
                    quota=Element('quota')
                    item.append(quota)
                    
                    if data[11]!='' :
                        quota.set('spec',data[11])
                    quota.text=data[10]
                    
                    field=Element('field')
                    item.append(field)
                    field.text=data[9]
                    
                    if data[12]=='':
                        temp_min='0'
                    else:
                        temp_min=data[12]
                    last_min_score=Element('last_min_score')
                    item.append(last_min_score)
                    last_min_score.set('order',temp_min)
                    
                     
                    if data[13]=='':
                        temp_min='0'
                    else:
                        temp_min=data[13]
                    last_min_score.text=temp_min
                    
                index=index+1
    #oluşturulan tree'yi output dosyasına(xml) yazdırma
    tree.write(outputfile) 

#*****************************************************************************************************************************
#*****************************************************************************************************************************
#*****************************************************************************************************************************

#xml to csv part

def XMLtoCSV(inputfile,outputfile):
    with open(outputfile, 'w', newline='') as csvfile:
        
        
        #csvde oluşturacağımız başlıklar
        fieldnames = [
        'ÜNİVERSİTE_TÜRÜ', 'ÜNİVERSİTE', 'FAKÜLTE', 'PROGRAM_KODU', 'PROGRAM', 'DİL','ÖĞRENİM_TÜRÜ','BURS','ÖĞRENİM_SÜRESİ',
        'PUAN_TÜRÜ', 'KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI', 'GEÇEN_YIL_MİN_SIRALAMA', 'GEÇEN_YIL_MİN_PUAN']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=';')
    
        writer.writeheader()
        
        #xml den tree yapısı oluşturma
        tree = ET.parse(inputfile)
        root = tree.getroot()
        
        
        #tree yapısını dolaşır
        for elem in root.iter('university'):
            university=elem.get('name')
            uType=elem.get('uType')
            
            langList = list()
            secondList = list()
            orderList = list()
            quotaSpecList= list()
            for el in elem.iter('item'):
                x=0
                y=0
                z=0
                i=0
                for e in el.iter('name'):
                    langList.insert(x,e.get('lang'))
                    secondList.insert(x,e.get('second'))
                    x=x+1
                
                for e in el.iter('last_min_score'):
                    if e.get('order')=='0':
                        orderList.insert(y,e.get(''))
                    else:
                        orderList.insert(y,e.get('order'))
                    y=y+1
                
                for e in el.iter('quota'):
                    quotaSpecList.insert(z,e.get('spec'))
                    z=z+1
                
                
                
                faculty=el.get('faculty')
                idS=el.get('id')
                if langList[i]=='tr':
                    lang='Türkçe'
                else:
                    lang='İngilizce'
                
                if secondList[i]=='Yes' or secondList[i]=='yes':
                    ogr_turu='İkinci Öğretim'
                else:
                    ogr_turu=''
                

                last_min_order=orderList[i]
                qSpec=quotaSpecList[i]
                i+=1
                
                
                    
                name=el[0].text
                cnt=0;
                if el[1].text=='25' or el[1].text=='50' or el[1].text=='75' or el[1].text=='100' or el[1].text=='0':
                    cnt+=1
                    scholarship=el[1].text
                else:
                    scholarship=''
                period=el[1+cnt].text
                quota=el[2+cnt].text
                field=el[3+cnt].text
                if el[4+cnt].text=='0' or el[4+cnt].text=='-' :
                    last_min_score=''
                else:
                    last_min_score=el[4+cnt].text
     
                    
    
        
                #tutulan verilere uygun yeni satır oluşturulur    
                writer.writerow({'ÜNİVERSİTE_TÜRÜ': uType, 'ÜNİVERSİTE': university, 'FAKÜLTE': faculty, 'PROGRAM_KODU': idS, 'PROGRAM': name,
                                 'DİL': lang,'ÖĞRENİM_TÜRÜ':ogr_turu,'BURS':scholarship, 'ÖĞRENİM_SÜRESİ': period, 'PUAN_TÜRÜ': field,
                                 'KONTENJAN': quota,'OKUL_BİRİNCİSİ_KONTENJANI':qSpec, 'GEÇEN_YIL_MİN_SIRALAMA':last_min_order, 'GEÇEN_YIL_MİN_PUAN': last_min_score})

#************************************************************************************************************************************
#************************************************************************************************************************************
#************************************************************************************************************************************

# csv to json part

def CSVtoJSON(inputfile,outputfile):
    if inputfile=='DEPARTMENTS.csv':
        csvfile = open(inputfile, 'r',encoding="utf-8")
    else:
        csvfile = open(inputfile,'r')
    

    jsonfile = open(outputfile, 'w')
    
    
    #csv reader objesi
    reader = csv.DictReader(csvfile,delimiter=';')

    i=0
    itemList = list()
    #bütün üniversite yapılarının bulunacağı list
    departmentsList = []

    for row in reader:

        if i==0:
            tempUni=row.get('ÜNİVERSİTE')
            tempUType=row.get('ÜNİVERSİTE_TÜRÜ')
            i+=1
    
        
        
       
        if row.get('DİL')=='İngilizce':
            lang='en'
        else:
            lang='tr'
        if row.get('ÖĞRENİM_TÜRÜ')=='İkinci Öğretim':
            second='Yes'
        else :
            second='No'
    
        if row.get('OKUL_BİRİNCİSİ_KONTENJANI')=='':
            spec='0'
        else:
            spec=row.get('OKUL_BİRİNCİSİ_KONTENJANI')
        
        if row.get('BURS')=='':
    
            grant='0'
        else:
            grant=row.get('BURS')
        
        
        if row.get('GEÇEN_YIL_MİN_SIRALAMA')=='':
            min_order='0'
        else:
            min_order=row.get('GEÇEN_YIL_MİN_SIRALAMA')
        if row.get('GEÇEN_YIL_MİN_PUAN')=='':
            min_score='0'
        else:
            min_score=row.get('GEÇEN_YIL_MİN_PUAN')
        #aynı üniversite olduğu sürece bölümleri üniversitenin içerisine atar
        if tempUni==row.get('ÜNİVERSİTE'):
                it={'id':row.get('PROGRAM_KODU'),'name':row.get('PROGRAM') ,'lang':lang,'second':second,
                                'period':row.get('ÖĞRENİM_SÜRESİ'),'spec':spec,'quota':row.get('KONTENJAN'),'field':row.get('PUAN_TÜRÜ'),
                                'last_min_score':min_score,'last_min_order':min_order,'grant':grant}
    
                itemList.append(it)

    
                     
        #farklı üniversite ismi geldiğinde elde bulunan üniversite yapısı departmentsList e atılır ve yeni üniversite yapısı oluşturulur
        else:
                
                rw= {'university name':tempUni,'uType':tempUType,'items':[{'faculty':row.get('FAKÜLTE'),
                     'department':[itemList]}]}
                temp = json.dumps(rw)


                itemList.clear()
                

                departmentsList.append(json.loads(temp))

                tempUni=row.get('ÜNİVERSİTE')
                tempUType=row.get('ÜNİVERSİTE_TÜRÜ')
                it={'id':row.get('PROGRAM_KODU'),'name':row.get('PROGRAM') ,'lang':lang,'second':second,
                                    'period':row.get('ÖĞRENİM_SÜRESİ'),'spec':spec,'quota':row.get('KONTENJAN'),'field':row.get('PUAN_TÜRÜ'),
                                    'last_min_score':min_score ,'last_min_order':min_order,'grant':grant}
                
                
                itemList.append(it)
            
    lastrw= {'university name':tempUni,'uType':tempUType,'items':[{'faculty':row.get('FAKÜLTE'),
                 'department':[itemList]}]}
    
    departmentsList.append(lastrw)

    generalRow={'departments':departmentsList}
    json.dump(generalRow, jsonfile, sort_keys=False, indent=4,ensure_ascii=False, separators=(',', ':'))
#*****************************************************************************************************************************
#*****************************************************************************************************************************
#*****************************************************************************************************************************

#csv to json part

def JSONtoCSV(inputfile,outputfile):
    with open(inputfile) as json_file: 
        data = json.load(json_file)
      
    departments = data['departments']
    
    
    
    
    data_file = open(outputfile, 'w',newline='') 
      
    #csv writer objesi oluşturma
    csv_writer = csv.writer(data_file,delimiter=';') 
      
    #csv dosyamızın başlığını oluşturucak array

    header=['ÜNİVERSİTE_TÜRÜ', 'ÜNİVERSİTE', 'FAKÜLTE', 'PROGRAM_KODU', 'PROGRAM', 'DİL','ÖĞRENİM_TÜRÜ','BURS','ÖĞRENİM_SÜRESİ',
        'PUAN_TÜRÜ', 'KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI', 'GEÇEN_YIL_MİN_SIRALAMA', 'GEÇEN_YIL_MİN_PUAN']
    csv_writer.writerow(header) 
    uniList=list()
    uTypeList=list()
    
    for emp in departments:
        uniList.append(emp['university name'])
        uTypeList.append(emp['uType'])
                    
                
    
    index=0
    for emp in departments: 
      
        uType=emp['uType']
        uName=emp['university name']

    
        for item in emp['items']:

            faculty=item['faculty']
            
            for department in item['department']:

                
                
                uType=uTypeList[index]
                uName=uniList[index]
                index=index+1
                for dep in department:
  

                    tmp=list()
                    tmp.append(uType)
                    tmp.append(uName)
                    tmp.append(faculty)
                    tmp.append(dep['id'])
                    tmp.append(dep['name'])
                    if dep['lang']=='en':
                        tmp.append('İngilizce')
                    else:
                        tmp.append('')
                    if dep['second']=='Yes':
                        tmp.append('İkinci Öğretim')
                    else:
                        tmp.append('')
                    if dep['grant']=='0':
                        tmp.append('')
                    else:
                        tmp.append(dep['grant'])
                    
                    tmp.append(dep['period'])
                    tmp.append(dep['field'])
                    tmp.append(dep['quota'])
                    
                    if dep['spec']=='0':
                        tmp.append('')
                    else:
                        tmp.append(dep['spec'])
                    tmp.append(dep['last_min_order'])
                    tmp.append(dep['last_min_score'])
                    csv_writer.writerow(tmp) 
                    
               
            
        
                    
    
                  
        # Writing data of CSV file 
       
             
        
    #    csv_writer.writerow(emp.values()) 
      
    data_file.close() 

#*****************************************************************************************************************************
#*****************************************************************************************************************************
#*****************************************************************************************************************************

#xml to json part

def XMLtoJSON(inputfile,outputfile):
    #xml'den çekilen verilerin atılacağı genel list
    rowList= list()
    
    #xml dosyasını tree olarak oluşturma
    tree = ET.parse(inputfile)
    root = tree.getroot()
            
            
            
    for elem in root.iter('university'):
          university=elem.get('name')
          uType=elem.get('uType')
                
          langList = list()
          secondList = list()
          orderList = list()
          quotaSpecList= list()
          for el in elem.iter('item'):
                    x=0
                    y=0
                    z=0
                    i=0
                    for e in el.iter('name'):
                        langList.insert(x,e.get('lang'))
                        secondList.insert(x,e.get('second'))
                        x=x+1
                    
                    for e in el.iter('last_min_score'):
                        if e.get('order')=='0':
                            orderList.insert(y,e.get(''))
                        else:
                            orderList.insert(y,e.get('order'))
                        y=y+1
                    
                    for e in el.iter('quota'):
                        quotaSpecList.insert(z,e.get('spec'))
                        z=z+1
                    
                    
                    
                    faculty=el.get('faculty')
                    idS=el.get('id')
                    if langList[i]=='tr':
                        lang='Türkçe'
                    else:
                        lang='İngilizce'
                    
                    if secondList[i]=='Yes' or secondList[i]=='yes':
                        ogr_turu='İkinci Öğretim'
                    else:
                        ogr_turu=''
                    
    
                    last_min_order=orderList[i]
                    qSpec=quotaSpecList[i]
                    i+=1
                    
                    
                        
                    name=el[0].text
                    cnt=0;
                    if el[1].text=='25' or el[1].text=='50' or el[1].text=='75' or el[1].text=='100' or el[1].text=='0':
                        cnt+=1
                        scholarship=el[1].text
                    else:
                        scholarship=''
                    period=el[1+cnt].text
                    quota=el[2+cnt].text
                    field=el[3+cnt].text
                    if el[4+cnt].text=='0' or el[4+cnt].text=='-' :
                        last_min_score=''
                    else:
                        last_min_score=el[4+cnt].text
         
                        
                    
            
                        
                    rowList.append({'ÜNİVERSİTE_TÜRÜ': uType, 'ÜNİVERSİTE': university, 'FAKÜLTE': faculty, 'PROGRAM_KODU': idS, 'PROGRAM': name,
                                     'DİL': lang,'ÖĞRENİM_TÜRÜ':ogr_turu,'BURS':scholarship, 'ÖĞRENİM_SÜRESİ': period, 'PUAN_TÜRÜ': field,
                                     'KONTENJAN': quota,'OKUL_BİRİNCİSİ_KONTENJANI':qSpec, 'GEÇEN_YIL_MİN_SIRALAMA':last_min_order, 'GEÇEN_YIL_MİN_PUAN': last_min_score})
    
    
        
    itemList = list()
    
    # json yapısında buluncak bütün verilerin toplanacağı lis
    departmentsList = []
    jsonfile = open(outputfile, 'w')
    i=0
    for row in rowList:
            if i==0:
    
                tempUni=row.get('ÜNİVERSİTE')
                tempUType=row.get('ÜNİVERSİTE_TÜRÜ')
                i+=1
        
            
            
           
            if row.get('DİL')=='İngilizce':
                lang='en'
            else:
                lang='tr'
            if row.get('ÖĞRENİM_TÜRÜ')=='İkinci Öğretim':
                second='Yes'
            else :
                second='No'
        
            if row.get('OKUL_BİRİNCİSİ_KONTENJANI') is None or row.get('OKUL_BİRİNCİSİ_KONTENJANI')=='':
                
                spec='0'
            else:
                spec=row.get('OKUL_BİRİNCİSİ_KONTENJANI')
            
            if row.get('BURS') is None or row.get('BURS')=='':
        
                grant='0'
            else:
                grant=row.get('BURS')
            
    
    
            if row.get('GEÇEN_YIL_MİN_SIRALAMA') is None or row.get('GEÇEN_YIL_MİN_SIRALAMA')=='':
                min_order='0'
            else:
                min_order=row.get('GEÇEN_YIL_MİN_SIRALAMA')
            
            if row.get('GEÇEN_YIL_MİN_PUAN') is None or row.get('GEÇEN_YIL_MİN_PUAN')=='':
    
                min_score='0'
            else:
                min_score=row.get('GEÇEN_YIL_MİN_PUAN')
            
            #aynı üniversite olduğu sürece bölümleri üniversitenin içerisine atar
            if tempUni==row.get('ÜNİVERSİTE'):
                    
                    it={'id':row.get('PROGRAM_KODU'),'name':row.get('PROGRAM') ,'lang':lang,'second':second,
                                    'period':row.get('ÖĞRENİM_SÜRESİ'),'spec':spec,'quota':row.get('KONTENJAN'),'field':row.get('PUAN_TÜRÜ'),
                                    'last_min_score':min_score,'last_min_order':min_order,'grant':grant}
        
                    itemList.append(it)
    
        
                         
            #farklı üniversite ismi geldiğinde elde bulunan üniversite yapısı departmentsList e atılır ve yeni üniversite yapısı oluşturulur
            else:
                    
                    rw= {'university name':tempUni,'uType':tempUType,'items':[{'faculty':row.get('FAKÜLTE'),
                         'department':[itemList]}]}
                    temp = json.dumps(rw)
    
    
                    itemList.clear()
                    
    
                    departmentsList.append(json.loads(temp))
    
                    tempUni=row.get('ÜNİVERSİTE')
                    tempUType=row.get('ÜNİVERSİTE_TÜRÜ')
                    it={'id':row.get('PROGRAM_KODU'),'name':row.get('PROGRAM') ,'lang':lang,'second':second,
                                    'period':row.get('ÖĞRENİM_SÜRESİ'),'spec':spec,'quota':row.get('KONTENJAN'),'field':row.get('PUAN_TÜRÜ'),
                                    'last_min_score':min_score,'last_min_order':min_order,'grant':grant}
         
                    
                    itemList.append(it)
                
    lastrw= {'university name':tempUni,'uType':tempUType,'items':[{'faculty':row.get('FAKÜLTE'),
                     'department':[itemList]}]}
        
    departmentsList.append(lastrw)


    generalRow={'departments':departmentsList}
    json.dump(generalRow, jsonfile, sort_keys=False, indent=2,ensure_ascii=False, separators=(',', ':'))   


#*****************************************************************************************************************************
#*****************************************************************************************************************************
#********************************************************************************************

#json to xml part

def JSONtoXML(inputfile,outputfile):
    with open(inputfile) as json_file: 
        data = json.load(json_file)
          
    departments = data['departments']
        
        
        
    #json dosyasından okunan verilerin atılacağı genel list
    allData = list()
          
    
    #universite ve typeları listte tutulur
    uniList=list()
    uTypeList=list()
        
    for emp in departments:
            uniList.append(emp['university name'])
            uTypeList.append(emp['uType'])
                        
                    
        
    index=0
    for emp in departments: 
          
            uType=emp['uType']
            uName=emp['university name']
    
        
            for item in emp['items']:
    
                faculty=item['faculty']
                
                for department in item['department']:
                   
                    
                    
                    uType=uTypeList[index]
                    uName=uniList[index]
                    index=index+1
                    for dep in department:
      
    
                        tmp=list()
                        tmp.append(uType)
                        tmp.append(uName)
                        tmp.append(faculty)
                        tmp.append(dep['id'])
                        tmp.append(dep['name'])
                        if dep['lang']=='en':
                            tmp.append('İngilizce')
                        else:
                            tmp.append('')
                        if dep['second']=='Yes':
                            tmp.append('İkinci Öğretim')
                        else:
                            tmp.append('')
                        if dep['grant']=='0':
                            tmp.append('')
                        else:
                            tmp.append(dep['grant'])
                        
                        tmp.append(dep['period'])
                        tmp.append(dep['field'])
                        tmp.append(dep['quota'])
                        
                        if dep['spec']=='0':
                            tmp.append('')
                        else:
                            tmp.append(dep['spec'])
                        tmp.append(dep['last_min_order'])
                        tmp.append(dep['last_min_score'])
                        
                        allData.append(tmp)
                        
                   
                
    outputfile=open(outputfile,'wb')      
    #alınan verilere uygun tree yapısı oluşturur
    
    
    root=Element('departmants')
    tree=ElementTree(root)
    index=0
    for data in allData:
    
            if index<=1:
                
                temp = data[1]
            
            if index==1 or temp != data[1]:
                
                uni=Element('university')
                root.append(uni)
               
                uni.set('name',data[1])
                uni.set('uType',data[0])
                temp = data[1]
           
            if index>=1:
                item=Element('item')
                uni.append(item)
                item.set('faculty',data[2])
                item.set('id',data[3])   
                name=Element('name')
                item.append(name)
                if data[5]=='İngilizce':
                    name.set('lang','en')
                else:
                    name.set('lang','tr')
                if data[6]=='İkinci Öğretim':  
                    name.set('second','Yes')
                else:
                    name.set('second','No')
                name.text=data[4]  
    
                if data[7]!='':
                    scholarship=Element('grant')
                    item.append(scholarship)
                    scholarship.text=data[7]
                period=Element('period')
                item.append(period)
                period.text=data[8]
                
                quota=Element('quota')
                item.append(quota)
                
                if data[11]!='' :
                    quota.set('spec',data[11])
                quota.text=data[10]
                
                field=Element('field')
                item.append(field)
                field.text=data[9]
                
                if data[12]=='':
                    temp_min='0'
                else:
                    temp_min=data[12]
                last_min_score=Element('last_min_score')
                item.append(last_min_score)
                last_min_score.set('order',temp_min)
                
                 
                if data[13]=='':
                    temp_min='0'
                else:
                    temp_min=data[13]
                last_min_score.text=temp_min
                
            index=index+1
    tree.write(outputfile) 


#*****************************************************************************************************************************
#*****************************************************************************************************************************
#********************************************************************************************

#Validate part

def validate(xmlparser, xmlfilename):
        try:
            with open(xmlfilename, 'rb') as f:
                etree.fromstring(f.read(), xmlparser) 
            return True
        except etree.XMLSchemaError:
            return False
def XSDValidation(inputfile,outputfile):
   #xml dosyasını okuyup pars etme
    with open(outputfile, 'rb') as f:
        schema_root = etree.XML(f.read())
    
    schema = etree.XMLSchema(schema_root)
    xmlparser = etree.XMLParser(schema=schema)
    
    if validate(xmlparser, inputfile):
        print("%s validates." % inputfile)
    else:
        print("%s doesn't validate!" % inputfile)




#*****************************************************************************************************************************
#*****************************************************************************************************************************
#********************************************************************************************

#Kullanıcının gireceği verilere göre uygun fonksiyon çalışır

if choice=='1':
    CSVtoXML(inputfile,outputfile)
elif choice=='2':
    XMLtoCSV(inputfile,outputfile)
elif choice=='3':
    XMLtoJSON(inputfile,outputfile)
elif choice=='4':
    JSONtoXML(inputfile,outputfile)
elif choice=='5':
    CSVtoJSON(inputfile,outputfile)
elif choice=='6':
    JSONtoCSV(inputfile,outputfile)
elif choice=='7':
    XSDValidation(inputfile,outputfile)
    
else:
    print("WRONG COMMAND")
    
    
    
    
    
#TEST 
    
"""CSVtoXML('DEPARTMENTS.csv','1.xml')    
XMLtoCSV('1.xml','2.csv')
CSVtoJSON('2.csv','3.json')
JSONtoCSV('3.json','4.csv')
XMLtoJSON('1.xml','5.json')
JSONtoXML('5.json','6.xml')"""




