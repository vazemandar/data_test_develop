import urllib2
import xml.etree.ElementTree as ET
import pandas as pd
import unittest
import os.path

class loadXMLtoCSV():
    
    def loadData(Link): 
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
        print "The Data frame is ready."
        return Listings    
    
    def DataManip(DataF):
        #Data cleaing and sorting 
        DataF['DateListed'] =pd.to_datetime(DataF['DateListed'])    
        DataF=DataF.sort_values(by='DateListed')
        print 'Data sorted in acending order of datelisted...'
        return DataF
    
    def csvDownLoad(DataF, Donwnload_Path):    
        # to downaload the csv
        DataF.to_csv(Donwnload_Path,index=False)
        print 'CSV is available to review at your download location.' 
    
    def main(self):
        # URL of the XML loation 
        ListingDF=self.loadData('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
        FinalDF=self.DataManip(ListingDF)
        #feed the Download location for the csv file
        self.csvDownLoad(FinalDF, 'C:\Users\mandar\Desktop\KaggleData\CodeTestBooj\listing.csv')
        
    if __name__ == "__main__":
         
        # calling main function
        main() 
    
    
class TestdataFrame(unittest.TestCase, loadXMLtoCSV):
    
    def test_csvDnld(self,loadclass):
        #Please feed the location for download
        loadXMLtoCSV.__main__
        isExists=os.path.isfile('C:\Users\mandar\Desktop\KaggleData\CodeTestBooj\listing.csv')
        self.assertEqual(isExists, True)
     
    def testDataframe(self, loadclass):    
        isDatafr=loadXMLtoCSV.loadData('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
        self.assertEqual(len(isDatafr.columns), 10)
    
    def testData_Year(self, loadclass):    
        isDatafr=loadXMLtoCSV.loadData('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
        self.assertEqual(isDatafr['DateListed'][0][:4], 2016)
    
    def testData_description(self,loadclass):
        isDatafr=loadXMLtoCSV.loadData('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
        self.assertTrue(len(isDatafr['Description'][0]) <=200)
        
    def main(self,loadXMLtoCSV):
        self.test_csvDnld(loadXMLtoCSV)
        print "All Tests Performed"
    