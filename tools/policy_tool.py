import os
import re

POLICY_PATH = "d:/agent/Tool_Bot/policies.txt"

def load_policies():
    policies = {}
    current_section = None
    current_role = None
    if not os.path.exists(POLICY_PATH):
        return policies
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("=") or line.startswith("Company Name") or line.startswith("Document Title") or line.startswith("Version") or line.startswith("max_annual_leaves"):
                continue
            # Section header
            section_match = re.match(r"^\d+\.\s+(.+)$", line)
            if section_match:
                current_section = section_match.group(1).strip()
                continue
            # Role header
            if line.endswith(":"):
                current_role = line[:-1]
                if current_role not in policies:
                    policies[current_role] = {}
                # Always set current_section for this role, even if not present before
                if current_section and current_section not in policies[current_role]:
                    policies[current_role][current_section] = []
                continue
            # Policy line
            if line.startswith("-") and current_role and current_section:
                # Ensure current_section exists for current_role
                if current_section not in policies[current_role]:
                    policies[current_role][current_section] = []
                policies[current_role][current_section].append(line[1:].strip())
    return policies

def get_policy_for_role(role):
    policies = load_policies()
    for key in policies:
        if role.lower() in key.lower():
            return policies[key]
    return ["No policies found for this role."]

def answer_policy_question(role, question):
    policies = load_policies()
    matched_role = None
    # Partial, case-insensitive role match
    for key in policies:
        if role.lower() in key.lower():
            matched_role = key
            break
    if not matched_role:
        return "No policies found for this role."
    # Extract topic keywords from question
    topic_keywords = set(re.findall(r"\b\w+\b", question.lower()))
    matched_policies = []
    for section, rules in policies[matched_role].items():
        for rule in rules:
            rule_words = set(rule.lower().split())
            # If any keyword matches, consider it relevant
            if topic_keywords & rule_words:
                matched_policies.append(f"[{section}] {rule}")
    if matched_policies:
        return f"Policy for '{matched_role}':\n" + "\n".join(matched_policies)
    # Fallback: show all policies for the role
    all_rules = []
    for section, rules in policies[matched_role].items():
        for rule in rules:
            all_rules.append(f"[{section}] {rule}")
    return f"No specific match found. Here are all policies for '{matched_role}':\n" + "\n".join(all_rules)

def register_policy_tool(mcp):
    @mcp.tool(
        "answer_policy_question",
        description="Answer a policy question for a specific role based on policies.txt."
    )
    def answer_policy_question_tool(role: str, question: str):
        return answer_policy_question(role, question)