import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import json

from pandas import pivot


class 数据处理():

    def __init__(self,文件=r'C:\Users\wei\PyCharmMiscProject\zhangben.csv'):
        self.文件=文件
        try:
            if 文件.endswith('.csv'):
                self.df = pd.read_csv(文件)
            elif 文件.endswith('.json'):
                self.df = pd.read_json(文件)
            else:
                print('不支持的文件')
        except FileNotFoundError:
            print('找不到文件')
            self.df = pd.DataFrame()
        except Exception as e:
            print(e)

    def 保存(self,输出文件=None):
        输出文件=输出文件 or self.文件
        self.df.to_csv(输出文件,index=False,encoding='utf-8-sig')

    def 总收入(self):
        x=sum(self.df.loc[self.df['类型'] == '收入', '金额'])
        print(self.df.loc[self.df['类型'] == '收入'])
        print('总收入',x)

    def 总支出(self):
        x=sum(self.df.loc[self.df['类型']=='支出','金额'])
        print(self.df.loc[self.df['类型']=='支出'])
        print('总支出',x)

    def 备注统计(self):
        self.df.groupby('备注')['金额'].sum()
        self.df.groupby('类型')['金额'].agg(['sum', 'mean', 'max', 'count'])
        print(self.df.groupby('备注').agg(总金额=('金额','sum'),
                                     最大金额=('金额','max'),
                                     最小金额=('金额','min'),
                                     出现次数=('备注','count')))

    def 月份统计(self):
        x=self.df.copy()
        x['日期'] = self.df['日期'].astype(str)
        x['日期']=self.df['日期'].str[:6]
        shou=x.loc[x['类型']=='收入']
        zhi=x.loc[x['类型']=='支出']
        print(shou.groupby('日期').agg(月收入总金额=('金额','sum')))
        print(zhi.groupby('日期').agg(月支出总金额=('金额','sum')))

    def 日期统计(self):
        self.df['日期'] = self.df['日期'].astype(str)
        shou=self.df.loc[self.df['类型']=='收入']
        zhi=self.df.loc[self.df['类型']=='支出']
        print(shou.groupby('日期').agg(总金额=('金额','sum'),
                                     最大金额=('金额','max'),
                                     最小金额=('金额','min'),
                                     出现次数=('备注','count')))
        print(zhi.groupby('日期').agg(总金额=('金额','sum'),
                                     最大金额=('金额','max'),
                                     最小金额=('金额','min'),
                                     出现次数=('备注','count')))

    def 日期查询(self,日期):
        self.df['日期'] = self.df['日期'].astype(str)
        try:
            datetime.strptime(日期,'%Y%m%d')
            x=self.df.loc[self.df['日期']==日期]
            if x.empty:
                print('无记录')
                return
            else:
                print(x)
        except ValueError:
            print('输入正确日期')

    def 修改内容(self,hang,gai,xiu):
        try:
            hang = int(hang)
            self.df.loc[hang, gai]
            self.df['日期'] = self.df['日期'].astype(str)
            if gai=='日期':
                try:
                    datetime.strptime(xiu,'%Y%m%d')
                except ValueError:
                    print('输入正确日期')
                    return
            elif gai=='金额':
                try:
                    xiu=int(xiu)
                except ValueError:
                    print('输入数字')
                    return
            self.df.loc[hang,gai]=xiu
            self.保存()
        except ValueError:
            print('输入正确编号')
            return
        except (IndexError,KeyError):
            print('输入正确范围的编号或者文字')
            return
        print('修改成功')
        print(self.df)
class image():
    def __init__(self,文件=r'C:\Users\wei\PyCharmMiscProject\zhangben.csv'):
        self.文件 = 文件
        try:
            if 文件.endswith('.csv'):
                self.df = pd.read_csv(文件)
            elif 文件.endswith('.json'):
                self.df = pd.read_json(文件)
            else:
                print('不支持的文件')
        except FileNotFoundError:
            print('找不到文件')
            self.df = pd.DataFrame()
        except Exception as e:
            print(e)

    def bar_chart(self):
        income=self.df.loc[self.df['类型']=='收入']
        income=income.groupby('备注')['金额'].sum()
        spending=self.df.loc[self.df['类型']=='支出']
        spending=spending.groupby('备注')['金额'].sum()
        fig, ax = plt.subplots(1,2)
        x=income.index
        y=income.values
        x1=spending.index
        y1=spending.values
        plt.rcParams["font.sans-serif"] = [
            "Microsoft YaHei"]
        plt.rcParams["axes.unicode_minus"] = False
        ax[0].bar(x,y,alpha=0.8)
        ax[0].set_title('各备注收入汇总')
        ax[0].set_xlabel('备注')
        ax[0].set_ylabel('金额')
        ax[1].bar(x1,y1,alpha=0.8)
        ax[1].set_title('各备注支出汇总')
        ax[1].set_xlabel('备注')
        ax[1].set_ylabel('金额')
        fig.savefig("备注.png", dpi=300, bbox_inches="tight")
        plt.show()

    def Line_chart(self):
        shou=self.df.loc[self.df['类型']=='收入'].groupby('日期')['金额'].sum()
        zhi=self.df.loc[self.df['类型']=='支出'].groupby('日期')['金额'].sum()
        net_income=shou.sub(zhi,fill_value=0)
        plt.rcParams["font.sans-serif"] = [
            "Microsoft YaHei"]
        plt.rcParams["axes.unicode_minus"] = False
        plt.plot(net_income.index,net_income)
        plt.xticks(net_income.index)
        plt.xlabel('日期')
        plt.title('月金额变化')
        plt.ylabel('金额')
        plt.savefig("月折线图.png", dpi=300, bbox_inches="tight")
        plt.show()

    def 用pandas画图试试(self):
        plt.rcParams["font.sans-serif"] = [
            "Microsoft YaHei"]
        plt.rcParams["axes.unicode_minus"] = False
        pi=self.df.groupby(['备注','类型'])['金额'].sum().unstack('类型')
        pi.plot(kind='bar',title='备注分析')
        plt.tight_layout()
        plt.savefig("备注汇总.png", dpi=300, bbox_inches="tight")
        plt.show()


if __name__ == '__main__':
    cl = 数据处理()
    im = image()
    while True:
        xuan = input('按数字选择功能')
        xuan = xuan.replace(' ', '').strip()
        try:
            xuan = int(xuan)
            if 1 > xuan or xuan > 9:
                print('无该功能')
                continue
        except ValueError:
            print('输入数字')
            continue
        if xuan == 1:
            hang=input('输入行编号')
            gai=input('输入需要修改的内容\n类型 金额 备注 日期')
            if gai=='类型':
                xx=input('输入编号，1改为收入，2改为支出')
                if xx=='1':
                    xiu='收入'
                elif xx=='2':
                    xiu='支出'
            else:
                xiu = input('更改的数据')
            cl.修改内容(hang, gai, xiu)
            continue
        if xuan == 2:
            cl.总收入()
            cl.总支出()
            continue
        if xuan == 3:
            cl.备注统计()
            continue
        if xuan == 4:
            cl.日期统计()
            continue
        if xuan == 5:
            cl.月份统计()
            continue
        if xuan == 6:
            日期=input('输入日期，格式20260909')
            cl.日期查询(日期)
            continue
        if xuan == 7:
            im.用pandas画图试试()
            im.Line_chart()
            im.bar_chart()
            break
