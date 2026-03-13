import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def clean_json(raw):
    raw = re.sub(r',\s*([}\]])', r'\1', raw)
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()

def generate_ddr(inspection_text, thermal_text):
    print("Sending data to Groq AI...")

    prompt = f"""
You are a professional building diagnostics expert. Analyze both documents below and generate a complete DDR.

INSPECTION REPORT:
{inspection_text[:15000]}

THERMAL REPORT:
{thermal_text[:8000]}

CRITICAL REQUIREMENTS:
1. For EACH area, you MUST explicitly link the thermal temperature reading to the inspection finding.
   Example: "Thermal imaging confirmed temperature drop to 24.0°C at Hall ceiling, consistent with observed dampness and paint spalling."
2. You MUST cover ALL of these areas found in the documents:
   - Hall ceiling (thermal shows 22.3°C - 27.3°C)
   - Bedroom skirting and wall corner (ground floor)
   - Common Bathroom passage area
   - Staircase Area
   - Master Bedroom skirting (1st floor, thermal shows 26.8°C - 31.8°C)
   - Master Bedroom-2 skirting and ceiling (1st floor, thermal shows 23.2°C - 29°C)
   - External Wall (hairline cracks, dampness)
   - Balcony tile joints
   - Terrace (hollowness, vegetation growth, IPS surface cracks)
3. Severity MUST be assigned to EVERY area individually
4. Root causes MUST be specific — link to concealed plumbing, tile gaps, terrace screed failure etc.
5. If inspection and thermal data contradict each other → explicitly state the conflict
6. If information is missing → write exactly: Not Available


Return ONLY valid JSON with this exact structure, no text before or after:
{{
  "property_issue_summary": "Comprehensive summary mentioning all major issues",
  "area_wise_observations": [
    {{
      "area": "Area name",
      "observation": "Detailed observation combining both inspection and thermal findings with specific temperature readings",
      "source": "both"
    }}
  ],
  "probable_root_cause": [
    {{
      "issue": "Specific issue name",
      "cause": "Detailed root cause with technical explanation"
    }}
  ],
  "severity_assessment": [
    {{
      "area": "Area name",
      "severity": "High / Medium / Low",
      "reasoning": "Specific reasoning based on observations"
    }}
  ],
  "recommended_actions": [
    {{
      "area": "Area name",
      "action": "Specific actionable repair recommendation"
    }}
  ],
  "additional_notes": "Pattern analysis, seasonal factors, structural risks if unaddressed",
  "missing_or_unclear_information": [
    "List specific data gaps or conflicts between inspection and thermal reports"
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=6000,
    )

    raw = response.choices[0].message.content.strip()
    raw = clean_json(raw)

    try:
        ddr_json = json.loads(raw)
        # Validate all 7 sections exist and are non-empty
        required = ["property_issue_summary", "area_wise_observations",
                    "probable_root_cause", "severity_assessment",
                    "recommended_actions", "additional_notes",
                    "missing_or_unclear_information"]
        for key in required:
            if key not in ddr_json or not ddr_json[key]:
                print(f"WARNING: Section '{key}' is empty or missing!")
        print("AI extraction successful!")
        return ddr_json
    except json.JSONDecodeError as e:
        print("JSON parse error:", e)
        print("Raw response snippet:", raw[:800])
        return None