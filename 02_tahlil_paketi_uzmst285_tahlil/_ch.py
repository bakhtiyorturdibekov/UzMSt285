import numpy as np, itertools, json, time
from chegaralar import min_chaqiruv
R={}
t=time.time(); R['dif_min_128_toliq']=min_chaqiruv(8); print('128 (m=8), barcha kirishlar:',R['dif_min_128_toliq'],round(time.time()-t,1),'s',flush=True)
t=time.time(); R['dif_min_256_w3']=min_chaqiruv(16,maxw=3); print('256 (m=16), og‘irligi ≤3 kirishlar:',R['dif_min_256_w3'],round(time.time()-t,1),'s',flush=True)
json.dump(R,open('/home/claude/ka/chegaralar.json','w'))
