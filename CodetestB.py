import urllib2
import xml.etree.ElementTree as ET
import pandas as pd

def loadData(Link): 
    tree = ET.ElementTree(file=urllib2.urlopen(Link))
    root = tree.getroot()
    Listings=pd.DataFrame(columns=['MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price', 'Bedrooms', 'Bathrooms', 'Appliances', 'Rooms', 'Description'])    
    for i, Listing in enumerate(root.findall('Listing')):        
        if Listing.find('ListingDetails').find('DateListed').text[:4]=='2016' and ' and ' in Listing.find('BasicDetails').find('Description').text:       
                misid_= Listing.find('ListingDetails/MlsId').text 
                MlsName_=Listing.find('ListingDetails/MlsName').text 
                DateListed_=Listing.find('ListingDetails/DateListed').text
                StreetAddress=Listing.find('Location/StreetAddress').text       
                Price=Listing.find('ListingDetails/Price').text  
                Bedrooms= Listing.find('BasicDetails/Bedrooms').text  
                Bathrooms=Listing.find('BasicDetails/Bathrooms').text  
                elemList=[]
                for appl in Listing.find('RichDetails').find('Appliances').findall('Appliance'):
                    elemList.append(appl.text)
                Appliances=','.join(elemList)
                rmlist=[]
                try:
                    for rm  in Listing.find('RichDetails').find('Rooms').findall('Room'): 
                        rmlist.append(rm.text)  
                    Room=','.join(rmlist)
                except AttributeError :
                    Room=''
                Description = Listing.find('BasicDetails').find('Description').text[:200] 
                Listings.loc[i] = [misid_,MlsName_,DateListed_,StreetAddress,Price,Bedrooms,Bathrooms,Appliances,Room,Description]
    return Listings    

def DataManip(DataF):
    DataF['DateListed'] =pd.to_datetime(DataF['DateListed'])
    DataF=DataF.sort_values(by='DateListed')
    return DataF

def csvDownLoad(DataF, Donwnload_Path):    
    DataF.to_csv(Donwnload_Path,index=False)

def main():
    ListingDF=loadData('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')
    FinalDF=DataManip(ListingDF)
    csvDownLoad(FinalDF, 'C:\Users\mandar\Desktop\KaggleData\CodeTestBooj\listing.csv')
    
if __name__ == "__main__":
     
    # calling main function
    main()    