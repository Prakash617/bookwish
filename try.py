# import datetime
# def day_ago(date):
#     previous_date = datetime.datetime.strptime(date, '%m-%d-%Y')
#     # print(type(previous_date))
#     today = datetime.datetime.today()
#     # compute difference
#     # ndays = (today - previous_date).days
#     ndays = 62
#     # print(ndays)
#     # Calculating years
#     years = ndays / 365
#     # month = ndays // 30
    
    
#     if ndays <= 30:
#         if ndays == 1:
#             # print(f"yesterday {ndays}.")
#             print(f"Yesterday")
#         else:
#             week = int(ndays%365)/7
#             print(f"{int(week)}w.")
#     elif ndays >= 30 and  ndays < 365 :
#         # month = ndays/30
#         month = int(ndays%365)/30
#         # week = int((ndays%365)%30)/7
#         print(f"{int(month)}m")
#     elif ndays >= 365:
#         # month =  365
      
#         # month = int(ndays%365)/30
#         # print(f"type {type(int(month))}, {month}).")
#         # month  = 'and ' + str(int(month)) + " month " if int(month) != 0 else ''
        
    
#         print(f"a year {int(years)}y {int(month)} ")
#     else:
#         print(f"a month than a year ago ")

#     # print output
#     # print(ndays)
    
# date =  "10-01-2021"  
# day_ago(date)





# cloudinary

# import datetime
# def day_ago(date):
#     previous_date = datetime.datetime.strptime(date, '%m-%d-%Y')
#     # print(type(previous_date))
#     today = datetime.datetime.today()
#     # compute difference
#     # ndays = (today - previous_date).days
#     ndays = 62
#     # print(ndays)
#     # Calculating years
#     years = ndays / 365
#     # month = ndays // 30
    
    
#     if ndays <= 30:
#         if ndays == 1:
#             # print(f"yesterday {ndays}.")
#             print(f"Yesterday")
#         else:
#             week = int(ndays%365)/7
#             print(f"{int(week)}w.")
#     elif ndays >= 30 and  ndays < 365 :
#         # month = ndays/30
#         month = int(ndays%365)/30
#         # week = int((ndays%365)%30)/7
#         print(f"{int(month)}m")
#     elif ndays >= 365:
#         # month =  365
      
#         # month = int(ndays%365)/30
#         # print(f"type {type(int(month))}, {month}).")
#         # month  = 'and ' + str(int(month)) + " month " if int(month) != 0 else ''
        
    
#         print(f"a year {int(years)}y {int(month)} ")
#     else:
#         print(f"a month than a year ago ")

#     # print output
#     # print(ndays)
    
# date =  "10-01-2021"  
# day_ago(date)

# import cloudinary
# import cloudinary.api
# import cloudinary.uploader
# def delete_image(image_url):
    # cloudinary.config(
    #     cloud_name = "YOUR_CLOUD_NAME",
    #     api_key = "YOUR_API_KEY",
    #     api_secret = "YOUR_API_SECRET"
    # )
    
    # cloudinary.config( 
    #         cloud_name = "dn9ss6sem", 
    #         api_key = "274374323315513", 
    #         api_secret = "eHJ3Z-U6vPdwmUQ2ZXtHnkzgbz4" 
    #         )
    
#     cloudinary.config( 
#   cloud_name = "mediaholic-nepal", 
#   api_key = "353428766987396", 
#   api_secret = "SjTPgChloMGOsXbZxEkiTKMSezM"  
# )
    # image_id = cloudinary.uploader.upload(image_url)
    # # print(image_id)
    # result = cloudinary.api.resource(image_url)
    # print(result["public_id"])
    # Delete the image from Cloudinary
    
    # i = cloudinary.uploader.destroy(image_url)
    # print(i)
    # # Handle the response from Cloudinary
    # if i['result'] == 'ok':
    #     print('delete successful')
        
    # else:
    #     print('Something went wrong')
#     o=cloudinary.api.delete_resources([image_url])
#     print(o)
        
# delete_image("isivf4nsdlbl3ylex5fi")

# import re
# import cloudinary
# import cloudinary.api
# import cloudinary
# from cloudinary import api

# import cloudinary.uploader 
  
# cloudinary.config( 
#   cloud_name = "mediaholic-nepal", 
#   api_key = "353428766987396", 
#   api_secret = "SjTPgChloMGOsXbZxEkiTKMSezM"  
# )






# def delete():

#     folder_name = "Bookwishes/test/test1/"

# # Get all assets in the folder
#     assets = api.resources(type="upload", prefix=folder_name)

#     # Delete all assets in the folder
#     for asset in assets["resources"]:
#         api.delete_resources(asset["public_id"])

#     # Print the number of deleted assets
#     print("Number of deleted assets:", len(assets["resources"]))


# delete()
# from django.utils import timezone
# from datetime import datetime
# import calendar
# def data():
#     now = datetime.now()
#     last_day_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], 0, 0, 0)
#     print(last_day_of_month)
# data()

# import re
# import cloudinary
# import cloudinary.api
# import cloudinary.uploader

# cloudinary.config( 
#   cloud_name = "dnfwsqh2e", 
#   api_key = "919115597456222", 
#   api_secret = "QaKxal5JcvH_UyHXop-30___9fA"  
# )

# public_id = "empty_sky55l"
# # result = cloudinary.api.delete_resources([image_public_id])
# response = cloudinary.uploader.destroy(public_id)
# print(response)


# def delete_image_from_url(url):
#     # Use a regular expression to extract the public ID from the URL
#     match = re.search(r"upload/(.+)\.", url)
#     if not match:
#         print("Error: Could not extract public ID from URL")
#     else:
#         public_id_with_version = match.group(1)
#         public_id = public_id_with_version.split('/')[-1].split('.')[0]
#         print("Public ID: " + public_id)

#     # Call the destroy method to delete the image
#     response = cloudinary.uploader.destroy(public_id)

#     # Check the response to see if the image was successfully deleted
#     if response['result'] == 'ok':
#         print("Image was successfully deleted")
#     else:
#         print("Failed to delete image: " + response['message'])

# delete_image_from_url("https://res.cloudinary.com/dnfwsqh2e/image/upload/v1677648347/Screenshot_from_2023-02-26_09-09-50_ycqjzm.png")



from datetime import datetime, timedelta

# def get_week_dates(base_date_str, start_day, end_day=None):
#     base_date = datetime.strptime(base_date_str, '%Y %b %d').date()
#     print(base_date)
#     monday = base_date - timedelta(days=base_date.isoweekday() - 1)
#     week_dates = [monday + timedelta(days=i) for i in range(7)]
#     return week_dates[start_day - 1:end_day or 7]

# # Example usage
# base_date_str = '2023 Mar 19'
# week_dates = get_week_dates(base_date_str, start_day=1, end_day=6)
# print(week_dates)
# Print the dates
# for d in week_dates:
#     print(d.strftime('%Y %b %d'))


import csv
from django.http import HttpResponse

# def generate_csv():
#     # sample data to write to CSV
#     data = [
#         ['John', 'Doe', 'jdoe@example.com', '123 Main St.'],
#         ['Jane', 'Doe', 'jane@example.com', '456 Elm St.'],
#         ['Bob', 'Smith', 'bsmith@example.com', '789 Oak St.'],
#     ]

#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="Badegs_club_summary.csv"'
#     writer = csv.writer(response)

#     # write header row with "Full Name" column
#     writer.writerow(['Full Name', 'Email', 'Address'])

#     # write data rows with full name column
#     for row in data:
#         full_name = row[0] + ' ' + row[1]
#         writer.writerow([full_name, row[2], row[3]])

#     # return the HTTP response with the CSV data
#     return response

# generate_csv()

from pytz import timezone
nepal_tz = timezone('Asia/Kathmandu')

# Define a datetime object for 9 PM Nepali time
nepal_time = datetime.now(tz=nepal_tz).replace(hour=21, minute=0, second=0, microsecond=0)

print(nepal_time)
