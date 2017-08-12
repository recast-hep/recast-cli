import yaml
import numpy as np
import zipfile

data = yaml.load(open('scantemplate.yml'))

data['parameters'] = ['m1','m2']



for m1 in np.linspace(200,800,7).tolist():
  for m2 in np.linspace(0,500,6).tolist():
    if m1 < m2: continue

    request_data = {
	    "nevents": "50000",
	    "run_conditions": {
	    	"energy": 8000
	    },
	    "parameters": {
	    	"m1": m1,
	    	"m2": m2
	    }
    }

    datafile = 'data/{}_{}.zip'.format(m1,m2)
    with zipfile.ZipFile(datafile,'w') as zf:	
    	zf.writestr('input.yaml', yaml.dump(request_data, default_flow_style = False))
	data['points'].append({
		'coordinates': [m1,m2],
		'data': datafile
	})

yaml.dump(data,open('scan.yml','w'))
