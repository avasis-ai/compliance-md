"""Tests for compliance MD."""

import pytest
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from compliance_md.enforcer import (
    ComplianceEnforcer,
    ComplianceStatus,
    ComplianceCheck,
    PolicyLoader,
    PolicyRule,
    AuditTrailManager
)


class TestPolicyLoader:
    """Tests for PolicyLoader."""
    
    def test_load_policy(self):
        """Test loading a single policy."""
        loader = PolicyLoader()
        
        policy_data = {
            "id": "test_001",
            "name": "Test Policy",
            "description": "A test policy",
            "condition": {"data_type": "test"},
            "action": "block",
            "audit_required": True,
            "regulation": "GDPR"
        }
        
        rule = loader.load_policy(policy_data)
        
        assert rule.id == "test_001"
        assert rule.name == "Test Policy"
        assert rule.action == "block"
    
    def test_list_policies(self):
        """Test listing all policies."""
        loader = PolicyLoader()
        
        loader.load_policy({
            "id": "policy_1",
            "name": "Policy 1",
            "description": "Description 1",
            "condition": {},
            "action": "allow",
            "audit_required": False,
            "regulation": "GDPR"
        })
        
        policies = loader.list_policies()
        
        assert len(policies) == 1
        assert policies[0]["name"] == "Policy 1"
    
    def test_get_policy(self):
        """Test getting a policy by ID."""
        loader = PolicyLoader()
        
        loader.load_policy({
            "id": "policy_1",
            "name": "Policy 1",
            "description": "Desc",
            "condition": {},
            "action": "allow",
            "audit_required": False,
            "regulation": "GDPR"
        })
        
        policy = loader.get_policy("policy_1")
        
        assert policy is not None
        assert policy.name == "Policy 1"
    
    def test_clear_policies(self):
        """Test clearing all policies."""
        loader = PolicyLoader()
        
        loader.load_policy({
            "id": "policy_1",
            "name": "Policy 1",
            "description": "Desc",
            "condition": {},
            "action": "allow",
            "audit_required": False,
            "regulation": "GDPR"
        })
        
        assert len(loader.list_policies()) == 1
        
        loader.clear_policies()
        
        assert len(loader.list_policies()) == 0


class TestComplianceEnforcer:
    """Tests for ComplianceEnforcer."""
    
    def test_initialization(self):
        """Test enforcer initialization."""
        enforcer = ComplianceEnforcer()
        
        assert len(enforcer._loader.list_policies()) > 0
        assert len(enforcer.get_check_history()) == 0
    
    def test_check_compliant_action(self):
        """Test checking a compliant action."""
        enforcer = ComplianceEnforcer()
        
        action = {
            "action_type": "file_read",
            "data_type": "general_data"
        }
        
        check = enforcer.check_compliance(action)
        
        assert check.status == ComplianceStatus.COMPLIANT
        assert check.message == "Compliant with all policies"
    
    def test_check_non_compliant_action(self):
        """Test checking a non-compliant action."""
        enforcer = ComplianceEnforcer()
        
        action = {
            "action_type": "data_transfer",
            "data_type": "personal_data",
            "destination_region": "US"
        }
        
        check = enforcer.check_compliance(action)
        
        assert check.status == ComplianceStatus.NON_COMPLIANT
        assert len(check.rules_violated) > 0
    
    def test_check_requires_approval(self):
        """Test checking action requiring approval."""
        enforcer = ComplianceEnforcer()
        
        action = {
            "action_type": "file_write",
            "data_type": "healthcare_data",
            "access_type": "read"
        }
        
        check = enforcer.check_compliance(action)
        
        assert check.status == ComplianceStatus.WARNING
    
    def test_get_compliance_summary(self):
        """Test getting compliance summary."""
        enforcer = ComplianceEnforcer()
        
        # Run some checks
        enforcer.check_compliance({"action_type": "test1", "data_type": "general"})
        enforcer.check_compliance({"action_type": "test2", "data_type": "personal_data", "destination_region": "US"})
        
        summary = enforcer.get_compliance_summary()
        
        assert summary["total_checks"] == 2
        assert "compliant" in summary
        assert "non_compliant" in summary


class TestAuditTrailManager:
    """Tests for AuditTrailManager."""
    
    def test_log_action(self):
        """Test logging an action."""
        manager = AuditTrailManager()
        
        audit_id = manager.log_action(
            action={"type": "test"},
            compliance_status="compliant",
            details={"extra": "info"}
        )
        
        assert audit_id is not None
        assert audit_id.startswith("audit_")
    
    def test_get_audit_trail(self):
        """Test getting audit trail."""
        manager = AuditTrailManager()
        
        audit_id = manager.log_action(
            action={"type": "test"},
            compliance_status="compliant",
            details={}
        )
        
        trail = manager.get_audit_trail(audit_id)
        
        assert trail is not None
        assert trail["audit_id"] == audit_id
    
    def test_verify_audit_trail(self):
        """Test verifying audit trail integrity."""
        manager = AuditTrailManager()
        
        audit_id = manager.log_action(
            action={"type": "test"},
            compliance_status="compliant",
            details={}
        )
        
        assert manager.verify_audit_trail(audit_id) is True
    
    def test_get_trail_history(self):
        """Test getting trail history."""
        manager = AuditTrailManager()
        
        manager.log_action({"type": "test1"}, "compliant", {})
        manager.log_action({"type": "test2"}, "warning", {})
        
        history = manager.get_trail_history()
        
        assert len(history) == 2


class TestComplianceStatus:
    """Tests for ComplianceStatus enum."""
    
    def test_status_values(self):
        """Test status values."""
        assert ComplianceStatus.COMPLIANT.value == "compliant"
        assert ComplianceStatus.NON_COMPLIANT.value == "non_compliant"
        assert ComplianceStatus.WARNING.value == "warning"
        assert ComplianceStatus.BLOCKED.value == "blocked"


class TestPolicyRule:
    """Tests for PolicyRule."""
    
    def test_rule_creation(self):
        """Test creating policy rule."""
        rule = PolicyRule(
            id="test_001",
            name="Test Rule",
            description="Test description",
            condition={"data_type": "test"},
            action="block",
            audit_required=True,
            regulation="GDPR"
        )
        
        assert rule.id == "test_001"
        assert rule.action == "block"
    
    def test_rule_to_dict(self):
        """Test converting rule to dictionary."""
        rule = PolicyRule(
            id="test_002",
            name="Test Rule 2",
            description="Desc",
            condition={"test": "value"},
            action="allow",
            audit_required=False,
            regulation="HIPAA"
        )
        
        data = rule.to_dict()
        
        assert data["id"] == "test_002"
        assert data["regulation"] == "HIPAA"
        assert data["audit_required"] is False


class TestComplianceCheck:
    """Tests for ComplianceCheck."""
    
    def test_check_creation(self):
        """Test creating compliance check."""
        check = ComplianceCheck(
            check_id="check_001",
            timestamp=datetime.now(),
            resource_type="data",
            resource_id="res_001",
            status=ComplianceStatus.COMPLIANT,
            rules_violated=[],
            audit_trail={},
            message="Compliant"
        )
        
        assert check.check_id == "check_001"
        assert check.status == ComplianceStatus.COMPLIANT
    
    def test_check_to_dict(self):
        """Test converting check to dictionary."""
        check = ComplianceCheck(
            check_id="check_002",
            timestamp=datetime.now(),
            resource_type="data",
            resource_id="res_002",
            status=ComplianceStatus.NON_COMPLIANT,
            rules_violated=["rule_1"],
            audit_trail={},
            message="Non-compliant"
        )
        
        data = check.to_dict()
        
        assert data["check_id"] == "check_002"
        assert data["status"] == "non_compliant"
        assert "rule_1" in data["rules_violated"]


class TestDefaultPolicies:
    """Tests for default policies."""
    
    def test_gdpr_policy_loaded(self):
        """Test GDPR policy is loaded by default."""
        enforcer = ComplianceEnforcer()
        
        policies = enforcer._loader.list_policies()
        
        assert any(p["regulation"] == "GDPR" for p in policies)
    
    def test_hipaa_policy_loaded(self):
        """Test HIPAA policy is loaded by default."""
        enforcer = ComplianceEnforcer()
        
        policies = enforcer._loader.list_policies()
        
        assert any(p["regulation"] == "HIPAA" for p in policies)
    
    def test_soc2_policy_loaded(self):
        """Test SOC2 policy is loaded by default."""
        enforcer = ComplianceEnforcer()
        
        policies = enforcer._loader.list_policies()
        
        assert any(p["regulation"] == "SOC2" for p in policies)
