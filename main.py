import ftplib
import qrcode
from PIL import Image
from dotenv import load_dotenv
import os


load_dotenv()
ftp_host= os.getenv('FTP_HOST')
folder = os.getenv('FOLDER')
slong = os.getenv('SLONG')
ftp_id= os.getenv('ID')
ftp_pw = os.getenv('PW')
http= os.getenv('HTTP_HOST')
http_path = f"https://{http}/{folder}/"
http_path2 = f"https://{http}/{slong}/"
ftp = None

a = int(input('''請選譯要使用的功能
             1.證件照 QRCODE 生成。
             2.沙龍照 QRCODE 生成
          '''))


def login(x):
    try:
        global ftp
        ftp= ftplib.FTP(ftp_host)
        ftp.encoding = 'utf-8'
        ftp.login(ftp_id, ftp_pw)
    except ftplib.error_perm as e:
        print(f'到{x}資料夾失敗:請確認資料夾是否存在')
    except ConnectionRefusedError as e:
        print(f"{e}")
    except TimeoutError as e:
        print(f"{e}")
    except Exception as e:
            print(f"未知錯誤: {e}")

def creat_qrcode(xxx_path, save_path, result):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=2,
    )   
    qr.add_data(xxx_path)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f'{save_path}Q.jpg','JPEG')
    print(f'{result} 已生成')

def write_file(document_path, number, picture):
    with open(f'{document_path}/codes.txt', 'a+', encoding='utf-16') as document :        
        document.seek(0)  # 將文件指針移回文件開頭
        first_line = document.readline().strip()
        if first_line =='學號\t@照片\t@qrcode':  # 檢查第一行
            document.seek(0, 2)
            document.write(f'{number}\t{picture}\t{number}Q.jpg\n')  # 寫入新的內容 
        else:
            document.seek(0, 2) #將文件指針移到文件末尾
            document.write(f'學號\t@照片\t@qrcode\n')  # 寫入新的內容                   
            document.write(f'{number}\t{picture}\t{number}Q.jpg\n')


if a == 1:
    print("已選擇 1.證件照 QRCODE 生成...")
    login(folder)
    ftp.cwd(f'qrcode/{folder}')
    # 獲取資料夾中的所有檔案和目錄名稱
    dirs = ftp.nlst()
    # 如果有師長沙龍照目錄則移出
    if '師長沙龍照' in dirs:
        dirs.remove('師長沙龍照')
    for dir in dirs:
        try:
            ftp.cwd(dir)
            photos = ftp.nlst()
            if not photos:
                print(f'{dir}資料夾沒有檔案')
            else:
                os.makedirs(f'./{folder}/{dir}', exist_ok=True) #檢查生成目標資料夾是否存在
                for photo in photos: #生成QRcode及文件
                    p = photo.split(".")
                    doc_path = f'./{folder}/{dir}/'
                    file_path = f'{http_path}{dir}/{photo}'
                    qr_path = f'./{folder}/{dir}/{p[0]}'
                    p = photo.split(".") #去除原始圖檔副檔名
                    if not os.path.exists(f'./{folder}/{dir}/{p[0]}Q.jpg'): #判斷檔案是否已生成過
                        if p[1].lower() == 'jpg': #判斷檔案是否為jpg
                            creat_qrcode(file_path, qr_path, photo)
                            write_file(doc_path, p[0], photo )
                    else:
                        print(f'{photo} 的QRcode已存在')
                ftp.cwd('..')
        except:
            pass

elif a == 2:
    print("已選擇 2.沙龍照 QRCODE 生成...")
    login(slong)
    ftp.cwd(f'qrcode/{slong}/師長沙龍照')
    subjects = ftp.nlst()
    if subjects != []:
        for subject in subjects:
            ftp.cwd(subject)
            teachers = ftp.nlst()
            if teachers != []:
                for teacher in teachers:
                    ftp.cwd(teacher)   
                    files = ftp.nlst()
                    if files != []: # 檢查生成目標資料夾是否存在
                        os.makedirs(f'./{slong}/師長沙龍照/{subject}/{teacher}/', exist_ok=True)
                        for file in files:
                            f = file.split(".")
                            if f[1].lower() == 'zip': # 檢查目標檔案是否為zip
                                qrcode_path = f'./{slong}/師長沙龍照/{subject}/'
                                file_path = f'{http_path2}/師長沙龍照/{subject}/{teacher}/{file}'
                                picture_path = f'./{slong}/師長沙龍照/{subject}/{teacher}/{f[0]}'
                                if not os.path.exists(f'{qrcode_path}{f[0]}Q.jpg'): # 檢查目標檔案是否存在
                                    creat_qrcode(file_path, picture_path, teacher)
                                    for file2 in files:
                                        f2 = file2.split(".")
                                        if f2[1].lower() == 'jpg': # 檢查目標檔案是否為jpg
                                            write_file(qrcode_path, f[0], file2 )
                                            break                              
                                else:
                                    print(f'{file} 的QRcode已存在')        
                    else:
                        print(f'{teacher}資料夾沒有檔案')
                    ftp.cwd('..')                
            else:
                print(f'{subject}目錄沒有檔案')
            ftp.cwd('..')
else:
    print("輸入錯誤，請重新輸入")

input("請按Enter鍵退出...")