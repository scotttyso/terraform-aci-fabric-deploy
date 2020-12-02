#!/usr/bin/env python3

import json

def aci_rest(resrc_desc, path_attrs, class_name, data_out, wr_file):
    template_payload = '{0} {1}\n\tpath\t\t= {2}\n\tclass_name\t= "{3}"\n\tpayload\t\t= <<EOF\n{4}\n\tEOF\n{5}\n\n'

    resource_line = 'resource "aci_rest" "{}"'.format(resrc_desc)

    # Attached Data to template
    wr_to_file = template_payload.format(resource_line, "{", path_attrs, class_name, json.dumps(data_out, indent=4), "}")

    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr1(resrc_type, resrc_desc, attr_1, wr_file):
    template_payload = '{0} {1}\n\t{2}\n{3}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr2(resrc_type, resrc_desc, attr_1, attr_2, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n{4}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1, attr_2, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr3(resrc_type, resrc_desc, attr_1, attr_2, attr_3, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n\t{4}\n{5}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1, attr_2, attr_3, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr4(resrc_type, resrc_desc, attr_1, attr_2, attr_3, attr_4, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n\t{4}\n\t{5}\n{6}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1, attr_2, attr_3, attr_4, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr5(resrc_type, resrc_desc, attr_1, attr_2, attr_3, attr_4, attr_5, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n\t{4}\n\t{5}\n\t{6}\n{7}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1, attr_2, attr_3, attr_4, attr_5, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)

def aci_terraform_attr9(resrc_type, resrc_desc, attr_1, attr_2, attr_3, attr_4, attr_5, attr_6, attr_7, attr_8, attr_9, wr_file):
    template_payload = '{0} {1}\n\t{2}\n\t{3}\n\t{4}\n\t{5}\n\t{6}\n\t{7}\n\t{8}\n\t{9}\n\t{10}\n{11}\n\n'

    resource_line = 'resource "{}" "{}"'.format(resrc_type, resrc_desc)

    wr_to_file = template_payload.format(resource_line, "{", attr_1, attr_2, attr_3, attr_4, attr_5, attr_6, attr_7, attr_8, attr_9, "}")
    # Write Data to Template
    wr_file.write(wr_to_file)