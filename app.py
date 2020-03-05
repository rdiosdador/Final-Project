from __future__ import division
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine
import pandas as pd
import pandas as pd
from datetime import datetime, timedelta,date
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import plotly.plotly as py
import plotly.offline as pyoff
import plotly.graph_objs as go
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam 
from keras.callbacks import EarlyStopping
from keras.utils import np_utils
from keras.layers import LSTM
from sklearn.model_selection import KFold, cross_val_score, train_test_split

connection_string="postgresql://postgres:12345@localhost:5432/Toscalia"
engine = create_engine(connection_string)

def itera(array_entrada,array_salida):
    for r in array_entrada:
        array_salida.append(r)

app=Flask(__name__)

@app.route("/")
def home():
    
    return render_template("index.html") 

@app.route("/costos")
def costos():

    return render_template("costos.html") 


@app.route("/API", methods=["POST"])
def echo():
    costos_precios=engine.execute("SELECT * FROM costos_precios WHERE costo_porcentaje IS NOT NULL AND costo_porcentaje !=0 ORDER BY costo_porcentaje DESC")
    venta_total=engine.execute("SELECT SUM(importe_con_iva) FROM enero_2020")
    venta_grupos=engine.execute("SELECT grupo, SUM(precio) AS total_ventas FROM costos_precios GROUP BY grupo ORDER BY total_ventas DESC")
    promedio_costos_base=engine.execute("SELECT grupo, AVG(costo_porcentaje) AS total_costos FROM costos_precios GROUP BY grupo HAVING AVG(costo_porcentaje)>0 ORDER BY total_costos DESC")
    ventas_empleado=engine.execute("SELECT nombre,venta_neta FROM venta_empleado")
    clientes_empleado=engine.execute("SELECT nombre,clientes FROM venta_empleado")
    propinas_empleado=engine.execute("SELECT nombre,propina FROM venta_empleado")
    promedio_utilidad=engine.execute("SELECT grupo, AVG(utilidad) AS promedio FROM costos_precios GROUP BY grupo ORDER BY promedio DESC")
    consumo_promedio=engine.execute("SELECT nombre, consumo_promedio FROM venta_empleado WHERE nombre!='DOMICILIO'")
   
    promedio_consumo=[]
    utilidad_promedio=[]
    propinas=[]
    clientes_por_empleado=[]
    venta_por_empleado=[]
    promedio_costo=[]
    costo_precio=[]
    venta_acumulada=[]
    venta_grupos_total=[]

    itera(costos_precios,costo_precio)
    itera(venta_total,venta_acumulada)
    itera(venta_grupos,venta_grupos_total)
    itera(promedio_costos_base,promedio_costo)
    itera(ventas_empleado,venta_por_empleado)
    itera(clientes_empleado,clientes_por_empleado)
    itera(propinas_empleado,propinas)
    itera(promedio_utilidad,utilidad_promedio)
    itera(promedio_utilidad,utilidad_promedio)
    itera(consumo_promedio,promedio_consumo)


    costo_precio_df=pd.DataFrame(costo_precio, columns=["clave","descripcion","costo","precio","utilidad","costo_porcentaje","grupo"])
    costo_precio_dict=costo_precio_df.to_dict(orient='list')
    venta_acumulada_df=pd.DataFrame(venta_acumulada)
    venta_acumulada_dict=venta_acumulada_df.to_dict()
    venta_grupos_df=pd.DataFrame(venta_grupos_total, columns=["grupo","total_ventas"])
    venta_grupos_dict=venta_grupos_df.to_dict()
    promedio_costo_df=pd.DataFrame(promedio_costo, columns=["grupo","costo_promedio"])
    promedio_costo_dict=promedio_costo_df.to_dict(orient='records')
    venta_por_empleado_df=pd.DataFrame(venta_por_empleado, columns=["nombre","venta"])
    venta_por_empleado_dict=venta_por_empleado_df.to_dict(orient='list')
    clientes_por_empleado_df=pd.DataFrame(clientes_por_empleado, columns=["nombre","clientes"])
    clientes_por_empleado_dict=clientes_por_empleado_df.to_dict(orient='list')
    propinas_df=pd.DataFrame(propinas,columns=["nombre","propina"])
    propinas_dict=propinas_df.to_dict(orient='list')
    utilidad_promedio_df=pd.DataFrame(utilidad_promedio, columns=["grupo","utilidad_promedio"])
    utilidad_promedio_dict=utilidad_promedio_df.to_dict(orient='list')
    promedio_consumo_df=pd.DataFrame(promedio_consumo, columns=["nombre","consumo"])
    promedio_consumo_dict=promedio_consumo_df.to_dict(orient='list')

    return  jsonify({
        "costo_precio":costo_precio_dict,
        "venta_acumulada":venta_acumulada_dict,
        "venta_grupos":venta_grupos_dict,
        "promedio_costo":promedio_costo_dict,
        "venta_empleado":venta_por_empleado_dict,
        "clientes_empleado":clientes_por_empleado_dict,
        "propinas":propinas_dict,
        "utilidad":utilidad_promedio_dict,
        "consumo_promedio":promedio_consumo_dict

        })

@app.route("/API-INDEX", methods=["POST"])
def index():
    
    ventas_empleado=engine.execute("SELECT nombre,venta_neta FROM venta_empleado")
    grupos=engine.execute("SELECT grupo, SUM(cantidad) FROM enero_2020 GROUP BY grupo ORDER BY sum DESC")
    venta_total=engine.execute("SELECT SUM(importe_con_iva) FROM enero_2020")
    clientes_empleado=engine.execute("SELECT nombre,clientes FROM venta_empleado")
    platillo_max=engine.execute("SELECT platillo,cantidad FROM enero_2020 WHERE unidad ='ORDEN' AND platillo !='ANTIPASTI DE LA CASA' AND platillo !='SEGUNDO TIEMPO' ORDER BY cantidad DESC")
     
    venta_acumulada=[]
    clientes_por_empleado=[]
    grupos_venta=[]
    venta_por_empleado=[]
    max_platillo=[]
 
    itera(grupos,grupos_venta)
    itera(venta_total,venta_acumulada)
    itera(clientes_empleado,clientes_por_empleado)
    itera(ventas_empleado,venta_por_empleado)
    itera(platillo_max,max_platillo)

    venta_acumulada_df=pd.DataFrame(venta_acumulada)
    venta_acumulada_dict=venta_acumulada_df.to_dict()
    clientes_por_empleado_df=pd.DataFrame(clientes_por_empleado, columns=["nombre","clientes"])
    clientes_por_empleado_dict=clientes_por_empleado_df.to_dict(orient='list')
    grupos_venta_df=pd.DataFrame(grupos_venta, columns=["grupo","venta"])
    grupos_venta_dict=grupos_venta_df.to_dict(orient='list')
    venta_por_empleado_df=pd.DataFrame(venta_por_empleado, columns=["nombre","venta"])
    venta_por_empleado_dict=venta_por_empleado_df.to_dict(orient='list')
    max_platillo_df=pd.DataFrame(max_platillo, columns=["platillo", "cantidad"])
    max_platillo_dict=max_platillo_df.to_dict(orient='list')
    


    return  jsonify({
        "venta_acumulada":venta_acumulada_dict,
        "clientes_empleado":clientes_por_empleado_dict,
         "venta_empleado":venta_por_empleado_dict,
        "venta_grupo":grupos_venta_dict,
        "platillo_max":max_platillo_dict
 
        })
    
@app.route("/reviews")
def reviews():
    return render_template("reviews.html")

@app.route("/API-REVIEWS", methods=["POST"])
def APIreviews():
    count_reviews=engine.execute("SELECT classification, COUNT(classification) FROM reviews GROUP BY classification")
    reviews_count=[]

    itera(count_reviews,reviews_count)
    reviews_count_df=pd.DataFrame(reviews_count, columns=["classification","count"])
    reviews_count_dct=reviews_count_df.to_dict(orient='list')

    return jsonify({
        "reviews":reviews_count_dct
    })

@app.route("/ventas_empeado")
def ventas_empleado():
    return render_template("ventas_empleado.html")

@app.route("/tripadvisor")
def tripadvisor():
    return render_template("tripadvisor.html")

@app.route("/yelp")
def yelp():
    return render_template("yelp.html")

@app.route("/opentable")
def opentable():
    return render_template("opentable.html")

@app.route("/prediccion")
def prediccion_ventas():
    return render_template("prediccion.html")

@app.route("/MLPRED" , methods=["POST"])
def prediction():
    pyoff.init_notebook_mode()
    total_sales=engine.execute("SELECT * FROM total_sales")
    total_sales_out=[]
    itera(total_sales, total_sales_out)
    dataset_final=pd.DataFrame(total_sales_out, columns=["anio","mes","grupo","cantidad","Fecha"])
    dataset_final['Fecha']=pd.to_datetime(dataset_final['Fecha'])
    df_sales = dataset_final.groupby('Fecha').cantidad.sum().reset_index()
    #create a new dataframe to model the difference
    df_diff = df_sales.copy()#add previous sales to the next row
    df_diff['prev_cantidad'] = df_diff['cantidad'].shift(1)#drop the null values and calculate the difference
    df_diff = df_diff.dropna()
    df_diff['diff'] = (df_diff['cantidad'] - df_diff['prev_cantidad'])
    # df_diff.head(10)
    #create dataframe for transformation from time series to supervised
    df_supervised = df_diff.drop(['prev_cantidad'],axis=1)#adding lags
    for inc in range(1,20):
        field_name = 'lag_' + str(inc)
        df_supervised[field_name] = df_supervised['diff'].shift(inc)#drop null values
    df_supervised = df_supervised.dropna().reset_index(drop=True)
    # Import statsmodels.formula.api
    import statsmodels.formula.api as smf# Define the regression formula
    model = smf.ols(formula='diff ~ lag_1', data=df_supervised)# Fit the regression
    model_fit = model.fit()# Extract the adjusted r-squared
    regression_adj_rsq = model_fit.rsquared_adj
    # print(regression_adj_rsq)
    model = smf.ols(formula='diff ~ lag_1+lag_2+lag_3+lag_4+lag_5+lag_6+lag_7+lag_8+lag_9+lag_10+lag_11+lag_12+lag_13+lag_14+lag_15+lag_16', data=df_supervised)# Fit the regression
    model_fit = model.fit()# Extract the adjusted r-squared
    regression_adj_rsq = model_fit.rsquared_adj
    # print(regression_adj_rsq)
    #import MinMaxScaler and create a new dataframe for LSTM model
    from sklearn.preprocessing import MinMaxScaler
    df_model = df_supervised.drop(['cantidad','Fecha'],axis=1)#split train and test set
    train_set, test_set = df_model[0:-6].values, df_model[-6:].values
    #apply Min Max Scaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(train_set)
    # reshape training set
    train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
    train_set_scaled = scaler.transform(train_set)# reshape test set
    test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
    test_set_scaled = scaler.transform(test_set)
    X_train, y_train = train_set_scaled[:, 1:], train_set_scaled[:, 0:1]
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_test, y_test = test_set_scaled[:, 1:], test_set_scaled[:, 0:1]
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
    model = Sequential()
    model.add(LSTM(4, batch_input_shape=(1, X_train.shape[1], 
    X_train.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, nb_epoch=100, batch_size=1, verbose=1, shuffle=False)
    y_pred = model.predict(X_test,batch_size=1)#for multistep prediction, you need to replace X_test values with the predictions coming from t-1
    #reshape y_pred
    y_pred = y_pred.reshape(y_pred.shape[0], 1, y_pred.shape[1])
    #rebuild test set for inverse transform
    pred_test_set = []
    for index in range(0,len(y_pred)):
        print (np.concatenate([y_pred[index],X_test[index]],axis=1))
    pred_test_set.append(np.concatenate([y_pred[index],X_test[index]],axis=1))
    #reshape pred_test_set
    pred_test_set = np.array(pred_test_set)
    pred_test_set = pred_test_set.reshape(pred_test_set.shape[0], pred_test_set.shape[2])
    #inverse transform
    pred_test_set_inverted = scaler.inverse_transform(pred_test_set)
    #create dataframe that shows the predicted sales
    result_list = []
    sales_dates = list(df_sales[-7:].Fecha)
    act_sales = list(df_sales[-7:].cantidad)
    for index in range(0,len(pred_test_set_inverted)):
        result_dict = {}
        result_dict['pred_value'] = int(pred_test_set_inverted[index][0] + act_sales[index])
        result_dict['Fecha'] = sales_dates[index+1]
        result_list.append(result_dict)
    df_result = pd.DataFrame(result_list)
    #merge with actual sales dataframe
    df_sales_pred = pd.merge(df_sales,df_result,on='Fecha',how='left')
    df_result_dict=df_result.to_dict()
    prediccion=df_result_dict["pred_value"][0]
    df_sales_dict = df_sales.to_dict(orient='list')

    return jsonify({
        "predictor" : prediccion,
        "total_sales" : df_sales_dict,
        "confiabilidad": regression_adj_rsq
    })

if __name__=="__main__":
    app.run(debug=True)