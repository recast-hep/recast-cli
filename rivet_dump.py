import import_analysis_data
import json
import click


@click.command()
@click.argument('rivet_analysis_json')
@click.argument('outputfile')
@click.option('--max-entries',default = None, type=int)
def main(rivet_analysis_json,outputfile,max_entries):
    rivetdata = json.load(open(rivet_analysis_json))
    dumpdata = []

    i = 0
    for inspire_id,rivet_ids in rivetdata.iteritems():
        if any([('ATLAS' in x) for x in rivet_ids]):
            if max_entries and (i >= max_entries):
                click.secho('max reached.')
                break
            print inspire_id
            data = import_analysis_data.download_inspire(inspire_id)
            data = import_analysis_data.extract_inspire(inspire_id,data)
            dumpdata.append(data)
            i = i + 1

    json.dump(dumpdata,open(outputfile,'w'))


if __name__ == '__main__':
    main()