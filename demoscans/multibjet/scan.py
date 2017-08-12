import yaml
import numpy as np
import zipfile

data = yaml.load(open('scantemplate.yml'))

data['parameters'] = ['mGluino','mStop','mNeutralino']

for x in open('gtt.list').readlines():
    coords = mGluino,mStop,mNeutralino = map(float,x.strip().split('.')[2].split('_')[-3:])
    request_data = {
        'dataset': x
    }

    datafile = 'data/{}_{}_{}.zip'.format(*coords)
    with zipfile.ZipFile(datafile,'w') as zf:   
        zf.writestr('input.yaml', yaml.dump(request_data, default_flow_style = False))
    data['points'].append({
        'coordinates': coords,
        'data': datafile
    })

yaml.dump(data,open('scan.yml','w'))
