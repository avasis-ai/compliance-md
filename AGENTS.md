# AGENTS.md - Compliance MD Project Context

This folder is home. Treat it that way.

## Project: Compliance-MD (#35)

### Identity
- **Name**: Compliance-MD
- **License**: Apache-2.0
- **Org**: avasis-ai
- **PyPI**: compliance-md
- **Version**: 0.1.0
- **Tagline**: Regulatory compliance translated into executable agent rules

### What It Does
Replacing dense PDF compliance manuals with executable SKILL.md files. If an agent attempts to write data to a server outside the EU, the GDPR Compliance.md skill intercepts and blocks the action autonomously, providing a cryptographically secure audit trail.

### Inspired By
- Open-source Policy
- Kubernetes OPA
- Legal/Finance + Automation
- Compliance automation

### Core Components

#### `/enforcer/`
- Policy enforcement engine
- Compliance checking
- Action blocking
- Audit trail logging

#### `/policies/`
- GDPR compliance policies
- HIPAA data protection
- SOC2 security requirements
- Custom policy loading

### Technical Architecture

**Key Dependencies:**
- `cryptography>=41.0` - Cryptographic operations (Trust score: 8)
- `pyyaml>=6.0` - Configuration parsing (Trust score: 7.4)
- `jsonschema>=4.0` - Schema validation (Trust score: 6.8)
- `click>=8.0` - CLI framework (Trust score: 8.8)

**Core Modules:**
1. `enforcer.py` - Policy enforcement and compliance checking
2. `cli.py` - Command-line interface

### AI Coding Agent Guidelines

#### When Contributing:

1. **Understand the domain**: Legal compliance requires precision and legal awareness
2. **Use Context7**: Check trust scores for new libraries before adding dependencies
3. **Security first**: Never compromise on audit trail integrity
4. **Legal accuracy**: Ensure policy implementations match regulations
5. **Cryptographic verification**: All audits must be tamper-proof
6. **Audit trails**: Complete, verifiable history for compliance

#### What to Remember:

- **Cryptographic audits**: All actions must be verifiable
- **Policy enforcement**: Real-time, automatic blocking
- **Legal authority**: Verified, signed policy files
- **Regulatory coverage**: GDPR, HIPAA, SOC2 support
- **Audit verification**: Tamper-proof logs
- **Zero violations**: Prevent violations before they occur

#### Common Patterns:

**Load compliance policies:**
```python
from compliance_md.enforcer import ComplianceEnforcer

enforcer = ComplianceEnforcer()

# Check action compliance
action = {
    "action_type": "data_transfer",
    "data_type": "personal_data",
    "destination_region": "US"
}

check = enforcer.check_compliance(action)
```

**Load custom policy:**
```python
custom_policy = {
    "id": "custom_001",
    "name": "Custom Policy",
    "description": "Custom compliance rule",
    "condition": {
        "data_type": "sensitive_data",
        "encryption": "none"
    },
    "action": "block",
    "audit_required": True,
    "regulation": "CUSTOM"
}

enforcer.load_policy(custom_policy)
```

**Manage audit trail:**
```python
from compliance_md.enforcer import AuditTrailManager

manager = AuditTrailManager()
audit_id = manager.log_action(
    action=action,
    compliance_status="compliant",
    details={}
)

# Verify audit
is_valid = manager.verify_audit_trail(audit_id)
```

### Project Status

- ✅ Initial implementation complete
- ✅ GDPR enforcement
- ✅ HIPAA protection
- ✅ SOC2 compliance
- ✅ Cryptographic audit trails
- ✅ Policy management
- ✅ CLI interface
- ✅ Comprehensive test suite
- ⚠️ Additional regulations pending
- ⚠️ Policy signing pending

### How to Work with This Project

1. **Read `SOUL.md`** - Understand who you are
2. **Read `USER.md`** - Know who you're helping
3. **Check `memory/YYYY-MM-DD.md`** - Recent context
4. **Read `MEMORY.md`** - Long-term decisions (main session only)
5. **Execute**: Code → Test → Commit

### Red Lines

- **No stubs or TODOs**: Every function must have real implementation
- **Type hints required**: All function signatures must include types
- **Docstrings mandatory**: Explain what, why, and how
- **Test coverage**: New features need tests
- **Security critical**: Never compromise audit integrity

### Development Workflow

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Format code
black src/ tests/
isort src/ tests/

# Check syntax
python -m py_compile src/compliance_md/*.py

# Run CLI
compliance-md --help

# Commit
git add -A && git commit -m "feat: add CCPA compliance"
```

### Key Files to Understand

- `src/compliance_md/enforcer.py` - Core enforcement logic
- `src/compliance_md/cli.py` - Command-line interface
- `tests/test_enforcer.py` - Comprehensive tests
- `README.md` - Usage examples

### Security Considerations

- **Cryptographic audits**: Tamper-proof verification
- **Policy enforcement**: Real-time blocking
- **Audit trails**: Complete history
- **Legal authority**: Verified policies
- **Trusted dependencies**: All verified via Context7
- **Apache 2.0**: Open source, community-driven

### Next Steps

1. Add more regulations (CCPA, GLBA, etc.)
2. Policy signing and verification
3. Web-based dashboard
4. Automated policy updates
5. Integration with major cloud providers
6. Legal expert consortium

### Unique Defensible Moat

The **verified, cryptographically signed policy files maintained by an open-source consortium of certified legal professionals** establish an absolute legal authority that unverified code cannot replace. This requires:

- Legal expertise for policy creation
- Cryptographic verification systems
- Consortium governance structure
- Continuous policy updates
- Legal certification processes
- Tamper-proof audit infrastructure

This is complex work requiring both legal and technical expertise, making it difficult to replicate effectively.

---

**This file should evolve as you learn more about the project.**
