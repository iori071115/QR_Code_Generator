import os

def file_write ():
    os.makedirs('./QRcode', exist_ok=True)
    with open('./QRcode/QRcode.txt', 'a+', encoding='utf-8-sig') as file:        
        file.seek(0)  # 將文件指針移回文件開頭
        first_line = file.readline()
        if first_line.strip() != "學號":  # 檢查第一行
            file.write("學號    @qrcode\n")  # 寫入新的內容
        else:
            file.seek(0, 2)
            file.write("學號    @qrcode\n")  # 寫入新的內容


# if os.path.exists('example.txt'):
#     print('檔案已經存在...')
# else:
#     file_write ()
#     print("檔案寫入成功...")
byte_string = b'317\xc3\xa5\xc2\x8b\xc2\x87-38'
decoded_string_utf16 = '317å-38'.decode('utf-16')
print(decoded_string_utf16)  # 可能會輸出中文字符


