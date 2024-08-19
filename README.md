# Hello!
This is a repository for my project!

## Description
This is my project repository, a project about studying the contribution of human industrial activities in global warming, I collected and processed a lot of data sets and analyzed them. And I put all the python code I used here, and some important figures and figures I used in the poster will also be in the ipynb file.  
And because the entire data processing process is constantly repeated and modified, one stage at a time, there is no one-click function to complete the entire analysis. Below I will list the purpose of each of my files.  
**BUT**, please note that there may be path problems. These file paths only work on my computer, I'm really not sure whether they will work properly in other environments. Therefore, if there is a problem that the file cannot be read, please modify the path first.

---

## File Structure
First, there are two folders here, as their names suggest, one for **code** and one for **datasets**.
Since the full dataset is so large (400+GB) I obviously can't upload it all, so I just put all the csv and output files I could upload here.

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

### [datasets/](./datasets/)
Here I put all the csv and output files I could upload,




[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/PwK3l629)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=14975143&assignment_repo_type=AssignmentRepo)

