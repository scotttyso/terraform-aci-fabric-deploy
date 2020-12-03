#!/usr/bin/env python3

import json

def aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file):
    template_payload = '{0} {1}\n\tpath\t\t= "{2}"\n\tclass_name\t= "{3}"\n\tpayload\t\t= <<EOF\n{4}\n\tEOF\n{5}\n\n'

    resource_line = 'resource "aci_rest" "{}"'.format(resrc_desc)

    # Attached Data to template
    wr_to_file = template_payload.format(resource_line, "{", path_attrs, class_name, json.dumps(data_out, indent=4), "}")

    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_rest_depends_on(resrc_desc, depends_on, path_attrs, class_name, data_out, wr_file):
    template_payload = '{0} {1}\n\tdepends_on\t\t= [{2}]\n\tpath\t\t= "{3}"\n\tclass_name\t= "{4}"\n\tpayload\t\t= <<EOF\n{5}\n\tEOF\n{6}\n\n'

    resource_line = 'resource "aci_rest" "{}"'.format(resrc_desc)

    # Attached Data to template
    wr_to_file = template_payload.format(resource_line, "{", depends_on, path_attrs, class_name, json.dumps(data_out, indent=4), "}")

    # Write Data to Template
    wr_file.write(wr_to_file)