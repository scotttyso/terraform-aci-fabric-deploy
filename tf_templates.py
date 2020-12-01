#!/usr/bin/env python3

import json

def aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file):
    template_payload = '{0} {1}\n\tpath\t\t= {2}\n\tclass_name\t= "{3}"\n\tpayload\t\t= <<EOF\n{4}\n\tEOF\n{5}\n\n'

    resource_line = 'resource "aci_rest" "{}"'.format(resrc_desc)

    # Attached Data to template
    wr_to_file = template_payload.format(resource_line, "{", path_attrs, class_name, json.dumps(data_out, indent=4), "}")

    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr1(resrc_type, resrc_desc, attr_1st, wr_file):
    template_payload = '{0} {1}\n\t{2}\n{3}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1st, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr2(resrc_type, resrc_desc, attr_1st, attr_2nd, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n{4}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1st, attr_2nd, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr3(resrc_type, resrc_desc, attr_1st, attr_2nd, attr_3rd, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n\t{4}\n{5}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1st, attr_2nd, attr_3rd, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)