# Recommender Systems
## ("Réalisez une application de recommandation de contenu")

[This project is part of the AI Engineer class on OpenClassrooms]


---


## Running the notebooks online

As the notebooks are sometimes too big to be displayed on GitHub (and because the hyperlinks used for the navigation, doesn't work on GitHub), note that they are also avaible on [nbviewer.org](https://nbviewer.org/github/Valkea/OC_AI_09/tree/main/) and [dagshub.com](https://dagshub.com/Valkea/OC_AI_09) for convenience.


## Running the notebooks locally

In order to use this project locally, you will need to have Python and Jupyter notebook installed.
Once done, we can set the environment by using the following commands:


> #### First, 
> let's duplicate the project github repository
>
> ```bash
> >>> git clone https://github.com/Valkea/OC_AI_09
> >>> cd OC_AI_09
> ```

> #### Secondly,
>let's download the [dataset](https://www.kaggle.com/gspmoreira/news-portal-user-interactions-by-globocom#clicks_sample.csv) and unzip it in the 'data' folder:
> * data/news-portal-user-interactions-by-globocom/articles_metadata.csv
>
> * data/news-portal-user-interactions-by-globocom/clicks/clicks_hour_XXX.csv
>
> * data/news-portal-user-interactions-by-globocom/articles_embeddings.pickle
>
> and let's clone the large file with DVC *(you need to install [DVC](https://dvc.org) prior to using the following command line)*:
> ```bash
> >>> dvc remote add origin https://dagshub.com/Valkea/OC_AI_09.dvc
> >>> dvc pull -r origin
> ```

> #### Thirdly,
> let's create a virtual environment and install the required Python libraries
>
> (Linux or Mac)
> ```bash
> >>> python3 -m venv venvP9
> >>> source venvP9/bin/activate
> >>> pip install -r requirements.txt
> ```
>
> (Windows):
> ```bash
> >>> py -m venv venvP9
> >>> .\venvP9\Scripts\activate
> >>> py -m pip install -r requirements.txt
> ```

> #### Finally,
> let's configure and run the virtual environment for Jupyter notebook
>
> ##### Install jupyter kernel for the virtual environment using the following command:
>
> ```bash
> >>> pip install ipykernel
> >>> python -m ipykernel install --user --name=venvP9
> ```
>
> ##### Select the installed kernel
> 
> In order to run the various notebooks, you will need to use the virtual environnement created above.
So once the notebooks are opened (see below), prior to running it, follow this step:
![alt text](medias/venv_selection.png) 

> ##### Run the jupyter notebooks
>
> To see the notebooks, run:
> ```bash
> >>> jupyter lab
> ```
>
> * `01_EDA.ipynb` shows the Exploratory Data Analysis of the available files
> * `02_Recommender_systems.ipynb` shows 


## Running the API server locally 
The hybrid model is deployed using Azure functions, but if I didn't shared the FUNCTION_KEY with you, you can still start a local instance of the very same Azure function with the following steps:

> #### 1. Install the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and [Azure CORE](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Clinux%2Ccsharp%2Cportal%2Cbash#v2)

> #### 2. Move to the azure_function folder
> ```bash
> >> cd azure_function
> ```

> #### 3. Create a new virtual environment for the azure function & install the requiered files
>
> (Linux or Mac)
> ```bash
> >>> python3 -m venv venvP9azure
> >>> source venvP9azure/bin/activate
> >>> pip install -r requirements.txt
> ```
>
> (Windows):
> ```bash
> >>> py -m venv venvP9azure
> >>> .\venvP9azure\Scripts\activate
> >>> py -m pip install -r requirements.txt
> ```

> #### 4. Start the local Azure function
> ```bash
> (venv9azure) >>> func host start --port 5000
> ```

#### Tests
Once you have access to the Azure function *(either locally or in the cloud with the secret key)*, you can test some recommendations using the Streamlit user interface *(from another terminal if you are already running the local Azure function server)*:

```bash
>>> streamlit run 03_Streamlit.py
```

Stop with CTRL+C *(once the tests are done, from another terminal...)*


## Cloud deployement

I used Azure Function to deploy this project in the cloud. So let's recall the deployment steps...

> #### 1. Intialize the folder you’re working in
> ```bash
> >>> func init FOLDER_NAME
> or
> >>> func init FOLDER_NAME --python
> ```

> #### 2. Set up the bare bones Azure Function
> ```bash
> >>> cd FOLDER_NAME
> >>> func new
> ```
> then select *HTTP trigger*

> #### 3. Add the requiered libs to the FOLDER_NAME/requirements.txt file

> #### 4. Create a virtual environment & install libs
> ```bash
> >>> python -m venv MY_VENV
> >>> source MY_VEN/bin/activate
> >>> pip install -r requirements.txt
> ```

> #### 5. Run local Azure instance
> ```bash
> >>> func host start
> or 
> >>> func host start --port 5000
> ```

> #### 6. Create & configure an Azure Function APP_NAME on the Azure Portal

> #### 7. Deploy to Azure (you need APP_NAME azure function created on the portal)
> ```bash
> >>> az login
> >>> func azure functionapp publish APP_NAME --build remote
> ```

> #### 8. Grab the function URL on top right of the *function page* for remote calls


## Uninstalling the venv kernel
Once done with the project, the kernel can be listed and removed using the following commands:

```bash
>>> jupyter kernelspec list
>>> jupyter kernelspec uninstall venvp9
```
