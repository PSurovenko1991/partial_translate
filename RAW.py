# from textblob import TextBlob
#
# # s = ['я','ты','он','они']
# # for i in range(len(s)):
# #     word = TextBlob(s[i])
# #     if __name__ == '__main__':
# #         word2 = word.translate(to='en')
# #
# # print(s)
# s = [1,2]
# s1 = [' в ','он,','она','они']
# for i in range(len(s1)):
#     if TextBlob(s1[i]).detect_language()=='ru':
#         s1[i] = str(TextBlob(s1[i]).translate(to='en'))
#
#
# print(s1)
# print(type("*"))


# s = [1,'a',3,"v",5,6,7]
# print(s)
# i=0
# while i < len(s):
# 	if  type(s[i])!=str:
# 		del s[i]
# 	else:
# 		i += 1
#
# print(s)

#
# s =['x','b','b','v']
# s1 =['x','d','s','1']
# for i in range(len(s)):
#     if s[i]=='b':
#         i+=1
#         continue
#     s[i] +=" "+s1[i]
#
# print(s)
#
# s = [1,3,2,4,5,6,8,0,1,2,4,5,6]
#
# for i in range(len(s),0,-1):
#     if s[i]-s[i-1]==1:
#         print(i)
#         # s[i]=[s[i-1],s[i]]
#         # s.pop(i - 1)
#
#
#
#
#
# print(s)

#
# s = ['a','g',1,2,3]
# s = map(str,s)
# print(s)
# s1 = " ".join(s)
# print(s1)



# #Тест WAY
# from core import way
#
# x = "/home/pablo/Mlearn/PT/file.txt"
# print(way(x))

# from tkinter import *
# from PIL import Image, ImageTk
# root = Tk()
# root.geometry('1000x1000')
# canvas = Canvas(root,width=999,height=999)
# canvas.pack()
# pilImage = Image.open("001")
# image = ImageTk.PhotoImage(pilImage)
# imagesprite = canvas.create_image(700,400,image=image)
# root.mainloop()


# a = [1,9,3,4,5,6,7,8,9,0,10]
# map(lambda x: if x<5: x=[], a)
# print(a)

# a = [1,2,3,4,5]
# b = a[:]
# b.reverse()
# print(a)
# print(b)



# from tkinter import *
# from tkinter import messagebox
# from tkinter import ttk
# import sys
# root= Tk()
# root.title("Чат - бот")
# root.geometry("500x600")
#
# def chat():
#     name = ttk.Label(root,text = "Пообщайся с ботом)")
#     name.grid(column = 50)
#     chatx = Entry(root,width = 40)
#     chatx.grid(row = 40,column=10,columnspan = 70)
#     ot = ttk.Button(root,text = "Отправить",width = 10,command=lambda: otvet())
#     ot.grid(row = 40,column=90,columnspan = 70,)
#     label = Label(root, text=(""))
#     label.grid(columnspan=700)
#     def otvet():
#
#         phrase_dict={
#             "привет":"Siri: Привет",
#             "ты джеймс!":"Siri: ты угадал",
#             "выйди за меня":"Siri: прости,но у меня есть масса других потенциальных женихов",
#             "ты красивая?":"Siri: Эм",
#             "ты голодная?":"Siri: Нет,я не сильно то люблю есть...",
#             "что делаешь?":"Siri: рисую процессор на системном блоке",
#             "как дела?": "Siri: супер"
#         }
#
#
#         if phrase_dict.get(chatx.get().lower())!=None:
#             label["text"]=phrase_dict[chatx.get().lower()]
#         else: label["text"]= "Siri: мой словарный запас мал..."
#
#
# chat()
#
#
# root.mainloop()
#
# a = [1,2,3,4,5]
# i = 1
# while True:
#     if i in a:
#         pass
#     else:
#         a.append(i)