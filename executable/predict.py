import pandas as pd
import sklearn.covariance


def predict(initial_u_values, initial_v_values, serie_numbers, path):
    el = sklearn.covariance.EllipticEnvelope(store_precision=True, assume_centered=False, support_fraction=None, contamination=0.0075, random_state=0)
    d = pd.DataFrame()
    
    d['u'] = initial_u_values
    d['v'] = initial_v_values
    el.fit(d)
    d['anomaly'] = el.predict(d)
    predictions = d.loc[d['anomaly'] < 1]
    anomalies = []
    anomaly_index = list(predictions.index.values)


    for i in range(len(anomaly_index)):
        anomalies.append(serie_numbers[anomaly_index[i]])

    file1 = open(path+"/prediction_seri.txt", "w")
    for i in anomalies:
        file1.write(i+"\n")
    file1.close()
