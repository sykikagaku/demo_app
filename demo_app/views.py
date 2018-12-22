from django.shortcuts import render, redirect # 追加
from .forms import InputForm
from .models import Customers # 追加
from sklearn.externals import joblib
import numpy as np
from django.contrib.auth.decorators import login_required # 追加
from .forms import InputForm, SignUpForm # 追加
from django.contrib.auth import login, authenticate # 追加
import pandas as pd
import json


# モデルの読み込み 関数の前に置いておくこと　毎回読み込むと結構処理量が多い
#loaded_model = joblib.load('demo_app/demo_model.pkl')
loaded_model = joblib.load('/home/sykikagaku/sykikagaku.pythonanywhere.com/demo_app/demo_model.pkl')

@login_required # 追加
def index(request):
    return render(request,'demo_app/index.html',{})

def input_form(request):
    if request.method == "POST":
        form = InputForm(request.POST) # 入力データの取得
        if form.is_valid():
            form.save() # 入力を保存
            return redirect('result')

    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html', {'form':form})

def result(request):

    _data = Customers.objects.order_by('id').reverse().values_list('limit_balance', 'sex', 'education', 'marriage', 'age', 'pay_0', 'pay_2', 'pay_3', 'pay_4', 'pay_5', 'pay_6', 'bill_amt_1', 'pay_amt_1', 'pay_amt_2', 'pay_amt_3', 'pay_amt_4', 'pay_amt_5', 'pay_amt_6')
    x = np.array([_data[0]]) # データをNumpy形式に変換
    y = loaded_model.predict(x) # クラスの推論
    y_proba = loaded_model.predict_proba(x) # クラスの確率を推論
    _y_proba =y_proba *100

    # 結果に基づいてコメントを返す
    if y[0] == 0:
        if y_proba[0][y[0]] > 0.75:
            comment = 'この方への貸し出しは危険です'
        else:
            comment = 'この方への貸し出しは要検討です'
    else:
        if y_proba[0][y[0]] > 0.75:
            comment = 'この方への貸し出しは全く問題ありません'
        else:
            comment = 'この方への貸し出しは問題ないでしょう'

    customer = Customers.objects.order_by('id').reverse()[0] # Customerの切り出し
    customer.proba = _y_proba[0][y[0]]
    customer.result = y[0]
    customer.comment = comment
    customer.save() # データを保存

    return render(request, 'demo_app/result.html', {'y':y[0], 'y_proba':round(_y_proba[0][y[0]], 2), 'comment':comment})

def history(request):
    if request.method == 'POST': # POSTメソッドが送信された場合
        d_id = request.POST # POSTされた値を取得→顧客ID
        d_customer = Customers.objects.filter(id=d_id['d_id']) # filterメソッドでidが一致するCustomerを取得
        d_customer.delete() # 顧客データを消去
        customers = Customers.objects.all() # 顧客全データを取得
        return render(request, 'demo_app/history.html', {'customers':customers})

    else:
        customers = Customers.objects.all()
        return render(request, 'demo_app/history.html', {'customers':customers})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
        return render(request, 'demo_app/signup.html', {'form': form})

def info(request):
    return render(request,'demo_app/info.html',{})


def info(request):
    # DBからデータの読み込み
    customers = Customers.objects.values_list(\
    'sex', 'education', 'marriage', 'age', 'result', 'proba')

    # データをDataFarame型に変換
    lis, cols = [], ['sex', 'education', 'marriage', 'age', 'result', 'proba']
    for customer in customers:
        lis.append(customer)
    df = pd.DataFrame(lis, columns=cols)

    # データの整形
    df['sex'].replace({1:"男性", 2:"女性"}, inplace=True)
    df['education'].replace({1:'graduate_school', 2:'university', 3:'high school', 4:'other'}, inplace=True)
    df['marriage'].replace({1:'married', 2:'single', 3:'others'}, inplace=True)
    df['result'].replace({0:'審査落ち', 1:'審査通過', 2:'その他'}, inplace=True)
    df['age'] = pd.cut(df['age'], [0,10,20,30,40,50,60,100], labels=['10代', '20代','30代','40代','50代','60代','70代以上'])
    df['proba'] = pd.cut(df['proba'], [0,75,100], labels=['要審査', '信頼度高'])

    # データのユニークな値とその数の取得
    dic_val, dic_index = {}, {}
    for col in cols:
        _val = df[col].value_counts().tolist()
        _index = df[col].value_counts().index.tolist()
        dic_val[col] = _val
        dic_index[col] = _index

    # データをJson形式に変換 Javaの場合、文字がきちんと変換できない
    val, index = json.dumps(dic_val), json.dumps(dic_index)

    return render(request, 'demo_app/info.html', {'index':index, 'val':val})

@login_required # 追加
def info(request):
    customers = Customers.objects.values_list(\
,
,
