![numbers](https://user-images.githubusercontent.com/73858914/151681458-11de4950-b503-470f-8f8d-69cb4fb61035.png)
# gColab
 Makes script for import of dataset archive to colab from Google Drive.   

If you have a CSV dataset for a shared colab notebook, consider using this utility script.

1. It uploads the most recently created zip archive to a specified Google Drive folder.
2. Then it creates a snippet for insertion into your colab notebook. Just paste from the clipboard.

That's it. The snippet looks like this:
```
# Download data from Google Drive
import gdown
!mkdir ../data
url = "https://drive.google.com/uc?export=download&id=1m17Q3tRRypU3ZrJhsxBKo4RXBkKqhTnO"
data = pd.read_csv(gdown.download(url, output="../data/weatherAUS.zip",  
                                  quiet=True), compression="zip")
data.head()
```
The script can be easily modified to deal with many more use cases.

Examples of configuration files are located in config folder. Please check [PyDrive documentation on OAuth](https://pythonhosted.org/PyDrive/oauth.html) for details.

Install:  
Clone repository to your computer, then
```
pip install -e /path/to/src/folder
```

Use:
```
>>> cd path/to/archive/folder
>>> gdrive
```
