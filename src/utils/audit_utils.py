from fastapi import Request

from src.schemas.audit import AuditSchema


def create_audit_schema(request: Request, table_name:str, service_name:str, action_name:str) -> AuditSchema:
    audit_schema = AuditSchema(ip_address=str(request.client.host),
                               table_name=table_name,
                               service_name=service_name,
                               action_name=action_name,
                               request_url=str(request.url),
                               request_method=str(request.method))

    return audit_schema