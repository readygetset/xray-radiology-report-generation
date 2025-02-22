from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
    
client = OpenAI(api_key=api_key)
    

def create_classification_prompt():
    prompt = """As a medical expert, classify the findings from this chest X-ray report into the following anatomical categories:
    - Lung: Include findings related to lungs, pulmonary vessels, pleural space, and airways
    - Heart: Include findings about cardiac size, contour, and related features
    - Mediastinal: Include findings about mediastinum, hilar regions, and great vessels
    - Bone: Include findings about ribs, spine, and other bony structures
    - Others: Include findings that don't fit into above categories

    Format the output as a JSON with these exact keys: "lung", "heart", "mediastinal", "bone", "others"
    Keep the original medical terminology and phrasing when possible.
    If there are no findings for a category, use an empty string.

    Example Input:
    The cardiomediastinal silhouette and pulmonary vasculature are within normal limits in size.
    The lungs are mildly hypoinflated but grossly clear of focal airspace disease, pneumothorax, or pleural effusion.
    There are mild degenerative endplate changes in the thoracic spine.
    There are no acute bony findings.

    Example Output:
    {
        "lung": "Lungs are mildly hypoinflated but grossly clear of focal airspace disease, pneumothorax, or pleural effusion. Pulmonary vasculature are within normal limits in size.",
        "heart": "Cardiac silhouette within normal limits in size.",
        "mediastinal": "Mediastinal contours within normal limits in size.", 
        "bone": "Mild degenerative endplate changes in the thoracic spine. No acute bony findings.",
        "others": ""
    }

    Now classify the following report:
    """
    return prompt

def process_validation_data():
    with open('data/annotation_quiz_all.json', 'r') as f:
        data = json.load(f)
    
    validation_cases = [item for item in data['val']]
    
    prompts = []
    for case in validation_cases:
        full_prompt = create_classification_prompt() + "\n" + case['original_report']
        prompts.append({
            'id': case['id'],
            'prompt': full_prompt,
            'original_report': case['original_report']
        })
    
    return prompts

def process_with_gpt4(prompts):
    results = []
    
    for case in prompts:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical expert specializing in X-ray report classification."},
                    {"role": "user", "content": case['prompt']}
                ],
                temperature=0.3
            )
            
            classification_str = response.choices[0].message.content
            classification_json = json.loads(classification_str)
            
            result = {
                'id': case['id'],
                'original_report': case['original_report'],
                'classification': classification_json 
            }
            results.append(result)
            
            print(f"Processed case {case['id']}")
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON (case {case['id']}): {str(e)}")
            continue
        except Exception as e:
            print(f"Error processing case {case['id']}: {str(e)}")
            continue
        break
            
    return results

prompts = process_validation_data()
classified_reports = process_with_gpt4(prompts)

with open('classified_reports.json', 'w') as f:
    json.dump(classified_reports, f, indent=2)

print("\nSample classification result:")
print(json.dumps(classified_reports[0], indent=2))
