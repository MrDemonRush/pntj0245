from django.shortcuts import render
import json
from datetime import datetime
from .forms import UploadJSONForm
from .models import Record
from django.contrib import messages
from django.shortcuts import redirect

def upload_json(request):
    if request.method == 'POST':
        form = UploadJSONForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            try:
                data = json.load(file)
                errors= []
                valid_records = []
                
                for i, item in enumerate(data):
                    name = item.get('name')
                    date_str = item.get('date')
                    
                    if not name or not date_str:
                        errors.append(f"{i}: is missing 'name' or 'date'")
                        continue
                    if len(name) >= 50:
                        errors.append(f"{i} is too long")
                        continue
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d_%H:%M")
                    except ValueError:
                        errors.append(f"{i} is not in the correct data format")
                        continue
                        
                    valid_records.append(Record(name=name, date=date))
                    
                if errors:
                    for err in errors:
                        messages.error(request, err)
                else:
                    Record.objects.bulk_create(valid_records)
                    messages.success(request, "Data uploaded successfully")
                    
            except json.JSONDecodeError:
                messages.error(request, "Invalid JSON")
                
    else:
        form = UploadJSONForm()
    return render(request, 'upload.html', {'form': form})

def records_table(request):
    records = Record.objects.all()
    return render(request, 'table.html', {'records': records})
    
def index(request):
    return redirect('upload_json')
