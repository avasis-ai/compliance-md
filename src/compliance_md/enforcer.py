"""Policy enforcer for compliance enforcement."""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import hashlib


class ComplianceStatus(Enum):
    """Compliance status enum."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    WARNING = "warning"
    BLOCKED = "blocked"


@dataclass
class PolicyRule:
    """Represents a compliance policy rule."""
    id: str
    name: str
    description: str
    condition: Dict[str, Any]
    action: str  # allow, block, require_approval
    audit_required: bool
    regulation: str  # GDPR, HIPAA, SOC2, etc.
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "condition": self.condition,
            "action": self.action,
            "audit_required": self.audit_required,
            "regulation": self.regulation
        }


@dataclass
class ComplianceCheck:
    """Result of a compliance check."""
    check_id: str
    timestamp: datetime
    resource_type: str
    resource_id: str
    status: ComplianceStatus
    rules_violated: List[str]
    audit_trail: Dict[str, Any]
    message: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "check_id": self.check_id,
            "timestamp": self.timestamp.isoformat(),
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "status": self.status.value,
            "rules_violated": self.rules_violated,
            "audit_trail": self.audit_trail,
            "message": self.message
        }


class PolicyLoader:
    """Loads and manages compliance policies."""
    
    def __init__(self):
        """Initialize policy loader."""
        self._policies: Dict[str, PolicyRule] = {}
    
    def load_policy(self, policy_data: Dict[str, Any]) -> PolicyRule:
        """
        Load a policy from data.
        
        Args:
            policy_data: Policy data dictionary
            
        Returns:
            PolicyRule object
        """
        rule = PolicyRule(
            id=policy_data["id"],
            name=policy_data["name"],
            description=policy_data["description"],
            condition=policy_data["condition"],
            action=policy_data["action"],
            audit_required=policy_data.get("audit_required", False),
            regulation=policy_data.get("regulation", "UNKNOWN")
        )
        
        self._policies[rule.id] = rule
        return rule
    
    def load_policies_from_dict(self, policies_data: List[Dict[str, Any]]) -> List[PolicyRule]:
        """
        Load multiple policies from data.
        
        Args:
            policies_data: List of policy data dictionaries
            
        Returns:
            List of PolicyRule objects
        """
        return [self.load_policy(policy) for policy in policies_data]
    
    def get_policy(self, policy_id: str) -> Optional[PolicyRule]:
        """Get a policy by ID."""
        return self._policies.get(policy_id)
    
    def list_policies(self) -> List[Dict[str, Any]]:
        """List all policies."""
        return [policy.to_dict() for policy in self._policies.values()]
    
    def clear_policies(self) -> None:
        """Clear all policies."""
        self._policies = {}


class ComplianceEnforcer:
    """Enforces compliance policies on actions."""
    
    def __init__(self):
        """Initialize compliance enforcer."""
        self._loader = PolicyLoader()
        self._checks: List[ComplianceCheck] = []
        self._audit_logs: List[Dict[str, Any]] = []
        
        # Load default GDPR policy
        self._load_default_policies()
    
    def _load_default_policies(self) -> None:
        """Load default compliance policies."""
        default_policies = [
            {
                "id": "gdpr_001",
                "name": "GDPR - Data Transfer Restriction",
                "description": "Personal data cannot be transferred outside EU without consent",
                "condition": {
                    "data_type": "personal_data",
                    "destination_region": ["US", "CA", "AU", "JP"]
                },
                "action": "block",
                "audit_required": True,
                "regulation": "GDPR"
            },
            {
                "id": "hipaa_001",
                "name": "HIPAA - Healthcare Data Access",
                "description": "Healthcare data requires explicit access logging",
                "condition": {
                    "data_type": "healthcare_data",
                    "access_type": ["read", "write", "delete"]
                },
                "action": "require_approval",
                "audit_required": True,
                "regulation": "HIPAA"
            },
            {
                "id": "soc2_001",
                "name": "SOC2 - Financial Data Encryption",
                "description": "Financial data must be encrypted at rest",
                "condition": {
                    "data_type": "financial_data",
                    "encryption": "none"
                },
                "action": "block",
                "audit_required": True,
                "regulation": "SOC2"
            }
        ]
        
        self._loader.load_policies_from_dict(default_policies)
    
    def load_policy(self, policy_data: Dict[str, Any]) -> PolicyRule:
        """Load a custom policy."""
        return self._loader.load_policy(policy_data)
    
    def check_compliance(self, action: Dict[str, Any]) -> ComplianceCheck:
        """
        Check if an action complies with policies.
        
        Args:
            action: Action data dictionary
            
        Returns:
            ComplianceCheck result
        """
        check_id = f"check_{datetime.now().timestamp():.0f}"
        timestamp = datetime.now()
        
        rules_violated = []
        status = ComplianceStatus.COMPLIANT
        message = "Compliant with all policies"
        
        for rule_id, rule in self._loader._policies.items():
            if self._check_action_against_rule(action, rule):
                rules_violated.append(rule_id)
                
                if rule.action == "block" and status != ComplianceStatus.BLOCKED:
                    status = ComplianceStatus.NON_COMPLIANT
                    message = f"Action blocked by policy: {rule.name}"
                elif rule.action == "require_approval" and status == ComplianceStatus.COMPLIANT:
                    status = ComplianceStatus.WARNING
                    message = f"Action requires approval: {rule.name}"
        
        # Create audit trail
        audit_trail = {
            "action": action,
            "timestamp": timestamp.isoformat(),
            "rules_checked": list(self._loader._policies.keys()),
            "rules_violated": rules_violated
        }
        
        check = ComplianceCheck(
            check_id=check_id,
            timestamp=timestamp,
            resource_type=action.get("resource_type", "unknown"),
            resource_id=action.get("resource_id", "unknown"),
            status=status,
            rules_violated=rules_violated,
            audit_trail=audit_trail,
            message=message
        )
        
        self._checks.append(check)
        self._audit_logs.append(audit_trail)
        
        return check
    
    def _check_action_against_rule(self, action: Dict[str, Any], rule: PolicyRule) -> bool:
        """Check if action violates a rule."""
        condition = rule.condition
        
        # Check data type
        if "data_type" in condition:
            action_data_type = action.get("data_type")
            if action_data_type not in condition["data_type"]:
                return False
        
        # Check destination region
        if "destination_region" in condition:
            action_region = action.get("destination_region")
            if action_region in condition["destination_region"]:
                return True
        
        # Check access type
        if "access_type" in condition:
            action_access = action.get("access_type")
            if action_access in condition["access_type"]:
                return True
        
        # Check encryption status
        if "encryption" in condition:
            action_encryption = action.get("encryption_status")
            if action_encryption == condition["encryption"]:
                return True
        
        return False
    
    def get_check_history(self) -> List[ComplianceCheck]:
        """Get compliance check history."""
        return self._checks.copy()
    
    def get_audit_logs(self) -> List[Dict[str, Any]]:
        """Get audit logs."""
        return self._audit_logs.copy()
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get compliance summary."""
        return {
            "total_checks": len(self._checks),
            "compliant": sum(1 for c in self._checks if c.status == ComplianceStatus.COMPLIANT),
            "warnings": sum(1 for c in self._checks if c.status == ComplianceStatus.WARNING),
            "non_compliant": sum(1 for c in self._checks if c.status == ComplianceStatus.NON_COMPLIANT),
            "blocked": sum(1 for c in self._checks if c.status == ComplianceStatus.BLOCKED)
        }


class AuditTrailManager:
    """Manages audit trail for compliance."""
    
    def __init__(self):
        """Initialize audit trail manager."""
        self._audit_trails: List[Dict[str, Any]] = []
    
    def log_action(self, action: Dict[str, Any], compliance_status: str, 
                   details: Dict[str, Any]) -> str:
        """
        Log an action to audit trail.
        
        Args:
            action: Action details
            compliance_status: Compliance status
            details: Additional details
            
        Returns:
            Audit trail ID
        """
        audit_id = f"audit_{datetime.now().timestamp():.0f}"
        
        trail = {
            "audit_id": audit_id,
            "action": action,
            "compliance_status": compliance_status,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "hash": hashlib.sha256(json.dumps(action, sort_keys=True).encode()).hexdigest()
        }
        
        self._audit_trails.append(trail)
        return audit_id
    
    def get_audit_trail(self, audit_id: str) -> Optional[Dict[str, Any]]:
        """Get audit trail by ID."""
        for trail in self._audit_trails:
            if trail["audit_id"] == audit_id:
                return trail
        return None
    
    def verify_audit_trail(self, audit_id: str) -> bool:
        """Verify audit trail integrity."""
        trail = self.get_audit_trail(audit_id)
        if not trail:
            return False
        
        # Verify hash
        expected_hash = hashlib.sha256(
            json.dumps(trail["action"], sort_keys=True).encode()
        ).hexdigest()
        
        return trail["hash"] == expected_hash
    
    def get_trail_history(self) -> List[Dict[str, Any]]:
        """Get audit trail history."""
        return self._audit_trails.copy()
