import yaml
import numpy as np
import zipfile

data = yaml.load(open('scantemplate.yml'))

data['parameters'] = ['m1','m2','m3']
for m1 in np.linspace(200,800,7).tolist():
	for m2 in np.linspace(0,200,7).tolist():
		for tan_beta in np.linspace(0,20,3).tolist():
		    request_data = {}

		    datafile = 'data/{}_{}_{}.zip'.format(m1,m2,tan_beta)
		    with zipfile.ZipFile(datafile,'w') as zf:	
		    	zf.writestr('input.yaml', yaml.dump(request_data, default_flow_style = False))
			data['points'].append({
				'coordinates': [m1,m2,tan_beta],
				'data': datafile
			})

yaml.dump(data,open('scan.yml','w'))
