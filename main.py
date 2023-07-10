'''
# 1.设置壁纸
# 2.设置字体
# 3.更改路径
# 4.更改默认路径
# 5.搜索
#6.id下载
7.链接提取
# 8.批量下载
'''
import os
import re
import sys
import pygame
import requests
from tkinter import *
from tkinter import filedialog
from tqdm import tqdm
# 下载
def get(id,path):
    lyrics_url = f'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={id}&httpsStatus=1&reqId=b69780a0-9d9a-11ed-bcbc-899372fa07c7'
    lrclist = requests.get(url=lyrics_url).json()['data']['lrclist']
    lycics = ''
    for i in tqdm(lrclist):
        lycic = i['lineLyric']
        time = float(i['time'])
        S = time % 60
        M = int((time - S) / 60)
        if len(str(M)) == 1:
            M = f"0{str(M)}"
        else:
            M = str(M)
        Sint = str(int(S - (S % 1)))
        Ssmall = S % 1
        if len(Sint) == 1:
            Sint = '0' + Sint
        if len(str(S % 1)) - 2 > 3:
            Ssmall = round(Ssmall,3)
        if len(str(Ssmall).replace('.','')) < 3:
            Ssmall = str(Ssmall) + '0' * (3 - len(str(Ssmall).replace('.','')))
        S = f'{Sint}.{str(Ssmall).replace(".","")}'
        lycics += f'[{M}:{S}]{lycic}\n'
    download_url_text_url = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={id}&type=true&httpsStatus=1&reqId=56a671c1-9cd1-11ed-a6e0-1330c847175f'
    download_url = requests.get(url=download_url_text_url).json()['data']['url']
    music = requests.get(url=download_url).content
    url = f'http://www.kuwo.cn/play_detail/{id}'
    urlText = requests.get(url=url).text
    nameAndSinger = re.findall('<title>(.*?)_单曲在线试听_酷我音乐',urlText)[0]
    name = re.findall('(.*?)_(.*?)',nameAndSinger)[0][0]
    singer = re.findall(f'{name}_(.*?)1',f'{nameAndSinger}1')[0]
    try:
        os.mkdir(path + singer)
    except:
        pass
    open(f'{path}{singer}/{singer}-{name}.mp3','wb').write(music)
    open(f'{path}{singer}/{singer}-{name}.lrc', 'w',encoding='utf-8').write(lycics)
    print(name + "下载好了")
# id下载
def idDownloadPage():
    idDownloadScreen = Tk()
    idDownloadScreen.iconbitmap('imge\\icon.ico')
    idDownloadScreen.title('id下载')
    wallpaperPath = open('text\\searchWallpaperPath.txt', 'r').read()
    wallpaperSize = pygame.image.load(wallpaperPath).get_size()
    idDownloadScreen.geometry(f'{wallpaperSize[0]}x{wallpaperSize[1]}')
    idDownloadScreen.resizable(width=False, height=False)
    wallpaper = PhotoImage(file=wallpaperPath)
    w = Label(idDownloadScreen, image=wallpaper)
    w.place(x=0,y=0)
    musicId = Entry(idDownloadScreen)
    musicId.place(x=100,y=0,height=25)
    Button(idDownloadScreen,text='下载',command=lambda: get(id=musicId.get(),path=defaultPath)).place(x=250,y=0)
    mainloop()
# 搜索显示函数
def search():
    def nextPage(page,searchText):
        searchDisplay(searchText=searchText,page=page+1)
    def previousPage(page,searchText):
        searchDisplay(searchText=searchText,page=page-1)
    def batchDownloadsPage(rids):
        def batchDownloads(rids,start,end):
            for i in tqdm(range(start,end + 1)):
                get(id=rids[i - 1],path=defaultPath)
        batchDownloadsScreen = Tk()
        batchDownloadsScreen.iconbitmap('imge\\icon.ico')
        Label(batchDownloadsScreen,text='开始编号：').place(x=0,y=0)
        Label(batchDownloadsScreen, text='结束编号：').place(x=0,y=20)
        start = Entry(batchDownloadsScreen)
        start.place(x=50,y=0)
        end = Entry(batchDownloadsScreen)
        end.place(x=50,y=20)
        Button(batchDownloadsScreen,text='确定',command=lambda: batchDownloads(rids=rids,end=int(end.get()),start=int(start.get()))).place(x=0,y=40)
        mainloop()
    def searchDisplay(searchText,page):
        cookies = {
            'kw_token': '5YEU1UR8LHR',
            'Hm_lvt_cdb524f42f0ce19b169a8071123a4797': '1688298485,1688614796,1688788632',
            'Hm_lpvt_cdb524f42f0ce19b169a8071123a4797': '1688788662',
            'Hm_token': '4DrzfX7fkT8AwSG6xs37CyHDcfMSnm8c',
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            # 'Cookie': 'kw_token=5YEU1UR8LHR; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1688298485,1688614796,1688788632; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1688788662; Hm_token=4DrzfX7fkT8AwSG6xs37CyHDcfMSnm8c',
            'Cross': 'e8161f82841dfb629ee35624e4f0a35b',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
        }

        params = {
            'key': searchText,
            'pn': page,
            'rn': '30',
            'httpsStatus': '1',
            'reqId': 'aac2c6d0-1d43-11ee-b8a8-e7c44fd78752',
            'plat': 'web_www',
            'from': '',
        }

        listData = requests.get(
            'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord',
            params=params,
            cookies=cookies,
            headers=headers,
            verify=False,
        ).json()['data']
        total = listData['total']
        listData = listData['list']
        listb = Listbox(searchScreen,height=31,width=50)
        listb.place(x=100,y=50)
        rids = []
        totalPage = ((int(total) - (int(total) % 30)) / 30) + 1
        listb.insert(0,f'共有{total}首,共有{totalPage}页.')
        j = 1
        for i in listData:
            rids.append(i['rid'])
            listb.insert(j,f'编号：{j} | 名字：{i["name"]} | 歌手：{i["artist"]} | 时长：{i["songTimeMinutes"]}')
            j += 1
        Label(searchScreen,text='输入编号:').place(x=100,y=625)
        num = Entry(searchScreen)
        num.place(x=160,y=625)
        Button(searchScreen, text='批量下载', command=lambda: batchDownloadsPage(rids=rids)).place(y=625,x=350)
        Button(searchScreen,text='下一页',command=lambda: nextPage(page=page,searchText=searchText)).place(y=0,x=350)
        Button(searchScreen, text='上一页', command=lambda: previousPage(page=page, searchText=searchText)).place(y=0,x=290)
        Button(searchScreen,text='下载',command=lambda: get(id=rids[int(num.get()) - 1],path=defaultPath)).place(x=310,y=625)
    searchScreen = Tk()
    searchScreen.iconbitmap('imge\\icon.ico')
    searchScreen.title('搜索下载')
    wallpaperPath = open('text\\searchWallpaperPath.txt', 'r').read()
    wallpaperSize = pygame.image.load(wallpaperPath).get_size()
    searchScreen.geometry(f'{wallpaperSize[0]}x{wallpaperSize[1]}')
    searchScreen.resizable(width=False, height=False)
    wallpaper = PhotoImage(file=wallpaperPath)
    w = Label(searchScreen, image=wallpaper)
    w.place(x=0,y=0)
    searchText = Entry(searchScreen)
    searchText.place(x=100,y=0,height=25)
    Button(searchScreen,text='搜索',command=lambda:searchDisplay(page=1,searchText=searchText.get())).place(x=250,y=0)
    mainloop()
# 设置下载页的壁纸
def setSearchWallpaper():
    newWallpaper = filedialog.askopenfilename(title='设置下载页的壁纸',filetypes=[('图片文件','.gif')])
    if newWallpaper != '':
        open('text\\searchWallpaperPath.txt','w').write(newWallpaper)
#提取链接
def extractTheLink():
    def urlPrint(rid):
        url1 = f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid.get()}&type=true&httpsStatus=1&reqId=56a671c1-9cd1-11ed-a6e0-1330c847175f'
        url = requests.get(url=url1).json()['data']['url']
        print(url)
    searchScreen = Tk()
    searchScreen.iconbitmap('imge\\icon.ico')
    searchScreen.title('提取链接')
    wallpaperPath = open('text\\searchWallpaperPath.txt', 'r').read()
    wallpaperSize = pygame.image.load(wallpaperPath).get_size()
    searchScreen.geometry(f'{wallpaperSize[0]}x{wallpaperSize[1]}')
    searchScreen.resizable(width=False, height=False)
    wallpaper = PhotoImage(file=wallpaperPath)
    w = Label(searchScreen, image=wallpaper)
    w.place(x=0, y=0)
    rid = Entry(searchScreen)
    rid.place(x=0,y=0)
    Button(searchScreen,text='确定',command=lambda :urlPrint(rid)).place(x=150,y=0)
    mainloop()
# 设置路径
def setPath():
    newPath = filedialog.askdirectory(title='设置下载文件夹')
    global defaultPath
    defaultPath = f'{newPath}/'
# 设置默认路径
def setDefaultPath():
    newDefaultPath = f'{filedialog.askdirectory(title="设置默认下载文件夹")}/'
    if newDefaultPath != '/':
        open('text\\defaultPath.txt','w').write(newDefaultPath)
# 设置壁纸函数
def setWallpaper():
    newWallpaperPath = filedialog.askopenfilename(title='设置壁纸',filetypes=[("照片文件",".jpg"),("照片文件",".jpeg"),("照片文件",".png")])
    if newWallpaperPath != '':
        open('text/wallpaperPath.txt', 'w').write(newWallpaperPath)
        pygame.init()
        homePage()
# 设置字体函数
def setFont():
    newFontPath = filedialog.askopenfilename(title='设置字体',filetypes=[("字体文件",".ttc"),("字体文件",".ttf")])
    if newFontPath != '':
        open('text\\fontPath.txt','w').write(newFontPath)
        pygame.init()
        homePage()
# 按钮函数
def setButton(x,y,height,width,runEvent,event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] in range(x,x + width + 1) and mousePos[1] in range(y,y + height + 1):
            runEvent()
# 主页函数
def homePage():
    white = 255, 255, 255
    # 初始化
    pygame.init()
    # 壁纸加载
    wallpaperPath = open('text/wallpaperPath.txt', 'r').read()
    wallpaper = pygame.image.load(wallpaperPath)
    wallpaperWidth = wallpaper.get_width()
    wallpaperHeight = wallpaper.get_height()
    # 字体加载
    fontPath = open('text\\fontPath.txt', 'r').read()
    size60Font = pygame.font.Font(fontPath, 60)
    size40Font = pygame.font.Font(fontPath, 40)
    size20Font = pygame.font.Font(fontPath, 20)
    size30Font = pygame.font.Font(fontPath, 30)
    # 字体设置
    setExtractTheLinkText = size40Font.render('链接提取', True, white)
    setSearchWallpaperText = size40Font.render('设置下载页的壁纸', True, white)
    setWallpaperText = size40Font.render('设置壁纸', True, white)
    setFontText = size40Font.render('设置字体', True, white)
    setDefaultPathText = size40Font.render('设置默认下载路径', True, white)
    setPathText = size40Font.render('设置暂时下载路径', True, white)
    setSearchAndDownloadText = size40Font.render('搜索并下载音乐', True, white)
    setIdDownloadText = size40Font.render('id下载音乐', True, white)
    # 创建屏幕
    icon = pygame.image.load('imge\\icon.ico')
    pygame.display.set_icon(icon)
    home_screen = pygame.display.set_mode((wallpaperWidth, wallpaperHeight))
    pygame.display.set_caption('主页')
    # 显示
    home_screen.blit(wallpaper, (0, 0))
    home_screen.blit(setWallpaperText,(200,100))
    home_screen.blit(setFontText, (200, 140))
    home_screen.blit(setDefaultPathText, (200, 180))
    home_screen.blit(setSearchAndDownloadText, (200, 220))
    home_screen.blit(setPathText, (200, 260))
    home_screen.blit(setSearchWallpaperText, (200, 300))
    home_screen.blit(setIdDownloadText, (200, 340))
    home_screen.blit(setExtractTheLinkText,(200, 380))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            # 按钮制作
            setButton(x=200,y=100,event=event,runEvent=setWallpaper,width=160,height=40)
            setButton(x=200, y=140, event=event, runEvent=setFont, width=160, height=40)
            setButton(x=200, y=180, event=event, runEvent=setDefaultPath, width=320, height=40)
            setButton(x=200, y=220, event=event, runEvent=lambda: search(), width=280, height=40)
            setButton(x=200,y=260,event=event,runEvent=setPath,width=320,height=40)
            setButton(x=200, y=300, event=event, runEvent=setSearchWallpaper, width=320, height=40)
            setButton(x=200, y=340, event=event, runEvent=idDownloadPage, width=200, height=40)
            setButton(x=200, y=380, event=event, runEvent=extractTheLink, width=160, height=40)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
# 程序入口
if __name__ == "__main__":
    # 默认路径加载
    defaultPath = open('text\\defaultPath.txt','r').read()
    # 主页
    homePage()