# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.path as mpath
import numpy as np
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.util as cutil
from datetime import datetime

file = r'D:\気象データ\HGT\anl_p_hgt.2020.bin'

with open(file, mode='br') as f:
    data = np.fromfile(f, dtype='>f').reshape(366,37,145,288)[:,:,::-1]

# print(data[200,30])

# 定数定義
year=2020 
month=9
day=20
start_day = datetime(year, 1, 1)
today = datetime(year, month, day)
day_num = (today-start_day).days + 1
prsLev=10

pcord=np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
    650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
    50,30,20,10,7,5,3,2,1])

# print(pcord)
prs_num = np.where(pcord==prsLev)[0][0]

data_2d = data[day_num, prs_num]


xcord = np.arange(0, 358.751, 1.25)
ycord = np.arange(-90, 90.1, 1.25)
X,Y=np.meshgrid(xcord,ycord)

# 領域作成
fig=plt.figure(figsize=(8,8))
ax=fig.add_subplot(1,1,1)

# 投影図作成
# ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=0)) #北半球ポーラー
ax = plt.axes(projection=ccrs.SouthPolarStereo(central_longitude=315)) #南半球ポーラー
ax.set_extent([-180,180,-90,-30], ccrs.PlateCarree())
# ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=180))
# ax.set_extent([0,359.99,30,90], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND,fc='lightgreen')
# print(data_kinds[move_mean_count])
# ax.set_title(f'{year}/{month}/{day}',fontsize=20)
ax.coastlines(lw=0.4)
gl=ax.gridlines(linestyle='-', color='gray')

# グリッド調整
gl.xlocator = mticker.FixedLocator([-180,-135,-90, -45, 0, 45,90,135, 180])

# 等値線
# cont=plt.contour(X, Y, data_2d,locator=mticker.MultipleLocator(250), transform=ccrs.PlateCarree(),colors=
# cont=plt.contour(X, Y, data_2d, transform=ccrs.PlateCarree(),colors=['black'])
# cont.clabel(fmt='%1.0f', fontsize=10)


# 図の周囲を円形に切る
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# 陰影描写
cyclic_data, cyclic_xcord = cutil.add_cyclic_point(data_2d, coord=xcord)
# CF = ax.contourf(cyclic_xcord,ycord,cyclic_data, transform=ccrs.PlateCarree(),

                # clip_path=(circle, ax.transAxes) ) # clip_pathを指定して円形にする

# plt.colorbar(CF, orientation="horizontal")




# 方位書き込
# plt.text(-1, 37, "0", fontsize=20, color='k', transform=ccrs.PlateCarree())
# plt.text(185, 39, "180", fontsize=20, color='k', transform=ccrs.PlateCarree())
# plt.text(88, 39, "90E", fontsize=20, color='k', transform=ccrs.PlateCarree())
# plt.text(-88, 31, "90W", fontsize=20, color='k', transform=ccrs.PlateCarree())

title = f'GPH{prsLev}hPa'
date = f'{year}/{month}/{day}'

# タイトルを付ける
fig.suptitle( title, fontsize=20)
ax.set_title( date,fontsize=20)

# プロット範囲の調整
# plt.subplots_adjust(hspace=0.8,bottom=0.2)
cont=plt.contour(X, Y, data_2d,locator=mticker.MultipleLocator(400), 
            transform=ccrs.PlateCarree(),colors=['black'])
cont.clabel(fmt='%1.0f', fontsize=10)


# ファイルへの書き出し

month = str(month).zfill(2)
day = str(day).zfill(2)

plt.savefig( f'GPH{prsLev}hPa_{year}{month}{day}.png' , bbox_inches='tight')
plt.show()
plt.close()