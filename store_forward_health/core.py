from __future__ import annotations
import hashlib,json,re
from collections import defaultdict,deque
from typing import Any,Mapping
def stable(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(v): return hashlib.sha256(stable(v).encode()).hexdigest()
class BusinessError(ValueError): pass

from store_forward_health.journal.local_log import process_fixture
def run(raw,database):
 p=raw.get('payload',raw); now=float(p.get('now',0)); ready=[]; delayed=[]; corrupt=[]
 for item in [dict(x) for x in p.get('packets',[])]:
  body=str(item.get('body','')); actual=hashlib.sha256(body.encode()).hexdigest(); item['actual_checksum']=actual
  if item.get('checksum') and item['checksum']!=actual: corrupt.append(item)
  elif float(item.get('available_at',0))<=now: ready.append(item)
  else: delayed.append(item)
 ready.sort(key=lambda x:(-int(x.get('priority',0)),x.get('available_at',0),x.get('packet_id','')))
 versions=defaultdict(list)
 for item in ready: versions[item.get('logical_id',item.get('packet_id'))].append(item)
 merged={k:max(v,key=lambda x:(int(x.get('version',0)),x.get('device_id',''))) for k,v in versions.items()}
 result={'ready':ready,'delayed':delayed,'corrupt':corrupt,'merged':merged,'next_due':min((x.get('available_at',0) for x in delayed),default=None),'journal_hash':digest([ready,delayed,corrupt])}
 stored=process_fixture(database,{'subject_id':str(p.get('station_id','station-demo')),'request_key':result['journal_hash'],'payload':result})
 return {'delivery':result,'stored':stored}
