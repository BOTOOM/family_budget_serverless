import json
import pandas as pd
import io
import os
import base64


def lambda_handler(event, context):
    # Verifica si el archivo ha sido subido
    if "body" not in event:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "No file uploaded"}),
        }

    # Verifica si hay un archivo adjunto
    content_type = event["headers"].get("Content-Type", "")
    print("content_type", content_type)
    print("heaDERS", event["headers"])

    if "multipart/form-data" not in content_type:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Invalid content type"}),
        }

    # Decodifica el archivo recibido
    try:
        body = event["body"]
        is_base64_encoded = event.get("isBase64Encoded", False)
        print("is_base64_encoded", is_base64_encoded)
        if is_base64_encoded:
            print("holi")
            file_data = io.BytesIO(base64.b64decode(body))
            print("adios")

        else:
            file_data = io.BytesIO(body.encode("utf-8"))
        print("pasamos", {"content_type": content_type, "file_data": file_data})
        # Determina el tipo de archivo (CSV o XLSX)
        # if "csv" in content_type:
        #     df = pd.read_csv(file_data)
        # elif "excel" in content_type:
        #     df = pd.read_excel(file_data, engine="openpyxl")
        # else:
        #     return {
        #         "statusCode": 400,
        #         "body": json.dumps({"error": "Unsupported file format"}),
        #     }

        # Convierte el dataframe a JSON
        df = pd.read_excel(file_data, engine="openpyxl")
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')  # Convierte la columna a formato datetime
            df['Fecha'] = df['Fecha'].dt.strftime('%Y/%m/%d')  # Reformatea a 'YYYY/MM/DD'
        df.fillna(0, inplace=True)
        result = df.to_dict(orient="records")
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"data":result}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
