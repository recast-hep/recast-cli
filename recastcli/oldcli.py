import click
import recastapi.request
import recastapi.analysis
import recastapi.user
import recastapi.response
import yaml
import os

def request_fmt():
	fmt =\
		  u'''\
		  ============================================
		  RECAST request -- {title}
		  ---------------------------------------------
		  UUID: {uuid}
		  
		  reason for request: {reason_for_request}
		  
		  additional information: {additional_information}

		  Status: {status}
		  
		  post date: {post_date}

		  \n\n\
		  '''
	return fmt
	
def analysis_fmt():
	fmt =\
		  u'''\
		  ====================================================
		  RECAST analysis -- {title}
		  ----------------------------------------------------
		  id: {id}
		  
		  Collaboration: {collaboration}
		  
		  description: {description}
		  \n\n\
		  '''
	return fmt
	
def user_fmt():
	fmt =\
		  u'''\
		  ==================================
		  RECAST user -- {name}
		  ----------------------------------
		  email: {email}
		  orcid_id: {orcid_id}\
		  '''
	return fmt

def parameter_fmt():
	fmt =\
		  u'''\
		  ===============================================     
		  RECAST parameter -- {index}
		  -----------------------------------------------
		  '''
	return fmt
  
def coordinate_fmt():
	fmt =\
		  u'''\
		  \t==============================================
		  \tRECAST coordinate -- {title}
		  \t----------------------------------------------
		  \tvalue: {value}
		  \n\
		  '''
	return fmt

def file_fmt():
	fmt =\
		  u'''\
		  ================================================
		  Recast file -- {file_name}
		  ------------------------------------------------
		  original name: {original_file_name}
		  
		  zenodo file ID: {zenodo_file_id}
		  
		  path: {path}
		  
		  link: {file_link}
		  
		  \n\
		  '''
	return fmt

@click.group()
def cli():
	pass
  
@cli.command(name = 'list-users')
def list_users():
	for p in recastapi.user.user()['_items']:
		click.echo(user_fmt().format(**p))
    
@cli.command(name = 'list-analyses')
def list_analyses():
	for p in recastapi.analysis.analysis()['_items']:
		click.echo(analysis_fmt().format(**p))

@cli.command(name = 'list-analysis')
@click.argument('uuid')
def list_analysis(uuid):
	click.echo(analysis_fmt().format(**recastapi.analysis.analysis(uuid)))

@cli.command(name = 'list-requests')
def list_requests():
    for p in recastapi.request.request()['_items']:
		print request_fmt().format(**p)
		
@cli.command(name = 'list-request')
@click.argument('uuid')
def list_request(uuid):
	print request_fmt().format(**recastapi.request.request(uuid))
	
@cli.command(name= 'list-parameter')
@click.argument('request-id')
def list_parameter(request_id):

	response = recastapi.request.parameter(int(request_id))
	for i, parameter in enumerate(response):
		print parameter_fmt().format(**({'index': i}))
		
		for coordinate in parameter['coordinates']:
			print coordinate_fmt().format(**coordinate)
			
		for zip_file in parameter['file']:
			print file_fmt().format(**zip_file)
  

@cli.command(name = 'parameter')
@click.argument('request-id')
@click.argument('index')
def parameter(request_id, index):
	response = recastapi.request.parameter(int(request_id), int(index))
	print parameter_fmt().format(**({'index': index}))
	for coordinate in response['coordinates']:
		print coordinate_fmt().format(**coordinate)

	for zip_file in response['file']:
		print file_fmt().format(**zip_file)

@cli.command(name= 'list-coordinate')
@click.argument('request_id')
@click.argument('parameter_index')
def list_coordinate(request_id, parameter_index):

	response = recastapi.request.coordinate(int(request_id), int(parameter_index))


	for coordinate in response:
		print coordinate_fmt().format(**coordinate)

@cli.command(name= 'coordinate')
@click.argument('request_id')
@click.argument('parameter_index')
@click.argument('coordinate_index')
def coordinate(request_id, parameter_index, coordinate_index):
  
	response = recastapi.request.coordinate(int(request_id),
											int(parameter_index),
											int(coordinate_index)
										)
	print coordinate_fmt().format(**response)

@cli.command(name = 'add-analysis')
@click.argument('data')
def add_analysis(data):

	read_config()
	if not os.path.isfile(data):
		click.echo('File does not exist!')
		return
  
	f = open(data)
	data_map = yaml.load(f)
	f.close()
	
	try:
		response = recastapi.analysis.create(
			title = data_map['title'],
			collaboration = data_map['collaboration'],
			e_print = data_map['e_print'],
			journal = data_map['journal'],
			doi = data_map['doi'],
			inspire_url = data_map['inspire_url'],
			description = data_map['description'],
			run_condition_name = data_map['run_condition_name'],
			run_condition_description = data_map['run_condition_description']
		)
		click.echo('Successfully created the analysis')
		click.echo(response)
    
	except Exception, e:
		click.echo('Failed to create analysis. Please check the YAML file format')
		click.echo(e)

@cli.command(name = 'add-request')
@click.argument('data')
def add_request(data):
  
	read_config()
	if not os.path.isfile(data):
		click.echo('File does not exit!')
		return

	f = open(data)
	data_map = yaml.load(f)
	f.close()
  
	try:
		recastapi.request.create(
			analysis_id = int(data_map['analysis_id']),
			title = data_map['title'],
			description_model = data_map['description_model'],      
			reason_for_request = data_map['reason_for_request'],
			additional_information = data_map['additional_information'],
			status = data_map['status'],
			file_path = data_map['file_path'],
			parameter_value = float(data_map['parameter_value']),
			parameter_title = data_map['parameter_title']
		)
		click.echo('Successfully created the request')
	except Exception, e:
		click.echo('Failed to create the request. Please check the YAML file format')
		click.echo(e)

@cli.command(name = 'add-parameter')
@click.argument('data')
def add_parameter(data):

	read_config()
	if not os.path.isfile(data):
		click.echo('File does not exist!')
		return

	f = open(data)
	data_map = yaml.load(f)
	f.close()
  
	try:
		response = recastapi.request.add_parameter(
			request_id = data_map['request_id'],
			coordinate_value = float(data_map['coordinate_value']),
			coordinate_title = data_map['coordinate_name'],
			filename = data_map['filename']
		)
		click.echo('Successfully added the parameter')
	except Exception, e:
		click.echo('Failed to add the parameter. Please check the YAML file format')
		click.echo(e)
		
@cli.command(name = 'add-coordinate')
@click.argument('data')
def add_coordinate(data):

	read_config()
	if not os.path.isfile(data):
		click.echo('File does not exist!')
		return
  
	f = open(data)
	data_map = yaml.load(f)
	f.close()
	
	try:
		response = recastapi.request.add_coordinate(
			parameter_id = data_map['parameter_id'],
			coordinate_name = data_map['coodinate_name'],
			coodinate_value = data_map['coordinate_value']
		)
		click.echo('Successfully added the coordinate')
		
	except Exception, e:
		click.echo('Failed to add the coordinate. Please check the YAML file format!')
		click.echo(e)
		
@cli.command(name= 'download-basic-request')
@click.option('--path', help='Enter download destination')
@click.option('--dry-run')
@click.argument('request-id')
@click.argument('point-request-index')
@click.argument('basic-request-index')
def download_basic_request(request_id, 
                           point_request_index, 
                           basic_request_index, 
                           path=None,
                           dry_run=True):
	
	if dry_run == "False" or dry_run == "false":
		dry_run = False
	else:
		dry_run = True
	response = recastapi.request.download(int(request_id),
										  int(point_request_index),
										  int(basic_request_index),
										  path,
										  dry_run)
	click.echo(response)
  
@cli.command(name = 'upload-basic-request')
@click.option('--request_id', help='Request ID')
@click.option('--basic_id', help='Basic Request ID')
@click.option('--path', help='File to upload')
def upload_basic_request(request_id, basic_id, path):
	read_config()
	recastapi.request.upload_file(request_id=request_id,
								  basic_request_id=basic_id,
								  filename=path)

@cli.command(name = 'download-basic-response')
@click.option('--path', help='Enter download destination')
@click.option('--dry-run')
@click.argument('response-id')
@click.argument('point-response-index')
@click.argument('basic-response-index')
def download_basic_response(response_id, 
                            point_response_index,
                            basic_response_index,
                            path=None,
                            dry_run=True):
  

	if dry_run == "False" or dry_run == "false":
		dry_run = False
	else:
		dry_run = True
		
		response = recastapi.response.download(int(response_id),
											   int(point_response_index),
											   int(basic_response_index),
											   path,
											   dry_run)
		click.echo(response)
  
@cli.command(name = 'upload-basic-response')
@click.option('--basic_id', help='Basic Request')
@click.option('--path', help='File to upload')
def upload_basic_response(basic_id, path):
	read_config()
	recastapi.response.upload_file(basic_response_id=basic_id,
								   file_name=path)
	
@cli.command(name = 'request-tree')
@click.argument('request_id')
def request_tree(request_id):
	recastapi.request.request_tree(request_id)

@cli.command(name = 'response-tree')
@click.argument('response_id')
def response_tree(response_id):
	recastapi.request.response_tree(response_id)
  
def read_config(config_file=None):
	default_config = 'recastcli/resources/config.yaml'
	config_file = config_file or default_config
	
	f = open(config_file)
	config = yaml.load(f)
	f.close()
	
	recastapi.ORCID_ID = config['ORCID_ID']
	recastapi.ACCESS_TOKEN = config['ACCESS_TOKEN']
