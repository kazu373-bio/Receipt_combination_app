# -*- coding: utf-8 -*-
"""mnist

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W_Z7tks_n2FFIA3hbgWF01VFzOu3B-Zi
"""

import os
from flask import Flask, request, redirect, render_template, flash, send_from_directory
import pandas as pd
from mip import Model, xsum, maximize, BINARY
from itertools import count

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    df_answer = pd.DataFrame(columns=["Total","Each","number"])
    
    
    
    if request.method == 'POST':
        w = request.form["w"]
        W = request.form["W"]
        A = request.form["A"]
        
        A = int(A)
        W = int(W)
        w = w.split()
        w = [int(n) for n in w]
        print("入力レシートの合計:{}".format(sum(w)))
        v = [(int(n)/(len(w)-1))**5 for n in range(len(w))]
        v.reverse()
        
        r=range(len(w))
        for num in count():
            if A>=0:
                m=Model("knapsack")
                m.infeas_tol=10**-11 #MIPの最低演算桁を下げる
                x=[m.add_var(var_type=BINARY) for i in r]
                m.objective=maximize(xsum(v[i]*x[i] for i in r))
                m+=xsum(w[i]*x[i] for i in r)>=W
                m+=xsum(w[i]*x[i] for i in r)<=W+A
                m.optimize()
            else:
                break
            if None!=x[0].x:
                selected=[i for i in r if x[i].x>=0.99]
                result1=sum([w[i] for i in selected])
                result2=[w[i] for i in selected]
                result3=[w.index(w[i]) for i in selected]
                result4=sum([v[i] for i in selected])
                
                df_answer = df_answer.append({"Total":result1,"Each":result2,"number":result3},ignore_index=True)
                
                
            else:
                break
            A=result1-W-1

        print("解答数:{}".format(num))
        if num==0:
            ans="妥協金額を増やしてください。\nまたは、入力レシートの合計が目標金額以下の可能性があります。"
            return render_template("index.html",answer=ans)
        
        header = df_answer.columns
        record = df_answer.values.tolist()


        return render_template("index.html",header = header,record=record)
#,webbrowser.open(os.path.dirname(os.path.abspath(__file__))+"./templates/answer.html")
    
    return render_template("index.html",answer="")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)