import urllib2
import xml.etree.ElementTree as ET
import pandas as pd
import unittest
import os.path
import sys


class loadXMLtoCSV():
    
    def loadData(self,Link): 
        #Loading the link and parsing the root for the XML
        tree = ET.ElementTree(file=urllib2.urlopen(Link))
        print 'Link is loaded...'
        root = tree.getroot()
        # declaration of the column of the data frame
        Listings=pd.DataFrame(columns=['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price', 'Bedrooms', 'Bathrooms', 'Appliances', 'Rooms', 'Description'])    
        # Parsing throught the listing element 
        print 'Parsing through the XML ...'
        for i, Listing in enumerate(root.findall('Listing')):
            #conditional check for the elements        
            if Listing.find('ListingDetails').find('DateListed').text[:4]=='2016' and ' and ' in Listing.find('BasicDetails').find('Description').text:       
                    misid_= Listing.find('ListingDetails/MlsId').text 
                    MlsName_=Listing.find('ListingDetails/MlsName').text 
                    DateListed_=Listing.find('ListingDetails/DateListed').text
                    StreetAddress=Listing.find('Location/StreetAddress').text       
                    Price=Listing.find('ListingDetails/Price').text  
                    Bedrooms= Listing.find('BasicDetails/Bedrooms').text  
                    Bathrooms=Listing.find('BasicDetails/Bathrooms').text  
                    elemList=[]
                    # try and except to handle Nonetype and assign null for the value of the text in case none type
                    try:
                        for appl in Listing.find('RichDetails').find('Appliances').findall('Appliance'):
                            elemList.append(appl.text)
                        Appliances=','.join(elemList)   
                    except AttributeError :
                        Appliances=''
                    try:
                        rmlist=[]
                        for rm  in Listing.find('RichDetails').find('Rooms').findall('Room'): 
                            rmlist.append(rm.text)  
                        Room=','.join(rmlist)
                    except AttributeError :
                        Room=''
                    #Parsing first 200 charcater    
                    Description = Listing.find('BasicDetails').find('Description').text[:200] 
                    #adding the row in data frame
                    Listings.loc[i] = [misid_,MlsName_,DateListed_,StreetAddress,Price,Bedrooms,Bathrooms,Appliances,Room,Description]
        print "The Data frame is ready"
        return Listings    
    
    def DataManip(self, DataF):
        #Data cleaing and sorting 
        DataF['DateListed'] =pd.to_datetime(DataF['DateListed'])    
        DataF=DataF.sort_values(by='DateListed')
        print 'Data sorted in acending order of datelisted...'
        return DataF
    
    def csvDownLoad(self,DataF, Donwnload_Path):    
        # to downaload the csv
        DataF.to_csv(Donwnload_Path,index=False)
        print 'CSV is available to review at your download location.' 
    
    def main(self):
        # URL of the XML loation 
        path_ = raw_input("Please provide the location for download:")
        if not path_: 
            print "The file will be downloaded in C drive By default."
            path_ = raw_input("Please provide the location for download or else hit enter to continue downlaoding on c drive :")
            if not path_:
                path_='C:\\'
        link_='http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
        ListingDF=self.loadData(link_)
        FinalDF=self.DataManip(ListingDF)
        #feed the Download location for the csv file
        path_=os.path.join(path_, 'listing.csv')
        self.csvDownLoad(FinalDF, path_)
        return path_


class TestdataFrame(unittest.TestCase):
    
    def test_4_cases(self):
        #Please feed the location for download
        sys.stdout.flush()
        LoXML=loadXMLtoCSV()
        locat=LoXML.main()
        isExists=os.path.isfile(locat)
        print "Performing test case : Does csv file exist"
        #Testing the csv file download
        self.assertEqual(isExists, True)
        print "Performing test case : Checking Data frame columns"
        isDatafr=LoXML.loadData('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
        self.assertEqual(len(isDatafr.columns), 10)   
        print "Performing test case : Checking the condition if record are from 2016"
        for Rec_year in isDatafr['DateListed'] :
            self.assertEqual(Rec_year[:4], '2016')
        print "Performing test case : Checking the length of description field"
        for Rec_Desc in isDatafr['Description'] :
            self.assertTrue(len(Rec_Desc) <=200)    
        print 'Testing completed'
    
if __name__ == "__main__":
    #L=loadXMLtoCSV()         
    # calling main function
    unittest.main()
    #L.main() 
    
