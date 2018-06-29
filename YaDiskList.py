# в файл YaDiskLogIn.txt необходимо вписать логин и пароль от яндекс почты, разделенные ";" без пробелов
from dbconnect import connect

from YaDiskClient.YaDiskClient import YaDisk



def diskk(YaLOGIN,YaPASSWORD):
    disk = YaDisk(YaLOGIN,YaPASSWORD)
    return (disk)


# print(disk.ls("/")) обзор диска

# print(disk.ls("/")[len(disk.ls("/"))-1]["path"]) #название последнего добавленного файла
# print(disk.publish_doc("/1q.docx"))
# disk.upload("2.txt", "2.txt")  # src - локальный, dst - файл на диске