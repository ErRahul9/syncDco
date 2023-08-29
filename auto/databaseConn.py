import psycopg2
import os
from dotenv import load_dotenv
from redis.cluster import ClusterNode, RedisCluster


class connecters():
    def __init__(self,query):
        load_dotenv()
        self.host = os.environ['POSTGRES_HOST']
        self.user = os.environ['POSTGRES_USER']
        self.pwd = os.environ['POSTGRES_PW']
        self.port = os.environ['POSTGRES_PORT']
        self.db = os.environ['POSTGRES_DATABASE']
        self.query = query

    def connectToPostgres(self):
        conn = psycopg2.connect(database=self.db, user=self.user, password=self.pwd, host= self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(self.query)
        results =  cursor.fetchall()
        print(results)
        conn.commit()
        conn.close()
        return results

    def connectToCache(host, port, mapping, key, action, insertType):
        ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../..", "resources"))
        startup_nodes = [ClusterNode(host, port)]
        rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)
        getValue = ""
        if "set" in insertType:
            # for data in mapping:
            #     rc.set(key, mapping.get(data))
            getValue = rc.get(key)
        elif "sadd" in insertType:
            # vals = [data for data in mapping.get(key)]
            # for value in vals:
            #     rc.sadd(key, value)
            getValue = rc.smembers(key)
        elif "hm" in insertType:
            # rc.hmset(name=key, mapping=mapping)
            getValue = rc.hgetall(key)
        elif "delete" in action:
            rc.flushall()
        return getValue


if __name__=="__main__":
    q = "select * from sync.campaign_thresholds where campaign_id = 164100"
    print(connecters(q).connectToPostgres())