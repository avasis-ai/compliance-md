"""Command-line interface for compliance MD."""

import click
import json
from typing import Optional

from .enforcer import ComplianceEnforcer, AuditTrailManager


@click.group()
@click.version_option(version="0.1.0", prog_name="compliance-md")
def main() -> None:
    """Compliance MD - Regulatory compliance as executable agent rules."""
    pass


@main.command()
def policies() -> None:
    """Show available compliance policies."""
    enforcer = ComplianceEnforcer()
    
    click.echo("\n📋 Available Compliance Policies")
    click.echo("=" * 50)
    
    policies = enforcer._loader.list_policies()
    
    for policy in policies:
        click.echo(f"\n  {policy['id']}: {policy['name']}")
        click.echo(f"     Regulation: {policy['regulation']}")
        click.echo(f"     Action: {policy['action']}")
        click.echo(f"     Audit Required: {'Yes' if policy['audit_required'] else 'No'}")
        click.echo(f"     Description: {policy['description']}")


@main.command()
@click.option("--action-type", "-t", default="data_transfer", help="Type of action to check")
@click.option("--data-type", "-d", default="personal_data", help="Data type")
@click.option("--region", "-r", default="US", help="Destination region")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def check(action_type: str, data_type: str, region: str, json_output: bool) -> None:
    """Check compliance for an action."""
    enforcer = ComplianceEnforcer()
    
    action = {
        "action_type": action_type,
        "data_type": data_type,
        "destination_region": region,
        "resource_id": "demo_resource_001"
    }
    
    check = enforcer.check_compliance(action)
    
    if json_output:
        click.echo(json.dumps(check.to_dict(), indent=2))
    else:
        click.echo(f"\n🔍 Compliance Check Result")
        click.echo("=" * 50)
        click.echo(f"Check ID: {check.check_id}")
        click.echo(f"Status: {check.status.value}")
        click.echo(f"Message: {check.message}")
        
        if check.rules_violated:
            click.echo(f"\nRules Violated:")
            for rule_id in check.rules_violated:
                click.echo(f"  • {rule_id}")
        
        summary = enforcer.get_compliance_summary()
        click.echo(f"\n📊 Summary:")
        click.echo(f"  Total Checks: {summary['total_checks']}")
        click.echo(f"  Compliant: {summary['compliant']}")
        click.echo(f"  Warnings: {summary['warnings']}")
        click.echo(f"  Non-Compliant: {summary['non_compliant']}")
        click.echo(f"  Blocked: {summary['blocked']}")


@main.command()
def history() -> None:
    """Show compliance check history."""
    enforcer = ComplianceEnforcer()
    
    click.echo("\n📜 Compliance Check History")
    click.echo("=" * 50)
    
    checks = enforcer.get_check_history()
    
    if not checks:
        click.echo("No compliance checks yet.")
        return
    
    for i, check in enumerate(checks[-5:], 1):  # Show last 5
        click.echo(f"\n{i}. {check.check_id}")
        click.echo(f"   Status: {check.status.value}")
        click.echo(f"   Resource: {check.resource_type}/{check.resource_id}")
        click.echo(f"   Message: {check.message}")


@main.command()
def audit() -> None:
    """Show audit trail."""
    enforcer = ComplianceEnforcer()
    
    click.echo("\n📝 Audit Trail")
    click.echo("=" * 50)
    
    logs = enforcer.get_audit_logs()
    
    if not logs:
        click.echo("No audit entries yet.")
        return
    
    for i, log in enumerate(logs[-3:], 1):  # Show last 3
        click.echo(f"\n{i}. {log['timestamp']}")
        click.echo(f"   Resource: {log['resource_type']}/{log['resource_id']}")
        click.echo(f"   Rules Checked: {len(log['rules_checked'])}")


@main.command()
def demo() -> None:
    """Run compliance demo."""
    enforcer = ComplianceEnforcer()
    trail_manager = AuditTrailManager()
    
    click.echo("\n🧪 Compliance Demo")
    click.echo("=" * 50)
    
    # Simulate various actions
    actions = [
        {
            "action_type": "data_transfer",
            "data_type": "personal_data",
            "destination_region": "US"
        },
        {
            "action_type": "file_write",
            "data_type": "healthcare_data",
            "access_type": "read"
        },
        {
            "action_type": "database_access",
            "data_type": "financial_data",
            "encryption_status": "none"
        }
    ]
    
    for action in actions:
        click.echo(f"\n📄 Checking: {action['action_type']}")
        check = enforcer.check_compliance(action)
        
        status_color = {
            "compliant": "✅",
            "warning": "⚠️",
            "non_compliant": "❌",
            "blocked": "🚫"
        }.get(check.status.value, "❓")
        
        click.echo(f"   {status_color} {check.message}")
        
        if check.status != "compliant":
            audit_id = trail_manager.log_action(action, check.status.value, {})
            click.echo(f"   Audit ID: {audit_id}")
    
    # Show summary
    summary = enforcer.get_compliance_summary()
    click.echo(f"\n📊 Final Summary:")
    click.echo(f"   Total Checks: {summary['total_checks']}")
    click.echo(f"   Compliant: {summary['compliant']}")
    click.echo(f"   Blocked: {summary['blocked']}")


@main.command()
def help_text() -> None:
    """Show extended help information."""
    click.echo("""
Compliance MD - Regulatory Compliance as Executable Agent Rules

FEATURES:
  • GDPR compliance enforcement
  • HIPAA healthcare data protection
  • SOC2 data security policies
  • Cryptographically secure audit trails
  • Automated policy enforcement
  • Comprehensive compliance reporting

USAGE:
  compliance-md policies              Show available policies
  compliance-md check                 Check compliance for action
  compliance-md history               Show check history
  compliance-md audit                 Show audit trail
  compliance-md demo                  Run compliance demo

EXAMPLES:
  compliance-md check --data-type personal_data --region US
  compliance-md check --json-output
  compliance-md demo

For more information, visit: https://github.com/avasis-ai/compliance-md
    """)


def main_entry() -> None:
    """Main entry point."""
    main(prog_name="compliance-md")


if __name__ == "__main__":
    main_entry()
