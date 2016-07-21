#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2016 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

""" Bibcheck plugin to move info for OSTI from tag
    8564_w/y to tag 035__a/9
"""

from invenio.bibrecord import record_add_field
import re

PROVENANCE = 'OSTI'

OSTI_ID = re.compile(r'^https?://(?:www\.)?osti\.gov/.*?\D(\d+)$')


def check_record(record):
    """ move 8564_u/y to 035__a/9 """
    for pos, val in record.iterfield('8564_u',
                                     subfield_filter=('y', PROVENANCE)):
        if val:
            ostimatch = OSTI_ID.match(val)
            if ostimatch:
                ostimatch_tuple = ostimatch.groups()
                ostimatch_string = ''.join(ostimatch_tuple)
                osti_subfields = [('9', 'OSTI'), ('a', ostimatch_string)]
                record_add_field(record, '035', ' ', ' ',
                                     subfields=osti_subfields)
                record.delete_field((pos[0][0:3], pos[1], None))
                record.set_amended(
                    "%s: moved link '%s'" % (record.record_id, val))
            else:
                print "%s: no match for '%s'" % (record.record_id, val)

