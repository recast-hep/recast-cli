import yaml
import numpy as np
import zipfile

data = yaml.load(open('scantemplate.yml'))

data['parameters'] = ['zPrime']
for zprime_mass in np.linspace(200,800,7).tolist():

    request_data = {
    }

    datafile = 'data/{}.zip'.format(zprime_mass)
    with zipfile.ZipFile(datafile,'w') as zf:	
    	zf.writestr('input.yaml', yaml.dump(request_data, default_flow_style = False))
	data['points'].append({
		'coordinates': [zprime_mass],
		'data': datafile
	})

yaml.dump(data,open('scan.yml','w'))
