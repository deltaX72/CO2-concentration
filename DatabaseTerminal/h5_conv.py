import h5py
import os

#directories

d_buffer = "buffer"
d_archieves = "archieves"
d_urls = "urls"

path_to_archieve = 'https://data2.gosat.nies.go.jp/GosatDataArchiveService/usr/download/ProductPage/download?filePath=/data/wget_list/GU/SWIRL2CO2_GU_V0{}.zip'
versions = ["2.91", "2.90", "2.81", "2.80", "2.72"]
urls = [path_to_archieve.format(i) for i in versions]

# def read_data(dataset: h5py.File):
#     data = []

#     length = len(dataset['scanAttribute']['time'])
#     for i in range(length):
#         date_and_time = dataset['scanAttribute']['time'][i].split()
#         data.append({
#             "date": str(date_and_time[0].decode()),
#             "time": str(date_and_time[1].decode()),
#             "lat": str(dataset['Data']['geolocation']['latitude'][i]),
#             "lon": str(dataset['Data']['geolocation']['longitude'][i]),
#             "con": str(dataset['Data']['mixingRatio']['XCO2'][i])
#         })
    
#     return data
    
def unpack(path_to_archieve: str, output_directory: str = d_buffer):
    os.system(f"tar -xvf '{path_to_archieve}' -C '{output_directory}'")

def download_archieve(url: str, http_user: str, http_password: str, output_directory: str = d_archieves):
    os.system(f"wget '{url}' --http-user='{http_user}' --http-passwd='{http_password}' -P '{output_directory}'")

def check_updates(url: str, http_user: str, http_password: str):
    pass

def clear_directory(dir_name: str):
    os.system(f"rmdir '{dir_name}'")
    os.system(f"mkdir '{dir_name}'")

# def run():
    # url = "https://data2.gosat.nies.go.jp/GosatDataArchiveService/usr/download/ProductPage/view"
    # url_arch = "https://data2.gosat.nies.go.jp/GosatDataArchiveService/usr/download/ProductPage/download?filePath=/data/wget_list/GU/SWIRL2CO2_GU_V0*.zip"

    # user = "lit.ilya29@gmail.com"
    # password = "L57!EWCeSxh19cg_"

    # clear_directory(d_buffer)
    # clear_directory(d_archieves)
    # clear_directory(d_urls)

    # download_archieve(url_arch, user, password)

    # print(urls)



    # download
    # unpack
    # read
    # load data into database

# current_path = os.getcwd() + '/SWIRL2CO2/'
# lst = []
# for f in os.listdir(current_path):
#     lst.append(h5py.File(current_path + f, 'r'))
# # print(lst[0]['scanAttribute']['time'])
# # for i in lst[0]['scanAttribute']['time']:
# #     print(i)

# for i in read_data(lst[0]):
#     print(i)

# def read_files(path_to_h5_files):
#     data = []
#     for f in os.listdir(path_to_h5_files):
#         dataset = h5py.File(path_to_h5_files + f, 'r')
#         # [print(item) for item in dataset.items()]
#         # print(dataset['Data']['mixingRatio']['XCO2'])

#         # ===========================================================
        
#         for k, v in dataset.items():
#             print(f'{k}\n{v}')
#             for key, val in dataset[k].items():
#                 print(f'\t{key}\n\t{val}')
#                 for key2, val2 in dataset[k][key].items():
#                     print(f'\t\t{key2}\n\t\t{val2}')

#         print()
#         dataset.close()
#         break

# read_files(os.getcwd() + '/SWIRL2CO2/')

# =====================================================================

# wget https://data2.gosat.nies.go.jp/wgetdata/GU/SWIRL2CO2/2009/SWIRL2CO2_200904_V02.95.tar --http-user=lit.ilya29@gmail.com --http-passwd='L57!EWCeSxh19cg_'

# # msg = 'Уважаемые разработчики. Поздравляю вас с днем программиста'
# # def congrats(msg: str):
# #     data = []
# #     for i in msg:
# #         text = (i, bin(ord(i))[2:])
# #         data.append(text)
# #         # print(text)
    
# #     return data

# # get = congrats(msg)
# # for i in get:
# #     print(i[1])