# Copyright (C) 2012 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pymongo import MongoClient
from datetime import datetime


class MnemoDB(object):
    def __init__(self, database_name):
        conn = MongoClient()
        self.db = conn[database_name]

    def insert_normalized(self, ndata, original_hpfeed):
        for item in ndata:
            #every root item is requal to collection name
            for collection, document in item.items():
                self.db[collection].insert(document)
        self.db.hpfeed.update({'_id': original_hpfeed['_id']}, {"$set": {'normalized': True}})

    def insert_hpfeed(self, ident, channel, payload):

        entry = {'channel': channel,
                 'ident': ident,
                 'payload': str(payload),
                 'timestamp': datetime.utcnow(),
                 'normalized': False}
        self.db.hpfeed.insert(entry)

        #extract unnormalized hpfeed data
    def get_hpfeed_data(self, max=None):
        data = self.db.hpfeed.find({'normalized': False})
        return data
