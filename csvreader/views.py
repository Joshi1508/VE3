import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from django.conf import settings
import os

def success(request):
    return render(request, 'csvreader/success.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            
            fs = FileSystemStorage(location=settings.FILE_UPLOAD_TEMP_DIR)
            filename = fs.save(uploaded_file.name, uploaded_file)
            
            file_path = os.path.join(settings.FILE_UPLOAD_TEMP_DIR, filename)
            data = process_data(file_path)
            if 'error' in data:
                return render(request, 'csvreader/error.html', {'error': data['error']})
            
            return render(request, 'csvreader/data_processing.html', {'data': data, 'file_path': file_path})
    else:
        form = UploadFileForm()
    return render(request, 'csvreader/upload.html', {'form': form})

def data_visualization(request, file_path):
    data = visualize_data(file_path)
    return render(request, 'csvreader/data_visualization.html', {'data': data})

def process_data(file_path):
    try:
        
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            
            df = pd.read_csv(file_path, encoding='latin1')
        except Exception as e:
            
            return {'error': str(e)}

    
    first_few_rows = df.head()

    
    summary_statistics = df.describe()

   
    missing_values_info = df.isnull().sum()

   
    data = {
        'first_few_rows': first_few_rows,
        'summary_statistics': summary_statistics,
        'missing_values_info': missing_values_info
    }
    return data

def visualize_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')

    histograms = []
    for column in df.select_dtypes(include='number').columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column], kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        hist_file = f'static/{column}_histogram.png'
        plt.savefig(hist_file)  
        plt.close()
        histograms.append(hist_file)

    return {'histograms': histograms}
