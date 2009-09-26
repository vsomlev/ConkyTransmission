#!/usr/bin/python
# -*- coding: utf-8 -*-
from Transmission import Transmission
from Template import Template
from ColorCode import ColorCode
from optparse import OptionParser
import sys

if __name__ == "__main__":
    parser = OptionParser(version="0.3")
    parser.add_option('-s', '--server', metavar='SERVER', dest='server', help='The computer where transmission is running. [default is 127.0.0.1]', default="127.0.0.1")
    parser.add_option('-p', '--port', metavar='PORT', dest='port', type="string", help='The port on which transmission is reachable. [default is 9091]', default="9091")
    parser.add_option('-x', '--proxy' , metavar='PROXY', dest='http_proxy', default="\"\"", help='Set an http proxy variable if you need it in order to be able to access Transmission remotely.')
    parser.add_option('-t', '--torrenttemplate', metavar='FILE', dest='t_template_file', help='File containing the template for individual torrent details. If not given, torrent details are not displayed.')
    parser.add_option('-u', '--summarytemplate', metavar='FILE', dest='s_template_file', help='File containing the template for summary information. If not given, summary information is not displayed.')
    parser.add_option('-a', '--activeonly' , dest='activeonly', default=False, action="store_true", help='If set, only torrents that are active (not paused) are displayed. [default is show all]')
    parser.add_option('-l', '--limit' , metavar='LIMIT', dest='limit', type="int", help='Limit the number of torrents diplayed. 0 means no limit. [default is 0]', default=0)
    parser.add_option('-c', '--colorfile' , metavar='FILE', dest='colorfile', help='File containing color codes for different states of torrents, overriding the template (\"Stopped\", \"Downloading\", \"Up & Down\", \"Idle\", \"Seeding\"). If not given, the colors in the template are used.')
    parser.add_option('-U', '--username' , metavar='USERNAME', dest='username', help='Username for authorization')
    parser.add_option('-P', '--password' , metavar='PASSWORD', dest='password', help='Password for authorizaion')
    parser.add_option('-S', '--sort', metavar='FIELD', type='string', dest='sortfield', help='Sort the list of torrents by the value of the specified field. [default: none]')
    parser.add_option('-R', '--reverse', dest='reverse', default=False, action='store_true', help='If this option is used, the list of torrents is reversed (even if no sorting criterion is given).')
    #~ parser.add_option('short', 'long' , metavar='', dest='', help='')

    (opts, args) = parser.parse_args()

    if not opts.s_template_file and not opts.t_template_file:
        print "No templates specified at all. Please give a torrent and/or summary template."
        parser.print_help()
        sys.exit(1)

    transmission = Transmission(options=opts)
    torrents, summary = transmission.get_simple_torrent_data(active_only=opts.activeonly)

    color_code = ColorCode(color_filename=opts.colorfile)

    # Summary
    if opts.s_template_file:
        s_template = Template(opts.s_template_file)
        s_template.set_data(summary)

        s_info = s_template.get_string()

        print s_info

    # Torrents
    if opts.t_template_file:
        t_template = Template(opts.t_template_file, short_status=False)
        if opts.limit > 0:
            # Limit the number of displayed torrents
            del torrents[opts.limit:]
        for t in torrents:
            t_template.set_data(t)
            t_info = t_template.get_string()
            t_info = color_code.colorize(t, t_info)
            print t_info
