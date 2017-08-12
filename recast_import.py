import recastapi.analysis.write
import recastapi.analysis.read
import import_analysis_data
import json
import time
import click




@click.group()
def recast_import():
    pass

@recast_import.command()
@click.argument('inputdata')
@click.argument('returndata')
@click.option('--dry/--no-dry',default = True, help = 'dry run')
def from_disk(inputdata,returndata,dry):
    data = json.load(open(inputdata))
    return_data = []
    for entry in data:

        return_data.append({
            'pubtype': entry['pubtype'],
            'pubid': entry['pubid'],
            'recast_info': import_analysis_data.import_entry(entry, dry)
        })
    json.dump(return_data,open(returndata,'w'))

@recast_import.command()
@click.argument('pubkey')
@click.argument('returndata')
@click.option('--dry/--no-dry',default = True, help = 'dry run')
def from_web(pubkey,returndata,dry):
    pubtype, pubid = pubkey.split('/')

    if pubtype == 'cds':
        data = import_analysis_data.download_cds(pubid)
        data = import_analysis_data.extract_cds(pubid,data)
    if pubtype == 'inspire':
        data = import_analysis_data.download_inspire(pubid)
        data = import_analysis_data.extract_inspire(pubid,data)


    return_data = {
        'pubtype': data['pubtype'],
        'pubid': data['pubid'],
        'recast_info': import_analysis_data.import_entry(data, dry)
    }
    json.dump(return_data,open(returndata,'w'))

if __name__ == '__main__':
    recast_import()