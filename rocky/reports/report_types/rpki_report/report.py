from datetime import datetime
from logging import getLogger
from typing import Any, Dict

from django.utils.translation import gettext_lazy as _

from octopoes.models import Reference
from octopoes.models.ooi.dns.zone import Hostname
from octopoes.models.ooi.network import IPAddressV4, IPAddressV6
from reports.report_types.definitions import Report

logger = getLogger(__name__)


class RPKIReport(Report):
    id = "rpki-report"
    name = _("RPKI Report")
    description = _(
        "Shows whether the ip is covered by a valid RPKI ROA. For a hostname it shows "
        "the ip addresses and whether they are covered by a valid RPKI ROA."
    )
    plugins = {"required": ["dns-records", "rpki"], "optional": []}
    input_ooi_types = {Hostname, IPAddressV4, IPAddressV6}
    template_path = "rpki_report/report.html"

    def generate_data(self, input_ooi: str, valid_time: datetime) -> Dict[str, Any]:
        reference = Reference.from_str(input_ooi)
        if reference.class_type == Hostname:
            ips = self.octopoes_api_connector.query(
                "Hostname.<hostname[is ResolvedHostname].address", valid_time, reference
            )
        else:
            ips = [self.octopoes_api_connector.get(reference)]

        rpki_ips = {}
        number_of_ips = len(ips)
        number_of_available = number_of_ips
        number_of_valid = number_of_ips
        for ip in ips:
            finding_types = self.octopoes_api_connector.query(
                "IPAddress.<ooi[is Finding].finding_type", valid_time, ip.reference
            )
            rpki_ips[ip.address] = {}
            exists = not any([finding_type for finding_type in finding_types if finding_type.id in ["KAT-NO-RPKI"]])
            valid = not any([finding_type for finding_type in finding_types if finding_type.id in ["KAT-INVALID-RPKI"]])
            rpki_ips[ip.address]["exists"] = exists
            rpki_ips[ip.address]["valid"] = valid
            number_of_available -= 1 if not exists else 0
            number_of_valid -= 1 if not valid else 0

        return {
            "input_ooi": input_ooi,
            "rpki_ips": rpki_ips,
            "number_of_available": number_of_available,
            "number_of_valid": number_of_valid,
            "number_of_ips": number_of_ips,
        }
