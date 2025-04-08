import pandas as pd


candidatos_all = pd.read_csv(r'E:\All\infogob_data_peru\data\02_resultados\todas_elecciones.csv')

a = candidatos_all.columns
print(a)
# 

# # unique_doc  = data[['documento_identidad']].drop_duplicates()
# unique_doc_name  = data[['infractor', 'documento_identidad']].drop_duplicates()
# docs_id = unique_doc_name.value_counts('documento_identidad').reset_index()
# doc_more_1 = docs_id.query('count > 1')

# duplicates_names = unique_doc_name[unique_doc_name['documento_identidad'].isin(doc_more_1['documento_identidad'])]
# # print(unique_doc.shape)
# # print(unique_doc_name.shape)
# # print(data.columns)
# # print(data.shape)
# duplicates_names = duplicates_names.sort_values('documento_identidad')
# duplicates_names.to_csv('./test/duplicates.csv')
# print(duplicates_names)

