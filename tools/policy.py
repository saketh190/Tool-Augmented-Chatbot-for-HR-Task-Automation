import os

POLICY_PATH = "d:/agent/Tool_Bot/policies.txt"

def load_policies():
    policies = {}
    if not os.path.exists(POLICY_PATH):
        return policies
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        current_role = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.endswith(":"):
                current_role = line[:-1]
                policies[current_role] = []
            elif line.startswith("-") and current_role:
                policies[current_role].append(line[1:].strip())
    return policies

def get_policy_for_role(role):
    policies = load_policies()
    for key in policies:
        if role.lower() in key.lower():  # Partial, case-insensitive match
            return policies[key]
    return ["No policies found for this role."]

def answer_policy_question(role, question):
    policies = load_policies()
    # Find role by partial match
    matched_role = None
    for key in policies:
        if role.lower() in key.lower():
            matched_role = key
            break
    if not matched_role:
        return "No policies found for this role in the official policy document."
    role_policies = policies[matched_role]
    # Strict keyword match: only return if a rule matches the question
    matched_rules = []
    question_words = set(question.lower().split())
    for rule in role_policies:
        rule_words = set(rule.lower().split())
        if question_words & rule_words:
            matched_rules.append(rule)
    if matched_rules:
        return f"Official policy for '{matched_role}':\n" + "\n".join(matched_rules)
    else:
        return f"No official policy found for '{matched_role}' regarding your question in the policy document."

def register_policy_tool(mcp):
    @mcp.tool(
        "get_policy_for_role",
        description="Get all policies for a specific role."
    )
    def get_policy_for_role_tool(role: str):
        return get_policy_for_role(role)

    @mcp.tool(
        "answer_policy_question",
        description="Answer a policy question for a specific role based on policies.txt."
    )
    def answer_policy_question_tool(role: str, question: str):
        return answer_policy_question(role, question)