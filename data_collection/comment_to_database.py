import pandas as pd
import psycopg2
from secret import database_connect
from sqlalchemy import create_engine
import io

df = pd.read_csv('2021-02-02-lang_pred.csv')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')] # drop unnamed
df_todb = df.loc[(df['lang'] == 'en') | (df['lang'] == 'emoji')]
df_todb = df_todb.drop(['lang', 'lang_conf', 'stripped_body'], axis = 1)
df_todb.reset_index(drop=True, inplace=True)
try:
    engine = create_engine('postgresql+psycopg2://' + database_connect['user'] + ':' + database_connect['password'] + '@' + database_connect['host'] + ':' + str(5432) + '/comments')
    connection = engine.connect()
    df_todb.to_sql('comment', connection, schema='sentiment_anls', if_exists='replace',index=False)
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connection is not None:
        connection.close()
        print('Database connection closed.')