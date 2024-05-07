from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re
from datetime import datetime
from django.db.models import Prefetch
from pdfminer.high_level import extract_text
from io import BytesIO
@csrf_exempt
def parse_pdf(request):
    if request.method == "POST":
        file = request.FILES["file"]
        file = BytesIO(file.read())
        # pdf_list =["pdf/1.pdf",'pdf/2.pdf', 'pdf/3.pdf', 'pdf/4.pdf' , 'pdf/5.pdf', 'pdf/6.pdf' , 'pdf/7.pdf' , 'pdf/8.pdf' , 'pdf/9.pdf' , 'pdf/10.pdf']
        # for pdf in pdf_list:
        text = extract_text(file)
        lines = text.split('\n')
        lines = list(filter(lambda line: line.strip(), lines))
            # for i, item in enumerate(lines):
                # print(f"{i}. {item}")
        airline = lines[7].split('-')[0]
        sector = []
        pattern = r'\d{2}:\d{2} \(\s*\d{2}\s*[A-Za-z]{3}\s*\)'
        titles = ('Mr', 'Mrs', 'Ms', 'Mstr', 'MR')
        dates = []    
        names = []
        pnr = ""
        for i, item in enumerate(lines[:-6]):
            if 'PNR:' in item:
                pnr = item.split(':')[1].strip()
                continue
            elif 'Terminal' in item:
                sector.append(lines[i-1][-5:])
                continue
            elif re.search(pattern, item):
                dates.append(re.search(pattern, item).group())
                continue
            elif item.startswith(titles):
                name = item[4:-5] if item.startswith("Mstr") else item[3:-5]
                names.append(name)
                continue
        return_date = get_date(dates[-1][8:15]) if sector[0] == sector[-1] else None
        sector = (sector[0] + "-" + sector[1] + "-" + sector[-1]) if sector[0] == sector[-1] else (sector[0]+ "-"+ sector[-1])
        travel_date = get_date(dates[0][8:15])
        return JsonResponse({'status': 'success', 'pnr': pnr, 'sector': sector, 'passenger': names,'travel_date': travel_date,'return_date': return_date, 'airline': airline }, status=200)

def get_date(obj):
    year = datetime.now().year
    date_str = f"{obj.strip()} {year}"
    date_object = datetime.strptime(date_str, "%d %b %Y")
    return date_object.strftime("%Y-%m-%d")
            
# def pk_pdf(lines, length):
    
#     pnr = lines[1]
#     name = " ".join(lines[6].split()[:3]).replace(' /', '')
#     sector = lines[12] + '-' + lines[14]
#     if length == 50:
#         date_object = datetime.strptime(lines[24], "%d %b %Y")
#         travel_date = date_object.strftime("%Y-%m-%d")
#     elif 50 < length  < 100:
#         date_object = datetime.strptime(lines[23], "%d %b %Y")
#         travel_date = date_object.strftime("%Y-%m-%d")
#         date_object = datetime.strptime(lines[62], "%d %b %Y")
#         return_date = date_object.strftime("%Y-%m-%d")
#     elif length == 100:
#         date_object = datetime.strptime(lines[24], "%d %b %Y")
#         travel_date = date_object.strftime("%Y-%m-%d")
#         name = name  +" / "+" ".join(lines[56].split()[:3]).replace(' /', '')
#     elif length ==174:
#         date_object = datetime.strptime(lines[23], "%d %b %Y")
#         travel_date = date_object.strftime("%Y-%m-%d")
#         date_object = datetime.strptime(lines[62], "%d %b %Y")
#         return_date = date_object.strftime("%Y-%m-%d")
#         name  = name+ " / " + " ".join(lines[93].split()[:3]).replace(' /', '')
#     return JsonResponse({'status': 'success', 'pnr': pnr, 'sector': sector, 'passenger': name,'travel_date': travel_date,'return_date': return_date, 'airline': "PK" }, status=200)

