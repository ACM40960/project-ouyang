# Hello!
This is a repository for my project!
<a name="top"></a>

## Description
This is my project repository, a project about studying the contribution of human industrial activities in global warming, I collected and processed a lot of data sets and analyzed them. And I put all the python code I used here, and some important figures and figures I used in the poster will also be in the ipynb file.  
And because the entire data processing process is constantly repeated and modified, one stage at a time, there is no one-click function to complete the entire analysis. Below I will list the purpose of each of my files.  
**BUT**, please note that there may be path problems. These file paths only work on my computer, I'm really not sure whether they will work properly in other environments. Therefore, if there is a problem that the file cannot be read, please modify the path first.
[Back to top](#top)


## File Structure
First, there are two folders here, as their names suggest, one for **code** and one for **datasets**.
Since the full dataset is so large (400+GB) I obviously can't upload it all, so I just put all the csv and output files I could upload here.  
[Back to top](#top)

### Folder [code/](./code/)
Here I put all my codes:  
- [dataset_ghcnd_clean.py](./code/dataset_ghcnd_clean.py):    
    This is where I do some initial processing of the GHCND dataset, including some cleaning and statistics by site. I define a lot of functions in it and put a lot of paths after if  for easy calling. Because I need to constantly modify and reprocess the data, it is best to separate it into individual functions. Since the ghcnd dataset is over 100g and has over 100,000 files, this process took a really super long time.

- [dataset_ghcnd_by_year.py](./code/dataset_ghcnd_by_year.py)  
- [dataset_ghcnd_by_year_v2.py](./code/dataset_ghcnd_by_year_v2.py)   
    After the initial cleaning process, these two files are Python files that I use to classify and store the processed ghcnd data set by month. Finally, the observation records will be stored according to the year and month instead of the site, which will facilitate my next statistical step. . The upgrade of v2 is to add multithreading, otherwise it is super slow. I ran the normal single-threaded version for 5 days and it still hasn't finished, so later I added this multithreaded v2 version

- [dataset_miads_clean.py](./code/dataset_miads_clean.py)      
    Just like the clean in ghcnd dataset, This file is used to initially clean the MIADS ocean dataset, delete the data without temperature, regularize the time column, and then save it in my format.
- [dataset_miads_process.py](./code/dataset_miads_process.py)  
    This is similar to the by_year file of ghcnd. It is used to separate the ocean (underwater) and air data above the sea surface, and assign reasonable weights according to their indicators.

- [dataset.ipynb](./code/dataset.ipynb)  
    This is where everything happens. I also made it into an ipynb file so you can hopefully see my plots when you open it (I really hope to keep the plots and not have any extra bugs). All the graphs in my poster are drawn from this ipynb file, including historical greenhouse gases concentration data, solar activity and volcanic activity, etc.   
    The specific content can be viewed in the ipynb file. Each code block in it is very short, and you can understand at a glance what I am doing.

- [granger_causality_results.csv](./code/granger_causality_results.csv)  
- [garnger_plot.py](./code/garnger_plot.py)  
    This file is used to plot the results of the Granger Causality Test. Because the granger results in ipynb are too long, I can only save them in a csv file first, then observe the results from the file, and finally use granger_plot.py to plot after determining the appropriate results. This is more convenient.

- [TSI_aerosol.py](./code/TSI_aerosol.py)
    This file is used to plot TSI and aerosol data at the beginning. Since this file is relatively old, ipynb files were not used for plotting at that time. However, I later added TSI and Aerosol charts to the ipynb file, and this file was discarded.  
     
[Back to top](#top)  

### Folder [datasets/](./datasets/)
Here I put all the csv and output files I could upload. 

- [aerogel.csv](./datasets/aerogel.csv)    
- [aerogel_dataset.csv](./datasets/aerogel_dataset.csv)  
    This is actually a typo. Earlier I named the **aerosol** dataset I collected as aerogel, but it contains **aerosol** data caused by historical volcanic activity. Later, I stopped using this separate file and integrated it into my superdataset and used that file.

- [Historical_TSI_Reconstruction.csv](./datasets/Historical_TSI_Reconstruction.csv)  
    Total Solar Irradiance data, from 1610 to 2018.  

- [monthly_sunspot.csv](./datasets/monthly_sunspot.csv)    
- [SN_m_tot_V2.0.csv](./datasets/SN_m_tot_V2.0.csv)  
    Abandoned. At first I wanted to use sunspots as a proxy for solar activity, but later I found that TSI, a more direct value, could be used for analysis solar activity.

- [ADF_test.txt](./datasets/ADF_test.txt)  
- [johansen_test_results.txt](./datasets/johansen_test_results.txt)  
- [VECM_results.txt](./datasets/VECM_results.txt)  
    These three files are used to store my analysis results. Because they are too long, I choose to store them in files and then analyze them.

- [superdataset.csv](./datasets/superdataset.csv)  
    This is the superdatset where I store all the data. Some columns are copied and pasted manually after I got the results.

- [range.csv](./datasets/range.csv)  
    Abandoned. I initially stored the temperature ranges for each year in separate csv files, but later integrated them into my superdataset

[Back to top](#top)

## Data Sources

**Temperature:**    
    NOAA: Global Historical Climatology Network daily (1750-2024)  [Link](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily)  
    CEDA: MIDAS Global Marine Meteorological Observations Data (1854-2024) [Link](https://catalogue.ceda.ac.uk/uuid/77910bcec71c820d4c92f40d3ed3f249#:~:text=The%20global%20marine%20meteorological%20observations,the%20stated%20date%20and%20time.)    
**Atmosphere:**    
    NOAA: Trends in CO2, CH4, N2O (1958-2022) [Link](https://gml.noaa.gov/ccgg/trends/data.html)  
    NOAA: Paleoclimatology - Law Dome Ice Core CO2, CH4, N2O (0-2004)[Link](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=noaa-icecore-9959)    
**Solar:**  
    SILSO: Sunspot Number (1818-2024)[Link](https://www.sidc.be/SILSO/datafiles)  
    LISIRD: Historical Total Solar Irradiance Reconstruction (1610-2018)[Link](https://lasp.colorado.edu/lisird/data/historical_tsi)  
**Geological:**  
    NASA: Stratospheric Aerosol Optical Thickness (1850-2012) [Link](https://data.giss.nasa.gov/modelforce/strataer/)   
    Copernicus: Stratospheric Aerosols Reconstruction (500BC-2024)[Link](https://essd.copernicus.org/articles/9/809/2017/)  

[Back to top](#top)

