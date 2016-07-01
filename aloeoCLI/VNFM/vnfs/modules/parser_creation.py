import yaml
import hot_template
import multicore
import multiprocessat

def parser_create_template(name, description, flavors=None ):

	print "INFO: Parser done."

	if flavors is None:
		multicore.main(name, description)
	else:
		multicore.main(name, description, flavors)

	print "INFO: Template created."

	return name	
