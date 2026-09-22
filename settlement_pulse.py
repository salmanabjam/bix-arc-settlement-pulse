import json, urllib.request, statistics
from datetime import datetime, timezone

RPC="https://rpc.mainnet.arc.io"

def rpc(method, params):
    payload=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    req=urllib.request.Request(RPC,data=payload,headers={"Content-Type":"application/json","User-Agent":"BiX-Arc-Settlement-Pulse/0.1"})
    with urllib.request.urlopen(req,timeout=15) as r:
        return json.loads(r.read()).get("result")

def main():
    tip=int(rpc("eth_blockNumber",[]),16)
    blocks=[]
    for n in range(max(0,tip-19),tip+1):
        b=rpc("eth_getBlockByNumber",[hex(n),False])
        if b: blocks.append(b)
    ts=[int(b["timestamp"],16) for b in blocks]
    intervals=[b-a for a,b in zip(ts,ts[1:])]
    tx=[len(b.get("transactions",[])) for b in blocks]
    out={
      "observed_at":datetime.now(timezone.utc).isoformat(),
      "latest_block":tip,
      "window_blocks":len(blocks),
      "median_block_interval_sec":statistics.median(intervals) if intervals else None,
      "max_block_interval_sec":max(intervals) if intervals else None,
      "avg_tx_per_block":round(statistics.mean(tx),3) if tx else None,
      "empty_blocks":sum(1 for x in tx if x==0),
      "read_only":True
    }
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()
