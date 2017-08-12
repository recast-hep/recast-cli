import yaml
import numpy as np
import zipfile

data = yaml.load(open('scantemplate.yml'))

data['parameters'] = ['mStop','mNeutralino']



for stop_mass in np.linspace(200,800,7).tolist():
  for neutralino_mass in np.linspace(0,500,6).tolist():
    if stop_mass < neutralino_mass: continue

    request_data = {
	    "events": "50000",
	    "analysis": "atlas_conf_2013_024",
	    "neutralino_mass": neutralino_mass,
	    "stop_mass": stop_mass,
    }

    datafile = 'data/{}_{}.zip'.format(stop_mass,neutralino_mass)
    with zipfile.ZipFile(datafile,'w') as zf:	
    	zf.writestr('input.yaml', yaml.dump(request_data, default_flow_style = False))
	data['points'].append({
		'coordinates': [stop_mass,neutralino_mass],
		'data': datafile
	})

yaml.dump(data,open('scan.yml','w'))
