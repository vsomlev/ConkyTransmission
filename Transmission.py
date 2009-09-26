#!/usr/bin/python
# -*- coding: utf-8 -*-
import commands
import sys

class Transmission:
    """
        A class for communication to a running transmission instance.
    """

    def __init__(self, options):
        # How are the functions of the object not lost?:
        self.__dict__ = vars(options)

    def get_simple_torrent_data(self, active_only=False):
        list_command = "http_proxy="+self.http_proxy+" transmission-remote "+self.server+":"+self.port+" -l"
        if self.username and self.password:
            list_command = list_command + " -n "+self.username+":"+self.password
        output = commands.getoutput(list_command)

        if "Couldn't connect to server" in output:
            print "Couldn't connect to server: ",self.server,":",self.port
            sys.exit(1)
        if "Unauthorized User" in output:
            print "Couldn't connect to server: Username & password authorization required"
            sys.exit(1)

        lines = output.split('\n')
        # First line is not needed
        del lines[0]

        summary_line = lines[-1]
        summary_info = summary_line.split('  ')
        summary_info = [x for x in summary_info if x!='']
        del summary_info[0]
        summary={}
        summary["s_have"]=summary_info[0]
        summary["s_up"]=summary_info[1]
        summary["s_down"]=summary_info[2]
        #print summary
        del lines[-1]

        torrents = []
        for line in lines:
            t_info = line.split('  ')
            # When splitting for '\ \ ', empty elements appear in l
            t_info = [x for x in t_info if x!='']
            if len(t_info)!=9:
                print "Error parsing transmission output: Wrong number of fields"
                sys.exit(1)
            torrent={}
            torrent["t_id"]=t_info[0]
            torrent["t_done"]=t_info[1]
            torrent["t_have"]=t_info[2]
            torrent["t_eta"]=t_info[3]
            torrent["t_up"]=t_info[4]
            torrent["t_down"]=t_info[5]
            torrent["t_ratio"]=t_info[6]
            torrent["t_status"]=t_info[7]
            torrent["t_name"]=t_info[8]

            inactive_states = ["Stopped", "Idle"]
            # If active_only is set, exclude inactive torrents
            if not (active_only and torrent["t_status"] in inactive_states):
                torrents.append(torrent)
            #~ print torrent
        #print torrents
        self._sort_torrents(torrents)
        return torrents, summary


    def _sort_torrents(self, torrents):
        def compare_by (fieldname):
            fieldname = "t_"+fieldname
            def compare_two_dicts (a, b):
                return cmp(a[fieldname], b[fieldname])
            return compare_two_dicts

        sort_fields = ['id', 'done', 'have', 'eta', 'up', 'down', 'ratio', 'status', 'name']

        if self.sortfield and self.sortfield in sort_fields:
            torrents.sort( compare_by(self.sortfield) )

        if self.reverse:
            torrents.reverse()


    def get_detailed_torrent_data(torrent_id):
        """
            Returns a lot of details about a single torrent. WARNING: Takes ~3 seconds for transmission to return the information.
        """
        cmd = 'http_proxy="" transmission-remote -t'+str(torrent_id)+' -i'
        output = commands.getoutput(cmd)
        if output.endswith("Couldn't connect to server"):
            return {}
        lines = output.split('\n')
        return lines

