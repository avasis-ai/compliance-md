# README.md - Compliance MD

## Regulatory Compliance Translated into Executable Agent Rules

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/compliance-md.svg)](https://pypi.org/project/compliance-md/)

**Compliance MD** transforms dense PDF compliance manuals into executable SKILL.md files. If an agent attempts to write data to a server outside the EU, the GDPR Compliance.md skill intercepts and blocks the action autonomously, providing a cryptographically secure audit trail.

## 🎯 What It Does

This tool replaces legal red tape with manageable code, transforming complex compliance requirements into executable, enforceable rules.

### Example Use Case

```python
from compliance_md.enforcer import ComplianceEnforcer, ComplianceStatus

# Initialize compliance enforcer
enforcer = ComplianceEnforcer()

# Check if an action is compliant
action = {
    "action_type": "data_transfer",
    "data_type": "personal_data",
    "destination_region": "US"
}

check = enforcer.check_compliance(action)

if check.status == ComplianceStatus.COMPLIANT:
    print("✅ Action is compliant")
else:
    print(f"❌ Action blocked: {check.message}")
```

## 🚀 Features

- **GDPR Enforcement**: Automatically blocks unauthorized personal data transfers
- **HIPAA Protection**: Requires approval for healthcare data access
- **SOC2 Compliance**: Enforces data encryption requirements
- **Cryptographic Audit Trails**: Secure, verifiable audit logs
- **Policy Management**: Load and manage compliance policies dynamically
- **Automated Enforcement**: Real-time compliance checking

### Compliance Regulations Supported

1. **GDPR** - General Data Protection Regulation
2. **HIPAA** - Health Insurance Portability and Accountability Act
3. **SOC2** - Service Organization Control 2

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- cryptography, jsonschema for compliance validation

### Install from PyPI

```bash
pip install compliance-md
```

### Install from Source

```bash
git clone https://github.com/avasis-ai/compliance-md.git
cd compliance-md
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
pip install pytest pytest-mock black isort
```

## 🔧 Usage

### Command-Line Interface

```bash
# Check version
compliance-md --version

# Show available policies
compliance-md policies

# Check compliance for an action
compliance-md check --data-type personal_data --region US

# View compliance history
compliance-md history

# View audit trail
compliance-md audit

# Run demo
compliance-md demo
```

### Programmatic Usage

```python
from compliance_md.enforcer import ComplianceEnforcer, AuditTrailManager, ComplianceStatus

# Initialize enforcer
enforcer = ComplianceEnforcer()

# Load custom policy
custom_policy = {
    "id": "custom_001",
    "name": "Custom Financial Policy",
    "description": "Financial data encryption requirement",
    "condition": {
        "data_type": "financial_data",
        "encryption": "none"
    },
    "action": "block",
    "audit_required": True,
    "regulation": "SOC2"
}

enforcer.load_policy(custom_policy)

# Check compliance
action = {
    "action_type": "file_write",
    "data_type": "financial_data",
    "encryption_status": "none"
}

check = enforcer.check_compliance(action)

print(f"Status: {check.status.value}")
print(f"Message: {check.message}")

# Get audit trail manager
trail_manager = AuditTrailManager()
audit_id = trail_manager.log_action(
    action=action,
    compliance_status=check.status.value,
    details={}
)

# Verify audit trail
is_valid = trail_manager.verify_audit_trail(audit_id)
print(f"Audit valid: {is_valid}")
```

## 📚 API Reference

### ComplianceEnforcer

Enforces compliance policies on actions.

#### `check_compliance(action)` → ComplianceCheck

Check if an action complies with policies.

#### `load_policy(policy_data)` → PolicyRule

Load a custom policy.

#### `get_compliance_summary()` → Dict

Get compliance summary statistics.

### PolicyLoader

Loads and manages compliance policies.

#### `load_policy(policy_data)` → PolicyRule

Load a single policy.

#### `list_policies()` → List[Dict]

List all policies.

### AuditTrailManager

Manages audit trail for compliance.

#### `log_action(action, compliance_status, details)` → str

Log an action to audit trail.

#### `verify_audit_trail(audit_id)` → bool

Verify audit trail integrity.

## 🧪 Testing

Run tests with pytest:

```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
compliance-md/
├── README.md
├── pyproject.toml
├── LICENSE
├── src/
│   └── compliance_md/
│       ├── __init__.py
│       ├── enforcer.py
│       └── cli.py
├── tests/
│   └── test_enforcer.py
└── .github/
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `python -m pytest tests/ -v`
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/avasis-ai/compliance-md.git
cd compliance-md
pip install -e ".[dev]"
pre-commit install
```

## 📝 License

This project is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE) for details.

## 🎯 Vision

Compliance MD is an absolute necessity for regulatory compliance in 2026. It transforms complex legal requirements into executable, enforceable code that prevents violations before they occur.

### Key Innovations

- **Executable Policies**: Compliance rules that actually run and enforce
- **Cryptographic Audits**: Tamper-proof audit trails
- **Automated Enforcement**: Real-time compliance checking
- **Regulatory Coverage**: GDPR, HIPAA, SOC2 support
- **Policy Management**: Dynamic policy loading and updates

## 🌟 Impact

This tool enables:

- **Zero Compliance Violations**: Prevent violations before they happen
- **Automated Enforcement**: No human intervention required
- **Cryptographic Security**: Tamper-proof audit trails
- **Legal Authority**: Verified, signed policy files
- **Startup Speed**: Rapid growth without compliance debt
- **Enterprise Trust**: Meeting the highest standards

## 🛡️ Security & Trust

- **Trusted dependencies**: cryptography (8), pyyaml (7.4), jsonschema (6.8), click (8.8) - [Context7 verified](https://context7.com)
- **Apache 2.0**: Open source, community-driven
- **Cryptographic Security**: Verified audit trails
- **Legal Authority**: Verified policy files
- **Compliance**: GDPR, HIPAA, SOC2 ready

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/avasis-ai/compliance-md/wiki)
- **Issues**: [GitHub Issues](https://github.com/avasis-ai/compliance-md/issues)
- **Security**: Report security vulnerabilities to security@avasis.ai

## 🙏 Acknowledgments

- **Legal Experts**: Contributing to policy framework
- **Open Policy Agent**: Inspiration for policy enforcement
- **GDPR & HIPAA Guidelines**: Compliance standards
- **Open Source Community**: Shared best practices

---

**Made with ❤️ by [Avasis AI](https://avasis.ai)**

*The essential framework for regulatory compliance. Meet requirements automatically, stay compliant always.*
