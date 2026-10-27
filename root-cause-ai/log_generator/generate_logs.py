from pathlib import Path
import csv, random, argparse
from datetime import datetime, timedelta

SERVICES = ["API_Gateway","Auth_Service","Order_Service","Payment_Service","Database_Service"]

def generate(count=300, scenario="mixed", seed=42, output=None):
    random.seed(seed)
    rows=[]
    base=datetime(2026,10,27,10,0,0)
    for i in range(1,count+1):
        tid=f"TXN{i:05d}"
        t=base+timedelta(seconds=i*3)
        failure = scenario
        if scenario=="mixed":
            failure=random.choice(["normal","normal","normal","payment_failure","database_failure","auth_failure","high_latency"])
        flow=[
            ("API_Gateway","INFO","Request received",200,120),
            ("Auth_Service","INFO","User authenticated",200,180),
            ("Order_Service","INFO","Order created",200,300),
            ("Payment_Service","INFO","Payment completed",200,450),
            ("Database_Service","INFO","Database query completed",200,220),
        ]
        if failure=="payment_failure":
            flow[3]=("Payment_Service","ERROR","Payment timeout",500,3200)
            flow[4]=("Database_Service","ERROR","Transaction rollback after payment failure",500,2500)
        elif failure=="database_failure":
            flow[4]=("Database_Service","ERROR","Database connection failure",503,3500)
        elif failure=="auth_failure":
            flow[1]=("Auth_Service","ERROR","Authentication failed",401,500)
        elif failure=="high_latency":
            flow[3]=("Payment_Service","WARNING","Payment completed slowly",200,4200)
        for j,(svc,lvl,msg,status,rt) in enumerate(flow):
            rows.append([ (t+timedelta(seconds=j)).isoformat(sep=" "),
                          svc, tid, lvl, status, rt, msg, f"/api/{svc.lower()}"])
    if output is None: output=Path(__file__).resolve().parents[1]/"sample_data"/f"{scenario}_logs.csv"
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["timestamp","service","transaction_id","log_level","status_code","response_time","message","endpoint"])
        w.writerows(rows)
    return output

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--count",type=int,default=300)
    p.add_argument("--scenario",choices=["mixed","normal","payment_failure","database_failure","auth_failure","high_latency"],default="mixed")
    p.add_argument("--output")
    a=p.parse_args()
    print(generate(a.count,a.scenario,output=a.output))
