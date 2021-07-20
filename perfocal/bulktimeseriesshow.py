import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from mindsphere_core import RestClientConfig, AppCredentials
from mindsphere_core import serialization_filter
from mindsphere_core.exceptions import MindsphereError
from iottsbulk.clients.read_operations_client import ReadOperationsClient
from iottsbulk.models.retrieve_timeseries_request import RetrieveTimeseriesRequest
from . import admin

AppName = os.environ['MDSP_OS_VM_APP_NAME']
AppVersion = os.environ['MDSP_OS_VM_APP_VERSION']
HostTenant = os.environ['MDSP_HOST_TENANT']
UserTenant = os.environ['MDSP_USER_TENANT']


class ShowBulkTimeValueSeries:
    def __init__(
            self,
            id_new=None,
            property_set_name=None,
            _from=None,
            to=None,
            DataHandshakeConfig=None
    ):
        self.DataHandshakeConfig = DataHandshakeConfig
        self.id = id_new
        self.property_set_name = property_set_name
        self._from = _from
        self.to = to
        self.DataHandshakeConfig = ReadOperationsClient()
        self.DataHandshakeConfig.rest_client_config = RestClientConfig()
        self.DataHandshakeConfig.mindsphere_credentials = AppCredentials(app_name=AppName, app_version=AppVersion,
                                                                         host_tenant=HostTenant,
                                                                         user_tenant=UserTenant)

    def showbulkplot(self):

        try:
            retrieveTimeseriesRequest = RetrieveTimeseriesRequest()
            retrieveTimeseriesRequest.entity = self.id
            retrieveTimeseriesRequest.property_set_name = self.property_set_name
            retrieveTimeseriesRequest._from = self._from
            retrieveTimeseriesRequest.to = self.to
            response2 = ReadOperationsClient.retrieve_timeseries(self=self.DataHandshakeConfig,
                                                                 request_object=retrieveTimeseriesRequest)
            records = serialization_filter.sanitize_for_serialization(response2)
            record = records.get("records")
            # print(records)

            return records
        except MindsphereError as err:
            print("ERROR:", err)
            return err
            # Exception Handling
